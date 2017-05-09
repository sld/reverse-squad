from sys import argv


def load_vocab(filename):
    with open(filename, 'r') as f:
        return set([word_.strip() for word_ in f])


def filter_dataset(filename, vocab):
    with open(filename, 'r') as f:
        for line in f :
            sentence = []
            for word in line.strip().split(' '):
                if word not in vocab:
                    sentence.append('UNK')
                else:
                    sentence.append(word)
            print(' '.join(sentence))


if __name__ == '__main__':
    vocab_filename = argv[1]
    dataset_filename = argv[2]
    vocab = load_vocab(vocab_filename)
    filter_dataset(dataset_filename, vocab)
