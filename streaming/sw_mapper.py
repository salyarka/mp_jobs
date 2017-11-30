import sys
import re

from optparse import OptionParser


usage = 'Usage: -f <filename>'
parser = OptionParser(usage=usage)
parser.add_option(
    '-f', '--file', dest='filename',
    help='file with stop words', metavar='FILE'
)
options, args = parser.parse_args()
if options.filename is None:
    parser.print_help()
    sys.exit(1)

with open(options['filename']) as f:
    stop_words_set = set(word.strip() for word in f)

for line in sys.stdin:
    try:
        article_id, text = unicode(line.strip()).split('\t', 1)
    except ValueError as e:
        continue
    words = re.split('\W*\s+\W*', text, flags=re.UNICODE)
    for word in words:
        if word.lower() in stop_words_set:
            print >> sys.stderr, 'reporter:counter:Wiki stats,Stop words,%d' % 1
        print >> sys.stderr, 'reporter:counter:Wiki stats,Total words,%d' % 1
        print '%s\t%d' % (word.lower(), 1)
