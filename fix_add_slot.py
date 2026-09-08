with open('app/HHCApp.jsx','r',encoding='utf-8') as f:
    c=f.read()

old='''                <Btn sm onClick={async()=>{if(nSlot.date&&nSlot.time){
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

new='''                <Btn sm onClick={async()=>{if(nSlot.date&&nSlot.time){
                  try{
                    const {data:slot,error}=await supabase.from('slots').insert({
                      slot_date:nSlot.date,
                      slot_time:nSlot.time,
                      duration_mins:nSlot.dur||60,
                      members_only:true,
                      is_blocked:false,
                      booked:false,
                    }).select().single();
                    if(slot){
                      setSlots(p=>[...p,{id:slot.id,sId:nSlot.sId,date:nSlot.date,time:nSlot.time,dur:nSlot.dur,vip:true,booked:false}]);
                      setNSlot(p=>({...p,date:"",time:""}));
                    } else {console.log('Error:',error);}
                  }catch(e){console.log('Error:',e);}
                }}}>Add</Btn>'''

print("Found:", old[:50] in c)
c=c.replace(old,new,1)
with open('app/HHCApp.jsx','w',encoding='utf-8') as f:
    f.write(c)
print("Done!")