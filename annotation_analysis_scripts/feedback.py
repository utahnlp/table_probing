"""Filter the feedback"""
import sys
import csv
import json

filename = sys.argv[1]

with open(filename) as f:
    rows = list(csv.reader(f))
    titles = rows[0]

    ans_idx = titles.index("Answer.taskAnswers")
    ann_idx = titles.index("WorkerId")

    # filter out answer and annotator
    answers = [(x[ann_idx], json.loads(x[ans_idx])) for x in rows[1:]]

    for ann, ans in answers[1:]:

        if "feedback" in ans[0]:
            print(ann)
            print(ans["feedback"])
            print("-------------------------------------------------")

