
from glob import glob
import numpy as np
import pandas as pd

fs = glob("*_anoPeaks.txt")
fs.sort()
cut = 20000
for i,f in enumerate(fs):
    n = f.split("_anoPeaks")[0]
    mat = pd.read_csv(f,index_col=0,sep="\t")
    s = mat["5_nearestDistanceToTSS"]
    s = s[s<=cut]
    gs = set()
    print(n, mat.shape, s.shape)
    for t in mat.loc[s.index,].itertuples():
        g = t[6].split("|")[2].split("-")[0]
        gs.add(g)
    with open(f"{n}_targetGene.list","w") as fo:
        fo.write("\n".join(gs))


