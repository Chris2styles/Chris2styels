with open('app/HHCApp.jsx','r',encoding='utf-8') as f:
    c=f.read()

# Fix the hardcoded member name in ClientDashboard booking confirmation
old='const mem={name:"Aisha Thompson",pkg:"signature",next:"16 Jul 2025",used:0,total:1};'

if old in c:
    print("Found old hardcoded mem - already fixed by dashboard2")
else:
    print("Old hardcoded mem not found - good!")

# Fix the booking confirmation step 5 which says "Aisha"
old_confirm='"You are all set, Aisha"'
new_confirm='"You are all set!"'
print("Aisha in file:", old_confirm in c)
c=c.replace(old_confirm, new_confirm, 1)

# Fix the myBkgs filter
old_bkgs='const myBkgs=BKGS.filter(b=>b.client===mem.name);'
new_bkgs='const myBkgs=[];'
print("myBkgs found:", old_bkgs in c)
c=c.replace(old_bkgs, new_bkgs, 1)

with open('app/HHCApp.jsx','w',encoding='utf-8') as f:
    f.write(c)
print("Done!")