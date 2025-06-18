import argparse
import csv

from tabulate import tabulate

import definitions

parser = argparse.ArgumentParser(description='a .csv reader')

parser.add_argument('--where', type=str, help='filter in a "field<=>value" format')
parser.add_argument('--aggregate', type=str, help='aggregate a int column in a "field=avg/min/max" format')
parser.add_argument('--file', type=str, required=True, help='name of a file to read')
parser.add_argument('--order-by', metavar='order_by', type=str,
                    help='order by a single table in a "field=desc/asc format"')

args = parser.parse_args()
file = args.file

with open(file, 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    tabledata = None
    if args.where:
        tabledata = definitions.where(csv_reader, args.where)
    if args.aggregate:
        if tabledata:
            tabledata = definitions.aggregate(tabledata, args.aggregate)
        else:
            tabledata = definitions.aggregate(csv_reader, args.aggregate)
    if args.order_by:
        if tabledata:
            tabledata = definitions.order_by(tabledata, args.order_by)
        else:
            tabledata = definitions.order_by(csv_reader, args.order_by)
    # Если ничего не произошло, то просто считываем файл
    if not tabledata:
        tabledata = []
        for line in csv_reader:
            tabledata.append(line)

print(tabulate(tabledata, headers='keys', tablefmt='psql'))
