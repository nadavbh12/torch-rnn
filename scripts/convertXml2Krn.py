import argparse, os
import music21
import glob
import matplotlib
import scipy

parser = argparse.ArgumentParser()
parser.add_argument('--input_dir')
parser.add_argument('--output_dir')
args = parser.parse_args()

# ll = glob.glob(args.input_dir + "4 Serpents Tooth Rollins Bird Take 1.xml")
ll = glob.glob(args.input_dir + "*.xml")
for song in ll:
    nameArray = song.split('/')
    songName = nameArray[-1]
    inputName = song.replace(' ', '\ ')
    outputName = songName.replace(' ', '_')
    outputName = outputName.replace('.xml', '.krn')
    runCommand = "./scripts/xml2hum %s > %s" % (inputName, args.output_dir + '/' + outputName)

    os.system(runCommand)
    