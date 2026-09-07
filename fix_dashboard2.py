with open('app/HHCApp.jsx','r',encoding='utf-8') as f:
    c=f.read()

old='''    async function loadMember(){
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
    }'''

new='''    async function loadMember(){
      try{
        const {data:{user}}=await supabase.auth.getUser();
        if(!user){setMem(p=>({...p,name:"Please sign in"}));return;}
        const {data:clients}=await supabase.from('clients').select('*');
        const client=clients&&clients.find(c=>c.email===user.email);
        if(!client){setMem(p=>({...p,name:user.email,pkg:'essential'}));return;}
        const {data:memberships}=await supabase.from('memberships').select('*');
        const membership=memberships&&memberships.find(m=>m.client_id===client.id);
        setMem({
          name:client.full_name||user.email,
          pkg:membership?.package||'essential',
          next:'Contact salon to book',
          used:membership?.sessions_used||0,
          total:membership?.sessions_total||1,
        });
      }catch(e){setMem(p=>({...p,name:"Error loading - please refresh"}));}
    }'''

print("Found:", old[:50] in c)
c=c.replace(old,new,1)
with open('app/HHCApp.jsx','w',encoding='utf-8') as f:
    f.write(c)
print("Done!")