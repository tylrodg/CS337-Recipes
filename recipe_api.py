from bs4 import BeautifulSoup
from vegetarianHelper import replacer, nonVegChecker, helper
from veganHelper import veganReplacer, veganHelper, nonVeganChecker
import bs4
import requests
import nltk
import fractions
from difflib import SequenceMatcher, get_close_matches
import json
import re
import string
import difflib

# spoonacular and api key
#import spoonacular as sp

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
    recipe_name = bs.find(
        "h1", attrs={"id": "recipe-main-content"}).contents[0]
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
            list_obj = bs.find(
                "ul", attrs={"id": "lst_ingredients_" + str(i)}).contents
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

def step_breakdown(recipe_info):

    methods = recipe_info["methods"]
    tools = recipe_info["tools"]
    step_data = {}
    
    for i in recipe_info["steps"]:
    
        time_words = ['hours', 'minutes', 'seconds', 'hour', 'minute', 'second']
        step_dict = { }
        m = [ ]
        t = [ ]
        ig = [ ]
        ig_final = [ ]
        tim = [ ]
        
        no_punc = i.translate(str.maketrans('', '', string.punctuation))
        i_lst = no_punc.split()
        for word in time_words:
            for ind, var in enumerate(i_lst):
                if word == var:
                    message = i_lst[ind-1] + " " + var
                    tim.append(message)
    
        step_dict["times"] = tim
        
        ingr = api.detect_food_in_text(i)
        ingr = ingr.json()

        for annotation in ingr['annotations']:
            ig.append(annotation['annotation'])

        for item in ig:
            k = item
            if not get_close_matches(k, ig_final, cutoff=0.5):
                ig_final.append(k)
        step_dict["ingredients"] = ig_final
        
        for method in methods:
            if method in i:
                m.append(method)
        step_dict["methods"] = m
        
        for tool in tools:
            if tool in i:
                t.append(tool)
        step_dict["tools"] = t

        step_data[i] = step_dict

    return step_data

def transform_to_veg(recipe_info):
    return helper(recipe_info, "vegetarian")


def transform_from_veg(recipe_info):
    """
    check if a suitable substitute exists; if so, replace it
        
    otherwise, add new meat
    """
    b = nonVegChecker(recipe_info)
    if b == "True":
        return helper(recipe_info, "nonVegetarian")
    else:
        return replacer(recipe_info)


def transform_to_vegan(recipe_info):
    recipe = veganHelper(recipe_info, "vegan")
    return recipe 

def transform_from_vegan(recipe_info):
    recipe = nonVeganChecker(recipe_info)
    if (recipe == "True"):
        return veganHelper(recipe_info, "nonVegan")
    else:
        return veganReplacer(recipe_info)


def transform_to_healthy(recipe_info):
    global db

    new_info = recipe_info
    to_healthy = db.unhealthyToHealthy

    for i in range(len(recipe_info["ingredients"])):
        for key in to_healthy:
            new_info["ingredients"][i] = recipe_info["ingredients"][i].replace(
                key, to_healthy[key])

    for i in range(len(recipe_info["steps"])):
        for key in to_healthy:
            new_info["steps"][i] = recipe_info["steps"][i].replace(
                key, to_healthy[key])
    return new_info


def transform_from_healthy(recipe_info):

    global db

    new_info = recipe_info
    to_unhealthy = db.healthyToUnhealthy

    for i in range(len(recipe_info["ingredients"])):
        for key in to_unhealthy:
            new_info["ingredients"][i] = recipe_info["ingredients"][i].replace(
                key, to_unhealthy[key])

    for i in range(len(recipe_info["steps"])):
        for key in to_unhealthy:
            new_info["steps"][i] = recipe_info["steps"][i].replace(
                key, to_unhealthy[key])

    return new_info


def shorter_name(spoonacular_name, originalName):
    if not spoonacular_name:
        return originalName
    if not originalName:
        return spoonacular_name
    if len(spoonacular_name) < len(originalName):
        return spoonacular_name
    return originalName


def transform_to_chinese(recipe_info):
    return cuisine_transformer(recipe_info, 'chinese')

def transform_to_indian(recipe_info):
    return cuisine_transformer(recipe_info, 'indian')

def cuisine_transformer(recipe_info, cuisine):
    cuisine_db = getattr(db, cuisine)
    # ingredients mapping
    new_ingredients = []
    new_ing_names = dict()
    new_ing_names['new_vals'] = []
    data = api.parse_ingredients('\n'.join(recipe_info['ingredients']))
    ing_classified = json.loads(data.content)
    if not ing_classified:
        return recipe_info
    repl_dict = dict()
    for i in ing_classified:
        name = i['name']
        originalName = i['originalName']
        amount = str(i['amount'])
        unit = i['unitShort']
        repl_dict[shorter_name(name, originalName)] = [
            amount, unit, originalName]
    #print(repl_dict)
    for ingredient in repl_dict:
        db_name = ''
        good_matches = []
        repl_dict[ingredient].append(['', 0])
        # ing_tok = nltk.word_tokenize(ingredient)
        for amer_ingredient in cuisine_db:
            # c_tok = nltk.word_tokenize(c_i)
            # if len(set(ing_tok) & set(c_tok))/len(set(ing_tok))>=.6:
            s = SequenceMatcher(None, ingredient, amer_ingredient)
            temp_score = s.ratio()
            if temp_score > repl_dict[ingredient][3][1]:
                db_name = amer_ingredient
                repl_dict[ingredient][3][0] = cuisine_db[amer_ingredient]
                repl_dict[ingredient][3][1] = temp_score
                good_matches.append(amer_ingredient)
        # if no good match in chinese ingredient db, keep ingredient the same
        if repl_dict[ingredient][3][1] < .65 or repl_dict[ingredient][3][0] in new_ing_names['new_vals']:
            ing_str = ' '.join(repl_dict[ingredient][0:3])
            new_ingredients.append(ing_str)

        # otherwise, replace (but w/ same ratio)
        else:
            ing_str = ' '.join(
                [repl_dict[ingredient][0], repl_dict[ingredient][1], repl_dict[ingredient][3][0]])
            new_ingredients.append(ing_str)
            new_ing_names[db_name] = [
                repl_dict[ingredient][3][0], good_matches]
            new_ing_names['new_vals'].append(repl_dict[ingredient][3][0])
#print(new_ingredients)
    recipe_info['ingredients'] = new_ingredients

    new_steps = recipe_info['steps']
    for i in range(len(recipe_info["steps"])):
        for key in new_ing_names:
            if key != "new_vals":
                new_steps[i] = recipe_info["steps"][i].lower().replace(
                    key, new_ing_names[key][0])
                for near in new_ing_names[key][1]:
                    new_steps[i] = recipe_info["steps"][i].lower().replace(
                        near, new_ing_names[key][0])
            # if len(key.split()) > 1:
            #     for key_split in key.split():
            #         if key_split not in new_ing_names[key]:
            #             new_steps[i] = recipe_info["steps"][i].replace(
            #                 key_split, new_ing_names[key])
    recipe_info['steps'] = new_steps
    return recipe_info


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
                fraction_obj = sum(
                    map(fractions.Fraction, fraction_str.split()))
                divided = float(fractions.Fraction.from_float(
                    float(fraction_obj) / 2))
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
                fraction_obj = sum(
                    map(fractions.Fraction, fraction_str.split()))
                divided = float(fractions.Fraction.from_float(
                    float(fraction_obj) * 2))
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
