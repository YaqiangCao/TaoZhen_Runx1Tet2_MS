
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
    print(n, mat.shape, s.shape)
    ds = {}
    for t in mat.loc[s.index,].itertuples():
        ano = t[4]
        g = t[6]
        site = "|".join(t[0].split("|")[:2])
        if g not in ds:
            ds[g] = {"Enhancer":[],"Promoter":[]}
        ds[g][ano].append(site)
    with open(f"{n}_targetGene.txt","w") as fo:
        line = ["TSS","#PromoterCpG","#EnhancerCpG","PromoterCpG","EnhancerCpG"]
        fo.write("\t".join(line)+"\n")
        for g, anos in ds.items():
            line = [g, str(len(anos["Promoter"])), str(len(anos["Enhancer"])), ",".join(anos["Promoter"]),",".join(anos["Enhancer"])]
            fo.write("\t".join(line)+"\n")

#select target gene 
fs = glob("*_targetGene.txt")
for f in fs:
    n = f.split("_targetGene")[0]
    mat = pd.read_csv( f,index_col=0,sep="\t" )
    s = mat["#PromoterCpG"] + mat["#EnhancerCpG"]
    s = s[s>=10]
    gs = [g.split("|")[-1].split("-")[0] for g in s.index]
    gs = list(set(gs))
    print(n, len(gs))
    with open(n+"_targetGeneSel.list","w") as fo:
        fo.write("\n".join(gs))
