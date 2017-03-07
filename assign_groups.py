#!/usr/bin/env python
import csv
import sys

HEADERS = ["Your name and username", "Partner 1", "Partner 2"]
GROUP_PATTERN = "G%02d"

if __name__ ==  '__main__':
    if len(sys.argv) < 3:
        msg = "The first argument should be csv file from Google Spreadsheet"
        msg += "The second argument should be csv file form FEN with student list"
        sys.exit(msg)

    # read in usernames downloaded form FEN
    students = []
    uids = []
    with open(sys.argv[2], 'r') as usernames:
        u = csv.reader(usernames)
        for i in u:
            if not i:
                continue
            students.append(i)
    students.reverse()

    header = students.pop()
    uid_index = header.index("Username")

    for i in students:
        uids.append(i[uid_index].lower().strip())

    choices = []
    with open(sys.argv[1], 'r') as csvfile:
        choices_csv = csv.reader(csvfile)
        for row in choices_csv:
            if not row:
                continue
            choices.append(row)
    choices.reverse()

    header = choices.pop()
    uid_index = []
    for i in HEADERS:
        if i in header:
            uid_index.append(header.index(i))

    groups = []
    seen = []
    for i in choices:
        gr = []
        visited = False
        for j in uid_index:
            k = i[j].split("-")
            for ki in k:
                kis = ki.strip()
                if kis in uids and kis not in gr:
                    gr.append(kis)
                    if kis in seen:
                        visited = True
                    else:
                        seen.append(kis)
        gr = list(set(gr))
        gr.sort()

        # Check for duplicates
        if gr not in groups and visited:
            repeated_groups = []
            for x in groups:
                for y in x:
                    if y in gr:
                        repeated_groups.append(x)
                        break
            if len(repeated_groups) > 1:
                sys.exit("Two groups with the same person")
            else:
                groups.remove(repeated_groups[0])
                for z in gr:
                    if z not in repeated_groups[0]:
                        repeated_groups[0].append(z)
                groups.append(repeated_groups[0])
        elif gr not in groups:
            groups.append(gr)

    for i in groups:
        for j in i:
            try:
                uids.remove(j)
            except:
                print "double response: ", j
    print "Students without group submission:"
    print uids

    fen = "Student, Group\n"
    gs = ""
    gc = 1
    for i in groups:
        for j in i:
            fen += j + ", " + GROUP_PATTERN%gc + "\n"
        gc += 1
    for i in uids:
        fen += i + ", " + GROUP_PATTERN%gc + "\n"
        gc += 1
    for i in range(1, gc):
        gs += GROUP_PATTERN%i + ", "
    print gs[:-2]
    with open("group_assignment.csv", "w") as ff:
        ff.write(fen)
