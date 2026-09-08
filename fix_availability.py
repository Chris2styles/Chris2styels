with open('app/HHCApp.jsx','r',encoding='utf-8') as f:
    c=f.read()

# Connect admin slot creation to real API
old='''                <Btn sm onClick={()=>{if(nSlot.date&&nSlot.time){setSlots(p=>[...p,{id:Date.now(),sId:nSlot.sId,date:nSlot.date,time:nSlot.time,dur:nSlot.dur,vip:nSlot.vip,booked:false}]);setNSlot(p=>({...p,date:"",time:""}));}}}>Add</Btn>'''

new='''                <Btn sm onClick={async()=>{if(nSlot.date&&nSlot.time){
                  try{
                    const res=await fetch('/api/slots',{method:'POST',headers:{'Content-Type':'application/json'},
                      body:JSON.stringify({date:nSlot.date,time:nSlot.time,duration:nSlot.dur,stylistId:nSlot.sId})});
                    const data=await res.json();
                    if(data.slot){
                      setSlots(p=>[...p,{id:data.slot.id,sId:nSlot.sId,date:nSlot.date,time:nSlot.time,dur:nSlot.dur,vip:true,booked:false}]);
                      setNSlot(p=>({...p,date:"",time:""}));
                    }
                  }catch(e){console.log('Error:',e);}
                }}}>Add</Btn>'''

print("Found:", old[:50] in c)
c=c.replace(old,new,1)

# Load real slots in ClientBooking
old_slots_state='  const [slot,setSlot]=useState(null);'
new_slots_state='''  const [slot,setSlot]=useState(null);
  const [realSlots,setRealSlots]=React.useState([]);
  React.useEffect(()=>{
    fetch('/api/slots').then(r=>r.json()).then(d=>{
      if(d.slots&&d.slots.length>0){
        setRealSlots(d.slots.map((s,i)=>({
          id:s.id,
          date:new Date(s.slot_date).toLocaleDateString('en-GB',{weekday:'short',day:'numeric',month:'short'}),
          time:s.slot_time.slice(0,5),
          avail:!s.booked
        })));
      }
    }).catch(e=>console.log('Slots error:',e));
  },[]);
  const displaySlots = realSlots.length>0 ? realSlots : SLOTS;'''

print("Found slots state:", old_slots_state in c)
c=c.replace(old_slots_state,new_slots_state,1)

# Replace SLOTS with displaySlots in ClientBooking
c=c.replace('{SLOTS.map(s=>(','{displaySlots.map(s=>(',1)

with open('app/HHCApp.jsx','w',encoding='utf-8') as f:
    f.write(c)
print("Done!")