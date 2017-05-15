from sys import argv
from signal import signal, SIGPIPE, SIG_DFL


def read_file(filename):
    features = set(['PADDING'])
    with open(filename, 'r') as f:
        for line in f:
            for feature in line.strip().split(' '):
                features.add(feature)
    return features


if __name__ == '__main__':
    for ind, feature in enumerate(sorted(list(read_file(argv[1])))):
        print("{}\t{}".format(feature, ind+1))
