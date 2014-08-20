import os
import sys

import pandas as pd


int_cols = ['I{}'.format(num) for num in range(1, 14)]
multivar_cols = ['C{}'.format(num) for num in range(1, 27)]
all_cols = int_cols + multivar_cols


def fill(df):
    # fill with median values for integer features
    for col in int_cols:
        df[col][df[col].isnull()] = df[col].median()

    # map all multivariate features to integers, then fill with median
    for col in multivar_cols:
        column = df[col]
        column[column.isnull()] = -1  # fill missing values with -1 pre-mapping
        distinct_vals = column.unique()
        mapper = dict(zip(distinct_vals, range(len(distinct_vals))))
        df[col] = column.map(mapper)
        df[col][column == -1] = df[col].median()


def labels_data(df):
    labels = df['Label'].values
    data = df[all_cols].values
    return labels, data


if __name__ == "__main__":
    df = pd.DataFrame.from_csv(sys.argv[1])
    fill(df)
