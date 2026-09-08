with open('app/HHCApp.jsx','r',encoding='utf-8') as f:
    c=f.read()

old='''              const {data:{user}}=await supabase.auth.getUser();
              const slot=SLOTS.find(s=>s.id===slot);
              await fetch('/api/book',{method:'POST',headers:{'Content-Type':'application/json'},
                body:JSON.stringify({clientEmail:user?.email,service:svc,slotDate:slot?.date,slotTime:slot?.time,addons:adds.map(id=>ADDONS.find(a=>a.id===id)?.name||id)})});'''

new='''              const {data:{user}}=await supabase.auth.getUser();
              const selectedSlot=SLOTS.find(s=>s.id===slot);
              await fetch('/api/book',{method:'POST',headers:{'Content-Type':'application/json'},
                body:JSON.stringify({clientEmail:user?.email,service:svc,slotDate:selectedSlot?.date,slotTime:selectedSlot?.time,addons:adds.map(id=>ADDONS.find(a=>a.id===id)?.name||id)})});'''

print("Found:", old[:50] in c)
c=c.replace(old,new,1)
with open('app/HHCApp.jsx','w',encoding='utf-8') as f:
    f.write(c)
print("Done!")