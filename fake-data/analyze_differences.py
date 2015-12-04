#! /usr/bin/env python
from __future__ import print_function

import sys
import json
import collections

"""
Compares the expected and actual cuisines.
Reports what gets confused.
"""


def get_cuisine(line):
    # line is "id,cuisine\n"
    # get 'cuisine' part
    return line.split(',')[1][:-1]

def get_id(line):
    return line.split(',')[0]


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

# Initalize the dict
mistakes = {}
for cuisine in cuisines:
    mistakes[cuisine] = {}
    mistakes[cuisine]['count'] = 0

    for cuisine2 in cuisines:
        mistakes[cuisine][cuisine2] = 0


if len(sys.argv) < 2:
    print("  Pass in your .csv submission file as an argument to the script")
    exit()

submission_file = sys.argv[1]


same_count = 0
total_count = 0
with open('solutions.csv', 'r') as sol:
    with open(submission_file, 'r') as sub:

        # skip 'id,cuisine' line
        sol.readline()
        sub.readline()

        for l1 in sol:
            l2 = sub.readline()

            recipe_id = get_id(l1)
            actual_cuisine = get_cuisine(l1)
            guessed_cuisine = get_cuisine(l2)

            if actual_cuisine == guessed_cuisine:
                same_count += 1
            else:
                mistakes[actual_cuisine][guessed_cuisine] += 1
                mistakes[actual_cuisine]['count'] += 1        # number of total mistakes with this cuisine


            total_count += 1


print("%d%% lines are the same" % (float(same_count)/total_count * 100))

diff_count = total_count - same_count


for actual_cuisine in cuisines:
    actual_dict = mistakes[actual_cuisine]
    count = mistakes[actual_cuisine]['count']

    print (actual_cuisine + ": %d mistakes (%d%% of total):" % ( count ,(float(count)/diff_count * 100)))

    top_3_mistaken_for = sorted(actual_dict, key=actual_dict.get, reverse=True)[1:4]  # [0] is the total count 

    for cuisine_mistaken_for in top_3_mistaken_for:
        print ("     ", cuisine_mistaken_for, mistakes[actual_cuisine][cuisine_mistaken_for],    
                            "%d%%" % ((mistakes[actual_cuisine][cuisine_mistaken_for])/float(count) * 100))

