with open('app/HHCApp.jsx','r',encoding='utf-8') as f:
    c=f.read()

# Fix overview upcoming bookings to use real bookings
old='{BKGS.map((b,i)=>('
new='{(realBookings.length>0?realBookings:BKGS).map((b,i)=>('

print("Found:", old in c)
c=c.replace(old,new,1)

with open('app/HHCApp.jsx','w',encoding='utf-8') as f:
    f.write(c)
print("Done!")