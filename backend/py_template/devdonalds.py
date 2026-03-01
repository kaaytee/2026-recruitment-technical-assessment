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
	(ls)
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

#  checkss ssearch name
# returns true if valid 
# false overwise
def check_recipe (name: str):
	name_lookup = {item["name"]: item for item in cookbook}

	result = name_lookup.get(name)
 
	if not result:
		return False
 
	if result["type"] != "recipe":
		return False

	for item in result.get("requiredItems", []):
		if not name_lookup.get(item["name"]):
			return False
      
	return True


@app.route('/summary', methods=['GET'])
def summary():
	# The endpoint should additionally return with status code 400 if:

    # A recipe with the corresponding name cannot be found.
    # The searched name is NOT a recipe name (ie. an ingredient).
    # The recipe contains recipes or ingredients that aren't in the cookbook.
	search = request.args.get("name")
	if  not search or not check_recipe(search):
		print("hi")
		return "recipe does not exist ", 400 

	name_lookup = {item["name"]: item for item in cookbook}

 
	#  Iteratively add entries into a stack and calcualte the sum
	# if the value iss a recipie just multiple the current qunality to the entry and add its required items 
	# if its a ingredient jusst calcualt total time and add to total-ingredidents
 
	# only have 1 since we only want 1 "serving" of the searched value
	s = [(search, 1)] 
	total_time = 0
	total_ingredients = {}
	while s:
		current_name, current_q = s.pop()
		current_item = name_lookup.get(current_name)
		if current_item["type"] == "ingredient":
			total_time += current_item.get("cookTime") * current_q
			total_ingredients[current_name] = total_ingredients.get(current_name, 0) + current_q
   
		elif current_item["type"] == "recipe":
			for n in current_item["requiredItems"]:
				s.append((n["name"], (n["quantity"] * current_q)))
			

	return jsonify({
		"name": search,
		"cookTime": total_time,
		"ingredients": [{"name": k, "quantity": v} for k, v in total_ingredients.items()]
	}), 200


# =============================================================================
# ==== DO NOT TOUCH ===========================================================
# =============================================================================

if __name__ == '__main__':
	app.run(debug=True, port=8080)