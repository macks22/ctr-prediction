import os
import sys


MB = 1024*1024
MB100 = 100*MB


def iterchunk(fpath, block_size=MB100):
    with open(fpath, 'r') as f:
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
        usage = '{} <csvfile> [<outdir>]'.format(PROG)
        print usage
        sys.exit(1)

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
        for chunk in iterchunk(source, block_size):
            prefix = prefixgen.next()
            path = os.path.join(outdir, '{}-split.csv'.format(prefix))
            with open(path, 'w') as dest:
                dest.write(headers)
                dest.writelines(chunk)

    sys.exit(0)
