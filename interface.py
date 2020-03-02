import sys
import json
import re
import recipe_api

def input_recipe():
    url = ""
    while not url:
        url = input("Recipe URL: ").lower()
        if url == "quit":
            print("Thanks for using ReciParser! Bye!\n")
            sys.exit(0)
        if "allrecipes" not in url:
            print("Invalid URL provided! Please submit again.\n")
            url = ""
    name = recipe_api.get_name(url)
    print(
        "Thanks for submitting that URL! The recipe you requested was " + name + ".\n"
    )
    return url, name

def confirm_recipe(url):
    response = ""
    while not response:
        response = input("Is that the correct recipe? ([y]es/[n]o): ").lower()
        if response == "quit":
            print("Thanks for using ReciParser! Bye!\n")
            sys.exit(0)
        elif response == "no" or response == "n":
            print("No worries! Please provide the correct URL.")
            url = input_recipe()
            response = ""
        elif response == "yes" or response == "y":
            print("Great! Let's get started.")
        else:
            print("Sorry I didn't understand that.")
            response = ""
    return url

def fetch_recipe_info(url, name):

    print(
        "First, we'll fetch the recipe information for you. Sit tight, this might take a minute or two. This will be provided below, as well as in a document for your reference later on."
    )
    fields = ["recipe_name", "ingredients", "tools", "methods", "steps"]
    recipe_data = {c: None for c in fields}

    for f in fields:
        if f == "recipe_name":
            recipe_data[f] = name
        else:
            recipe_data[f] = getattr(recipe_api, "get_%s" % f)(url)

    doc_name = re.sub(r"\W+", "", name.lower())
    with open(doc_name + ".json", "w") as recipe_file:
        json.dump(recipe_data, recipe_file)
    return recipe_data

def transform_recipe(recipe_info):
    print(
        "Which transformation would you like to apply to the recipe? Type [o]ptions to show what transformations are available."
    )
    transformed_recipe = {}
    available_transforms = [t for t in dir(recipe_api) if "transform" in t]
    transform = ""
    while not transform:
        transform = input("Transformation: ").lower()
        if transform == "quit":
            print("Thanks for using ReciParser! Bye!\n")
            sys.exit(0)
        elif transform == "option" or transform == "options" or transform == "o" or transform == "Options":
            for at in available_transforms:
                print(at)
            # reset to blank
            transform = ""
        elif transform not in available_transforms:
            print("Sorry, I didn't quite understand that.")
            transform = ""
        else:
            print(transform + "? Great choice! We'll get on that right away.")
            transformed_recipe = getattr(recipe_api, transform)(recipe_info)
    return transformed_recipe

def main():
    # Begin process
    print(
        "Welcome to ReciParser! Let's get started! \nPlease provide a valid AllRecipes.com URL or type 'quit' to quit the program. You can quit whenever we request your input.\n"
    )
    # Request recipe
    url, name = input_recipe()
    # Confirm URL submitted
    url = confirm_recipe(url)
    # Get data from allrecipes.com
    recipe_info = fetch_recipe_info(url, name)
    # Display data
    for i in recipe_info:
        if i == "recipe_name":
            print("Recipe Name: " + recipe_info[i])
        else:
            print(i.capitalize())
            for e in recipe_info[i]:
                print("- " + e)
        print("\n")

    # Apply transformations (allows for multiple until user wants to stop)
    nq = True
    while nq:
        transformed_recipe = transform_recipe(recipe_info)
        for i in transformed_recipe:
            if i == "recipe_name":
                print("Recipe Name: " + transformed_recipe[i])
            else:
                print(i.capitalize())
                for e in transformed_recipe[i]:
                    print("- " + e)
            print("\n")
        cont = ""
        while not cont:
            cont = input(
                "Would you like to continue applying transformations? ([y]es/[n]o): "
            ).lower()
            if cont == "y" or cont == "yes":
                continue
            elif cont == "n" or cont == "no":
                nq = False
            else:
                print("Sorry I didn't understand that.")
                cont = ""
    print("Thanks for using ReciParser! Bye!\n")
    sys.exit(0)

if __name__ == "__main__":
    main()
