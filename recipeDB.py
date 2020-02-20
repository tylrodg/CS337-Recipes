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

            # set of descriptions
            self.meat = json_data["descriptions"]["meat"]
            self.seafood = json_data["descriptions"]["seafood"]
            self.dessert = json_data["descriptions"]["dessert"]
            self.veggie = json_data["descriptions"]["veggie"]
            self.other = json_data["descriptions"]["veggie"]

            # set of seasons
            self.seasonings = json_data["seasonings"]

            # set of styles
            self.styles = json_data["styles"]

            # set of measurements
            self.solidMeasurements = json_data["measurement"]["solids"]
            self.liquidMeasurements = json_data["measurement"]["liquids"]

            # set of cooking methods