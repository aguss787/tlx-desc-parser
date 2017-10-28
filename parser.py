import argparse
from utils.segment import parse

parser = argparse.ArgumentParser(description='Parse statement file to html')
parser.add_argument('filename', type=argparse.FileType('r'),
                                help='statement file')
args = parser.parse_args()
with args.filename as statement:
    with open('statement.html', 'w') as outFile:
        outFile.write(parse(statement))
