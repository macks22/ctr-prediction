import os
import cPickle as pickle

import config


int_cols = ['I{}'.format(num) for num in range(1, 14)]
multivar_cols = ['C{}'.format(num) for num in range(1, 27)]
all_cols = int_cols + multivar_cols


def make_mappers():
    fileiter = (line.strip().split(',')
                for line in open(config.TRAINING_DATA_FILE))
    headers = fileiter.next()

    idx = {}
    for col in multivar_cols:
        idx[col] = headers.index(col)

    colsets = {col: set() for col in all_cols}
    # num_read = 0
    for record in fileiter:
        # num_read += 1
        # if num_read % 10000 == 0:
        #     print 'records read: {}'.format(num_read)
        for col in colsets:
            colsets[col].add(record[idx[col]])

    for col, colset in colsets.items():
        mapper = dict(zip(colset, range(len(colset))))
        fname = '{}.pickle'.format(col.lower())
        fpath = os.path.join(config.MAPPER_DIR, fname)
        with open(fpath, 'w') as f:
            pickle.dump(mapper, f)


if __name__ == "__main__":
    make_mappers()
    sys.exit(0)
