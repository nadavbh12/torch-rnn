import glob
import argparse
import re
import os
import subprocess

REP="@\n"
    
def removeHeader(lines):
    found_first = False
    for i in range(len(lines)):
        if not lines[i].startswith("*") and found_first == True:
            break
        if lines[i].startswith("="):
            found_first = True
    return lines[i:]
        
def removeTrailer(lines):
    for i in range(len(lines)-1, -1, -1):
        if lines[i].startswith("=="):
            break
    return lines[:i]

def removeBreakLines(lines):
    i = 0
    for i in range(len(lines)):
#         print lines[i]
        if lines[i].startswith('='):
            continue
        if not lines[i].startswith('1r'):
            break
    return lines[max(i-1,0):]

def removeBeamChars(line):
    line = line.replace('L','')
    line = line.replace('/','')
    line = line.replace('\\','')
    line = line.replace('J','')
    line = line.replace('k','')
    line = line.replace('K','')
    line = line.replace('K','')
    return line

parser = argparse.ArgumentParser()
parser.add_argument('--meter', type=int, default=4)
args = parser.parse_args()

composers = ["parker"]
keys = ["P1", "m2", "M2", "m3", "M3", "P4", "A4", "P5", "m6", "M6", "m7", "M7"]
# keys = ["P1"]
dynamIndices = {}
for composer in composers:
    comp_txt = open(composer + ".txt","w")
##    ll = glob.glob(dir + "/ana-music/corpus/{composer}/*.krn".format(composer=composer))
    ll = glob.glob("/home/nadav/Jazz/torch-rnn/music/ana-music/corpus/{composer}/*.krn".format(composer=composer))
    
    for song in ll:
        for key in keys:
#             song = "/home/nadav/Jazz/torch-rnn/music/ana-music/corpus/parker/262_Lady_Be_Good_Charlie_Parker_J_McShann.krn"
            cmd = "transpose -t m2 %s > /tmp/%s" % (song, key)
            proc = subprocess.Popen([cmd], stdout=subprocess.PIPE, shell=True)
            (out, err) = proc.communicate()
#             print "program output:", out
            lines = open("/tmp/" + key,"r").readlines()
            
            out = []
            lines = removeHeader(lines)
            lines = removeTrailer(lines)
            lines = removeBreakLines(lines)
            lines = removeBreakLines(list(reversed(lines)))
            lines = list(reversed(lines))
            found_first = False
            for l in lines:
                if args.meter == 4: 
                ## take only pieces with meter of 4/4
                    if l.startswith("*M3") or l.startswith("*M6"):
                           break
                elif args.meter == 3:
                ## take only pieces with meter of 3/4
                    if l.startswith("*M2") or l.startswith("*M4"):
                            break
                
                if l.startswith("="):
                    ## new measure, replace the measure with the @ sign, not part of humdrum
                    out.append(REP)
                    continue
                if l.startswith("!"):
                    ## ignore comments
                    continue
                if l.startswith("=="):
                    break
                l = removeBeamChars(l)
                out.append(l)
                
            comp_txt.writelines(out)
#         break
    comp_txt.close()
