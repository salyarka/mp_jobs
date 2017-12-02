import math
import sys

from optparse import OptionParser


def idf_tf(documents_total, documents_with_term, tf):
    return math.log(documents_total/float(documents_with_term)) * tf

if __name__ == '__main__':
    usage = 'Usage: -d <number_of_documents_with_term> -t <tf>'
    parser = OptionParser(usage=usage)
    parser.add_option(
        '-d', '--dt', dest='dt',
        help='number of documents with term',
        metavar='DT'
    )
    parser.add_option(
        '-f', '--frequency', dest='frequency',
        help='term frequency',
        metavar='FREQUENCY'
    )
    parser.add_option(
        '-t', '--total', dest='total',
        help='number of documents',
        metavar='TOTAL'
    )
    options, args = parser.parse_args()
    if not all([options.dt, options.frequency, options.total]):
        parser.print_help()
        sys.exit(1)
    try:
        d_total = int(options.total)
        d_term = int(options.dt)
        ft = float(options.frequency)
    except ValueError:
        print(
            'number of documents and documents with term must be integer, '
            'and frequency must be integer or float'
        )
        sys.exit(1)
    print(idf_tf(d_total, d_term, ft))
