f=open("ings_list")
lines=f.readlines()
suff={}
for line in lines:
    s=line.split(" ")[-1]
    if s in suff:
        suff[s]=suff[s]+1
    else:
        suff[s]=1

lim=10
for s in suff:
    if suff[s]>=lim:
        print s
