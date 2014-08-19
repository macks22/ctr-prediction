import os


SIZE_TRAINING_DATA = 45840617
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(PROJECT_DIR, 'data')
TRAINING_DATA_FILE = os.path.join(DATA_DIR, 'train.csv')
TEST_DATA_FILE = os.path.join(DATA_DIR, 'test.csv')
ZIPTRAIN = os.path.join(DATA_DIR, 'train.zip')
ZIPTEST = os.path.join(DATA_DIR, 'test.zip')
