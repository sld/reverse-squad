#!/bin/bash

cd ..
python convert_to_conll.py redistribute/QG/dev/dev.txt.shuffle.dev.source.txt \
 redistribute/QG/dev/dev.txt.shuffle.dev.bio \
 redistribute/QG/dev/dev.txt.shuffle.dev.pos \
 redistribute/QG/dev/dev.txt.shuffle.dev.ner \
 redistribute/QG/dev/dev.txt.shuffle.dev.case > torch-conv-ner/data/reverse-squad/dev


python convert_to_conll.py redistribute/QG/train/train.txt.source.txt \
 redistribute/QG/train/train.txt.bio \
 redistribute/QG/train/train.txt.pos \
 redistribute/QG/train/train.txt.ner \
 redistribute/QG/train/train.txt.case > torch-conv-ner/data/reverse-squad/train

python get_features.py redistribute/QG/train/train.txt.pos > data/pos_features
python get_features.py redistribute/QG/train/train.txt.ner > data/ner_features
python get_features.py redistribute/QG/train/train.txt.case > data/case_features
cd torch-conv-ner

cat data/reverse-squad/dev | python utils/iob-iobes.py false iob | python utils/iob-iobes.py false iobes > data/reverse-squad/dev.iobes
cat data/reverse-squad/train | python utils/iob-iobes.py false iob | python utils/iob-iobes.py false iobes > data/reverse-squad/train.iobes

head -n 300000 data/reverse-squad/train.iobes > data/reverse-squad/train.iobes-300000

python utils/data_indexer_reverse_squad.py

th utils/index-to-torch-tensors-converter.lua -inFile data/embeddings/senna.index \
  -len 50 -outFile data/embeddings/senna.torch -mode win

th utils/index-to-torch-tensors-converter.lua \
  -inFile data/reverse-squad/dev.iobes.win.index \
  -isCapDataset \
  -len 20 -outFile data/reverse-squad/dev.iobes.win.torch -mode win

th utils/index-to-torch-tensors-converter.lua \
  -inFile data/reverse-squad/train.iobes.win.index \
  -isCapDataset \
  -len 20 -outFile data/reverse-squad/train.iobes.win.torch -mode win

# th conll_learn.lua -version 2-ans-win -mode win -model_name win -batch_size 128
