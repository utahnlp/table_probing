"""Disagreement between batches- i.e: which individuals marked which rows, presented as an UI"""
import csv
import sys
import json
import os
from os import listdir
from os.path import isfile, join


def mkRow(key, values):

    row = '<tr> <th> {key} </th> <td>'.format(key=key, nums=nums)

    for value in values:
        row += value + "<br/>"
    row += "</td> </tr>"

    return row 


def mkCheckboxRow(key, values, workers):

    begin = '<tr> <td> {workers} </td> \
                    <th> {key} </th> <td>'
    end = '</td> </tr>'

    begin = begin.format(key=key,
                         workers=workers)

    row = ''
    for value in values:
        row += value + '<br/>'

    return begin + row + end


def has_disagreement(labelList):

    init = labelList[0]
    for l in labelList[1:]:
        if l != init:
            return True 

    return False


def all_is_zero(labelList):

    for l in labelList:
        if l != '0':
            return False
    return True


def json_to_table(table_dir, files, table_id, labels):

    begin = '<table border="1px solid black"> \
                <tr class="table-heading"> <th style="border: 0;"> \
                {title} </th> </tr>'
    end = '</table>'

    dict_table = json.loads(fetch_table(table_dir, files, table_id))
    table_keys = list(dict_table.keys())
    table_keys.append('none')
    dict_table['none'] = []


    html = begin.format(title=dict_table["title"][0])
    for index, k in enumerate(table_keys):
        index -= 1
        if k == 'title':
            pass
        else:
            labelSet = [label[index] for label in labels]

            if not all_is_zero(labelSet):
                annSet = [('A' + str(i)) for i in range(len(labelSet)) if labelSet[i] != '0']
                print(annSet)
                html += mkCheckboxRow(k, dict_table[k], str(annSet))

    return html + end


def fetch_table(table_dir, files, table_id):

    if table_id + ".json" in files:
        table_file = join(table_dir, table_id + ".json")

        with open(table_file) as f:
            table = f.read()
            return table

    else:
        return 0


def mkDiv(hypothesis, truth_value, table):

    main = "<div> \
              <div class='container'> \
                <div class='row'> \
                  <div class='hypothesis'> \
                    <div class='hypo-card'> \
                        {hypothesis} ( {truth_value} ) \
                    </div> \
                  </div> \
                  <div class='input-table'>{table}</div> \
                </div> \
              </div> \
            </div>"

    return main.format(hypothesis=hypothesis, 
                       truth_value=truth_value,
                       table=table)


def to_html(hypothesis, truth_value, table_1, table_2):

    html = ""
    container = "<div> \
              <div class='container'> \
                <div class='row'> \
                  <div class='hypothesis'> \
                    <div class='hypo-card'> \
                        {hypothesis} ( {truth_value} ) \
                    </div> \
                  </div> \
                  {table_pair} \
                </div> \
              </div> \
            </div>"

    pair = "<div class='pair'> {value} </div>"

    table_pair = pair.format(value=table_1) + \
                 pair.format(value=table_2)
    table_display = container.format(hypothesis=hypothesis, 
                                     truth_value=truth_value,
                                     table_pair=table_pair)
    return table_display


def main():

    csvfile1 = sys.argv[1]
    csvfile2 = sys.argv[2]
    template = "src/disagreement.html"
    htmlfile = sys.argv[3]

    with open(csvfile1) as f1:
        annotations1 = list(csv.reader(f1))

    with open(csvfile2) as f2:
        annotations2 = list(csv.reader(f2))
    
    table_dir = "./data/tables/json"
    onlyfiles = [f for f in listdir(table_dir) 
                 if isfile(join(table_dir, f))]

    data = {}
    for row in annotations1[1:]:
        table_id = row[0]
        hypothesis = row[1]
        labels = eval(row[5])
        truth_val = row[3]

        key = table_id + " " + hypothesis

        if has_disagreement(labels):
            table = json_to_table(table_dir, onlyfiles, table_id, labels)
            data[key] = {'hypothesis': hypothesis,
                     'truth_val': truth_val,
                     'table_1': table}       
    
    for row in annotations2[1:]:
        table_id = row[0]
        hypothesis = row[1]
        labels = eval(row[5])
        truth_val = row[3]

        key = table_id + " " + hypothesis

        table = json_to_table(table_dir, onlyfiles, table_id, labels)
        
        try:
            data[key]["table_2"] = table      
        except KeyError:
            pass


    content = ""
    for key in data:
        row = data[key]
        content += to_html(row['hypothesis'], row['truth_val'],
                           row['table_1'], row['table_2'])

    with open(htmlfile, 'w') as html_input:

        with open(template) as tf:
            template = tf.read()

        s = template.replace("{{MAIN}}", content)
        html_input.write(s)


if __name__ == "__main__":
    main()