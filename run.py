#! /usr/bin/env python
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument('--composer', default='parker')
parser.add_argument('--meter', type=int, default=4)
parser.add_argument('--rnn_size', type=int, default=512)
parser.add_argument('--num_layers', type=int, default=3)
parser.add_argument('--dropout', type=float, default=0.01)
parser.add_argument('--max_epoch', type=int, default=50)
parser.add_argument('--length', type=int, default=1000)
args = parser.parse_args()

# networkSize = [128, 256, 512]

# os.system("python music/gatherData.py --meter 4")
preprocessCommand = ("python scripts/preprocess.py"
                     " --input_txt %s.txt"
                     " --output_h5 music/%s.h5"
                     " --output_json music/%s.json"
                    ) % \
                    (args.composer, \
                     args.composer, \
                     args.composer)
# os.system(preprocessCommand)

print "\n"

cvName = "%s_meter%d_size%d_layers%d_dropout%f" % \
         ( args.composer, \
           args.meter, \
           args.rnn_size, \
           args.num_layers, \
           args.dropout, \
         )

trainCommand = ("th train.lua"
                " -input_h5 music/%s.h5"
                " -input_json music/%s.json"
                " -rnn_size %d"
                " -num_layers %d"
                " -dropout %f"
                " -max_epochs %d"
                " -checkpoint_name"
                " cv/%s"
               ) % \
               (args.composer, \
                args.composer, \
                args.rnn_size, \
                args.num_layers, \
                args.dropout, \
                args.max_epoch, \
                cvName \
               )
# print trainCommand
# os.system(trainCommand)

cvName = "parker_meter4_size512_layers3_dropout0.500000_8000.t7"
# print 'cvName = ' + cvName
sampleCommand = ("th sample.lua"
                 " -checkpoint cv/%s"
                 " -temperature %.2f" 
                 " -length %d"
#                  " -bar_length %d"
                 " > music/%s_sample.krn") % \
                 (
                  cvName, \
#                   cvName + '_5050.t7', \
                  2, \
                  args.length, \
#                   32, \
                  args.composer                  
                 )
print sampleCommand
os.system(sampleCommand)

postProcessCommand = ("python music/postprocess.py"
                      " --input_krn music/%s_sample.krn"
                      " --header music/header_parker"
                      " --trailer music/trailer_parker") % args.composer
print postProcessCommand
os.system(postProcessCommand)


displayXmlCommand = ("python music/displayXml.py"
                     " --input_krn music/%s_sample.krn") % args.composer
print displayXmlCommand 
os.system(displayXmlCommand)