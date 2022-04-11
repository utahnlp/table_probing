"""Parse MTURK output files that consist of one or two tables/HIT, so we can feed them to the analyzer scripts.

Basically process_data.py but with a different mkSample function"""

import csv
import json

from sample import Sample
from annotator import Annotator
from table_hyp_pair import TableHypPair


datafile_2 = "/home/kw/Data/batches_remaining/Batch_train_109_results.csv"
datafile_1 = "/home/kw/Data/batches_remaining/Batch_train_110_results.csv"
write_to_prefix = "results/remaining"

d1 = ["HITId", "AssignmentId", "WorkerId", "Input.set1", "Input.aid1",
      "Input.h1", "Input.input1", "Input.l1", "Answer.taskAnswers",
      "Input.tableid"]
d2 = ["HITId", "AssignmentId", "WorkerId", "Input.set1", "Input.set2",
      "Input.aid1", "Input.aid2", "Input.h1", "Input.h2", 
      "Input.input1", "Input.input2", "Input.l1", "Input.l2", 
      "Answer.taskAnswers", "Input.tableid"]
 

def indexing(titles, d):
    indexes = {}
    for i in d:
        indexes[i] = titles.index(i)

    return indexes


def process_results_1(results):

    results = json.loads(results)[0]

    ds_results = {1: {}}

    for res in results:

        if res != "feedback":

            value = results[res]['selected']

            res_ = res.split("_")
            row_name = " ".join(res_[:-1])
            num = int(res_[-1]) + 1

            # print(row_name, "|", num, value)

            if value is False:
                ds_results[num][row_name] = 0
            elif value is True:
                ds_results[num][row_name] = 1
            
    return ds_results


def process_results_2(results):

    results = json.loads(results)[0]

    ds_results = {1: {}, 2: {}}

    for res in results:

        if res != "feedback":

            value = results[res]['selected']

            res_ = res.split("_")
            row_name = " ".join(res_[:-1])
            num = int(res_[-1]) + 1

            # print(row_name, "|", num, value)

            if value is False:
                ds_results[num][row_name] = 0
            elif value is True:
                ds_results[num][row_name] = 1
            
    return ds_results


def mkSamples1(idx, hit_row):
    """Make a list of samples out of a HIT with one table-hyp pair per hit"""

    # HIT ID
    id_idx = idx["HITId"]
    id = hit_row[id_idx]

    # annotator ID
    ann_idx = idx["WorkerId"]
    annotator = hit_row[ann_idx]

    # ids of annotators who generated hypothesis
    aid_idx = [idx["Input.aid1"]]
    aids = [hit_row[x] for x in aid_idx]

    # truth values of hypotheses w.r.t table
    truth_idx = [idx["Input.l1"]]
    truths = [hit_row[x] for x in truth_idx]

    # input tables
    tables_idx = [idx["Input.input1"]]
    tables = [hit_row[x] for x in tables_idx]

    # hypotheses
    hyp_idx = [idx["Input.h1"]]
    hyp = [hit_row[x] for x in hyp_idx]

    # answers given
    res_idx = idx["Answer.taskAnswers"]
    results = process_results_1(hit_row[res_idx])

    # table ID
    tableid_idx = idx["Input.tableid"]
    tableid = hit_row[tableid_idx]

    samples = []
    for i in results:

        result = results[i]
        hitID = id + "_" + str(i)

        sample = Sample(hitID, tableid, 
                        tables[i - 1], hyp[i - 1],
                        truths[i - 1], aids[i - 1], 
                        annotator, result)
        sample.printOne()  # TEST
        samples.append(sample)

    return samples


def mkSamples2(idx, hit_row):
    """Make 'n' samples out of a HIT that has 'n' table-hyp
    pairs per hit"""

    # HIT ID
    id_idx = idx["HITId"]
    id = hit_row[id_idx]

    # annotator ID
    ann_idx = idx["WorkerId"]
    annotator = hit_row[ann_idx]

    # ids of annotators who generated hypothesis
    aid_idx = (idx["Input.aid1"], idx["Input.aid2"]) 
    aids = [hit_row[x] for x in aid_idx]

    # truth values of hypotheses w.r.t table
    truth_idx = (idx["Input.l1"], idx["Input.l2"])
    truths = [hit_row[x] for x in truth_idx]

    # input tables
    tables_idx = (idx["Input.input1"], idx["Input.input2"])
    tables = [hit_row[x] for x in tables_idx]

    # hypotheses
    hyp_idx = (idx["Input.h1"], idx["Input.h2"])
    hyp = [hit_row[x] for x in hyp_idx]

    # answers given
    res_idx = idx["Answer.taskAnswers"]
    results = process_results_2(hit_row[res_idx])

    # table ID
    tableid_idx = idx["Input.tableid"]
    tableid = hit_row[tableid_idx]

    samples = []
    for i in results:

        result = results[i]
        hitID = id + "_" + str(i)

        sample = Sample(hitID, tableid, 
                        tables[i - 1], hyp[i - 1],
                        truths[i - 1], aids[i - 1], 
                        annotator, result)
        sample.printOne()  # TEST
        samples.append(sample)

    return samples


if __name__ == "__main__":

    with open(datafile_1) as f1:
        data1 = list(csv.reader(f1))

    with open(datafile_2) as f2:
        data2 = list(csv.reader(f2))

    titles1 = data1[0]
    titles2 = data2[0]

    indexes1 = indexing(titles1, d1)
    indexes2 = indexing(titles2, d2)

    samples1 = []
    for row in data1[1:]:
        samples1 += mkSamples1(indexes1, row)

    samples2 = []
    for row in data2[1:]:
        samples2 += mkSamples2(indexes2, row)

    samples = samples1 + samples2

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

        anns[sample.annotatorID].score_majority(sample.label, sample.noneLabel,
                                                sample.majorityLabel, 
                                                sample.majorityNone)

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
