import json

# Open and read the JSON file
with open('q12a.json', 'r') as file:
    data = json.load(file)


def sum_numbers(data):
    total = 0
    if isinstance(data, list):
        for item in data:
            total += sum_numbers(item)
    if isinstance(data, dict):
        sub_total = 0
        for key, value in data.items():
            if value == "red": # part 2, ignore dict if one of its values is red
                sub_total = 0
                break
            sub_total += sum_numbers(value)
        total += sub_total
    if isinstance(data, int):
        return data

    return total

print("Total", sum_numbers(data))