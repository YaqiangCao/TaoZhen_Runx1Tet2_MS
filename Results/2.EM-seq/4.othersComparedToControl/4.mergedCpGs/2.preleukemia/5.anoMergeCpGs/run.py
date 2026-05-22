import os
from glob import glob

for f in glob("../4.mergeCpGs/*.bed"):
    n = f.split("/")[-1].split(".bed")[0]
    cmd = f"python anoPeaks.py -f {f} -gtf ~/caoy7/Projects/0.Reference/2.mm10/2.annotations/gencode.vM21.basic.annotation.gtf -tid -pdis 1000 -o {n} &"
    print(cmd)
    os.system(cmd)
