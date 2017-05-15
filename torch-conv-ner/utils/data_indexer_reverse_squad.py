import data_indexer as di


def windowed_conll_in_id(docs, window, label_int_map, voc_int_map, case, ner, pos):
    windowed_docs = []
    line_pointer = 0
    for doc in docs:
        line_pointer += 2
        windowed_doc = []
        for sent in doc:
            line_pointer += 1
            windowed_sent = []
            for ind, parts in enumerate(sent):
                label_id = label_int_map[parts[-1]]
                row = [label_id]
                word_ids = []
                case_ids = []
                ner_ids = []
                pos_ids = []
                for win_ind in range(ind - window, ind + window + 1):

                    if win_ind < 0 or win_ind >= len(sent):
                        case_id = case['PADDING']
                        ner_id = ner['PADDING']
                        pos_id = pos['PADDING']
                        word_id = voc_int_map['PADDING']
                        word_ids.append(word_id)
                        case_ids.append(case_id)
                        ner_ids.append(ner_id)
                        pos_ids.append(pos_id)
                    else:
                        word = di.normalize(sent[win_ind][0])
                        pos_id = pos[sent[win_ind][1]]
                        case_id = case[sent[win_ind][2]]
                        ner_id = ner[sent[win_ind][3]]
                        word_id = voc_int_map.get(word, voc_int_map['UNKNOWN'])
                        word_ids.append(word_id)
                        case_ids.append(case_id)
                        ner_ids.append(ner_id)
                        pos_ids.append(pos_id)
                row += word_ids
                row += case_ids
                row += ner_ids
                row += pos_ids
                windowed_sent.append(row)

                line_pointer += 1
            windowed_doc.append(windowed_sent)
        windowed_docs.append(windowed_doc)
    return windowed_docs


def load_features_map(filename):
    features_map = {}
    with open(filename, 'r') as f:
        for line in f:
            name, ind = line.strip().split('\t')
            ind = int(ind)
            features_map[name] = ind
    return features_map


def run_win():
    w2v_file = 'data/embeddings/senna.w2v'
    data_dir = 'data/reverse-squad/'
    filenames = ['dev.iobes', 'train.iobes']

    senna_vecs = di.get_senna_vecs(w2v_file)
    normalized_conll_tokens = di.get_normalized_conll_tokens(data_dir, filenames)
    # senna_vecs = get_intersect_vecs(senna_vecs, normalized_conll_tokens)

    vocabulary = senna_vecs.keys()
    voc_int_map = di.get_vocabulary_int_map(vocabulary)
    senna_int_map = di.get_features_int_map(senna_vecs, voc_int_map)
    label_int_map = di.get_label_int_map(data_dir + filenames[-1])
    di.save_index_by_table(senna_int_map, 'data/embeddings/senna.index')
    di.save_index_by_table(voc_int_map, data_dir + '/vocab-map.index')
    di.save_index_by_table(label_int_map, data_dir + '/label-map.index')

    pos_features = load_features_map('../data/pos_features')
    ner_features = load_features_map('../data/ner_features')
    case_features = load_features_map('../data/case_features')
    print(case_features)

    for filename in filenames:
        print('Processing {0}'.format(filename))
        docs = di.docs_with_sents(data_dir + filename)
        windowed_docs = windowed_conll_in_id(docs, 2, label_int_map, voc_int_map,
            case_features, ner_features, pos_features)
        to_torch, pos = di.convert_to_torch_format(windowed_docs)

        di.save_index_by_array(to_torch, data_dir + '/{0}.win.index'.format(filename))
        di.save_index_by_table(pos, data_dir + '/{0}.index-line-pos'.format(filename))

        print(len(windowed_docs), len(to_torch))

if __name__ == '__main__':
    run_win()
