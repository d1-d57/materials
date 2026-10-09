import sys
p=sys.argv[1]; s=open(p).read()
out=[]
for line in s.split("\n"):
    if line.startswith("*"):
        head,sep,rest=line.partition(".*")
        if sep: line=head.replace(" — "," — ")+sep+rest
    out.append(line)
s="\n".join(out); open(p,"w").write(s); print("ok", s.count(" — "))
