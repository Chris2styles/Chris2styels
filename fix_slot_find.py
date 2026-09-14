with open('app/HHCApp.jsx','r',encoding='utf-8') as f:
    c=f.read()

old='const selectedSlot=SLOTS.find(s=>s.id===slot);'
new='const selectedSlot=displaySlots.find(s=>s.id===slot)||SLOTS.find(s=>s.id===slot);'

print("Found:", old in c)
c=c.replace(old,new,1)

with open('app/HHCApp.jsx','w',encoding='utf-8') as f:
    f.write(c)
print("Done!")