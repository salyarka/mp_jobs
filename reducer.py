import sys


for line in sys.stdin:
    num, word = line.strip().split('\t', 1)
    print("%s\t%s" % (word, num))
