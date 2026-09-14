with open('app/HHCApp.jsx','r',encoding='utf-8') as f:
    c=f.read()

# Fix booking save to include proper date/time in notes
old='''body:JSON.stringify({clientEmail:user?.email,service:svc,slotDate:selectedSlot?.date,slotTime:selectedSlot?.time,addons:adds.map(id=>ADDONS.find(a=>a.id===id)?.name||id)})});'''

new='''body:JSON.stringify({clientEmail:user?.email,service:svc,slotDate:selectedSlot?.date||'TBC',slotTime:selectedSlot?.time||'TBC',addons:adds.map(id=>ADDONS.find(a=>a.id===id)?.name||id)})});'''

print("Found fetch:", old[:50] in c)
c=c.replace(old,new,1)

# Fix the booking API to store date and time properly
old_api='''      notes: `Date: ${slotDate} at ${slotTime}. Add-ons: ${addons.join(', ')}`,'''
new_api='''      notes: `${slotDate} at ${slotTime}`,
      service: service + (addons.length > 0 ? ' + ' + addons.join(', ') : ''),'''

print("Found api notes:", old_api in c)

# Fix how bookings display in admin
old_display='''return {id:b.id,client:cl?.full_name||'Unknown',service:b.service||'Appointment',addons:[],date:b.notes||'',time:'',status:b.status||'pending',pkg:'signature'};'''
new_display='''const notes=b.notes||'';
                    const datePart=notes.includes(' at ')?notes.split(' at ')[0]:'Contact salon';
                    const timePart=notes.includes(' at ')?notes.split(' at ')[1]:'';
                    return {id:b.id,client:cl?.full_name||'Unknown',service:b.service||'Appointment',addons:[],date:datePart,time:timePart,status:b.status||'pending',pkg:'signature'};'''

print("Found display:", old_display in c)
c=c.replace(old_display,new_display,1)

with open('app/HHCApp.jsx','w',encoding='utf-8') as f:
    f.write(c)
print("Done!")