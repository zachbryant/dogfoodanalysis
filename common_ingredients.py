import json

def main():
    with open("food.json", "r") as file:
        food_data = json.loads(file.read())
        ingredient_set_common = set()
        ingredient_set_unique = set()
        for food_entry in food_data:
            entry_ingredients = food_entry["ingredients"]
            for ingredient in entry_ingredients:
                if ingredient in ingredient_set_unique:
                    ingredient_set_common.add(ingredient)
                else:
                    ingredient_set_unique.add(ingredient)
        ingredient_set_unique = ingredient_set_unique.difference(ingredient_set_common)

        print("Unique ingredients:\n{}".format(ingredient_set_unique))
        print("===============")
        print("Common ingredients:\n{}".format(ingredient_set_common))


if __name__ == "__main__":
    main()