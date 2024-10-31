from collections import Counter

file1 = open('q4a.txt', 'r')
lines = file1.readlines()

valid = 0
for line in lines:
    words = line.rstrip().split(" ")
    if len(words) == len(set(words)):
        valid += 1

print("Part 1", valid)

# https://stackoverflow.com/questions/1151658/python-hashable-dicts
class hashabledict(dict):
  def __key(self):
    return tuple((k,self[k]) for k in sorted(self))
  def __hash__(self):
    return hash(self.__key())
  def __eq__(self, other):
    return self.__key() == other.__key()

valid = 0
for line in lines:
    print(line.rstrip())
    words = [hashabledict(Counter(x)) for x in line.rstrip().split(" ")]

    print(words)



    if len(words) == len(set(words)):
        valid += 1

print("Part 2", valid)

# 300 too high


