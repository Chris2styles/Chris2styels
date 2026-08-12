with open('app/HHCApp.jsx','r',encoding='utf-8') as f:
    c=f.read()

old='''function ClientLogin({onLogin}) {
  const [tab,setTab]=useState("login");
  const [showT,setShowT]=useState(false);
  if(showT) return <Terms onBack={()=>setShowT(false)} showAccept={tab==="signup"}'''

new='''function ClientLogin({onLogin}) {
  const [tab,setTab]=useState("login");
  const [showT,setShowT]=useState(false);
  const [email,setLoginEmail]=useState("");
  const [password,setPassword]=useState("");
  const [name,setName]=useState("");
  const [error,setError]=useState("");
  const [loading,setLoading]=useState(false);

  async function handleAuth() {
    setLoading(true);setError("");
    try {
      if(tab==="login"){
        const {error:e}=await supabase.auth.signInWithPassword({email,password});
        if(e)setError(e.message);else onLogin();
      } else {
        const {error:e}=await supabase.auth.signUp({email,password,options:{data:{full_name:name}}});
        if(e)setError(e.message);else onLogin();
      }
    } catch(e){setError("Something went wrong.");}
    setLoading(false);
  }

  if(showT) return <Terms onBack={()=>setShowT(false)} showAccept={tab==="signup"}'''

print("Found:",old[:50] in c)
c=c.replace(old,new,1)
print("Fixed:",new[:50] in c)
with open('app/HHCApp.jsx','w',encoding='utf-8') as f:
    f.write(c)
print("Done!")