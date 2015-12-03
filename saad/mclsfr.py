import json
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import LabelEncoder
import pandas as pd

train_set = json.load(open("../train.json"))
test_set = json.load(open("../test.json"))

train_ingredients = []
test_ingredients = []
train_cuisines = [entry['cuisine'] for entry in train_set]
test_ids = [entry['id'] for entry in test_set]

for entry in train_set:
    ings = [w.replace(' ', '-') for w in entry['ingredients']]
    train_ingredients.append(' '.join(ings))

for entry in test_set:
    ings = [w.replace(' ', '-') for w in entry['ingredients']]
    test_ingredients.append(' '.join(ings))

le = LabelEncoder()
train_cuisines = le.fit_transform(train_cuisines) #encode cuisines as numbers

vectorizer = CountVectorizer()
train_features = vectorizer.fit_transform(train_ingredients).toarray()

forest = RandomForestClassifier(n_estimators = 500)
forest = forest.fit(train_features, train_cuisines)

result = forest.predict(vectorizer.transform(test_ingredients).toarray())

output = pd.DataFrame(data={'id':test_ids, 'cuisine':le.inverse_transform(result)} )
output = output[['id', 'cuisine']] #force explicit ordering
output.to_csv('saad.csv', index=False)


