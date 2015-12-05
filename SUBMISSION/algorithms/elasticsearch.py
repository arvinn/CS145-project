#! /usr/bin/env python
import time
import sys
import json


from elasticsearch import Elasticsearch
from elasticsearch.client import IndicesClient
from elasticsearch.helpers import streaming_bulk
from elasticsearch_dsl.connections import connections


# Analyzer used for search queries
whitespace_analyzer = {
    'type': 'custom',
    'tokenizer': 'whitespace',
    'filter': [
      'lowercase',
      'asciifolding',
      'word_delimiter',
    ]
}


def create_index(indices_client):
    """
    Creates the ElasticSearch index
    Place all index settings here.
    """

    indices_client.create(
        index="kaggle",
        body={
            'settings': {
                'number_of_shards': 1,
                'number_of_replicas': 0,
            }
        }
    )


def create_cuisine_mapping(indices_client, cuisine):
    indices_client.put_mapping(
        index = 'kaggle',
        doc_type = cuisine,
        body = {
            'properties': {
                'ingredients': {
                    'type': 'string',
                    "index_analyzer": "english",
                    "search_analyzer": "english"
                },
            }
        }
    )



cuisines = [
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


def recipe_iterables():
    # Load the json
    with open('train.json', 'r') as f:
        data = json.load(f)

        for recipe in data:
            yield {
                '_type': recipe['cuisine'],
                'ingredients': " ".join(recipe['ingredients']),
            }


def index_training_data(client):
    # Index the training data
    count = 0
    
    print ("Indexing the data")
    for _ in streaming_bulk(
            client,
            (recipe_iterables()),
            index='kaggle'
            ):

        count += 1

    print ("Done indexing")

if __name__ == '__main__':

    client = Elasticsearch()
    indices_client = IndicesClient(client)

    # Index the data only if passed in an argument to the script.
    if len(sys.argv) > 1:
        # Create index and mappings
        indices_client.delete(index='kaggle', ignore=404)
        create_index(indices_client)
        for cuisine in cuisines:
            create_cuisine_mapping(indices_client, cuisine)
        index_training_data(client)


    print("Analyzing: results will be posted in submissions.csv")
    with open('submission.csv', 'w') as sol:
        print('id,cuisine', file=sol)

        with open('test.json') as f:
            recipes = json.load(f)

            count = 0
            for recipe in recipes:

                ingredients = " ".join(recipe['ingredients'])

                response = client.search(
                        index="kaggle",
                        size=10,
                        body={
                            "query": {
                                "match": {
                                    'ingredients': {
                                        'query': ingredients,
                                    }
                                }
                            }
                        }
                    )

                hits = []
                for i in range(10):
                    hits.append(response['hits']['hits'][i])

                #print (json.dumps(response, indent=4))
                #print (response['hits']['hits'][0])
                percent_diff_between_first_two_matches = ((1 - float(hits[1]['_score'])/hits[0]['_score']) * 100) 
                if hits[0]['_type'] != hits[1]['_type'] and percent_diff_between_first_two_matches < 10:  # percent threshold == 10
                    recipe_id = recipe['id']
                    if hits[1]['_type'] == hits[2]['_type']:
                        cuisine = (hits[1]['_type'])                # get the majority, else just get the first one
                    else:
                        cuisine = (hits[0]['_type'])
                else:
                    recipe_id = recipe['id']
                    cuisine = (hits[0]['_type'])


                print (recipe_id, cuisine, sep=',', file=sol) # write it to file





##############################



                """
                print()
                print ("==============================")
                print (recipe['id'])
                print ("1st and 2nd % diff = ", (1 - float(hits[1]['_score'])/hits[0]['_score']) * 100) 
                print (hits[0]['_type'], hits[0]['_score'])
                print (hits[1]['_type'], hits[1]['_score'])
                print (hits[2]['_type'], hits[2]['_score'])
                print (hits[3]['_type'], hits[3]['_score'])
                print (hits[4]['_type'], hits[4]['_score'])
                print (hits[5]['_type'], hits[5]['_score'])
                print (hits[6]['_type'], hits[6]['_score'])
                print (hits[7]['_type'], hits[7]['_score'])
                print (hits[8]['_type'], hits[8]['_score'])
                print (hits[9]['_type'], hits[9]['_score'])
                """


                count += 1
                if count % 500 == 0: print (count)
                #if count == 100: break   # stop early for debugging


    print("Done")
