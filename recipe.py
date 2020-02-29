import utils

# recipe class is the basic shell of the recipe
# has to get all of the ingredients and the directions first, which is done elsewhere
class Recipe:
    def __init__(self, name="Name", ingredients=[], directions=[], cookingMethods=[], tools=[])

    self.name = name
    self.ingredients = ingredients
    self.directions = directions
    self.cookingMethods = cookingMethods
    self.tools = tools
