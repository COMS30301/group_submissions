import sys
import pandas as pd

# Read in group/students assignment
groups = pd.read_csv("group_def_safe_upload.csv")
groups.index = groups["Student"]

# Read in students list
students = pd.read_csv("student_list.csv")
students.index = students["Username"].values
students["Groups"] = groups["Groups"]
del students["Name"]

s = students[pd.notnull(students["Groups"])]

# Read in group marking
marks = pd.read_csv("M5_marks.csv")
marks.index = marks["Groups"]

for i,r in s.iterrows():
    s.set_value(i, "M5", marks.loc[r["Groups"]]["Mark"])
    s.set_value(i, "Feedback", marks.loc[r["Groups"]]["Feedback"])

# Save student marks
out = s[["Candidate", "M5", "Feedback"]]
out.to_csv("student_marks.csv", index=False)
