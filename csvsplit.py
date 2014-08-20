import os
import sys
import time
import logging


MB = 1024*1024
MB100 = 100*MB


def iterchunk(f, block_size=MB100):
    lines = []
    size = 0
    for line in f:
        size += len(line)
        lines.append(line)
        if size > block_size:
            yield lines
            lines = []
            size = 0

    # return final chunk
    yield lines


def iterprefix(cap):
    """Yield prefixes of the form "00X" where X is an incrementing counter."""
    size_cap = len(str(cap))
    for num in xrange(cap):
        count = str(num)
        prefix = '{}{}'.format('0' * (size_cap - len(count)), count)
        yield prefix


if __name__ == "__main__":

    # usage check
    if len(sys.argv) < 2:
        prog = os.path.basename(__file__)
        usage = '{} <csvfile> [<outdir>] [<block-size>]'.format(prog)
        print usage
        sys.exit(1)

    # set up logging
    logging.basicConfig(level=logging.INFO)

    # parse CL args
    csvfile = sys.argv[1]
    dirname = os.path.dirname(__file__) if len(sys.argv) < 3 else sys.argv[2]
    outdir = os.path.abspath(dirname)
    block_size = MB100 if len(sys.argv) < 4 else sys.argv[3]

    fsize = os.path.getsize(csvfile)
    num_files = int(round(fsize / float(block_size)))
    prefixgen = iterprefix(num_files)

    with open(csvfile, 'r') as source:
        headers = source.readline()
        logging.info('output directory: {}'.format(outdir))
        for chunk in iterchunk(source, block_size):
            prefix = prefixgen.next()
            fname = '{}-split.csv'.format(prefix)
            path = os.path.join(outdir, fname)
            logging.info('writing ~{} bytes to: {}'.format(block_size, fname))
            with open(path, 'w') as dest:
                dest.write(headers)
                dest.writelines(chunk)

    sys.exit(0)
