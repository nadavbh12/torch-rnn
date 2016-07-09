import glob
import argparse
import re
REP="@\n"

parser = argparse.ArgumentParser()
parser.add_argument('--meter', type=int, default=4)
args = parser.parse_args()

# composers = ["mozart","beethoven","haydn","chopin"]
composers = ["parker"]
dynamIndices = {}
for composer in composers:
    comp_txt = open(composer + ".txt","w")
##    ll = glob.glob(dir + "/ana-music/corpus/{composer}/*.krn".format(composer=composer))
    ll = glob.glob("/home/nadav/Jazz/torch-rnn/music/ana-music/corpus/{composer}/*.krn".format(composer=composer))
    for song in ll:
        lines = open(song,"r").readlines()
        out = []
        found_first = False
#         out.append(song)
        for l in lines:
# 	    if l.startswith("**kern") and l.count("**kern") != 1:
# 		#print "Number of coloumns: %d" % l.count("**kern")
#                 ## take only pieces with two voices
# 		    break
    	    if args.meter == 4: 
    		## take only pieces with meter of 4/4
    		if l.startswith("*M3") or l.startswith("*M6"):
       		    break
    	    elif args.meter == 3:
    		## take only pieces with meter of 3/4
    		if l.startswith("*M2") or l.startswith("*M4"):
    		    break
 #           if l.startswith("**kern\t"):
 #               #print l
 #               strings = re.split(r'\t+', l)
 #               #print strings
 #               dynamIndices = [i for i, x in enumerate(strings) if (x == "**dynam" or x == "**dynam\n")]
 #               #print song
 #               #print dynamIndices
            if l.startswith("="):
                ## new measure, replace the measure with the @ sign, not part of humdrum
                out.append(REP)
                found_first = True
                continue
            if not found_first:
                ## keep going until we find the end of the header and metadata
                continue
            if l.startswith("!"):
                ## ignore comments
                continue
#             lineArray = re.split(r'\t+', l)
#            for i in sorted(dynamIndices, reverse=True): 
#                del lineArray[i]
#             newL = "\t".join(lineArray) + "\n"
#             if newL.count("\t") != 1:
#                 continue
            #print "l: %s" %l
            #print "newL: %s" %newL
#             out.append(newL)
            out.append(l)
        comp_txt.writelines(out)
    comp_txt.close()
