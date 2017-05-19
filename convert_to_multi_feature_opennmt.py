from preserve_only_numeric_and_ner import feature_types
from convert_to_conll import read_file
from sys import argv


def main(dataset):
    basepath = 'data/filtered/{}/'.format(dataset)
    features = {}
    for feature_type in feature_types:
        filename = basepath + feature_type + '.txt'
        features[feature_type] = read_file(filename)

    featured_sents = []
    for i in range(len(features['pos'])):
        ner_tags = features['ner'][i].split(' ')
        pos_tags = features['pos'][i].split(' ')
        ans_tags = features['bio'][i].split(' ')
        case_tags = features['case'][i].split(' ')
        source_tokens = features['source.txt'][i].split(' ')
        featured_source_tokens = []
        for j in range(len(source_tokens)):
            featured_source_token = "{}￨{}￨{}￨{}￨{}".format(
                source_tokens[j],
                ans_tags[j],
                case_tags[j],
                pos_tags[j],
                ner_tags[j]
            )
            featured_source_tokens.append(featured_source_token)
        featured_sents.append(" ".join(featured_source_tokens))

    with open(basepath + 'featured_source.txt', 'w') as f:
        for sent in featured_sents:
            print(sent, file=f)


if __name__ == '__main__':
    main(argv[1])



