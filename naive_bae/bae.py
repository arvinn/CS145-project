import json
import sys

train=True
if(len(sys.argv)<2):
    raise Exception("Need to pass 'train' or 'test' as parameter")
if(sys.argv[1]=="test"):
    train=False
elif(sys.argv[1]!="train"):
    raise Exception("Invalid parameter passed to script")

suffix_ing=True

f=open("train.json")
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
        if suffix_ing:
            if len(ing.split(" "))>1:
                print ing
            ing=ing.split(" ")[-1]
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

if train==False:
    f=open("test.json")
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
            if suffix_ing:
                ing=ing.split(" ")[-1]
            if ing in custoing[c]:
                currprob=currprob*( float(custoing[c][ing]) / float(classcount[c]) )
            else:
                currprob=0
        if currprob*occurr>maxprob:
            maxprob=currprob*occurr
            maxclass=c
    predict[id_num]=maxclass
    if train and predict[id_num]==answer[id_num]:
        correct=correct+1
    #print "Predicted: {0},  Expected: {1},  MaxProb: {2}".format(predict[id_num], answer[id_num], str(maxprob))

if train:
    print "Percentage of correction predictions: "+str(float(correct) / float(classtot))
else:
    print "id,cuisine"
    for id_num in predict:
        print "{0},{1}".format(id_num, predict[id_num])
