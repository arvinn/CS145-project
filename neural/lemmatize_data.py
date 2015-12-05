import json
from nltk.stem import WordNetLemmatizer
import re

f=open("test.json")
lines=f.readlines()
d=""
for line in lines:
    d=d+line
pj=json.loads(str(d))
key=0
for entry in pj:
    count=0
    for ing in entry["ingredients"]:
        #entry["ingredients"][count]=ing.split(" ")[-1]
        temp = [WordNetLemmatizer().lemmatize(re.sub('[^A-Za-z]', ' ', w)) for w in ing.split(' ')]

        entry["ingredients"][count]=' '.join(temp)
        count=count+1
    pj[key]=entry
    key=key+1

with open('test_lemmatized.json', 'w') as outfile:
        json.dump(pj, outfile, indent=4)
