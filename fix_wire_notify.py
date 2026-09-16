with open('app/HHCApp.jsx','r',encoding='utf-8') as f:
    c=f.read()

# Wire booking notification when client confirms booking
old='''            setStep(5);
          }}>Confirm Booking</Btn></div>'''

new='''            try{
              const {data:{user}}=await supabase.auth.getUser();
              await fetch('/api/notify',{method:'POST',headers:{'Content-Type':'application/json'},
                body:JSON.stringify({type:'booking_submitted',data:{
                  clientName:user?.email||'Member',
                  service:svc,
                  date:selectedSlot?.date||'TBC',
                  time:selectedSlot?.time||'TBC',
                  addons:adds.map(id=>ADDONS.find(a=>a.id===id)?.name||id).join(', '),
                }})});
            }catch(e){console.log('Notify error:',e);}
            setStep(5);
          }}>Confirm Booking</Btn></div>'''

print("Found booking confirm:", old in c)
c=c.replace(old,new,1)

# Wire approve notification in admin
old_approve='''onClick={async()=>{await supabase.from('bookings').update({status:'confirmed'}).eq('id',b.id);setRealBookings(p=>p.map(x=>x.id===b.id?{...x,status:'confirmed'}:x));}} style={{background:G.okBg,color:G.ok,border:"none",borderRadius:6,padding:"5px 12px",cursor:"pointer",fontSize:12,fontWeight:700}}>Approve</button>'''

new_approve='''onClick={async()=>{
  await supabase.from('bookings').update({status:'confirmed'}).eq('id',b.id);
  setRealBookings(p=>p.map(x=>x.id===b.id?{...x,status:'confirmed'}:x));
  try{
    const {data:clients}=await supabase.from('clients').select('*');
    const bkg=realBookings.find(x=>x.id===b.id);
    const cl=clients&&clients.find(c=>c.id===b.client_id);
    if(cl){await fetch('/api/notify',{method:'POST',headers:{'Content-Type':'application/json'},
      body:JSON.stringify({type:'booking_confirmed',data:{clientEmail:cl.email,clientName:cl.full_name,service:bkg?.service||'Appointment',date:bkg?.date||'',time:bkg?.time||''}})});}
  }catch(e){console.log('Notify error:',e);}
}} style={{background:G.okBg,color:G.ok,border:"none",borderRadius:6,padding:"5px 12px",cursor:"pointer",fontSize:12,fontWeight:700}}>Approve</button>'''

print("Found approve:", old_approve[:50] in c)
c=c.replace(old_approve,new_approve,1)

# Wire decline notification
old_decline='''onClick={async()=>{await supabase.from('bookings').update({status:'cancelled'}).eq('id',b.id);setRealBookings(p=>p.map(x=>x.id===b.id?{...x,status:'cancelled'}:x));}} style={{background:G.errBg,color:G.err,border:"none",borderRadius:6,padding:"5px 12px",cursor:"pointer",fontSize:12,fontWeight:700}}>Decline</button>'''

new_decline='''onClick={async()=>{
  await supabase.from('bookings').update({status:'cancelled'}).eq('id',b.id);
  setRealBookings(p=>p.map(x=>x.id===b.id?{...x,status:'cancelled'}:x));
  try{
    const {data:clients}=await supabase.from('clients').select('*');
    const cl=clients&&clients.find(c=>c.id===b.client_id);
    if(cl){await fetch('/api/notify',{method:'POST',headers:{'Content-Type':'application/json'},
      body:JSON.stringify({type:'booking_declined',data:{clientEmail:cl.email,clientName:cl.full_name}})});}
  }catch(e){console.log('Notify error:',e);}
}} style={{background:G.errBg,color:G.err,border:"none",borderRadius:6,padding:"5px 12px",cursor:"pointer",fontSize:12,fontWeight:700}}>Decline</button>'''

print("Found decline:", old_decline[:50] in c)
c=c.replace(old_decline,new_decline,1)

with open('app/HHCApp.jsx','w',encoding='utf-8') as f:
    f.write(c)
print("Done!")