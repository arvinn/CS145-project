import json
import sys
from sklearn import tree


with open("input/ing_to_id") as ing_to_id:
    ingtoid=json.load(ing_to_id)

with open("input/train.json") as train:
    train_entries=json.load(train)

with open("input/test.json") as test:
    test_entries=json.load(test)

lening=len(ingtoid)
lentrain=len(train_entries)
lentest=len(test_entries)

mat_train = [[0 for x in range(lening)] for x in range(lentrain)]

custoid={}
idtocus={}
labels=[]

count=0;

#map cuisines to id's and map create label vector
for entry in train_entries:
    cus=entry["cuisine"]
    if cus not in custoid:
        custoid[cus]=count;
        idtocus[count]=cus;
        count=count+1
    labels.append(custoid[cus])

#create feature vector of ingredients for each recipie
currentry=0
for entry in train_entries:
    ings=entry["ingredients"]
    for i in ings:
        ing_id=ingtoid[i]
        mat_train[currentry][ing_id]=1
    currentry=currentry+1

currentry=0
mat_test=[[0 for x in range(lening)] for x in range(lentest)]
for entry in test_entries:
    ings=entry["ingredients"]
    for i in ings:
        if i in ingtoid:
            ing_id=ingtoid[i]
        else:
            ing_id=0
        mat_test[currentry][ing_id]=1
    currentry=currentry+1


clf=tree.DecisionTreeClassifier()
clf=clf.fit(mat_train, labels)
preds=clf.predict(mat_test)

count=0
print "id, cuisine"
for entry in test_entries:
    print str(entry["id"])+","+str(idtocus[preds[count]])
    count=count+1

