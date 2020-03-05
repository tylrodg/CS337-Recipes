import requests
import nltk
import fractions
import re
import string
import difflib

vegan = {
    "chicken bouillon": "vegetable bouillon",
    "beef bouillon": "vegetable bouillon",
    "pork bouillon": "vegetable bouillon",
    "chicken broth": "vegetable broth",
    "chicken stock": "vegetable broth",
    "seafood stock": "vegetable broth",
    "fish stock": "vegetable broth",
    "beef stock": "vegetable broth",
    "beef broth": "vegetable broth",
    "pork stock": "vegetable broth",
    "clam juice": "vegetable broth",
    "fish juice": "vegetable broth",
    "oyster juice": "vegetable broth",
    "ground meat": "textured soy protein",
    "ground turkey": "textured soy protein",
    "ground beef": "textured soy protein",
    "ground pork": "textured soy protein",
    "minced meat": "textured soy protein",
    "sea scallops": "pieces of cut and cubed tofu",
    "crab meat": "spicy tofu",
    "shellfish": "tofu and tempah",
    "worcestershire sauce": "soy sauce and splash of lemon juice",
    "fish sauce": "soy sauce and splash of lemon juice",
    "eel sauce": "teriyaki sauce",
    "refried beans": "pinto beans",
    "pepperoni": "veggie deli slice",
    "pastrami": "veggie deli slice",
    "salami": "veggie deli slice",
    "steak": "thickly sliced eggplant",
    "filet mignon": "portobello mushroom",
    "rib-eye": "portobello mushroom",
    "ribs": "portobello mushroom",
    "burger": "veggie patty",
    "patty": "veggie patty",
    "meatball": "veggie meatball",
    "sausage": "veggie sausage",
    "bacon": "tempeh strips",
    "turkey": "soy patties",
    "chicken breast": "beyond meat chicken breast",
    "chicken leg": "beyond meat chicken leg",
    "chicken thigh": "beyond meat chicken thigh",
    "chicken nuggets": "soy nuggets, non-dairy crust",
    "chicken soup": "vegetable soup",
    "chicken": "tofu",
    "jerky": "oven-dried eggplant",
    "hot dogs": "veggie dogs",
    "pork": "chopped jackfruit",
    "meat": "tofurky deli slice",
    "beef": "tofurky deli slice",
    "veal": "tofurky deli slice",
    "lamb": "tofurky deli slice",
    "tuna": "tempeh",
    "tilapia": "tempeh",
    "sardine": "tempeh",
    "salmon": "tempeh",
    "squid": "cut and cubed tempeh",
    "cod": "pieces of tempeh",
    "clam": "pieces of tempeh",
    "mussel": "pieces of tempeh",
    "halibut": "tempeh",
    "anchovy": "tempeh",
    "oyster": "eggplant",
    "anchovies": "tempeh",
    "mackerel": "tempeh",
    "calamari": "tempeh",
    "shrimp": "cut and cubed tofu",
    "prawn": "cut and cubed tofu",
    "gelatin": "agar flakes",
    "fish": "soy",
    "crab": "spicy tofu",
    "crabmeat": "spicy tofu",
    "scallop": "pieces of cut and cubed tofu",
    "scallops": "pieces of cut and cubed tofu",
    "marshmallow": "gelatin-free marshmallow",
    "milk": "almond milk",
    "cows milk": "milk",
    "butter": "coconut oil",
    "cheese": "cashew-based cheese alternative",
    "yogurt": "almond milk-based yogurt alternative",
    "carmel": "dairy-free carmel",
    "cream": "dairy-free cream",
    "whey": "hemp protein",
    "casein": "hemp",
    "dressing": "dairy-free dressing",
    "tomato sauce": "non-dairy tomato sauce",
    "honey": "maple syrup",
    "egg": "mashed banana",
    "eggs": "mashed banana",
    "milk": "soy milk",
    "mayonnaise": "vegan mayonnaise"
}

