from os import listdir
from os.path import isdir, isfile, join

# get all files in the batch directory
batch_dir = "./release_batches"
batchfiles = [join(batch_dir, f) for f in listdir(batch_dir) 
             if isfile(join(batch_dir, f))]

for batchfile in batchfiles:
    with open(batchfile) as f:
        rows = f.readlines()
        title = rows[0]

        subbatch1 = [title] + rows[1:int(len(rows)/2) + 1]
        subbatch2 = [title] + rows[int(len(rows)/2) + 1:]

        root = batchfile[:-4] 
        subbatch1_f = root + "_1.csv"
        subbatch2_f = root + "_2.csv"

        with open(subbatch1_f, "w+") as sub1:
            sub1.writelines(subbatch1)
        with open(subbatch2_f, "w+") as sub2:
            sub2.writelines(subbatch2)
        
        print(batchfile[:-4], len(rows), len(subbatch1), len(subbatch2))

