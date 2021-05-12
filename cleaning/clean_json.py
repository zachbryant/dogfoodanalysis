import json, re

def clean_ing(ingredients):
    for x in range(len(ingredients)):
        ing = re.sub('\(.*\)', '', ingredients[x].strip())
        if ing == "flax seed":
            print("hi")
        ing = ing.replace("flax seed", "flaxseed")
        ing = ing.replace("dehydrated", "").replace("flax seed", "flaxseed").replace("freeze-dried", "")
        ing = ing.replace("whole", "").replace(" and", "").replace("vitamins (", "").replace("vitamins [", "").replace(
            "minerals [", "").replace("minerals (", "").replace("minerals(", "")
        ing = ing.replace("trace minerals [", "").replace("]", "").replace("[", "").replace(
            "preserved with mixed tocopherols", "mixed tocopherols").replace("preserved with natural mixed tocopherols",
                                                                             "mixed tocopherols")
        ing = ing.replace("by- product", "byproduct").replace("mixed-tocopherols", "mixed tocopherols").replace(
            "naturally preserved with", "preserved with").replace("naturally", "").replace("natural", "")
        ing = ing.replace(".", "").replace(".", "").replace("", "").replace(")", "").replace("de-boned", "").replace(
            "deboned", "").replace("organic", "").replace("fresh", "").replace("ground", "")
        ing = re.sub("(\w\d{6}|\w\-\d{4}|\d[a-z]\d{5})", "", ing)
        if ',' in ing:
            split_ing = ing.split(',')
            ing = split_ing[0].strip()
            ingredients.insert(x + 1, split_ing[1].strip())
        if ' & ' in ing:
            split_ing = ing.split(' & ')
            ing = split_ing[0].strip()
            ingredients.insert(x + 1, split_ing[1].strip())
        if ' and ' in ing:
            split_ing = ing.split(' and ')
            ing = split_ing[0].strip()
            ingredients.insert(x + 1, split_ing[1].strip())
        if ' preserved with ' in ing:
            print(ing)
            split_ing = ing.split(' preserved with ')
            ing = split_ing[0].strip()
            print(split_ing[1])
            ingredients.insert(x + 1, split_ing[1].strip())
        if ing.startswith("preserved with"):
            ing = ing.replace("preserved with", "")
        if ing.endswith("mixed tocopherols"):
            ing = ing.replace("mixed tocopherols", "")
            ingredients.insert(x + 1, "mixed tocopherols")

        ingredients[x] = ing.strip()
    while '' in ingredients:
        ingredients.remove('')

    return ingredients


def fix_ga(old_ga):
    new_ga = {}
    for ga in old_ga.items():
        ga_key = ga[0].strip().lower()
        ga_value = ga[1]
        ga_value["amount"] = ga_value["amount"].strip()
        ga_value["bound"] = ga_value["bound"].strip().replace("(", "").replace(")", "")
        if not ("min" in ga_value["bound"] or "max" in ga_value['bound']) and len(ga_value['bound']) > 0:
            print(ga_value["bound"])
            ga_value["amount"] = "{} {}".format(ga_value["amount"], ga_value["bound"]).lower()
            ga_value["bound"] = ""
        new_ga[ga_key] = ga_value

    return new_ga


def fix_cal(calories):
    for x in range(len(calories)):
        # calories[x] = calories[x].replace("kcal me", "kcal").replace("me ", "").replace("on an as fed basis","").replace("cup.","cup").replace("kcal / kg1", "kcal/kg").replace("this food contains ", "").replace("=", "").replace("me","").replace("(me)", "").replace(",", "").replace(" of () kilogram", "/kg").replace(".", "")
        calories[x] = calories[x].replace(" / ", "/")

    if len(calories) >= 2:
        index = 0
        while index < len(calories) - 1:
            if len(calories[index]) == 1 and calories[index].isdigit():
                # print("{}, {}, {}".format(calories[index], calories[index + 1], calories[index + 2]))
                print("{}, {}".format(calories[index], calories[index + 1]))
                calories[index] = calories[index] + calories[index + 1]
                calories.pop(index + 1)
                index = 0
            index = index + 1

    if len(calories) == 1 and " : " in calories[0]:
        print(calories)
        calories = calories[0].split(" : ")
        print(calories)

    # for sym in [',', ';', 'or', '=', '', '()']:
        # while sym in calories:
            # calories.remove(sym)

    return calories


def trim(arr):
    return [x.strip() for x in arr]


def fix_weight_name(name, weight):
    if weight == "null" or len(weight) == 0:
        return name, ''
    if not weight[0].isdigit():
        name = '{}, {}'.format(name, weight)
        weight = ''
        print(name)
    return name, weight


with open("food.old.json", "r") as file:
    with open("../food.json", "w") as outfile:
        raw_data = file.read().lower()
        raw_data = re.sub('\\s+', ' ', raw_data)
        data = json.loads(raw_data)
        new_data = []
        for entry in data:
            entry["calories"] = fix_cal(entry["calories"])
            name, weight = fix_weight_name(entry["name"], entry["weight"])
            entry["weight"] = weight
            entry["name"] = name
            # entry["guaranteed_analysis"] = fix_ga(entry["guaranteed_analysis"])
            entry["ingredients"] = trim(entry["ingredients"]) # trim(clean_ing(entry["ingredients"]))
            new_data.append(entry)

        outfile.write(json.dumps(new_data))