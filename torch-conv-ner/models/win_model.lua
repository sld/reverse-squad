require 'torch'
require 'nn'
require 'conll_utils'
local nninit = require 'nninit'

module('win_model', package.seeall)

function make_net(embeddings_path)
  local hidden_units = 1024
  local num_classes = 5

  local data = torch.load(embeddings_path)
  local vocab_size = data.data:size(1)
  local embedding_dim = data.data:size(2)
  local emb_lookup_table = nn.LookupTable(vocab_size, embedding_dim)
  emb_lookup_table.weight = data.data

  local case_lookup_table = nn.LookupTable(3, 5):init('weight', nninit.uniform, -1.0, 1.0)
  local pos_lookup_table = nn.LookupTable(46, 30):init('weight', nninit.uniform, -1.0, 1.0)
  local ner_lookup_table = nn.LookupTable(13, 30):init('weight', nninit.uniform, -1.0, 1.0)

  local total_vec_size = embedding_dim + 5 + 30 + 30

  local parallel_lookup = nn.ParallelTable()
  parallel_lookup:add(emb_lookup_table)
  parallel_lookup:add(case_lookup_table)
  parallel_lookup:add(ner_lookup_table)
  parallel_lookup:add(pos_lookup_table)

  local sp = nn.SplitTable(1, 2)
  sp.updateGradInput = function() end

  local net = nn.Sequential()
  net:add(sp)
  net:add(parallel_lookup)
  net:add(nn.JoinTable(3))
  linear_concat_size = total_vec_size * 5
  net:add(nn.Reshape(linear_concat_size, true))
  net:add(nn.Linear(linear_concat_size, hidden_units):init('weight', nninit.uniform, -1.0 / math.sqrt(linear_concat_size), 1.0 / math.sqrt(hidden_units)))
  net:add(nn.Dropout())
  net:add(nn.HardTanh())
  net:add(nn.Linear(hidden_units, num_classes):init('weight', nninit.uniform, -1.0 / math.sqrt(hidden_units), 1.0 / math.sqrt(hidden_units)))

  local criterion = nn.CrossEntropyCriterion()
  criterion = conll_utils.to_cuda(criterion)

  net = conll_utils.to_cuda(net)

  print(net)

  return net, criterion
end
