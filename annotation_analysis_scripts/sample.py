import csv
import json
from os import listdir
from os.path import join, isfile
from copy import copy


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
    "Answer.taskAnswers"
]


def fetch_table(table_dir, files, table_id):

    if table_id + ".json" in files:
        table_file = join(table_dir, table_id + ".json")

        with open(table_file) as f:
            table = f.read()
            return table

    else:
        print("TABLE {id} NOT PRESENT".format(id=table_id))


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


def process_results(results):

        results = json.loads(results)[0]

        ds_results = {1: {}, 2: {}, 3: {}}
        results_ = {}

        for res in results:

            if res != "feedback":

                value = results[res]['selected']

                res_ = res.split("_")
                row_name = " ".join(res_[:-1])
                num = int(res_[-1]) + 1

                # print(row_name, "|", num, value)

                if value == False:
                    ds_results[num][row_name] = 0
                elif value == True:
                    ds_results[num][row_name] = 1
            
        return ds_results


def getTableID(sno, datafile):

    with open(datafile) as f:
        datareader = list(csv.reader(f, delimiter='\t'))

        return datareader[int(sno)][1]


class Sample:

    def __init__(self, hitID, tableID, table, hyp, 
                 truthLabel, truthAnnotator,
                 annotatorID, results):

        self.hitID = hitID
        # table ID as in serial no. of table
        self.tableID = tableID
        self.table = table
        self.hyp = hyp
        self.truthLabel = truthLabel
        self.truthAnnotator = truthAnnotator
        self.annotatorID = annotatorID
        self.results = results

        # label: result as binary string
        # fetch table
        table_dir = "./infotabs/data/tables/json"
        onlyfiles = [f for f in listdir(table_dir) 
                     if isfile(join(table_dir, f))]

        # convert table to dict
        table_dict = json.loads(fetch_table(table_dir, onlyfiles, tableID))
        table_rows = list(table_dict.keys())

        self.label, self.noneLabel = to_binary(results, copy(table_rows))

        self.majorityLabel = "".join(['2' for i in range(len(self.label))])
        self.majorityNone = '2'

    def print(self):

        print("%3s %15s %15s %20s %5s %20s %5s" % (self.tableID,
                                                   self.hitID[15:], 
                                                   self.annotatorID, 
                                                   self.label, 
                                                   self.noneLabel,
                                                   self.majorityLabel,
                                                   self.majorityNone))

    def printOne(self):

        # fetch table
        table_dir = "./infotabs/data/tables/json"
        onlyfiles = [f for f in listdir(table_dir) 
                     if isfile(join(table_dir, f))]

        # convert table to dict
        table_dict = json.loads(fetch_table(table_dir, onlyfiles, self.tableID))
        table_rows = list(table_dict.keys())

        # print
        print("=========================================================")
        print(self.hyp)
        print("---------------------------------------------------------")

        print(table_dict["title"])
        table_rows.remove("title")

        for row in table_rows:
            print("%20s %10s" % (row, self.results[row]))
        print("%20s %10s" % ('none', self.results['none']))
            
        print("==========================================================")


    @staticmethod
    def printList(ls):

        print("%3s %15s %15s %20s %5s %20s %5s" % ("", "Hit ID", 
                                                   "Annotator", "Label", 
                                                   "None", "Majority Label",
                                                   "MNone"))
        
        for i in ls:
            i.print()


def to_binary(result, rows):
    """remember: rows does not have the 'none' value"""

    # remove 'title'
    rows.remove('title')
    
    bin = ""            

    noneBit = str(result['none'])

    for row in rows:
        bin += str(result[row])
        
    return bin, noneBit


def mkSamples(idx, hit_row):
    """Make 'n' samples out of a HIT that has 'n' table-hyp
    pairs per hit"""

    # HIT ID
    id_idx = idx["HITId"]
    id = hit_row[id_idx]

    # annotator ID
    ann_idx = idx["WorkerId"]
    annotator = hit_row[ann_idx]

    # index of line numbers of input (as taken from original csv)
    sets_idx = (idx["Input.set1"], idx["Input.set2"], idx["Input.set3"]) 
    sets = [hit_row[x] for x in sets_idx]

    # ids of annotators who generated hypothesis
    aid_idx = (idx["Input.aid1"], idx["Input.aid2"], idx["Input.aid3"]) 
    aids = [hit_row[x] for x in aid_idx]

    # truth values of hypotheses w.r.t table
    truth_idx = (idx["Input.l1"], idx["Input.l2"], idx["Input.l3"])
    truths = [hit_row[x] for x in truth_idx]

    # input tables
    tables_idx = (idx["Input.input1"], idx["Input.input2"],
                      idx["Input.input3"])
    tables = [hit_row[x] for x in tables_idx]

    # hypotheses
    hyp_idx = (idx["Input.h1"], idx["Input.h2"], idx["Input.h3"])
    hyp = [hit_row[x] for x in hyp_idx]

    # answers given
    res_idx = idx["Answer.taskAnswers"]
    results = process_results(hit_row[res_idx])

    # table ID
    tableid_idx = idx["Input.tableid"]
    tableid = hit_row[tableid_idx]

    samples = []
    for i in results:

        result = results[i]
        hitID = id + "_" + str(i)

        sample = Sample(hitID, tableid, 
                        tables[i-1], hyp[i-1],
                        truths[i-1], aids[i-1], 
                        annotator, result)
        sample.printOne() # TEST
        samples.append(sample)

    return samples










