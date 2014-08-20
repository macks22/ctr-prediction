import os
import sys
import cPickle as pickle

import pandas as pd

import clean
import config


if __name__ == "__main__":
    # sanity check CL args
    if len(sys.argv) < 2:
        prog = os.path.basename(__file__)
        usage = '{} <pickled-model>'.format(prog)
        print usage
        sys.exit(1)

    model_path = os.path.abspath(sys.argv[1])
    with open(model_path) as f:
        model = pickle.load(f)

    reader = pd.read_csv(config.TEST_DATA_FILE, chunksize=100000)
    with open('predictions.csv', 'w') as outfile:
        outfile.write(','.join(clean.all_cols) + '\n')
        for chunk in reader:
            clean.fill(chunk)  # fill in missing values and scale
            ids = chunk['Id'].values
            data = chunk[clean.all_cols]
            predictions = model.predict(data)
            for ID, prediction in zip(ids, predictions):
                outfile.write('{},{}\n'.format(ID, prediction))

