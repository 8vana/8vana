import os
import sys
import convert16

if(len(sys.argv) > 1):
    infile = sys.argv[1]
    if(len(sys.argv) > 2):
        outfile = sys.argv[2]
    else:
        outfile = infile
    if os.path.exists(infile):
        cnv = convert16.Convert16(infile)
        cnv.convert(outfile)
    else:
        print("file not found: " + infile)
else:
    print("invalid arguments.")
    print("ex: " + sys.argv[0] + " <infile> <outfile>")