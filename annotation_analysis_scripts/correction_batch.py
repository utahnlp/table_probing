"""Make list of hits and annotators who have worked on the correction batch"""
import sys
import csv

   
def annotator_in_list(annList, ls):
    """Check if any of the annotators in annList are
       in ls"""
    in_list = False

    for ann in annList:
        for i in ls:
            if ann == i:
                in_list = True
                break

    return in_list


def mkRepeat(titleRow, row):
    print("Making the repeat row", row[0])
    indexes = []
    titlist = []
    for index, title in enumerate(titleRow):
        if "Input." in title:
            indexes.append(index)
            titlist.append(title[6:])

    values = [row[idx] for idx in indexes]
    return values


def if_bad_hit(tableid, hyp, repeat_rows):
    """Check if this particular tableid-hypothesis pair
    is in list of tableid-hyp pairs to be repeated"""
    if (tableid, hyp) in repeat_rows:
        return True
    else:
        return False


"""usage: python src/correction_batch.py <file of annotations> <annotator id file>"""
annotations_file = sys.argv[1]
annotators_file = sys.argv[2]
hits_file = sys.argv[3]
template = "src/disagreement.html"

# read in list of annotators whose hits we want to correct
with open(annotators_file) as f:
    anns = f.readlines()
    anns = [x.rstrip(" \n").rstrip("\n ") for x in anns]

# GET LIST OF ANNOTATORS WITH BAD RESULTS
print("Annotators with bad results:")
for ann in anns:
    print(ann)
print("=============================================")


block_anns = {}
repeat_rows = []

# MAKE LIST OF ANNOTATORS TO BE BLOCKED
with open(annotations_file) as f:
    rows = list(csv.reader(f))

    # titles: Table ID, Hypothesis, Generator ID, Truth Label,
    #         Worker IDs, Labels, Majority Label 
    titles =  rows[0]
    anns_idx = titles.index("Worker IDs")

    for row in rows:
        
        # if annotator_in_list(anns, eval(row[anns_idx])):
        annString = row[anns_idx].lstrip("[").rstrip("]").split(',')
        annIds = [x.lstrip("' ").rstrip("' ") for x in annString]

        # if the red/yellow annotator marked this HIT
        if annotator_in_list(anns, annIds):

            # append tableID and hypothesis of hit to be repeated
            repeat_rows.append((row[0], row[1]))

            for annId in annIds:
                # leave out annotators who have been marked already
                if annId not in anns:

                    if annId not in block_anns:
                        block_anns[annId] = 1
                    else:
                        block_anns[annId] += 1

                    # TEST PRINT print("Intermediate: {annid}  :: {num}".format(annid=annId, num=block_anns[annId]))

for a in block_anns:
    print(a, block_anns[a])

# MAKE CSV OF HITS TO BE REPEATED
with open(hits_file) as hitf:
    hitlist = list(csv.reader(hitf))

hitlist_titles = hitlist[0]
hits_to_repeat = [["set1", "set2", "set3", "tableid", 
                   "aid1", "aid2", "aid3",
                   "input1", "input2", "input3",
                   "h1", "h2", "h3", "l1", "l2", "l3"]]

tableid_idx_hitlist = hitlist_titles.index("Input.tableid")
hyp_idx_hitlist = [hitlist_titles.index("Input.h1"),
                   hitlist_titles.index("Input.h2"),
                   hitlist_titles.index("Input.h3")]
hitid_idx_hitlist = hitlist_titles.index("HITId")

# list of HITS (by HIT id) that have already been
# included in the repeat batch
already_in_rbatch = []


for hit in hitlist[1:]:
    hitlist_hitid = hit[hitid_idx_hitlist]
    hitlist_tableid = hit[tableid_idx_hitlist]
    hitlist_hyp = [hit[i] for i in hyp_idx_hitlist]

    # if HIT in list of table-hyp pairs to be repeated
    for hyp in hitlist_hyp:
        if if_bad_hit(hitlist_tableid, hyp, repeat_rows):
            if hitlist_hitid not in already_in_rbatch:
                hits_to_repeat.append(mkRepeat(hitlist_titles, hit))
                already_in_rbatch.append(hitlist_hitid)

# write rows to csv
with open("repeat_batch.csv", "w+") as f:
    fwriter = csv.writer(f, delimiter=',')
    for row in hits_to_repeat:
        fwriter.writerow(row)        
    