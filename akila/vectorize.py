import json

f=open("ings_list")
lines=f.readlines()
count=0
strtoid={}
for line in lines:
    strtoid[line[:-1]]=count;
    count=count+1

with open("ing_to_id", "w") as fp:
    json.dump(strtoid, fp)
