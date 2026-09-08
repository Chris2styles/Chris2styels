with open('app/HHCApp.jsx','r',encoding='utf-8') as f:
    c=f.read()

old='{(realBookings.length>0?realBookings:BKGS).map(b=>('
new='{(realBookings.length>0?realBookings:[]).map(b=>('

print("Found:", old in c)
c=c.replace(old,new,1)

with open('app/HHCApp.jsx','w',encoding='utf-8') as f:
    f.write(c)
print("Done!")