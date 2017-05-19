from convert_to_conll import read_file
from sys import argv
from os import makedirs


feature_types = ['bio', 'case', 'ner', 'pos', 'source.txt', 'target.txt']


def _get_filtered_line_ids(features):
    filtered_line_indicies = []
    for i in range(len(features['pos'])):
        ner_tags = features['ner'][i].split(' ')
        pos_tags = features['pos'][i].split(' ')
        ans_tags = features['bio'][i].split(' ')
        for j in range(len(ans_tags)):
            if (ner_tags[j] != 'O' or pos_tags[j] == 'CD') and ans_tags[j] != 'O':
                filtered_line_indicies.append(i)
                break
    return filtered_line_indicies


def main(features, output_info):
    line_nums = _get_filtered_line_ids(features)
    for key, items in features.items():
        output_filepath = output_info[key]
        with open(output_filepath, 'w') as f:
            for line_num in line_nums:
                print(items[line_num], file=f)


def get_features(dataset):
    basepath = 'redistribute/QG/'

    if dataset == 'dev':
        prefix = 'dev/dev.txt.shuffle.dev.'
    elif dataset == 'train':
        prefix = 'train/train.txt.'

    features = {}
    for feature_type in feature_types:
        filename = basepath + prefix + feature_type
        features[feature_type] = read_file(filename)
    return features


def get_output_info(dataset):
    dir_path = 'data/filtered/' + dataset
    makedirs(dir_path, exist_ok=True)
    output_info = {}
    for feature_type in feature_types:
        filename = dir_path + '/' + feature_type + '.txt'
        output_info[feature_type] = filename
    return output_info


if __name__ == '__main__':
    dataset = argv[1]
    features = get_features(dataset)
    output_info = get_output_info(dataset)
    main(features, output_info)
