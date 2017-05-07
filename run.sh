#!/bin/bash

export VOCAB_SOURCE=data/vocab-20000
export VOCAB_TARGET=data/vocab-20000
export TRAIN_SOURCES=redistribute/QG/train/train.txt.source.txt
export TRAIN_TARGETS=redistribute/QG/train/train.txt.target.txt
export DEV_SOURCES=redistribute/QG/dev/dev.txt.shuffle.dev.source.txt
export DEV_TARGETS=redistribute/QG/dev/dev.txt.shuffle.dev.target.txt
export DEV_TARGETS_REF=redistribute/QG/dev/dev.txt.shuffle.dev.target.txt
export TRAIN_STEPS=1000000


export MODEL_DIR=/mnt/245d363f-e0e4-4c4e-b228-df2ec070f242/projects/reverse-squad/tmp/
mkdir -p $MODEL_DIR

python -m bin.train \
  --config_paths="
      ./seq2seq/example_configs/squad.yml,
      ./seq2seq/example_configs/train_seq2seq.yml,
      ./seq2seq/example_configs/text_metrics_bpe.yml" \
  --model_params "
      vocab_source: $VOCAB_SOURCE
      vocab_target: $VOCAB_TARGET" \
  --input_pipeline_train "
    class: ParallelTextInputPipeline
    params:
      source_files:
        - $TRAIN_SOURCES
      target_files:
        - $TRAIN_TARGETS" \
  --input_pipeline_dev "
    class: ParallelTextInputPipeline
    params:
       source_files:
        - $DEV_SOURCES
       target_files:
        - $DEV_TARGETS" \
  --batch_size 32 \
  --train_steps $TRAIN_STEPS \
  --output_dir $MODEL_DIR
