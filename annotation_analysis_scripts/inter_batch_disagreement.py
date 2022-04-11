"""Disagreement between batches- i.e: between majority scores from multiple CSV files for the same table-hypothesis pair"""
import csv
import sys


def disagreement(a, b):

    if len(a) != len(b):
        print("ERROR")
        return

    l = len(a)
    xor = ""

    for i in range(l):
        a_ = a[i]
        b_ = b[i]

        if a_ == '0' and b_ == '0':
            xor += '0'
        elif a_ == '1' and b_ == '1':
            xor += '0'
        elif a_ != b_:
            xor += '1'

    dis = 0.0
    for x in xor:
        if x == '1':
            dis += 1.0

    return xor, dis


def main():

    csv1 = sys.argv[1]
    csv2 = sys.argv[2]
    newfile = sys.argv[3]

    with open(csv1) as f1:
        batch1 = list(csv.reader(f1))
        
    with open(csv2) as f2:
        batch2 = list(csv.reader(f2))

    # hit id: (majority1, majority2)
    hm = {}

    for row in batch1[1:]:
        hit_id = row[0] +  "|" + row[1] + "|" + row[3]
        majority1 = str(row[6])
        hm[hit_id] = [majority1] 

    for row in batch2[1:]:
        hit_id = row[0] +  "|" + row[1]  + "|" + row[3]
        majority2 = str(row[6])
        hm[hit_id].append(majority2)

    with open(newfile, "w+") as f:
        writer = csv.writer(f)
        writer.writerow(["table_id", "hypothesis", "truth_value", "num_rows", "disagreement", "rows_disagreed"])

        for hitid in hm:
            hit_id = hitid.split("|")
            table_id = hit_id[0]
            hyp = hit_id[1]
            truth_val = hit_id[2]
            disagr, n_disagr = disagreement(hm[hitid][0], hm[hitid][1])
            writer.writerow([table_id, hyp, truth_val, 
                             len(str(hm[hitid][0])), n_disagr, disagr])

    # table_dir = "./data/tables/json"
    # onlyfiles = [f for f in listdir(table_dir) 
    #             if isfile(join(table_dir, f))]


if __name__ == "__main__":
    main()