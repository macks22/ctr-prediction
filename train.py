import sys
import cPickle as pickle
import zipfile

import sklearn.linear_model as sklin
import pandas as pd

import clean


def iterdata(archive_path):
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
    lreg = sklin.SGDClassifier(penalty='l1', loss='log')
    classes = [0, 1]

    num_files = 111  # should get this for real later
    num_train = 80
    num_test = num_files - num_train

    # train the model
    print 'training logistic regression on {} files'.format(num_train)
    for num in range(num_train):
        print 'file num: {}'.format(num)
        labels, data = clean.labels_data(datagen.next())
        lreg.partial_fit(data, labels, classes)

    # combine all test data
    testdf = datagen.next()
    for _ in range(num_test-1):
        testdf.append(datagen.next())

    testlabels, testdata = clean.labels_data(testdf)
    print lreg.score(testdata, testlabels)
    with open('logreg.pickle', 'w') as f:
        pickle.dump(lreg, f)
