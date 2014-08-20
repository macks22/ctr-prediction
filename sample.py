import os
import sys
import csv
import time

import numpy as np
import pandas as pd

import config


def iterfile(filepath):
    with open(filepath, 'r') as f:
        for num, line in enumerate(f):
            yield (num, line)


def iter_csv(csvfile, step=1):
    fileiter = ((num, line) for num, line in enumerate(open(csvfile)))
    _, line1 = fileiter.next()
    headers = line1.strip().split(',')
    stepiter = (line for num, line in fileiter if num % step == 0)
    return headers, (line.strip().split(',') for line in stepiter)


def write_sample(infile, outfile, sample_rate):
    headers, csviter = iter_csv(infile, sample_rate)
    with open(outfile, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        for line in csviter:
            writer.writerow(line)


def parse_df(csvfile, sample_rate):
    headers, iterator = iter_csv(csvfile, sample_rate)
    sample = [line for line in iter_csv(csvfile, sample_rate)]
    return pd.DataFrame(sample, columns=headers)


if __name__ == "__main__":
    sample_rate = 1000 if len(sys.argv) < 2 else sys.argv[1]
    num_samples = config.SIZE_TRAINING_DATA / sample_rate
    csvfile = config.TRAINING_DATA_FILE if len(sys.argv) < 3 else sys.argv[2]
    outfile = 'sample.csv' if len(sys.argv) < 4 else sys.argv[3]
    sample_file = os.path.join(config.DATA_DIR, outfile)

    print '-' * 80
    print 'input file: {}'.format(csvfile)
    print 'output file: {}'.format(sample_file)
    print 'sampling at a rate of 1 for every {}'.format(sample_rate)
    print '{} records will be written to the sample file'.format(num_samples)
    print '-' * 80

    start = time.time()
    write_sample(csvfile, sample_file, sample_rate)
    elapsed = time.time() - start
    print 'time elapsed: {}'.format(elapsed)

    # df = parse_df(csvfile, sample_rate)
    # df.to_csv(sample_file)
