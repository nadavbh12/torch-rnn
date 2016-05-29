
require 'torch'
require 'itorch'
--require 'gnuplot'

local plotError = {}

-- Function to plot the training and test Errors
function plotError.plotError(pointNum, trainError, testError, title)
--    local range = torch.range(1, trainError:size(1))
    local range = torch.range(1, pointNum)
    gnuplot.plot(trainError)
    
    
--    local plot = itorch.Plot()
--    plot:line(range, trainError * 100, 'red', 'Training error')
--    plot:line(range, testError * 100, 'blue', 'Test error'):draw()
--    plot:title(title):redraw()
--    plot:xaxis('epoch'):yaxis('% error'):redraw()
--    plot:legend(true)
    plot:redraw()
end

return plotError