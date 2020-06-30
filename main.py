import sys

from json import dumps
from xparse import XParse


OUTPUT_PATH = './output.json'


def get_parameters():
    """
    Accepts input file name as command line argument.
    """
    if len(sys.argv) < 1:
        print('\nMissing required command line argument <relative_file_path>.\n')
        sys.exit(1)

    cla_input_file = sys.argv[1]

    return cla_input_file


def read_html(filename):
    with open(filename, 'r') as input_file:
        return input_file.read()


def write_json(filename, content):
    with open(filename, 'w') as output_file:
        return output_file.write(dumps(content, indent=4))

if __name__ == '__main__':
    input_file = get_parameters()

    xparse = XParse(read_html(input_file))
    lead = xparse.extract_lead()

    write_json(OUTPUT_PATH, lead)
