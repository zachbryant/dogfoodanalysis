import json

with open("../food.json") as good_ing:
    with open("food.old.old.json") as bad_ing:
        with open("food.old.json", "w") as outfile:
            ents = []
            good_ing_ent = json.loads(good_ing.read())
            bad_ing_ent = json.loads(bad_ing.read())

            for bad_ent in bad_ing_ent:
                url = bad_ent['url']
                for good_ent in good_ing_ent:
                    if good_ent['url'] == url:
                        bad_ent['ingredients'] = good_ent['ingredients']
                        ents.append(bad_ent)
                        continue
            outfile.write(json.dumps(ents))