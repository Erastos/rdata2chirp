import csv

def getFile(filename):
    f = open(filename)
    reader = csv.reader(f)
    headers = next(reader)
    lines = []
    for line in reader:
        lines.append(line)
    return headers, lines
