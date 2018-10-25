#!.venv/bin/python
import csv
import json

with open('result.csv', 'r') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=';')
    headers = next(csvreader)
    column = {}
    rows = {}
    for h in headers:
        column[h] = []

    for (i, row) in enumerate(csvreader):
        json_key = ''
        full_row = {}
        for (j, column) in enumerate(row):
            if (j == 0):
                json_key = column.strip()
            else:
                header = headers[j]
                full_row[header] = column.strip()

        rows[json_key] = full_row

with open('isinRisk.json', 'w') as outfile:
    json.dump(rows, outfile)

with open("isinRisk.js", 'a') as file:
    file.write("window.isinRisk = %s" % rows)