nonVegan = {
    "vegetable bouillon": "beef bouillon",
    "vegetable broth": "beef broth",
    "textured soy protein": "ground beef",
    "veggie deli slice": "salami",
    "veg deli slice": "salami",
    "vegetarian deli slice": "salami",
    "portobello mushroom": "ribs",
    "mushroom": "chicken, cubed",
    "veggie burger": "chicken burger",
    "veg burger": "chicken burger",
    "tofu pieces": "beef, cubed",
    "veggie meatball": "chicken meatball",
    "veg meatball": "chicken meatball",
    "veggie sausage": "chicken sausage",
    "veg sausage": "chicken sausage",
    "veggie bacon": "bacon",
    "veg bacon": "bacon",
    "veggie patties": "chicken patties",
    "veg patties": "chicken patties",
    "soy turkey": "turkey",
    "beyond meant tenders": "chicken thigh",
    "soy chicken": "chicken",
    "veggie jerky": "jerky",
    "tempeh": "calamari",
    "tofurky deli slice": "lamb",
    "tofu": "cut and cubed chicken",
    "paneer": "cut and cubed lamb",
    "agar flakes": "gelatin",
    "butter": "lard",
    "pinto beans": "refried beans",
    "veg soup": "chicken soup",
    "vegetable soup": "chicken soup",
    "potatoes": "cubed chicken",
    "rice": "rice cooked in chicken stock",
    "pizza": "pepperoni pizza",
    "eggplant": " cubed beef",
    "jackfruit": "pulled pork",
    "cauliflower": "beef strip",
    "sweet potatoes": "cubed chicken breasts",
    "sweet potato": "cubed chicken breasts",
    "lentils": "cut fish of your choice",
    "lentil": "cut fish of your choice",
    "carrots": "prawns",
    "carrot": "prawn",
    "marshmallow": "gelatin-free marshmallow",
    "almond milk": "milk",
    "coconut milk": "milk",
    "cashew milk": "milk",
    "oat milk": "milk",
    "coconut oil": "butter",
    "cheese": "cashew-based cheese alternative",
    "yogurt": "almond milk-based yogurt alternative",
    "carmel": "dairy-free carmel",
    "cream": "dairy-free cream",
    "hemp protein": "whey",
    "pea protein": "whey",
    "casein": "hemp",
    "dairy-free dressing": "dressing",
    "maple syrup": "honey",
    "canola oil": "butter",
    "soy milk": "milk",
    "vegan mayonnaise": "mayonnaise",
    "agave nectar": "honey"
}

measurements = [
    "#",
    "#s",
    "bag",
    "bags",
    "bunch",
    "bunches",
    "can",
    "head",
    "heads",
    "cans",
    "clove",
    "cloves",
    "cube",
    "cubes",
    "dash",
    "dashes",
    "envelope",
    "envelopes",
    "gram",
    "grams",
    "inch",
    "inches",
    "kilogram",
    "kilograms",
    "lb",
    "lbs",
    "ounce",
    "ounces",
    "oz",
    "ozs",
    "package",
    "packages",
    "packet",
    "packets",
    "piece",
    "pieces",
    "pinch",
    "pinches",
    "pound",
    "pounds",
    "sheet",
    "sheets",
    "slice",
    "slices",
    "strip",
    "stripsTbsp",
    "Tbsps",
    "bottle",
    "bottles",
    "c",
    "cs",
    "cup",
    "cups",
    "dessertspoon",
    "dessertspoons",
    "fl oz",
    "fl ozs",
    "fluid ounce",
    "fluid ounces",
    "fluid oz",
    "fluid ozs",
    "gal",
    "gallon",
    "gallons",
    "gals",
    "jar",
    "jars",
    "liter",
    "liters",
    "milliliter",
    "milliliters",
    "ml",
    "mls",
    "pint",
    "pieces",
    "pints",
    "pt",
    "pts",
    "qt",
    "qts",
    "quart",
    "quarts",
    "tablespoon",
    "tablespoons",
    "teaspoon",
    "teaspoons",
    "tsp",
    "tsps",
]

