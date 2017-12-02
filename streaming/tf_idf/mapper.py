import sys
import re

from optparse import OptionParser

usage = 'Usage: -t <term>'
parser = OptionParser(usage=usage)
parser.add_option(
    '-t', '--term', dest='term',
    help='term to find in documents', metavar='TERM'
)
options, args = parser.parse_args()
if options.term is None:
    parser.print_help()
    sys.exit(1)

for line in sys.stdin:
    try:
        article_id, text = line.strip().split('\t', 1)
    except ValueError as e:
        continue

    text = re.sub('^\W+|\W+$', '', text, flags=re.UNICODE)
    words = re.split('\W*\s+\W*', text, flags=re.UNICODE)
    words = map(lambda x: x.lower(), words)

    if options.term in words:
        print('term\t1')
    print('total\t1')
