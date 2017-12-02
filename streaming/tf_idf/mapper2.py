import sys
import re

from optparse import OptionParser
from collections import Counter


usage = 'Usage: -f <filename> -a <article_id> -t <term>'
parser = OptionParser(usage=usage)
parser.add_option(
    '-f', '--file', dest='filename',
    help='file with stop words', metavar='FILE'
)
parser.add_option(
    '-a', '--article', dest='article',
    help='article id', metavar='ARTICLE'
)
parser.add_option(
    '-t', '--term', dest='term',
    help='term to find in documents', metavar='TERM'
)
options, args = parser.parse_args()
if not all([options.filename, options.article, options.term]):
    parser.print_help()
    sys.exit(1)

with open(options.filename) as f:
    stop_words_set = set(word.strip() for word in f)

for line in sys.stdin:
    try:
        article_id, text = line.strip().split('\t', 1)
    except ValueError as e:
        continue

    if article_id == options.article:
        text = re.sub('^\W+|\W+$', '', text, flags=re.UNICODE)
        words = re.split('\W*\s+\W*', text, flags=re.UNICODE)
        words = map(lambda x: x.lower(), words)
        words = filter(lambda x: x not in stop_words_set, words)
        counter = Counter(words)
        result = counter[options.term] / float(sum(counter.values()))
        print(result)
