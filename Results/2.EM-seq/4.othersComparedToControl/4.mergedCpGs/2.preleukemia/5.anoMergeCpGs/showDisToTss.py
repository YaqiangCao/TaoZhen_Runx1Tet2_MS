
from glob import glob
import numpy as np
import pandas as pd
from vince.settings import *

fig, ax = pylab.subplots()
fs = glob("*_anoPeaks.txt")
fs.sort()
for i,f in enumerate(fs):
    n = f.split("_anoPeaks")[0]
    mat = pd.read_csv(f,index_col=0,sep="\t")
    s = mat["5_nearestDistanceToTSS"]
    s = np.log10(s+1)
    sns.kdeplot( s, label=n, color=colors[i])
ax.legend()
ax.set_xlabel("distance to nearest TSS,log10(bp)")
pylab.savefig("distoTSS.pdf")
