"""To run file:

python process_data.py <csv file to get data from> \
                       <file prefix to write data to>

"""
import csv
import json
import sys
from os.path import isdir
from os import mkdir

from sample import Sample, mkSamples
from annotator import Annotator
from table_hyp_pair import TableHypPair

# CSV file to process data from
filename = sys.argv[1]

print(sys.argv[1])

# CSV file prefix to write data to
# extract csv name from path
if not isdir("./results"):
    mkdir("results")
    
read_csv_name = filename.split("/")
read_csv_name = read_csv_name[-1] 
write_to_prefix = "results/" + read_csv_name[:-4]


d = [
    "HITId", 
    "AssignmentId", 
    "WorkerId",
    "Input.set1",
    "Input.set2",
    "Input.set3",
    "Input.aid1",
    "Input.aid2",
    "Input.aid3",
    "Input.h1",
    "Input.h2",
    "Input.h3",
    "Input.input1",
    "Input.input2",
    "Input.input3",
    "Input.l1",
    "Input.l2",
    "Input.l3",
    "Answer.taskAnswers",
    "Input.tableid"
]


def indexing(titles):
    indexes = {}
    for i in d:
        indexes[i] = titles.index(i)

    return indexes


def readCSV(csvfile):

    # read data file
    rows = []
    with open(csvfile) as f:
        datareader = csv.reader(f, delimiter=',')

        for row in datareader:
            rows.append(row) 
        
    return rows


def xor(a, b):
    """XOR of two binary strings"""
    s = zip(list(a), list(b))
    xor = ""

    for p in s:
        if p[0] == p[1]:
            xor += '0'
        else:
            xor += '1'

    return xor


if __name__ == "__main__":

    data = readCSV(filename)

    titles = data[0]

    indexes = indexing(titles)

    samples = []
    for row in data[1:]:
        samples += mkSamples(indexes, row)
    """correct up to here"""
    print("======== SEPARATION INTO TABLE-HYPOTHESIS PAIRS ========")

    # make set of table-hypothesis pairs and get the majority label
    thPairs = {}
    for sample in samples:
        # sample.printOne() # TEST

        if sample.hitID not in thPairs:
            thPairs[sample.hitID] = TableHypPair()
            thPairs[sample.hitID].add(sample)
            thPairs[sample.hitID].populate()
        else:    
            thPairs[sample.hitID].add(sample)
    """
    # TEST
    for id in thPairs:
        thPairs[id].print()
    """

    for id in thPairs:
        thPairs[id].get_majority_label()
        thPairs[id].toJSON()
        print("-------------------------------------------------------")
        print(id)
        Sample.printList(thPairs[id].samples)

    # write CSV 1
    print(write_to_prefix)
    TableHypPair.writeCSV(list(thPairs.values()), write_to_prefix + "_annotations.csv")

    # make Annotator list based on that data
    anns = {}
    for sample in samples:
        if sample.annotatorID not in anns:
            anns[sample.annotatorID] = Annotator(sample.annotatorID)

    for sample in samples:

        anns[sample.annotatorID].score_majority(sample.label, sample.noneLabel, sample.majorityLabel, sample.majorityNone)

    for id in thPairs:
        pair = thPairs[id]

        Annotator.score_all_pairs(anns, pair)

    # make annotator list but normalized
    annsNormal = {}
    for sample in samples:
        if sample.annotatorID not in annsNormal:
            annsNormal[sample.annotatorID] = Annotator(sample.annotatorID)

    for sample in samples:

        annsNormal[sample.annotatorID].score_majority_normal(sample.label, sample.noneLabel, sample.majorityLabel, sample.majorityNone)

    for id in thPairs:
        pair = thPairs[id]

        Annotator.score_all_pairs_normal(annsNormal, pair)

    Annotator.printList(list(anns.values()))
    Annotator.printList(list(annsNormal.values()))

    Annotator.writeCSVMajorityNonNormal(list(anns.values()), 
                                        write_to_prefix + "_annotators_majority.csv")
    Annotator.writeCSVPairwiseNonNormal(list(anns.values()),
                                        write_to_prefix + "_annotators_pairwise.csv")
    Annotator.writeCSVMajorityNormal(list(annsNormal.values()), 
                                        write_to_prefix + "_annotators_majority_normal.csv")
    Annotator.writeCSVPairwiseNormal(list(annsNormal.values()),
                                        write_to_prefix + "_annotators_pairwise_normal.csv")


    
        

 

