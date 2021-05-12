import json
import re

def main():
    while True:
        food_name = input("Food name: ")
        food_ingredients = process_csl(input("List of ingredients: "))
        food_guaranteed_analysis = process_chewy_ga(input("Guaranteed analysis: "))
        food_kcal_cup = int(input("Kcals per cup: "))
        store_food(food_name, food_ingredients, food_guaranteed_analysis, food_kcal_cup)
        if input("Quit? ").lower() == 'q':
            print("Bye")
            break


def process_chewy_ga(raw):
    lines = raw.split("\n")
    data = {}
    for line in lines:
        cols = line.split("\t")
        category = cols[0]
        col_amount_pieces = cols[1].rsplit(" ")
        amount = col_amount_pieces[0]
        constraint = col_amount_pieces[1]
        data[category] = {
            "amount": amount,
            "constraint": constraint,
        }



def store_food(name, ingredients, guaranteed_analysis, food_kcal_cup):
    print(type(name))
    print(type(ingredients))
    print(type(guaranteed_analysis))
    with open("food.json", "r+") as file:
        raw_data = file.read()
        data = json.loads(raw_data)
        data[name] = {
            "ingredients": ingredients,
            "guaranteed_analysis": guaranteed_analysis,
            "kcals_cup": food_kcal_cup
        }
        raw_data = json.dumps(data)
        file.write(raw_data)

def process_csl(raw):
    raw = raw.lower().replace(".", "")
    return re.split(",\\s+", raw)

if __name__ == "__main__":
    main()


