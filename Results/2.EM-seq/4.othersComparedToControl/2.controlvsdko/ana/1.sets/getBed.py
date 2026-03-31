from glob import glob

fs = glob("../../../18.DCpGsControlDKORevisedHeatmap/c*.txt")
for f in fs:
    n = f.split("/")[-1].split(".txt")[0]
    ds = {}
    for line in open(f):
        line = line.split("\n")[0].split(".")
        chrom = line[0]
        p = int( line[1])
        if chrom not in ds:
            ds[chrom] = []
        ds[chrom].append(p)
    with open(n+".bed","w") as fo:
        for chrom, ps in ds.items():
            ps = sorted(ps)
            for p in ps:
                line = [ chrom, str(p),str(p+1)]
                fo.write("\t".join(line)+"\n")

