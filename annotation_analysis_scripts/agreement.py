"""Agreement: %(num times agreed/num. rows marked)
   11 Agreement: %(num times marked 1 and agreed/num times marked 1)
"""

import csv
import sys
from os import remove

print(sys.argv[1])

csvfile1 = sys.argv[1] + "_annotators_majority_normal.csv"
new_csvfile1 = sys.argv[1] + "_annotators_majority_normal_agreement.tsv"
csvfile2 = sys.argv[1] + "_annotators_pairwise_normal.csv"
new_csvfile2 = sys.argv[1] + "_annotators_pairwise_normal_agreement.tsv"

csvfile3 = sys.argv[1] + "_annotators_majority.csv"
new_csvfile3 = sys.argv[1] + "_annotators_majority_agreement.tsv"
csvfile4 = sys.argv[1] + "_annotators_pairwise.csv"
new_csvfile4 = sys.argv[1] + "_annotators_pairwise_agreement.tsv"



def processCSV(csvfile, new_csvfile):

    with open(csvfile) as f:

        datareader = list(csv.reader(f))
        new_rows = []
        total = 0.0
        titles = datareader[0]
        new_titles = datareader[0] + ["Accuracy", "Accuracy_OOT",
                                      "Precision", "Precision_OOT", 
                                      "Recall", "Recall_OOT"]
        new_rows.append(new_titles)


        def idx(rowname):
            return titles.index(rowname)

        
        # calculate precision, precision,
        # precision_including_oot, and recall_11 rows
        for row in datareader[1:]:

            def val(rowname):
                return float(row[idx(rowname)])

            # precision = true pos / (true pos + false pos)
            # precision_oot = a11 + none_11 / 
            #             a11 + d10 + none_11 + none_10
            precision_oot_num = val("a11") + val("none_11")
            precision_oot_den = val("a11") + val("d10") + \
                                val("none_11") + val("none_10")
            if precision_oot_den == 0:
                precision_oot = 0
            else:
                precision_oot = precision_oot_num/precision_oot_den

            # precision = a11 / a11 + d10 
            precision = val("a11") / (val("a11") + val("d10"))

            # accuracy = true markings / total markings
            # accuracy = a11 + a00 / m1
            accuracy = val("a11") + val("a00") / (val("a11") + val("a00") + val("d10") + val("d01"))


            # accuracy_including_oot = a11 + none_11 / 
            #                 total markings + total none                       
            accuracy_oot_num = val("a11") + val("none_11") + val("a00") +  val("none_00")
            accuracy_oot = accuracy_oot_num / (val("a11") + val("a00") + val("d10") + val("d01")) + (val("none_11") + val("none_00") + val("none_10") + val("none_01"))

            # recall = true pos / true pos + false neg.
            # recall = a11 / a11 + d01
            recall = val("a11") / (val("a11") + val("d01"))

            # recall_including_oot = a11 + none_11 / 
            #                        a11 + d01 + none_11 + none_01
            recall_oot_den = val("a11") + val("d01") + \
                             val("none_11") + val("none_01")
            recall_oot_num = val("a11") + val("none_11")
            
            if recall_oot_den == 0:
                recall_oot = 0
            else:
                recall_oot = recall_oot_num / recall_oot_den

            new_row = row + [accuracy, accuracy_oot,
                             precision, precision_oot,
                             recall, recall_oot]
            new_rows.append(new_row)

        with open(new_csvfile, "w+") as f:
            writer = csv.writer(f, delimiter="\t")

            for row in new_rows:
                writer.writerow(row)

processCSV(csvfile1, new_csvfile1)
remove(csvfile1)
processCSV(csvfile2, new_csvfile2)
remove(csvfile2)
processCSV(csvfile3, new_csvfile3)
remove(csvfile3)
processCSV(csvfile4, new_csvfile4)
remove(csvfile4)
