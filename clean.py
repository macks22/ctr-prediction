import os
import sys

import pandas as pd
from sklearn import preprocessing


int_cols = ['I{}'.format(num) for num in range(1, 14)]
multivar_cols = ['C{}'.format(num) for num in range(1, 27)]
all_cols = int_cols + multivar_cols


def fill(df):
    """Fill in missing values and perform feature scaling."""

    # fill with median values for integer features
    for col in int_cols:
        df[col] = df[col].astype('float')
        df[col][df[col].isnull()] = df[col].median()
        df[col] = preprocessing.scale(df[col])

    # map all multivariate features to integers, then fill with median
    for col in multivar_cols:
        column = df[col]
        column[column.isnull()] = -1  # fill missing values with -1 pre-mapping
        distinct_vals = column.unique()
        mapper = dict(zip(distinct_vals, range(len(distinct_vals))))
        df[col] = column.map(mapper)
        df[col][column == -1] = df[col].median()
        df[col] = preprocessing.scale(df[col].astype('float'))


def labels_data(df, id_label='Label'):
    labels = df[id_label].values
    data = df[all_cols].values
    return labels, data


if __name__ == "__main__":
    df = pd.DataFrame.from_csv(sys.argv[1])
    fill(df)
