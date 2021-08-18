"""Take all CSV sheets within a folder and integrate them"""
import sys
import csv
from os import listdir
from os.path import isfile, join

def main():

    csv_folder = sys.argv[1]
    newfile = sys.argv[2]

    all_files = [join(csv_folder, f) 
                 for f in listdir(csv_folder) 
                 if isfile(join(csv_folder, f))]

    all_readers = []
    for filename in all_files:
        with open(filename) as f:
            reader = list(csv.reader(f))
            all_readers.append(reader) 
    
    # check if the title rows of all files are same
    # take reference as title row of first file
    ref = all_readers[0][0]
    equals = [reader[0] == ref for reader in all_readers]
    all_titles_equal = True
    for value in equals:
        all_titles_equal = all_titles_equal and value

    # if all files have same title row, integrate 
    if all_titles_equal:
        
        combined_reader = []
        combined_reader.append(ref)

        for reader in all_readers:
            for row in reader[1:]:
                combined_reader.append(row)

    else:
        print("CSV files do not match")

    # write the integrated files to a new files
    with open(newfile, "w+") as f:
        writer = csv.writer(f)

        for row in combined_reader:
            writer.writerow(row)


if __name__ == "__main__":
    main()





