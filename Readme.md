# `split_into_groups.py` #
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

# `generate_feedback.py` #
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
