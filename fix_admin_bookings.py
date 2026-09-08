with open('app/HHCApp.jsx','r',encoding='utf-8') as f:
    c=f.read()

old='''        {tab==="bookings"&&(
          <div>
            <div style={{color:G.goldDk,fontSize:10,letterSpacing:3,textTransform:"uppercase",marginBottom:4}}>Appointments</div>
            <h2 style={{fontFamily:SR,fontSize:22,color:"#1A1A1A",margin:"0 0 20px",fontStyle:"italic",fontWeight:400}}>All Bookings</h2>
            <div style={{display:"flex",flexDirection:"column",gap:10}}>
              {BKGS.map(b=>('''

new='''        {tab==="bookings"&&(
          <div>
            <div style={{color:G.goldDk,fontSize:10,letterSpacing:3,textTransform:"uppercase",marginBottom:4}}>Appointments</div>
            <h2 style={{fontFamily:SR,fontSize:22,color:"#1A1A1A",margin:"0 0 20px",fontStyle:"italic",fontWeight:400}}>All Bookings</h2>
            <div style={{display:"flex",flexDirection:"column",gap:10}}>
              {(realBookings.length>0?realBookings:BKGS).map(b=>('''

# Add realBookings state and fetch to AdminDashboard
old_state='  const [realMembers,setRealMembers]=useState([]);'
new_state='''  const [realMembers,setRealMembers]=useState([]);
  const [realBookings,setRealBookings]=useState([]);'''

print("Found bookings tab:", old[:50] in c)
print("Found state:", old_state in c)

c=c.replace(old,new,1)
c=c.replace(old_state,new_state,1)

# Add booking fetch inside loadMembers
old_load='''        const {data:memberships}=await supabase.from('memberships').select('*');
        if(clients&&memberships){'''

new_load='''        const {data:memberships}=await supabase.from('memberships').select('*');
        const {data:bookingsData}=await supabase.from('bookings').select('*');
        if(bookingsData){
          const bkgs=bookingsData.map((b,i)=>{
            const cl=clients&&clients.find(c=>c.id===b.client_id);
            return {id:b.id,client:cl?.full_name||'Unknown',service:b.service||'Appointment',addons:[],date:b.notes||'',time:'',status:b.status||'pending',pkg:'signature'};
          });
          setRealBookings(bkgs);
        }
        if(clients&&memberships){'''

print("Found load:", old_load[:50] in c)
c=c.replace(old_load,new_load,1)

with open('app/HHCApp.jsx','w',encoding='utf-8') as f:
    f.write(c)
print("Done!")