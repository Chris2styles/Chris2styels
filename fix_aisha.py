with open('app/HHCApp.jsx','r',encoding='utf-8') as f:
    c=f.read()

old='"You are all set, Aisha"'
new='"You are all set!"'

print("Found:", old in c)
c=c.replace(old,new,1)

with open('app/HHCApp.jsx','w',encoding='utf-8') as f:
    f.write(c)
print("Done!")