replacements = {
    "chocolate": ["3 strips of crispy bacon", "Chop bacon and sprinkle on top."],
    "almonds": ["3 strips of crispy bacon", "Chop bacon and sprinkle on top."],
    "baked good": [
        "1 jar (2 cups) ready-to-use mincemeat",
        "Ensure that you stir mincemeat with dry ingredients.",
    ],
    "noodles": [
        "2 cups cubed beef",
        "Cook beef thoroughly and then combine with noodles.",
    ],
    "romaine lettuce": [
        "2 cups grilled cubed chicken",
        "Combine grilled chicken with other ingredients.",
    ],
    "soy sauce": [
        "2 cups cubed beef",
        "Cook beef thoroughly and then combine at the end.",
    ],
    "cheese": ["1 pound ground beef", "Cook beef until browned. Combine."],
    "bread": ["1/2 pound diced chicken sausage", "Fry until browned."],
    "potatoes": [
        "1/2 pound cubed beef",
        "Cook beef thoroughly and then combine with potatoes",
    ],
    "zucchini": [
        "1/2 pound cubed beef",
        "Cook beef thoroughly and then combine with zucchini",
    ],
}


def veganReplacer(recipe_info):
    str1 = ""
    keys_lst = list(replacements.keys())
    for i in recipe_info["ingredients"]:
        str1 = str1 + " " + i

    if "egg" in str1 and "chocolate" not in str1:
        ingredient = replacements["baked good"][0]
        step = replacements["baked good"][1]
        recipe_info["ingredients"].append(ingredient)
        recipe_info["steps"].append(step)
    else:
        for i in keys_lst:
            if i in str1:
                ingredient = replacements[i][0]
                step = replacements[i][1]
                recipe_info["ingredients"].append(ingredient)
                recipe_info["steps"].append(step)
                break

    return recipe_info


def nonVeganChecker(recipe_info):
    lst = list(nonVegan.keys())
    all_matches = []
    for i in recipe_info["ingredients"]:
        matches = [x for x in lst if x in i]
        all_matches.extend(matches)
    if all_matches != []:
        return "True"
    return "False"


def veganHelper(recipe_info, chosen_dict):
    ingr_lst = []
    step_lst = []
    keys_lst = {}

    if chosen_dict == "vegan":
        chosen_dict = vegan
        # add a disclaimer
        ingr_lst.append(
            "It is important to recognize that when choosing a vegan recipe to avoid milk and gelatin. Please read the label carefully to check whether or not the ingredients used contain any milk, meat, or any other animal-derived products: \n"
        )
    if chosen_dict == "nonVegan":
        chosen_dict = nonVegan

    # generate the list
    for i in recipe_info["ingredients"]:
        no_punc = i.translate(str.maketrans("", "", string.punctuation))
        meat_matches = [x for x in chosen_dict if x in no_punc]
        if meat_matches != []:
            keys_lst[meat_matches[0]] = chosen_dict[meat_matches[0]]
            veg_substitute = chosen_dict[meat_matches[0]]

            """ get measurements """
            measurement_matches = []
            j = i.split()
            for each in j:
                if each in measurements:
                    measurement_matches.append(each)
            if measurement_matches != []:
                splitter = i.split(measurement_matches[0])
                measurement = splitter[0] + " " + measurement_matches[0]
                new_ingredient = measurement + " " + veg_substitute
            else:
                nums = re.findall("\\d+", i)[(-1)]
                sp = i.rfind(nums)
                measurement = i[:sp] + nums
                new_ingredient = measurement + " " + veg_substitute
            ingr_lst.append(new_ingredient)
        else:
            ingr_lst.append(i)

    recipe_info["ingredients"] = ingr_lst
    for i in recipe_info["steps"]:
        no_punc = i.translate(str.maketrans("", "", string.punctuation))
        meat_matches = [x for x in chosen_dict if x in no_punc]
        if meat_matches != []:
            list_of_keys = list(keys_lst.keys())
            for ind, meat in enumerate(meat_matches):
                m = difflib.get_close_matches(meat, list_of_keys)
                if m == []:
                    if meat == "meat" and ind != 0:
                        indexer = ind - 1
                        veg_substitute = chosen_dict[meat_matches[indexer]]
                    else:
                        veg_substitute = chosen_dict[meat]
                else:
                    veg_substitute = chosen_dict[m[0]]
                i = i.replace(meat, veg_substitute)

        # generate the steps
        step_lst.append(i)

    recipe_info["steps"] = step_lst
    return recipe_info
