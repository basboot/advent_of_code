from functools import reduce


print(sum([reduce(lambda a, b: ((a+b)*17) % 256, map(ord, h), 0) for h in open('q15a.txt').readlines()[0].split(",")]))



