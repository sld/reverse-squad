require 'torch'
require 'nn'
require 'conll_utils'
local nninit = require 'nninit'

module('win_model', package.seeall)

function make_net(embeddings_path)
  local hidden_units = 300
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

  local net_conv = nn.Sequential()
  net_conv:add(sp)
  net_conv:add(parallel_lookup)
  net_conv:add(nn.JoinTable(3))
  local conv_fan_in = 5 * total_vec_size
  net_conv:add(nn.TemporalConvolution(total_vec_size, hidden_units, 5, 1):init('weight', nninit.uniform, -1.0 / math.sqrt(conv_fan_in), 1.0 / math.sqrt(conv_fan_in)))
  net_conv:add(nn.Max(2))
  net_conv:add(nn.Dropout())
  net_conv:add(nn.Linear(hidden_units, hidden_units):init('weight', nninit.uniform, -1.0 / math.sqrt(hidden_units), 1.0 / math.sqrt(hidden_units)))
  net_conv:add(nn.Dropout())
  net_conv:add(nn.HardTanh())
  net_conv:add(nn.Linear(hidden_units, num_classes):init('weight', nninit.uniform, -1.0 / math.sqrt(hidden_units), 1.0 / math.sqrt(hidden_units)))

  local criterion = nn.CrossEntropyCriterion()
  criterion = conll_utils.to_cuda(criterion)

  net_conv = conll_utils.to_cuda(net_conv)

  print(net_conv)

  return net_conv, criterion
end
