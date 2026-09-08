with open('app/HHCApp.jsx','r',encoding='utf-8') as f:
    c=f.read()

# Find the myBkgs line and replace with real data fetch
old='  const myBkgs=[];'
new='''  const [myBkgs,setMyBkgs]=React.useState([]);

  React.useEffect(()=>{
    async function loadBookings(){
      try{
        const {data:{user}}=await supabase.auth.getUser();
        if(!user)return;
        const {data:clients}=await supabase.from('clients').select('*');
        const client=clients&&clients.find(c=>c.email===user.email);
        if(!client)return;
        const {data:bookings}=await supabase.from('bookings').select('*').eq('client_id',client.id);
        if(bookings){
          setMyBkgs(bookings.map(b=>({
            id:b.id,
            client:client.full_name,
            service:b.service,
            addons:[],
            date:b.notes||'Contact salon for details',
            time:'',
            status:b.status||'pending',
            pkg:'signature'
          })));
        }
      }catch(e){console.log('Error loading bookings:',e);}
    }
    loadBookings();
  },[]);'''

print("Found:", old in c)
c=c.replace(old,new,1)

with open('app/HHCApp.jsx','w',encoding='utf-8') as f:
    f.write(c)
print("Done!")