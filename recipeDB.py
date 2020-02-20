import json
import utils
import random

class RecipeDB:
    # initialize the recipeDB.json file
    def __init__(self, path):
        # open the file
        with open(path) as f:
            # load the data
            json_data = json.load(f)
            # process all of the content in the database
            # for example, set self.tools to be an array of tools
            self.tools = json_data["tools"]