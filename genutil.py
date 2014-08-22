"""
Generator utilities for parsing the csv files.

"""
# coding: utf-8


def csv_col(header, csvpath):
    lines = (line.strip() for line in open(csvpath))
    records = (line.split(',') for line in lines)
    headers = records.next()
    idx = headers.index(header)
    vals = (line[idx] for line in records)

def cast(vals, cast, fill=0):
    for val in vals:
        if val:
            yield cast(val)
        else:
            yield fill


def live_encoder(seq):

    def counter():
        count = 0
        while True:
            yield count
            count += 1

    idgen = counter()
    valmap = {}
    for val in seq:
        if not val:
            yield -1

        if val in valmap:
            yield valmap[val]
        else:
            next_id = next(idgen)
            valmap[val] = next_id
            yield next_id
