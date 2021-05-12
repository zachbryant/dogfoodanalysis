import csv, json, re

with open("food.csv", "r") as file:
    with open("../food.json", "w") as outfile:
        csv_reader = csv.reader(file, delimiter=",")
        foods = []
        for row in csv_reader:
            ga = row[4]

            ga_new = {}
            ga_rows = ga.split("</tr><tr>")
            for gar in ga_rows:
                gac = gar.split("</td><td>")
                if len(gac) == 1:
                    continue
                gac1 = gac[0].replace("<tr>", "").replace("<td>", "").replace("</td>", "").replace("</tr>", "")
                gac2 = gac[1].replace("<tr>", "").replace("<td>", "").replace("</td>", "").replace("</tr>", "")
                data_tmp = gac2.rsplit(" ", 1)
                bound = data_tmp[1] if len(data_tmp) > 1 else "null"
                ga_new[gac1] = {"amount": data_tmp[0], "bound": bound.lower()}
            name_weight = row[1].rsplit(", ", 1)
            name = name_weight[0]
            weight = name_weight[1] if len(name_weight) > 1 else "null"

            ingredients = row[2].lower()
            if ingredients.startswith("new:"):
                ingredients = re.sub("(original:.*|new: )", "", ingredients)
                print(row[5])
                #row[3] = input("Calories? ")
            print(len(row))

            calories = row[3].lower().replace("per", "").replace("this diet contains ", "").replace("kilocalories","kcal").replace(" ME", "").replace("(calculated)", "").replace("metabolizable energy", "").replace("kcal  cup","kcal/cup").replace("  8 oz. ", "/").replace("8-oz ", "").replace(" me/kg", "/kg")
            if calories.startswith("em kcal/lb"):
                continue
            calories = re.split("\s*(or|=|,|;)\s*", calories.strip())
            if ga_new == {} or calories is None or calories[0] == 'null':
                continue
            # if len(calories) == 1:
            # print(calories)

            food = {
                "url": row[5],
                "name": name,
                "weight": weight,
                "ingredients": ingredients,
                "calories": calories,
                "guaranteed_analysis": ga_new
            }
            foods.append(food)
        outfile.write(json.dumps(foods))
