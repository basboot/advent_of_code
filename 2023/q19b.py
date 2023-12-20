# Using readlines()
from copy import deepcopy

file1 = open('q19a.txt', 'r')
lines = file1.readlines()

from ast import literal_eval
import re
from functools import reduce

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


# returns part with redirect (p, r), part not redirected
# both can be None
def apply_workflow_part(worflow_part, part):
    # no real workflow, just a redirection
    if worflow_part["operator"] is None:
        return (part, worflow_part["redirect"]), None

    # do comparison
    workflow_range_start, workflow_range_end = part[worflow_part["property"]]

    if worflow_part["operator"] == ">":
        if workflow_range_start > worflow_part["argument"]: # full range true
            return part, worflow_part["redirect"], None
        else:
            if workflow_range_end <= worflow_part["argument"]: # full range false
                return None, part
            else:
                # split
                range_false = [workflow_range_start, worflow_part["argument"]]
                range_true = [worflow_part["argument"] + 1, workflow_range_end]
                part_false = deepcopy(part)
                part_true = deepcopy(part)
                part_false[worflow_part["property"]] = range_false
                part_true[worflow_part["property"]] = range_true
                return (part_true, worflow_part["redirect"]), part_false
    else:
        if workflow_range_end < worflow_part["argument"]: # full range true
            return (part, worflow_part["redirect"]), None
        else:
            if workflow_range_start >= worflow_part["argument"]: # full range false
                return None, part
            else: # < arg
                # split
                range_true = [workflow_range_start, worflow_part["argument"] - 1]
                range_false = [worflow_part["argument"] , workflow_range_end]
                part_true = deepcopy(part)
                part_false = deepcopy(part)
                part_false[worflow_part["property"]] = range_false
                part_true[worflow_part["property"]] = range_true
                return (part_true, worflow_part["redirect"]), part_false


def apply_workflow(name, part):

    part_to_process = part.copy()
    results = []

    for workflow_sequence in workflows[name]:

        # processed = redirect, to_process = next step in sequence (overwrites current part)
        part_processed, part_to_process = apply_workflow_part(workflow_sequence, part_to_process)

        # store A, R in results
        if part_processed is not None and part_processed[1] in ["A", "R"]:
            results.append(part_processed)
        else: # apply redirection to next workflow
            results += apply_workflow(part_processed[1], part_processed[0])

        # if there is no part left for the next sequence in current workflow break
        if part_to_process is None:
            break

    return results


# apply workflow to item with full ranges -> results in many items with broken ranges for A and R
results = apply_workflow("in", {
    "x": [1, 4000],
    "m": [1, 4000],
    "a": [1, 4000],
    "s": [1, 4000]
})


def range_to_size(r):
    return r[1] - r[0] + 1

total = 0
i = 0

active_parts = []

for result in results:
    i += 1
    part, state = result
    if state == "A":
        active_parts.append(part)
        options = reduce(lambda a, b: a * b, [range_to_size(part[x]) for x in part], 1)
        total += options

print("Total", total)

# real 1865419042316972 is too high


