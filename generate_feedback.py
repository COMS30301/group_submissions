#! /usr/bin/env python2
# -*- coding: utf-8 -*-
import os
import re
import sys

INFO = """
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
    print "Please specify students submission folder as an argument.\n"

    print INFO
    sys.exit(1)

ROOT = os.path.abspath(sys.argv[1])
COURSEWORK = os.path.split(ROOT)[-1]
FEEDBACK = ["Student,%s,Feedback" % COURSEWORK]
FEEDBACK_FILE = "feedback.txt"


# for each folder in current directory if it contains`feedback.txt`
dirs = []
for d in os.listdir(ROOT):
    if os.path.isdir(os.path.join(ROOT,d)):
        if os.path.exists(os.path.join(ROOT,d,FEEDBACK_FILE)):
            dirs.append(os.path.join(ROOT,d))
        else:
            print "No feedback for group %s" % d

escape_doublequotes = re.compile(r"\"(?!\")", re.IGNORECASE)
for d in dirs:
    feedback, mark = "", 0
    with open(os.path.join(d,FEEDBACK_FILE), "r") as ff:
        f = ff.read()
        f_split = f.split(",", 1)
        mark = int(f_split[0])
        feedback = f_split[1].strip()
        feedback = feedback.strip("\"")

        # check for unescaped double-quotes
        if feedback.find("\"") != -1:
            print "Unescaped *\"* in: %s/feedback.txt" % d
            feedback, _ = escape_doublequotes.subn("\"\"", feedback)
        feedback = "\"%s\"" % feedback


    for candidate in os.listdir(d):
        p = os.path.join(d, candidate)
        if not os.path.isdir(p) or not candidate.strip("/").isdigit():
            continue
        FEEDBACK.append("%s, %d, %s" % (candidate.strip(), mark, feedback))

with open(os.path.join(ROOT,"%s.csv"%COURSEWORK), "w") as ffile:
    ffile.write("\n".join(FEEDBACK))
