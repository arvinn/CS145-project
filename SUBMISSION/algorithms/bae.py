import json
import sys

suffix_ing=False

f=open("input/train.json")
lines=f.readlines()
d=""
for line in lines:
    d=d+line
pj=json.loads(str(d))
answer={}
predict={}
custoing={}
classcount={}
ingcount={}
for entry in pj:
    id_num=entry["id"]
    cuisine=entry["cuisine"]
    answer[id_num]=cuisine
    ingredients=entry["ingredients"]
    if cuisine not in classcount:
        classcount[cuisine]=1
    else:
        classcount[cuisine]=classcount[cuisine]+1
    for ing in ingredients:
        #map cuisine,ingredient to number of occurrences
        if cuisine not in custoing:
            custoing[cuisine]={}
        if ing not in custoing[cuisine]:
            custoing[cuisine][ing]=1
        else:
            custoing[cuisine][ing]=custoing[cuisine][ing]+1

        #count # of ingredient occurrences
        if ing not in ingcount:
             ingcount[ing]=1
        else:
            ingcount[ing]=ingcount[ing]+1

#predict
classtot=0
correct=0
for c in classcount:
    classtot=classtot+classcount[c]

f=open("input/test.json")
lines=f.readlines()
d=""
for line in lines:
    d=d+line
pj=json.loads(str(d))


for entry in pj:
    id_num=entry["id"]
    ingredients=entry["ingredients"]
    maxprob=0
    #choose best class for each entry
    for c in classcount:
        currprob=1
        occurr=float(classcount[c]) / float(classtot)
        for ing in ingredients:
            if ing in custoing[c]:
                currprob=currprob*( float(custoing[c][ing]) / float(classcount[c]) )
            else:
                currprob=0
        if currprob*occurr>maxprob:
            maxprob=currprob*occurr
            maxclass=c
    predict[id_num]=maxclass

print "id,cuisine"
for id_num in predict:
    print "{0},{1}".format(id_num, predict[id_num])
