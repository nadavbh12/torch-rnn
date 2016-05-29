import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--input_krn')
parser.add_argument('--header')
parser.add_argument('--trailer')
args = parser.parse_args()

f = open(args.input_krn,"r").readlines()
r = []
bar = 1
for l in f:
    if l.startswith("@"):
        if bar == 1:
            r.append("=1-\t=1-\n")
            #r.append("=1-\t=1-\t=1-\n")
        else:
            r.append("={bar}\t={bar}\n".format(bar=bar))
            #r.append("={bar}\t={bar}\t={bar}\n".format(bar=bar))
        bar += 1
    else:
        r.append(l)

header = open(args.header,"r").readlines()
trailer = open(args.trailer,"r").readlines()
open(args.input_krn,"w").writelines(header)
open(args.input_krn,"a").writelines(r)
open(args.input_krn,"a").writelines(trailer)
