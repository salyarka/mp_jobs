import sys

from optparse import OptionParser


sys.setdefaultencoding('utf-8')

parser = OptionParser()
parser.add_option(
    '-f', '--file', dest='filename',
    help='file with stop words', metavar='FILE'
)
options, args = parser.parse_args()

with open(options['filename']) as f:
    stop_words_set = set(word.strip() for word in f)

total = 0
stops = 0

for line in sys.stdin:
    try:
        word, num = line.split('\t', 1)
    except ValueError as e:
        continue
    if word in stop_words_set:
        print('stops\t%s' % num)
    print('total\t%s' % num)
