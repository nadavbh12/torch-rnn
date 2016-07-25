#! /usr/bin/env python
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument('--composer', default='parker')
parser.add_argument('--meter', type=int, default=4)
args = parser.parse_args()

# networkSize = [128, 256, 512]
networkSize = [256,512]
layers  = [3]
dropouts = [0.3, 0.5, 0.7]
meter   = 4
maxEpochs = 10
# print "nadav"

os.system("python music/gatherDataParker.py --meter 4")
preprocessCommand = ("python scripts/preprocess.py"
                     " --input_txt %s.txt"
                     " --output_h5 music/%s.h5"
                     " --output_json music/%s.json"
                    ) % \
                    (args.composer, \
                     args.composer, \
                     args.composer)
os.system(preprocessCommand)

print "\n"

i = 0
j = 0
k = 0
for size in networkSize:
    for layer in layers:
        for dropout in dropouts:
            trainCommand = ("th train.lua"
                            " -input_h5 music/%s.h5"
                            " -input_json music/%s.json"
                            " -rnn_size %d"
                            " -num_layers %d"
                            " -dropout %f"
                            " -checkpoint_name"
                            " cv/%s_meter%d_size%d_layers%d_dropout%f"
                            " -max_epochs %d"
                           ) % \
                           (args.composer, \
                            args.composer, \
                            size, \
                            layer, \
                            dropout, \
                            args.composer, \
                            args.meter, \
                            size, \
                            layer, \
                            dropout,
                            maxEpochs
                           )
            os.system(trainCommand)