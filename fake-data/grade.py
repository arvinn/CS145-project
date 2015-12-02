#! /usr/bin/env python
from __future__ import print_function

import sys

if len(sys.argv) < 2:
    print("  Pass in your .csv submission file as an argument to the script")
    exit()

submission_file = sys.argv[1]
print (submission_file)



same_count = 0
total_count = 0
with open('solutions.csv', 'r') as sol:
    with open('submission.csv', 'r') as sub:
        for l1 in sol:
            l2 = sub.readline()

            if l1 == l2:
                same_count += 1

            total_count += 1


print("%d%% lines are the same" % (float(same_count)/total_count * 100))
