with open('app/HHCApp.jsx','r',encoding='utf-8') as f:
    c=f.read()

# Add refresh button to bookings tab
old='''            <h2 style={{fontFamily:SR,fontSize:22,color:"#1A1A1A",margin:"0 0 20px",fontStyle:"italic",fontWeight:400}}>All Bookings</h2>'''

new='''            <div style={{display:"flex",justifyContent:"space-between",alignItems:"center",marginBottom:20}}>
              <h2 style={{fontFamily:SR,fontSize:22,color:"#1A1A1A",margin:0,fontStyle:"italic",fontWeight:400}}>All Bookings</h2>
              <button onClick={async()=>{
                const {data:bookingsData}=await supabase.from('bookings').select('*');
                const {data:clients}=await supabase.from('clients').select('*');
                if(bookingsData){
                  const bkgs=bookingsData.map((b)=>{
                    const cl=clients&&clients.find(c=>c.id===b.client_id);
                    return {id:b.id,client:cl?.full_name||'Unknown',service:b.service||'Appointment',addons:[],date:b.notes||'',time:'',status:b.status||'pending',pkg:'signature'};
                  });
                  setRealBookings(bkgs);
                }
              }} style={{background:"linear-gradient(135deg,#E2C97E,#C9A84C)",border:"none",borderRadius:4,padding:"8px 16px",cursor:"pointer",fontSize:12,fontWeight:700,fontFamily:"Trebuchet MS,sans-serif",letterSpacing:1,textTransform:"uppercase",color:"#1A1A1A"}}>Refresh</button>
            </div>'''

print("Found:", old in c)
c=c.replace(old,new,1)

with open('app/HHCApp.jsx','w',encoding='utf-8') as f:
    f.write(c)
print("Done!")