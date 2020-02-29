import spoonacular as sp
import yaml


with open('config.yaml', 'r') as f:
    doc = yaml.load(f)

api = sp.API(doc["key"])

def spoonacularAPI():
    return api
