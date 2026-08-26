with open('app/HHCApp.jsx','r',encoding='utf-8') as f:
    c=f.read()

# Find the AdminDashboard function and add real data fetching
old='''function AdminDashboard({onLogout}) {
  const [tab,setTab]=useState("overview");
  const [sel,setSel]=useState(null);
  const [filt,setFilt]=useState("all");
  const [openSec,setOpenSec]=useState(null);
  const [adds,setAdds]=useState(ADDONS);
  const [newA,setNewA]=useState({name:"",price:"",cat:ACATS[0]});
  const [aCat,setACat]=useState(ACATS[0]);'''

new='''function AdminDashboard({onLogout}) {
  const [tab,setTab]=useState("overview");
  const [sel,setSel]=useState(null);
  const [filt,setFilt]=useState("all");
  const [openSec,setOpenSec]=useState(null);
  const [adds,setAdds]=useState(ADDONS);
  const [newA,setNewA]=useState({name:"",price:"",cat:ACATS[0]});
  const [aCat,setACat]=useState(ACATS[0]);
  const [realMembers,setRealMembers]=useState([]);
  const [loading,setLoading]=useState(true);

  React.useEffect(()=>{
    async function loadMembers(){
      try {
        const {data:clients}=await supabase.from('clients').select('*');
        const {data:memberships}=await supabase.from('memberships').select('*');
        if(clients&&memberships){
          const merged=clients.map(cl=>{
            const mem=memberships.find(m=>m.client_id===cl.id)||{};
            return {
              id:cl.id,
              name:cl.full_name,
              email:cl.email,
              phone:cl.phone||'',
              pkg:mem.package||'essential',
              status:mem.status||'active',
              joined:new Date(cl.created_at).toLocaleDateString('en-GB',{month:'short',year:'numeric'}),
              next:'See Stripe',
              used:mem.sessions_used||0,
              total:mem.sessions_total||0,
              notes:'',
              visits:[],
            };
          });
          setRealMembers(merged);
        }
      } catch(e){console.error('Error loading members:',e);}
      setLoading(false);
    }
    loadMembers();
  },[]);

  const displayMembers = realMembers.length > 0 ? realMembers : MEMBERS;'''

print("Found AdminDashboard:", old[:50] in c)
c=c.replace(old,new,1)

# Update the members tab to show loading state and real count
old_active = "  const active=MEMBERS.filter(m=>m.status===\"active\").length;"
new_active = """  const membersToUse = realMembers.length > 0 ? realMembers : MEMBERS;
  const active=membersToUse.filter(m=>m.status==="active").length;"""

print("Found active:", old_active in c)
c=c.replace(old_active, new_active, 1)

# Update revenue calculation
old_rev = "  const revenue=MEMBERS.filter(m=>m.status===\"active\").reduce((s,m)=>{const p=PKGS.find(pk=>pk.id===m.pkg);return s+(p?p.price:0);},0);"
new_rev = "  const revenue=membersToUse.filter(m=>m.status===\"active\").reduce((s,m)=>{const p=PKGS.find(pk=>pk.id===m.pkg);return s+(p?p.price:0);},0);"
c=c.replace(old_rev, new_rev, 1)

# Update failed and paused
old_fail = "  const failed=MEMBERS.filter(m=>m.status===\"payment_failed\").length;"
new_fail = "  const failed=membersToUse.filter(m=>m.status===\"payment_failed\").length;"
c=c.replace(old_fail, new_fail, 1)

old_pause = "  const paused=MEMBERS.filter(m=>m.status===\"paused\").length;"
new_pause = "  const paused=membersToUse.filter(m=>m.status===\"paused\").length;"
c=c.replace(old_pause, new_pause, 1)

# Update the filtered members list
old_filtered = "  const filtered=filt===\"all\"?MEMBERS:MEMBERS.filter(m=>m.status===filt);"
new_filtered = "  const filtered=filt===\"all\"?membersToUse:membersToUse.filter(m=>m.status===filt);"
c=c.replace(old_filtered, new_filtered, 1)

with open('app/HHCApp.jsx','w',encoding='utf-8') as f:
    f.write(c)

print("Done! Size:", len(c)//1024, "KB")
