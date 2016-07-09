require 'torch'
require 'nn'
require 'LanguageModel'

function mysplit(inputstr, sep)
        if sep == nil then
                sep = "%s"
        end
        local t={} ; i=1
        for str in string.gmatch(inputstr, "([^"..sep.."]+)") do
                t[i] = str
                i = i + 1
        end
        return t
end



local cmd = torch.CmdLine()
cmd:option('-checkpoint', 'cv/checkpoint_4000.t7')
cmd:option('-length', 2000)
cmd:option('-bar_length', 32)
cmd:option('-start_text', '')
cmd:option('-sample', 1)
cmd:option('-temperature', 1)
cmd:option('-gpu', 0)
cmd:option('-gpu_backend', 'cuda')
cmd:option('-verbose', 0)
local opt = cmd:parse(arg)


local checkpoint = torch.load(opt.checkpoint)
local model = checkpoint.model

local msg
if opt.gpu >= 0 and opt.gpu_backend == 'cuda' then
  require 'cutorch'
  require 'cunn'
  cutorch.setDevice(opt.gpu + 1)
  model:cuda()
  msg = string.format('Running with CUDA on GPU %d', opt.gpu)
elseif opt.gpu >= 0 and opt.gpu_backend == 'opencl' then
  require 'cltorch'
  require 'clnn'
  model:cl()
  msg = string.format('Running with OpenCL on GPU %d', opt.gpu)
else
  msg = 'Running in CPU mode'
end
if opt.verbose == 1 then print(msg) end

model:evaluate()

--local sample = model:sample(opt)

-- nadav changes below:
local lastCorrectBar = 1
local sample = nil
local seperated = nil
local sampledSoFar = ''

while lastCorrectBar <= opt.bar_length do
  sample = model:sample(opt)
  seperated = mysplit(sample, '@')
  for i = lastCorrectBar, #seperated do
    seperated[i] = seperated[i]:gsub('\\', '\\\\')
--    print('a bar: ' .. seperated[i] .. '\n')
    local result = os.execute('python scripts/checkMeasure.py --krn_stream "' .. seperated[i] .. '\"')
--    print(result)
    if result == nil or result == 1 then 
--      print('Last bar incorrect')
      opt.start_text = sampledSoFar
      break
    elseif seperated[i] == '' then
--      print('Last bar empty')
      break
    else
      lastCorrectBar = lastCorrectBar + 1
      sampledSoFar = sampledSoFar .. '@' .. seperated[i]
--      print("Last bar correct")
    end
  end

end
--print(seperated[1])

--  os.execute('python scripts/checkMeasure.py --krn_stream "' .. seperated[1] .. '"')

--opt.start_text = "8r  24eee\\LL"
--local sample = model:sample(opt)
--sample = "maayan@nadav"
--local seperated = mysplit(sample)
--print()
--for i = 1, #seperated do
--  print(seperated[i])
--end

--table.concat(seperated, "@")
--print(seperated)
--print()
--end nadav changes



print(sampledSoFar)
