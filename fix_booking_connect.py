with open('app/HHCApp.jsx','r',encoding='utf-8') as f:
    c=f.read()

# Find the booking confirmation step and add real API call
old='''          <div style={{flex:1}}><Btn full onClick={()=>setStep(5)}>Confirm Booking</Btn></div>'''

new='''          <div style={{flex:1}}><Btn full onClick={async()=>{
            try{
              const {data:{user}}=await supabase.auth.getUser();
              const slot=SLOTS.find(s=>s.id===slot);
              await fetch('/api/book',{method:'POST',headers:{'Content-Type':'application/json'},
                body:JSON.stringify({clientEmail:user?.email,service:svc,slotDate:slot?.date,slotTime:slot?.time,addons:adds.map(id=>ADDONS.find(a=>a.id===id)?.name||id)})});
            }catch(e){console.log('Booking error:',e);}
            setStep(5);
          }}>Confirm Booking</Btn></div>'''

print("Found:", old in c)
c=c.replace(old,new,1)

with open('app/HHCApp.jsx','w',encoding='utf-8') as f:
    f.write(c)
print("Done!")