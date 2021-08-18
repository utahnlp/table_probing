import csv
import json
from os import listdir
from os.path import isfile, join

from sample import Sample 

datafile = "./infotabs/data/maindata/infotabs_dev.tsv"

def getTableID(sno):

    with open(datafile) as f:
        datareader = list(csv.reader(f, delimiter='\t'))

        return datareader[int(sno)][1]


def fetch_table(table_dir, files, table_id):

    if table_id + ".json" in files:
        table_file = join(table_dir, table_id + ".json")

        with open(table_file) as f:
            table = f.read()
            return table

    else:
        print("TABLE {id} NOT PRESENT".format(id=table_id))


class TableHypPair:

    def __init__(self):

        self.samples = []

        self.majorityLabel = "-1"
        self.majorityNone = "-1"

        # to be populated later
        self.tableID = ""
        self.table = ""
        self.hyp = ""
        self.truthLabel = ""
        self.truthAnnotator = ""

    def add(self, sample):
        self.samples.append(sample)

    def fetchWorkers(self):
        return [s.annotatorID for s in self.samples]

    def fetchLabels(self):
        return [(s.label + s.noneLabel) for s in self.samples]

    def populate(self):

        repr = self.samples[0]
        self.tableID = repr.tableID
        self.table = repr.table
        self.hyp = repr.hyp
        self.truthLabel = repr.truthLabel
        self.truthAnnotator = repr.truthAnnotator

    def print(self):

        # fetch table
        table_dir = "./infotabs/data/tables/json"
        onlyfiles = [f for f in listdir(table_dir) 
                     if isfile(join(table_dir, f))]
        table_dict = json.loads(fetch_table(table_dir, onlyfiles, self.tableID))
        table_rows = list(table_dict.keys())

        # print
        print("=========================================================")
        print(self.hyp)
        print("---------------------------------------------------------")

        print(table_dict["title"])
        table_rows.remove("title")

        for i, row in enumerate(table_rows):
            # collect results for that sample
            res = []
            for s in self.samples:
                res.append(s.label[i])

            print("%20s %20s" % (row, str(res)))

        res = []
        for s in self.samples:
            res.append(s.noneLabel)
        print("%20s %20s" % ('none', str(res)))
            
        print("==========================================================")

    def toJSON(self):
        """Add a JSON table-label field to object"""

        # fetch table
        table_dir = "./infotabs/data/tables/json"
        onlyfiles = [f for f in listdir(table_dir) 
                     if isfile(join(table_dir, f))]
        table_dict = json.loads(fetch_table(table_dir, onlyfiles, self.tableID))
        table_rows = list(table_dict.keys())

        # init json
        table_results = {}

        table_rows.remove("title")

        for i, row in enumerate(table_rows):
            # get majority label for that row
                table_results[row] = self.majorityLabel[i]

        table_results["none"] = self.majorityNone
        self.json = json.dumps(table_results)


    @staticmethod
    def writeCSV(ls, csvname):

        with open(csvname, "w+") as f:

            writer = csv.writer(f)

            writer.writerow(["Table ID", "Hypothesis", "Generator ID", 
                             "Truth Label", "Worker IDs", "Labels",
                             "Majority Label", "JSON"])

            for row in ls:
                row.populate()
                writer.writerow([row.tableID, row.hyp, row.truthAnnotator,
                                 row.truthLabel, row.fetchWorkers(), 
                                 row.fetchLabels(),
                                 row.majorityLabel + row.majorityNone,
                                 row.json])

    def get_majority_label(self):

        def majority_bit(bits):
            n1 = bits.count('1')
            n0 = bits.count('0')

            if n0 > n1:
                return '0'
            else:
                return '1'

        def nth_bit(n):
            return list(map(lambda x: x[n], labels))

        # get majority for label
        labels = [sample.label for sample in self.samples]
        label_size = len(labels[0])

        majority_label = ""
        for i in range(label_size):
            nth_bits = nth_bit(i)
            majority = majority_bit(nth_bits)
            majority_label += majority

        self.majorityLabel = majority_label

        # get majority for none label
        mbits = [s.noneLabel for s in self.samples]
        majority_none = majority_bit(mbits)

        self.majorityNone = majority_none

        # update all samples in group
        for sample in self.samples:
            sample.majorityLabel = majority_label
            sample.majorityNone = majority_none
