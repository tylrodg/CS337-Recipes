import bs4
import nltk


def get_name(url):
    '''
    Scrape the given url for the name of the recipe.

    Parameters: url (string): Link to an AllRecipes recipe. 

    Returns: recipe_name (string): Name of recipe.
    '''
    return 'vibes,,,132'


def get_ingredients(url):
    '''
    Scrape the given url for the ingredients of the recipe.

    Parameters: url (string): Link to an AllRecipes recipe.

    Returns: ingredients (list): List of ingredients from recipe.
    '''
    return ['hi', 'bye']
    pass


def get_tools(url):
    '''
    Scrape the given url for the name of the recipe.

    Parameters: url (string): Link to an AllRecipes recipe.

    Returns: tools (list): List of tools used in the recipe.
    '''
    return ['hi', 'bye']

    pass


def get_methods(url):
    '''
    Scrape the given url for the name of the recipe.

    Parameters: url (string): Link to an AllRecipes recipe.

    Returns: methods (list): List of cooking methods used in the recipe.
    '''
    return ['hi', 'bye']

    pass


def get_steps(url):
    '''
    Scrape the given url for the name of the recipe.

    Parameters: url (string): Link to an AllRecipes recipe.

    Returns: steps (list): List of steps required to complete the recipe.
    '''
    return ['hi', 'bye']
    pass

def transform_to_veg(recipe_info):
    pass

def transform_from_veg(recipe_info):
    return {'test':['test again!']}

def transform_to_healthy(recipe_info):
    pass

def transform_to_italian(recipe_info):
    pass