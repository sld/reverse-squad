#!/bin/bash

luarocks install nninit

git clone https://github.com/torch/cunn
cd cunn
luarocks make rocks/cunn-scm-1.rockspec
