import sys
import cPickle as pickle
import zipfile

import pandas as pd
import numpy as np
import sklearn.linear_model as sklin

import clean


def iterdata(archive):
    """Incrementally yield pre-processed data files from a zip archive. This
    assumes each file in the archive can be read into memory.

    :param str archive: The archive to read files from.
    :return: (label, data) vectors
    :rtype:  tuple of vectors

    """
    with zipfile.ZipFile(archive_path) as archive:
        for zipinfo in archive.filelist[1:]:
            with archive.open(zipinfo) as f:
                df = pd.DataFrame.from_csv(f)
                clean.fill(df)
                yield df


if __name__ == "__main__":
    zippath = sys.argv[1]
    datagen = iterdata(zippath)
    lreg = sklin.SGDRegressor(penalty='l1', loss='squared_loss', verbose=1)
    classes = [0, 1]

    with zipfile.ZipFile(zippath) as archive:
        num_files = len(archive.filelist)
        num_train = np.ceil((2/3) * num_files)
        num_test = num_files - num_train

    MB = 1024*1024
    # this estimation is from the sklearn docs
    lreg.n_iter = np.ceil(10**6 / (num_train * 100*MB))
    if lreg.n_iter < 5:
        lreg.n_iter = 5

    # train the model
    print 'training logistic regression on {} files'.format(num_train)
    print 'minimizing loss function: {}'.format(lreg.loss.replace('_', ' '))
    for num in range(num_train):
        print 'file num: {}'.format(num)
        labels, data = clean.labels_data(datagen.next())
        lreg.partial_fit(data, labels)
        # lreg.partial_fit(data, labels, classes)

    # combine all test data
    testdf = datagen.next()
    for num in range(num_test-1):
        print 'reading in test data file: {}'.format(num)
        testdf.append(datagen.next())

    testlabels, testdata = clean.labels_data(testdf)
    print lreg.score(testdata, testlabels)
    with open('logreg-ls.pickle', 'w') as f:
        pickle.dump(lreg, f)
