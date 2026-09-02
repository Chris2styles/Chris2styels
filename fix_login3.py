with open('app/HHCApp.jsx','r',encoding='utf-8') as f:
    c=f.read()

# After login, check if user already has membership and go to dashboard
old='''async function handleAuth() {
    setLoading(true);setError("");
    try {
      if(tab==="login"){
        const {error:e}=await supabase.auth.signInWithPassword({email,password});
        if(e)setError(e.message);else onLogin();
      } else {'''

new='''async function handleAuth() {
    setLoading(true);setError("");
    try {
      if(tab==="login"){
        const {error:e,data}=await supabase.auth.signInWithPassword({email,password});
        if(e){setError(e.message);}
        else{onLogin({hasMembership:true});}
      } else {'''

print("Found:", old[:50] in c)
c=c.replace(old,new,1)

# Update the App to handle hasMembership
old_login='if(cScr==="login") return <ClientLogin onLogin={()=>setCS("packages")}/>;'
new_login='if(cScr==="login") return <ClientLogin onLogin={(opts)=>setCS(opts&&opts.hasMembership?"dashboard":"packages")}/>;'

print("Found login routing:", old_login in c)
c=c.replace(old_login,new_login,1)

with open('app/HHCApp.jsx','w',encoding='utf-8') as f:
    f.write(c)
print("Done!")