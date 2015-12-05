#Output code based strategy
#~75% accuracy

import json
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.multiclass import OutputCodeClassifier
from sklearn.svm import LinearSVC
from nltk.stem import WordNetLemmatizer
import pandas as pd
import re

import nltk
nltk.data.path.append('/Users/arvinnguyen/developer/bruinwalk-redesign/cs145/CS145-project/fake-data/nltk_data')

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
for entry in train_set:
    ings = [WordNetLemmatizer().lemmatize(re.sub('[^A-Za-z]', ' ', w)) for w in entry['ingredients']]

    train_ingredients.append(' '.join(ings))

#construct test_ingredients
for entry in test_set:
    ings = [WordNetLemmatizer().lemmatize(re.sub('[^A-Za-z]', ' ', w)) for w in entry['ingredients']]

    test_ingredients.append(' '.join(ings))

#used to encode labels as numbers for use with RandomForestClassifier
le = LabelEncoder()

#encode cuisines as numbers
train_cuisines = le.fit_transform(train_cuisines)

#used to create bag of ingredients vocabulary and create features for each entry
vectorizer = CountVectorizer()
train_features = vectorizer.fit_transform(train_ingredients).toarray()
test_features = vectorizer.transform(test_ingredients).toarray()

clf = OutputCodeClassifier(LinearSVC(random_state=0), code_size=2, random_state=2)
result = clf.fit(train_features, train_cuisines).predict(test_features)

output = pd.DataFrame(data={'id':test_ids, 'cuisine':le.inverse_transform(result)})

#force explicit ordering of columns
output = output[['id', 'cuisine']]
output.to_csv('ecoc.csv', index=False)


