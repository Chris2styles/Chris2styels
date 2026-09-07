with open('app/HHCApp.jsx','r',encoding='utf-8') as f:
    c=f.read()

# Add real member data loading to ClientDashboard
old='''function ClientDashboard({onBook,onLogout}) {
  const mem={name:"Aisha Thompson",pkg:"signature",next:"16 Jul 2025",used:0,total:1};'''

new='''function ClientDashboard({onBook,onLogout}) {
  const [mem,setMem]=React.useState({name:"Loading...",pkg:"signature",next:"",used:0,total:1});

  React.useEffect(()=>{
    async function loadMember(){
      try{
        const {data:{user}}=await supabase.auth.getUser();
        if(!user)return;
        const {data:client}=await supabase.from('clients').select('*').eq('email',user.email).single();
        const {data:membership}=await supabase.from('memberships').select('*').eq('client_id',client?.id).single();
        if(client&&membership){
          setMem({
            name:client.full_name||user.email,
            pkg:membership.package||'essential',
            next:'Contact salon to book',
            used:membership.sessions_used||0,
            total:membership.sessions_total||0,
          });
        }
      }catch(e){console.log('Error loading member:',e);}
    }
    loadMember();
  },[]);'''

print("Found:", old[:60] in c)
c=c.replace(old,new,1)
with open('app/HHCApp.jsx','w',encoding='utf-8') as f:
    f.write(c)
print("Done! Size:",len(c)//1024,"KB")