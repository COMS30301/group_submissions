import os
import pandas as pd
import re
import shutil
import sys

INFO = """
Organise student's submissions by group rather than by candidate number.

The first argument is folder with students submissions, downloaded from FEN.

The second argument is CSV student list that can be downloaded from FEN as
*CSV Marks Download*, with *Student ID:* flag set to *All*, hence the following
format:

    Candidate,Name,StudentNumber,Username,"Coursework_name",Mark,Flag
    12345,"Doe, John",0987654,ab54321,0N#,0,N#

The third one is student group assignment in CSV format (with either *User* or
*Student* keyword):

    {User,Student},Groups
    ab12345,Group 1
    ba54321,Group 2
    yz67890,Group 2
    zy09876,Group 1

You can filter groups by setting `GROUP_FIX` variable. Then only groups
containing specified substring will be considered.
"""

if len(sys.argv) != 4:
    print "Too few arguments!\n"
    print INFO
    sys.exit(1)

GROUP_FIX = ""

ROOT = os.path.abspath(sys.argv[1])
OUTDIR = ROOT + "_sorted"

students = pd.read_csv(sys.argv[2])
students.index = students["Username"].values

groups = pd.read_csv(sys.argv[3])
groups_keyword = "Student" if "Student" in groups.columns else "User"
groups.index = groups[groups_keyword].values

students["Groups"] = groups["Groups"]
students.fillna("", inplace=True)
students.to_csv(os.path.join(os.path.split(ROOT)[0], "student_group.csv"))

################################################################################
def remove_archived(root):
    for k in os.listdir(root):
        if re.match("\d+-.*", k) is not None or k.startswith("."):
            l = os.path.join(root,k)
            if os.path.isdir(l):
                shutil.rmtree(l)
            else:
                os.remove(l)

students.index = students["Candidate"].values
groups = list(set(students["Groups"].values))
# Filter groups
groups = [i for i in groups if GROUP_FIX in i] if GROUP_FIX else groups
groups = [i for i in groups if (type(i) == str or type(i) == unicode) and i]

non_submitters = []
os.makedirs(OUTDIR)
for i in groups:
    os.makedirs(os.path.join(OUTDIR, i))
    st = students[students["Groups"] == i]["Candidate"].values
    for j in st:
        try:
            out_dir = os.path.join(OUTDIR,i,str(j))
            shutil.copytree(os.path.join(ROOT,str(j)), out_dir)
            # Remove archived submissions
            # On time
            remove_archived(out_dir)
            out_dir_ls = os.listdir(out_dir)
            # Day late
            if "daylate" in out_dir_ls:
                remove_archived(os.path.join(out_dir,"daylate"))
            # Week late
            if "weeklate" in out_dir_ls:
                remove_archived(os.path.join(out_dir,"weeklate"))
        except OSError:
            non_submitters.append((i, str(j)))
for i in sorted(non_submitters):
    print "Studnet %s from groups %s did not submit." % i[::-1]
