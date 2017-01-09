#! /usr/bin/env python2
# -*- coding: utf-8 -*-
import os
import sys

"""
Generate feedback from student submissions.
The folder name should be the name of the Courseowrk in FEN.
Required structure of the submission (12345, 54321, etc. are candidate numbers):
    ├── group1
    │   ├── 12345
    │   │   ├── submission_file_1
    │   │   └── submission_file_2
    │   └── 54321
    │   │   ├── submission_file_1
    │   │   └── submission_file_2
    │   └── feedback.txt
    ├── group2
    │   ├── 67890
    │   │   ├── file_submission_1
    │   │   └── file_submission_2
    │   └── 09876
    │   │   ├── file_submission_1
    │   │   └── file_submission_2
    │   └── feedback.txt
    .

Where feedback.txt structure is one line with mark (7) and feedback,"
separated by a comma e.g.:

    7, "Feedback."
"""

if len(sys.argv) != 2:
    print "Please give folder with submissions (using the above structure) as"
    print "an argument."
    sys.exit(1)

ROOT = os.path.abspath(sys.argv[1])
COURSEWORK = os.path.split(ROOT)[-1]
FEEDBACK = ["Student,%s,Feedback" % COURSEWORK]
FEEDBACK_FILE = "feedback.txt"


# for each folder in current directory if it contains`feedback.txt`
dirs = [os.path.join(ROOT,d) for d in os.listdir(ROOT) \
        if os.path.isdir(os.path.join(ROOT,d)) and \
           os.path.exists(os.path.join(ROOT,d,FEEDBACK_FILE))]

for d in dirs:
    feedback, mark = "", 0
    with open(os.path.join(d,FEEDBACK_FILE), "r") as ff:
        f = ff.read()
        f_split = f.split(",", 1)
        mark = int(f_split[0])
        feedback = f_split[1].strip()

        # check for unescaped double-quotes
        if feedback.strip("\"").find("\"") != -1:
            print "Unescaped *\"* in: %s/feedback.txt." % d
            sys.exit(1)

    for candidate in os.listdir(d):
        p = os.path.join(d, candidate)
        if not os.path.isdir(p):
            continue
        FEEDBACK.append("%s, %d, %s" % (candidate.strip(), mark, feedback))

with open(os.path.join(ROOT,"%s.csv"%COURSEWORK), "w") as ffile:
    ffile.write("\n".join(FEEDBACK))
