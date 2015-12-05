#! /usr/bin/env python
from __future__ import print_function

"""
This script takes the outputs of different algorithms.  For each recipe, it simply
takes the cuisine that the most algorithms identify the recipe as.  If all of the
algorithms disagree, we use the algorithm's classification that has the
highest percentage accuracy.

To run:
    ./get_majority best_algorithm_first.csv other_output.csv other2_output.csv ...
"""

import sys
from collections import Counter

if len(sys.argv) < 2:
    print("  Pass in your .csv submission files as arguments to the script")
    print("  The most accurate one should go first and will be used as a tie-breaker")
    exit()


# Open all CSVs
best = open(sys.argv[1])            # output of the best algo
csv_files = []
for filename in sys.argv[2:]:
    csv_files.append(open(filename))

# skip "id,cuisine" line
best.readline()
for csv in csv_files:
    csv.readline()


majority_csv = open('majority.csv', 'w')
print('id,cuisine', file=majority_csv)


def get_cuisine(line):
    # line is "id,cuisine\n"
    # get 'cuisine' part
    return line.split(',')[1][:-1]

def get_id(line):
    return line.split(',')[0]


line_count = 0
conflict_count = 0
for line in best:
    line_count += 1
    best_algo_cuisine = get_cuisine(line)

    cuisines = []
    cuisines.append(best_algo_cuisine)
    recipe_id = get_id(line)

    for csv in csv_files:
        line = csv.readline()
        cuisines.append(get_cuisine(line))

    counter = Counter(cuisines)
    conflict_count += len(counter)

    # All the CSVs conflict, use the best algorithm
    if counter.most_common()[0][1] == 1:
        cuisine = best_algo_cuisine
    else:
        cuisine = counter.most_common()[0][0]

    print (recipe_id, cuisine, sep=',', file=majority_csv)


print("  Average number of conflicting cuisines: %f " % (float(conflict_count)/line_count))
