from dataclasses import dataclass
from typing import List, Dict, Union
from flask import Flask, request, jsonify
import re

# ==== Type Definitions, feel free to add or modify ===========================
@dataclass
class CookbookEntry:
	name: str

@dataclass
class RequiredItem():
	name: str
	quantity: int

@dataclass
class Recipe(CookbookEntry):
	required_items: List[RequiredItem]

@dataclass
class Ingredient(CookbookEntry):
	cook_time: int


# =============================================================================
# ==== HTTP Endpoint Stubs ====================================================
# =============================================================================
app = Flask(__name__)

# Store your recipes here!
cookbook = [] 

# Task 1 helper (don't touch)
@app.route("/parse", methods=['POST'])
def parse():
	data = request.get_json()
	recipe_name = data.get('input', '')
	parsed_name = parse_handwriting(recipe_name)
	if parsed_name is None:
		return 'Invalid recipe name', 400
	return jsonify({'msg': parsed_name}), 200

# [TASK 1] ====================================================================
# Takes in a recipeName and returns it in a form that 
def parse_handwriting(recipeName: str) -> Union[str | None]:
	if not recipeName:
		return None
 
	remove_non_alp = re.sub(r'[^a-zA-Z\s\-]', '', recipeName)
	replace_space = re.sub(r'[^a-zA-Z]', ' ', remove_non_alp)
	return " ".join(replace_space.split()).title()


# [TASK 2] ====================================================================
# Endpoint that adds a CookbookEntry to your magical cookbook

def is_unique(string:str, ls: List[CookbookEntry]):
	print(ls)
	names = set([l["name"] for l in ls])
	return string not in names

def unique_requiredItems(ls: List ):
	names = set([l["name"] for l in ls])
	return len(names) == len(ls)
 
@app.route('/entry', methods=['POST'])
def create_entry():
	json = request.get_json()
	# check errors, if not a valid type 
	#  if cooktime is < 0 
	print(json, json["type"])
	if json["type"] not in ['ingredient', 'recipe'] :
		return jsonify(message="Not a valid type"), 400

	if  json.get("type") == "ingredient":
		if  json["cookTime"] < 0 or json["cookTime"] == None :
			return jsonify(message="cookTime musst be >= 0"), 400
		
	if not is_unique(json["name"], cookbook):
		return jsonify(message="name already exists!"), 400

	if json.get("type") == "recipe":
		if not  unique_requiredItems(json["requiredItems"]):
			return jsonify(message="required items must be unique!"), 400

	cookbook.append(json)

	return {}, 200


# [TASK 3] ====================================================================
# Endpoint that returns a summary of a recipe that corresponds to a query name
@app.route('/summary', methods=['GET'])
def summary():
	# TODO: implement me
	return 'not implemented', 500


# =============================================================================
# ==== DO NOT TOUCH ===========================================================
# =============================================================================

if __name__ == '__main__':
	print(parse_handwriting("meatball"))
	print(parse_handwriting("a b   c D"))
	print(parse_handwriting("A  @@b @c     F"))
	print(parse_handwriting("RizZ Riso00Tto"))
	app.run(debug=True, port=8080)