with open('app/HHCApp.jsx','r',encoding='utf-8') as f:
    c=f.read()

# Add auto-refresh to load bookings in AdminDashboard useEffect
old='''        const {data:bookingsData}=await supabase.from('bookings').select('*');
        const {data:clients}=await supabase.from('clients').select('*');
        if(bookingsData){
          const bkgs=bookingsData.map((b)=>{
            const cl=clients&&clients.find(c=>c.id===b.client_id);
            return {id:b.id,client:cl?.full_name||'Unknown',service:b.service||'Appointment',addons:[],date:b.notes||'',time:'',status:b.status||'pending',pkg:'signature'};
          });
          setRealBookings(bkgs);
        }'''

new='''        const {data:bookingsData}=await supabase.from('bookings').select('*');
        if(bookingsData){
          const bkgs=bookingsData.map((b)=>{
            const cl=clients&&clients.find(c=>c.id===b.client_id);
            const notes=b.notes||'';
            const datePart=notes.includes(' at ')?notes.split(' at ')[0]:'Contact salon';
            const timePart=notes.includes(' at ')?notes.split(' at ')[1]:'';
            return {id:b.id,client:cl?.full_name||'Unknown',service:b.service||'Appointment',addons:[],date:datePart,time:timePart,status:b.status||'pending',pkg:'signature'};
          });
          setRealBookings(bkgs);
        }'''

print("Found:", old[:50] in c)
c=c.replace(old,new,1)

# Add interval to auto-refresh every 30 seconds
old_effect='  React.useEffect(()=>{'
old_load='    async function loadMembers(){'

# Find the AdminDashboard useEffect and add interval
old_interval='''    loadMembers();
  },[]);'''

new_interval='''    loadMembers();
    const interval=setInterval(loadMembers,30000);
    return ()=>clearInterval(interval);
  },[]);'''

print("Found interval:", old_interval in c)
c=c.replace(old_interval,new_interval,1)

with open('app/HHCApp.jsx','w',encoding='utf-8') as f:
    f.write(c)
print("Done!")