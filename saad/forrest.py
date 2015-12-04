#Classification using RandomForrest bag of words model
#Modifed to do bag of ingredients instead of bag of words
#~76% accuracy

import json
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import LabelEncoder
#from nltk.stem import WordNetLemmatizer
#import re
import pandas as pd

train_set = json.load(open("../train.json"))
test_set = json.load(open("../test.json"))

#holds ingredients for each entry in train as a space seperated string
train_ingredients = []

#holds ingredients for each entry in test as a space seperated string
test_ingredients = []

#list of cuisines encountered in train
train_cuisines = [entry['cuisine'] for entry in train_set]

#list of IDs encountered in test
test_ids = [entry['id'] for entry in test_set]


#construct train_ingredients
#multiword ingredients become '-' connected so that they are distinguished in the
#space seperated string
#e.g. 'black pepper fish' becomes 'black-pepper-fish'
for entry in train_set:
    ings = [w.replace(' ', '-') for w in entry['ingredients']]

    train_ingredients.append(' '.join(ings))

#construct test_ingredients
for entry in test_set:
    ings = [w.replace(' ', '-') for w in entry['ingredients']]

    test_ingredients.append(' '.join(ings))

#used to encode labels as numbers for use with RandomForestClassifier
le = LabelEncoder()

#encode cuisines as numbers
train_cuisines = le.fit_transform(train_cuisines)

#used to create bag of ingredients vocabulary and create features for each entry
vectorizer = CountVectorizer()
train_features = vectorizer.fit_transform(train_ingredients).toarray()
test_features = vectorizer.transform(test_ingredients).toarray()

#fits features to specified cuisines
clf = RandomForestClassifier(n_estimators = 500)
clf = clf.fit(train_features, train_cuisines)

#predicts cuisines for test data set
result = clf.predict(test_features)

#inverse_transform maps decodes numbers back to cuisines
output = pd.DataFrame(data={'id':test_ids, 'cuisine':le.inverse_transform(result)})

#force explicit ordering of columns
output = output[['id', 'cuisine']]
output.to_csv('forrest.csv', index=False)


