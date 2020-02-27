from bs4 import BeautifulSoup
import bs4
import requests
import nltk
import fractions

# spoonacular and api key
import spoonacular as sp

# other files
from recipeDB import RecipeDB
from spoonacularKey import spoonacularAPI

api = spoonacularAPI()

db = RecipeDB("recipeDB.json")  # Get the DB data


def get_page(url):
    res = requests.get(url)
    html = res.content

    bs = BeautifulSoup(html, "html.parser")
    return bs


def get_name(url):
    """
    Scrape the given url for the name of the recipe.

    Parameters: url (string): Link to an AllRecipes recipe. 

    Returns: recipe_name (string): Name of recipe.
    """
    recipe_name = ""
    bs = get_page(url)
    recipe_name = bs.find("h1", attrs={"id": "recipe-main-content"}).contents[0]
    return recipe_name


def get_ingredients(url):
    """
    Scrape the given url for the ingredients of the recipe.

    Parameters: url (string): Link to an AllRecipes recipe.

    Returns: ingredients (list): List of ingredients from recipe.
    """
    ingredients = []
    bs = get_page(url)
    i = 1
    is_working = True
    while is_working:
        try:
            list_obj = bs.find("ul", attrs={"id": "lst_ingredients_" + str(i)}).contents
            for ing in list_obj:
                if isinstance(ing, bs4.element.Tag):
                    ingredients.append(ing.contents[1].attrs["title"])
            i += 1
        except:
            is_working = False
    return ingredients


def common_member(a, b):
    """
    Returns true if list a and b have common elements
    """
    a_set = set(a)
    b_set = set(b)
    if a_set & b_set:
        return True
    else:
        return False


def get_tools(url):
    """
    Scrape the given url for the name of the recipe.
    Parameters: url (string): Link to an AllRecipes recipe.
    Returns: tools (list): List of tools used in the recipe.
    """
    global db
    steps = get_steps(url)

    possible_tools = db.tools

    tools = []

    for step in steps:
        sl = step.lower().split(" ")
        if common_member(["cut", "slice"], sl) and ("Knife" not in tools):
            tools.append("knife")
        if common_member(["stir"], sl) and ("Spoon" not in tools):
            tools.append("spoon")

        for tool in possible_tools:
            if tool.isspace() or tool in tools or len(tool) == 0:
                continue
            if tool.lower() in step.lower():
                tools.append(tool)

    return tools


def get_methods(url):
    """
    Scrape the given url for the name of the recipe.
    Parameters: url (string): Link to an AllRecipes recipe.
    Returns: methods (list): List of cooking methods used in the recipe.
    """

    global db
    steps = get_steps(url)

    possible_methods = db.primaryMethods
    possible_methods.extend(db.secondaryMethods)

    methods = []

    for step in steps:
        sl = step.lower().split(" ")
        for method in possible_methods:
            if method.isspace() or method in methods or len(method) == 0:
                continue
            if method.lower() in step.lower():
                methods.append(method)

    return methods


def get_steps(url):
    """
    Scrape the given url for the name of the recipe.

    Parameters: url (string): Link to an AllRecipes recipe.

    Returns: steps (list): List of steps required to complete the recipe.
    """
    steps = []
    bs = get_page(url)
    list_obj = bs.find(
        "ol", attrs={"class": "list-numbers recipe-directions__list"}
    ).contents
    for step in list_obj:
        if isinstance(step, bs4.element.Tag):
            steps.append(step.contents[1].contents[0].strip())
    return steps
    pass


def transform_to_veg(recipe_info):
    pass


def transform_from_veg(recipe_info):
    return {"test": ["test again!"]}


def transform_to_healthy(recipe_info):
    pass


def transform_to_italian(recipe_info):
    pass


def transform_cut_in_half(recipe_info):
    new_lst = []
    for ingredient in recipe_info["ingredients"]:
        ig = ingredient.split()
        for j, i in enumerate(ig):
            if ")" in i:
                i = i.replace(")", "")
            if "(" in i:
                i = i.replace("(", "")
            try:
                fraction_str = i + " " + ig[j + 1]
                fraction_obj = sum(map(fractions.Fraction, fraction_str.split()))
                divided = float(fractions.Fraction.from_float(float(fraction_obj) / 2))
                ingredient = ingredient.replace(fraction_str, str(divided))
            except:
                try:
                    k = str(round(float(fractions.Fraction(i) / 2), 4))
                    ingredient = ingredient.replace(i, k)
                except:
                    pass
        new_lst.append(ingredient)
    recipe_info["ingredients"] = new_lst
    return recipe_info


def transform_double(recipe_info):
    new_lst = []
    for ingredient in recipe_info["ingredients"]:
        ig = ingredient.split()
        for j, i in enumerate(ig):
            if ")" in i:
                i = i.replace(")", "")
            if "(" in i:
                i = i.replace("(", "")
            try:
                fraction_str = i + " " + ig[j + 1]
                fraction_obj = sum(map(fractions.Fraction, fraction_str.split()))
                divided = float(fractions.Fraction.from_float(float(fraction_obj) * 2))
                ingredient = ingredient.replace(fraction_str, str(divided))
            except:
                try:
                    k = str(round(float(fractions.Fraction(i) * 2), 4))
                    ingredient = ingredient.replace(i, k)
                except:
                    pass
        new_lst.append(ingredient)
    recipe_info["ingredients"] = new_lst
    return recipe_info
