import music21
import argparse
import sys


def numOfPitchesInChord(chord, stream):
    num = 0
    for pitch in stream.pitches:
        for chordPitch in chord.pitches:
            if pitch.name == chordPitch.name:
                num = num + 1
    return num
                
                
parser = argparse.ArgumentParser()
parser.add_argument('--krn_file')
parser.add_argument('--krn_stream')
parser.add_argument('--chord')
args = parser.parse_args()

chord = music21.harmony.ChordSymbol(args.chord)

if args.krn_file is not None:
    kernIn = open(args.krn_file, "r").read()
elif args.krn_stream is not None:
    kernIn = args.krn_stream
#     print 'kernIn = \n' + kernIn
else:
    print 'invalid usage.'
    sys.exit(1)

wrappedInput = "**kern\n" + "*M4/4\n" + "*^\n" + kernIn + "\n==\n*-"
# print wrappedInput 
try:
    m = music21.converter.parse(wrappedInput)
#     catch music21.humdrum.spineParser.HumdrumException
except:
    print 'Exception occured'
    sys.exit(1)

# print "Highest time: " + str(m.highestTime)
# # print "Highest Offset: " + str(m.highestOffset)
# print "duration: " + str(m.duration)
# print "is well formed notation: " + str(m.isWellFormedNotation())



# print str(numOfPitchesInChord(chord,m))
restsOnly = ( len(m.pitches) == 0 )
if restsOnly or ( m.highestTime > 4.0 or not m.isWellFormedNotation() ):
    sys.exit(1)


score = float(numOfPitchesInChord(chord,m)) / float(len(m.pitches))
score *= 100;
score = int(score)

# sys.exit(score)
print score
sys.exit(0)
