# what computational problem is commonly associated with prime factorization ?
# the B-ANS
# integer I-ANS
# factorization I-ANS
# problem I-ANS
# is O
# the O
# computational O
# problem O
# of O
# determining O
# the O
# prime O
# factorization O
# of O
# a O
# given O
# integer O
# . O

from sys import argv
from signal import signal, SIGPIPE, SIG_DFL


def read_file(filename):
    with open(filename, 'r') as f:
        return [line.strip() for line in f]


def main_features(text_filename, answer_bio_filename, pos_filename, ner_filename, case_filename):
    sentences = read_file(text_filename)
    answers_bio = read_file(answer_bio_filename)
    ner = read_file(ner_filename)
    pos = read_file(pos_filename)
    case = read_file(case_filename)
    print('-DOCSTART- -X- -X- -X- O')
    print('')
    for i in range(len(sentences)):
        tokens = sentences[i].split(' ')
        ans_tags = answers_bio[i].split(' ')
        ner_tags = ner[i].split(' ')
        pos_tags = pos[i].split(' ')
        case_tags = case[i].split(' ')
        for j in range(len(tokens)):
            ans_tag = ans_tags[j]
            ner_tag = ner_tags[j]
            pos_tag = pos_tags[j]
            case_tag = case_tags[j]
            token = tokens[j]
            if ans_tag != 'O':
                ans_tag = "{}-ANS".format(ans_tag)
            print(token, pos_tag, case_tag, ner_tag, ans_tag)
        print('')


def main_pred(text_filename, true_bio_filename, pred_bio_filename):
    sentences = read_file(text_filename)
    true_answers_bio = read_file(true_bio_filename)
    pred_answers_bio = read_file(pred_bio_filename)
    print('-DOCSTART- X O')
    print('')
    for i in range(len(sentences)):
        tokens = sentences[i].split(' ')
        true_ans_tags = true_answers_bio[i].split(' ')
        pred_ans_tags = pred_answers_bio[i].split(' ')
#        print(i, len(tokens), len(true_ans_tags), len(pred_ans_tags))
        for j in range(len(tokens)):
            true_ans_tag = true_ans_tags[j]
            if j >= len(pred_ans_tags):
                pred_ans_tag = 'O'
            else:
                pred_ans_tag = pred_ans_tags[j]

            token = tokens[j]
            if true_ans_tag != 'O':
                true_ans_tag = "{}-ANS".format(true_ans_tag)

            if pred_ans_tag != 'O':
                pred_ans_tag = "{}-ANS".format(pred_ans_tag)
            print(token, true_ans_tag, pred_ans_tag)
        print('')



if __name__ == '__main__':
    signal(SIGPIPE, SIG_DFL)

    mode = argv[1]
    if mode == 'features':
        text_filename = argv[2]
        answer_bio_filename = argv[3]
        pos_filename = argv[4]
        ner_filename = argv[5]
        case_filename = argv[6]
        main_features(text_filename, answer_bio_filename, pos_filename, ner_filename, case_filename)
    elif mode == 'pred':
        text_filename = argv[2]
        true_bio_filename = argv[3]
        pred_bio_filename = argv[4]
        main_pred(text_filename, true_bio_filename, pred_bio_filename)
