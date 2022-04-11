"""See the pattern of markings of a single annotator (using the annotations file)"""
import sys
import csv
import json


def process_results(results):
    """To turn results from the format returned by mturk, to a 
       row-wise set"""

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



def mkRow(key, value):

    begin = '<tr> <td> {value} </td> \
                    <th> {key} </th>'
    end = '</tr>'

    if value == True:
        begin = begin.format(key=key,
                             value=value)
    else:
        begin = begin.format(key=key,
                             value="") 
    
    return begin + end


def answer_to_table(answer):

    begin = '<table border="1px solid black"> \
                <tr class="table-heading"> <th style="border: 0;"> \
                {title} </th> </tr>'
    end = '</table>'



    html = begin.format(title="")
    for row in answer:
        html += mkRow(row, answer[row])

    return html + end


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


def to_html(hypothesis, truth_value, table):

    html = ""
    container = "<div> \
              <div class='container'> \
                <div class='row'> \
                  <div class='hypothesis'> \
                    <div class='hypo-card'> \
                        {hypothesis} ( {truth_value} ) \
                    </div> \
                  </div> \
                  {table} \
                </div> \
              </div> \
            </div>"

   
    table_display = container.format(hypothesis=hypothesis, 
                                     truth_value=truth_value,
                                     table=table)
    return table_display

# ----------------------- MAIN ------------------------


"""usage: python src/annotator_markings.py <batch file> <annotator id>"""
batch_file = sys.argv[1]
annotator = sys.argv[2]
template = "src/disagreement.html"

data = []
with open(batch_file) as f:
    batch_rows = list(csv.reader(f))

    titles = batch_rows[0]

    ann_idx = titles.index("WorkerId")
    hyp_idx = [titles.index("Input.h1"), 
               titles.index("Input.h2"), 
               titles.index("Input.h3")]
    ans_idx = titles.index("Answer.taskAnswers")

    for row in batch_rows[1:]:

        if row[ann_idx] == annotator:

            d = {}

            d["WorkerId"] = row[ann_idx]
            d["h1"] = row[hyp_idx[0]]
            d["h2"] = row[hyp_idx[1]]
            d["h3"] = row[hyp_idx[2]]
            d["answer"] = process_results(row[ans_idx])

            data.append(d)

content = ""
for d in data:
    table1 = d["answer"][1]
    table2 = d["answer"][2]
    table3 = d["answer"][3]

    div1 = answer_to_table(table1)
    div2 = answer_to_table(table2)
    div3 = answer_to_table(table3)

    box1 = to_html(d["h1"], "", div1)
    box2 = to_html(d["h2"], "", div2)
    box3 = to_html(d["h3"], "", div3)

    content += box1 + box2 + box3

with open(template) as tf:
    template = tf.read()

    s = template.replace("{{MAIN}}", content)
        
    with open(annotator + ".html", "w+") as f:
        f.write(s)


        






