# Using readlines()
import math

from sympy import symbols

file1 = open('q21a.txt', 'r')
lines = file1.readlines()

import sympy

x = symbols('x')

class MonkeyProcessor:
    def __init__(self):
        self.queue = []
        self.observers = []


    def register(self, monkey):
        self.observers.append(monkey)

    def add_result(self, monkey):
        self.queue.append((monkey.name, monkey.value))

    def run(self):
        job = self.queue.pop(0)

        # print(job)

        for monkey in self.observers:
            monkey.update(job)
        return len(self.queue) > 0

class Monkey:
    def __init__(self, name, job, mp: MonkeyProcessor):
        self.name = name
        self.mp = mp

        if self.name == "humn":
            # const monkey
            self.value = job
            self.operation = "="
            self.mp.add_result(self)  # add result

        else:
            job_parts = job.split(" ")

            if len(job_parts) == 1:
                # const monkey
                self.value = int(job_parts[0])
                self.operation = "="
                self.mp.add_result(self) # add result

            else:
                self.ready = False
                self.params = {
                    "names": [job_parts[0], job_parts[2]],
                    "values": [None, None],
                    "operation": job_parts[1]
                }
                self.mp.register(self)


    def update(self, job):
        name, value = job
        # print(f"[{self.name}] message: ", name, value, self.params["names"])
        if not self.ready and name in self.params["names"]:
            # print(f"[{self.name}] process")
            # print(name, value)
            count_ready = 0
            for i in range(2):
                if self.params["values"][i] is not None:
                    count_ready += 1
                else:
                    if self.params["names"][i] == name:
                        self.params["values"][i] = value
                        count_ready += 1
            if count_ready == 2:

                if self.name == "root":
                    print(self.params["values"][0], " == ",  self.params["values"][1])
                    self.value = self.params["values"][0] == self.params["values"][1]
                else:
                    # do operation
                    match self.params["operation"]:
                        case "+":
                            self.value = self.params["values"][0] + self.params["values"][1]
                        case "*":
                            self.value = self.params["values"][0] * self.params["values"][1]
                        case "-":
                            self.value = self.params["values"][0] - self.params["values"][1]
                        case "/":
                            self.value = self.params["values"][0] / self.params["values"][1]
                        case _:
                            assert True, "Unknown operation"

                self.mp.add_result(self)

                self.ready = True

                # print("Ready: ", self.name, self.value)
                if self.name == "root":
                    print("ROOT: ", self.value)

monkey_processor = MonkeyProcessor()

for line in lines:
    name, job = line.rstrip().split(": ")
    # print("input: ", name, job)

    if name == "humn":
        monkey = Monkey(name, x, monkey_processor)
    else:
        monkey = Monkey(name, job, monkey_processor)
#
# print(monkey_processor.queue)
# print(monkey_processor.observers)

while monkey_processor.run():
    pass


# 156882979210595.0 - 5832*x/175  ==  37175119093215.0

print ("x = ", round(((37175119093215 - 156882979210595) * 175) / -5832))


