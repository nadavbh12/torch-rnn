import music21
import argparse
import sys

# def main():

parser = argparse.ArgumentParser()
parser.add_argument('--krn_file')
parser.add_argument('--krn_stream')
args = parser.parse_args()

if args.krn_file is not None:
    kernIn = open(args.krn_file, "r").read()
elif args.krn_stream is not None:
    kernIn = args.krn_stream
#     print 'kernIn = \n' + kernIn
else:
    print 'invalid usage.'
    sys.exit(2)


wrappedInput = "**kern\n" + "*M4/4\n" + "*^\n" + kernIn + "\n==\n*-"
# print wrappedInput 
try:
    m = music21.converter.parse(wrappedInput)
#     catch music21.humdrum.spineParser.HumdrumException
except:
    sys.exit(3)

# print "Highest time: " + str(m.highestTime)
# # print "Highest Offset: " + str(m.highestOffset)
# print "duration: " + str(m.duration)
# print "is well formed notation: " + str(m.isWellFormedNotation())

if m.highestTime > 4.0 or not m.isWellFormedNotation():
    sys.exit(1)
else:
    sys.exit(0)