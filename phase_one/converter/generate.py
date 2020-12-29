#!/usr/bin/env python
"""
Generates a bash script tp run many conversions in parallel
"""
import sys

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: [Starting number] [Ending number] [# of processes]")
        sys.exit(0)

    total = int((int(sys.argv[2]) - int(sys.argv[1]))/int(sys.argv[3]))

    print("Total is: ", total)
    print("Range is: ", sys.argv[3])
    for i in range(0, total):
        retval = "("
        for j in range(0, int(sys.argv[3])):
                retval += ("""./full.py /mnt/sdf/fma_large/{} 2>&1 && """.format(str((i*int(sys.argv[3]))+j).zfill(3)))
        retval += """echo "Done {}") &""".format(i)
        print(retval)


