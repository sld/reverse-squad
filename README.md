# Description

It is the implementation of seq2seq with attention model from
[[Neural Question Generation from Text: A Preliminary Study](https://arxiv.org/pdf/1704.01792.pdf)] paper.

Results almost the same as in the paper.

# Environment

* Python 3.6.0
* tensorflow 1.1.0
* Reverse-SQuAD dataset, download by the [link](https://res.qyzhou.me).
This corpus should be placed in the root of project (./redistribute/).
* Install google/seq2seq - goto seq2seq dir and do steps from README.md.


All packages are listed in requirements.txt.

# Reproduce results

0. Setup the environment.
1. Run: `bin/setup`
2. Run: `bin/seq2seq_with_att`
3. Goto tensorboard and see BLEU in dev set.
4. To check in test set modify and run `bin/seq2seq_with_att_eval`.


# Results

I've got 3.03 BLEU on dev set.

There is open issue with model inference. More information here: https://github.com/google/seq2seq/issues/214.
