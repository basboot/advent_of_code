# Using readlines()
file1 = open('q19a.txt', 'r')
lines = file1.readlines()

import re
from ast import literal_eval

reading_work_flows = True
parts = []

workflows = {}
for line in lines:
    row = line.rstrip()

    if row == "":
        reading_work_flows = False
        continue

    if reading_work_flows:
        name, wfs = row.replace("}", "").split("{")
        workflow_sequence = []
        for wf in wfs.split(","):
            w = wf.split(":")

            if len(w) > 1:
                prop = w[0][0]
                operator = w[0][1]
                arg = int(w[0][2:])
                redirect = w[1]
                x = re.search("[><]", w[0]).start()
            else:
                prop = None
                operator = None
                arg = None
                redirect = w[0]

            workflow_part = {
                "property": prop,
                "operator": operator,
                "argument": arg,
                "redirect": redirect
            }
            workflow_sequence.append(workflow_part)
        workflows[name] = workflow_sequence
    else:
        parts.append(literal_eval(row.replace("x", "'x'").replace("m", "'m'").replace("a", "'a'").replace("s", "'s'").replace("=", ":")))


def apply_workflow_part(worflow_part, part):
    # no real workflow, just a redirection
    if worflow_part["operator"] is None:
        return worflow_part["redirect"]

    # do comparison
    if worflow_part["operator"] == ">":
        result = part[worflow_part["property"]] > worflow_part["argument"]
    else:
        result = part[worflow_part["property"]] < worflow_part["argument"]

    return worflow_part["redirect"] if result else None

def apply_workflow(worflow_name, part):
    workflow_sequence = workflows[worflow_name]

    for workflow_part in workflow_sequence:
        result = apply_workflow_part(workflow_part, part)
        if result in {"A", "R"}: # endpoint
            return result
        if result is None:
            continue # to next part of this workflow if it is not a matcg
        return apply_workflow(result, part) # or go one deeper if it is a match but no A, R


# start at in
total = 0
for part in parts:
    result = apply_workflow("in", part)

    if result == "A":
        total += sum([part[x] for x in part])
print("Total", total)

