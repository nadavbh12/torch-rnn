require 'torch'
require 'nn'
require 'LanguageModel'
--require 'debugger.plugins.ffi'

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

local function isempty(s)
  return s == nil or s == ''
end

local tmpFileName = "/tmp/checkMeasureOutput"

local function checkMeasure(chord, bar)
    bar = bar:gsub('\\', '\\\\')
--    print('python scripts/checkMeasure.py --chord ' .. chord .. ' --krn_stream "' .. bar .. '\" 1>' .. tmpFileName)
    local result = os.execute('python scripts/checkMeasure.py --chord ' .. chord .. ' --krn_stream "' .. bar .. '\" 1>' .. tmpFileName)
    local f = io.open(tmpFileName)
    local output = f:read("*all")
    f:close()
    
--    print("result = " .. tostring(result) .. ", output: ".. tostring(output))
    
    return result, tonumber(output)
end
    
local function addToSet(set, key)
    set[key] = true
end

local function removeFromSet(set, key)
    set[key] = nil
end

local function setContains(set, key)
    return set[key] ~= nil
end


local cmd = torch.CmdLine()
cmd:option('-checkpoint', 'cv/checkpoint_4000.t7')
cmd:option('-length', 2000)
--cmd:option('-bar_length', 32)
cmd:option('-start_text', '')
cmd:option('-sample', 1)
cmd:option('-temperature', 1)
cmd:option('-gpu', 0)
cmd:option('-gpu_backend', 'cuda')
cmd:option('-verbose', 0)
cmd:option('-chords_file', 'music/chords/12_bar_blues.txt')
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

local sample = model:sample(opt)

-- nadav changes below:
local f = io.open(opt.chords_file)
local chords = f:read("*all")
f:close()
local chordsList = mysplit(chords, ' ')
--table.remove(chordsList, #chordsList)
for i = 1, #chordsList do
--  print(chordsList[i])
end


local lastCorrectBarIndex = 1
local sameBarCount = 0
local sameBarCountThreshold = 12
local lastIncorrectBar = ''
local sample = nil
local bars = nil
local sampledSoFar = ''
correctBars = {}
local enterForLoop = true
local badBars = {}


--while lastCorrectBar <= opt.bar_length do
while lastCorrectBarIndex <= (#chordsList - 1) do
  sample = model:sample(opt)
    
  bars = mysplit(sample, '@')
  
--  print("lastCorrectBar: " .. tostring(lastCorrectBarIndex))
--  print('lastIncorrectBar: ' .. lastIncorrectBar)
--  print("bars[lastCorrectBarIndex]: " .. bars[lastCorrectBarIndex])
  if setContains(badBars, bars[lastCorrectBarIndex]) then
    enterForLoop = false
  elseif lastIncorrectBar == bars[lastCorrectBarIndex] then
    sameBarCount = sameBarCount + 1
    enterForLoop = false
    if sameBarCount > sameBarCountThreshold then
--      print('threshold passed')
      sameBarCount = 0
      if lastCorrectBarIndex ~= 1 then
        lastIncorrectBar = bars[lastCorrectBarIndex-1]
      end
      addToSet(badBars, lastIncorrectBar)
      lastCorrectBarIndex = lastCorrectBarIndex - 1
      table.remove(correctBars)
      opt.start_text = table.concat(correctBars,'@')
    end
  else
    sameBarCount = 0
    enterForLoop = true
  end
  
  if enterForLoop then
    for i = lastCorrectBarIndex, #bars do
      lastIncorrectBar = bars[i]
      result, score = checkMeasure(chordsList[lastCorrectBarIndex], bars[i])
      
      if isempty(score) or result == nil or score < 30 then 
        opt.start_text = table.concat(correctBars,'@')
        break
      elseif bars[i] == '' then
        break
      else
        lastCorrectBarIndex = lastCorrectBarIndex + 1
--        print("lastCorrectBar: " .. tostring(lastCorrectBarIndex))
        table.insert(correctBars,bars[i])
--        print( '*******************************\n' .. table.concat(correctBars,'@') .. '*******************************\n')
  --      print("Last bar correct")
      end
    end
  end
  
end

print(table.concat(correctBars,'@'))
--end nadav changes

--print(sampledSoFar)
