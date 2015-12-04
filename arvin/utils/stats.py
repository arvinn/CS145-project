from __future__ import print_function
import json
import pprint
from collections import Counter


f = open('train.json')
data = json.load(f)

all_ingredients = []




cuisine_names = [
     'brazilian',
     'british',
     'cajun_creole',
     'chinese',
     'filipino',
     'french',
     'greek',
     'indian',
     'irish',
     'italian',
     'jamaican',
     'japanese',
     'korean',
     'mexican',
     'moroccan',
     'russian',
     'southern_us',
     'spanish',
     'thai',
     'vietnamese',
     ]



cuisine_ingredients = {
        'brazilian'     : [],
        'british'       : [],
        'cajun_creole'  : [],
        'chinese'       : [],
        'filipino'      : [],
        'french'        : [],
        'greek'         : [],
        'indian'        : [],
        'irish'         : [],
        'italian'       : [],
        'jamaican'      : [],
        'japanese'      : [],
        'korean'        : [],
        'mexican'       : [],
        'moroccan'      : [],
        'russian'       : [],
        'southern_us'   : [],
        'spanish'       : [],
        'thai'          : [],
        'vietnamese'    : [],
     }


for recipe in data:
    cuisine_name = recipe['cuisine']
    ingredients_list = recipe['ingredients']

    for i in ingredients_list:
        cuisine_ingredients[cuisine_name].append(i)
        all_ingredients.append(i)



stats = open('stats.csv', 'w')

for name in cuisine_names:
    counter = Counter(cuisine_ingredients[name])
    total_num_ingredients_for_this_cuisine = len(cuisine_ingredients[name])
    #print(name + ": ")

    top_5 = counter.most_common()[:5]



    print('', file=stats)
    print(name, file=stats)

    for i in top_5:
        count = i[1]
        ingredient = i[0]
        percentage = 100 * float(count)/total_num_ingredients_for_this_cuisine
        percentage = str(int(percentage))
        #print ("  ", ingredient, ":", count, percentage + "%")


        print(ingredient, ',',  count, sep='', file=stats)



overall_count = open('overall_count.csv', 'w')
print("ingredient,count", file=overall_count)
counter = Counter(all_ingredients)
for i in counter.most_common():
    ingredient = '"' + i[0] + '"'
    print(ingredient, i[1], sep=',', file=overall_count)


