import os
from glob import glob

fs = glob("../../5.anoMergeCpGs/*.list")
for f in fs:
    n = f.split("/")[-1].split("_target")[0]
    cmd = "findGO.pl %s mouse %s -cpu 10 &"%(f,n)
    print(cmd)
    os.system(cmd)
