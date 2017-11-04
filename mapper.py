import sys


for line in sys.stdin:
    try:
        word, num = line.split('\t', 1)
    except ValueError as e:
        continue
    print("%d\t%s" % (int(num), word))

