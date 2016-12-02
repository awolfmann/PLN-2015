"""
CSV creation script.

Usage:
    create_csv.py <csv_filename>
    create_csv.py -h | --help | --version

Options:
  -h --help             Show this screen
  --version             Version number
"""
import logging
import os
import codecs
from docopt import docopt


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger('createdb')
    opts = docopt(__doc__, version=0.1)
    csv_filename = opts['<csv_filename>']

    csv_file = codecs.open(csv_filename, 'w', encoding='utf-8')

    csv_file.write('document_id,document_text\n')

    # Create the documents.
    for i in [7, 30, 102]:
        filename = 'RHCD_{}_2014.txt'.format(i)
        file_path = os.path.join('resoluciones-unc','data', 'examples', filename)
        file_text = codecs.open(file_path, encoding='utf-8').read()

        csv_file.write(u'{},"{}"\n'.format(filename, file_text))

    csv_file.close()

    logger.info('Created CSV %s', csv_filename)
