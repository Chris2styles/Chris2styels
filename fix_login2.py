with open('app/HHCApp.jsx','r',encoding='utf-8') as f:
    c=f.read()

# Find the Sign In button and replace with real handler
old='<Btn full onClick={()=>onLogin()}>{tab==="login"?"Sign In to My Account":"Create My Account"}</Btn>'
new='<Btn full onClick={handleAuth} disabled={loading}>{loading?"Please wait...":tab==="login"?"Sign In to My Account":"Create My Account"}</Btn>'

# Also add email/password inputs connected to state
old_email='<input type="email" placeholder="you@email.com"'
new_email='<input type="email" placeholder="you@email.com" value={email} onChange={e=>setLoginEmail(e.target.value)}'

old_password='<input type="password" placeholder="Enter password"'
new_password='<input type="password" placeholder="Enter password" value={password} onChange={e=>setPassword(e.target.value)}'

old_name='<input placeholder="Your name"'
new_name='<input placeholder="Your name" value={name} onChange={e=>setName(e.target.value)}'

print("Btn found:",old[:30] in c)
c=c.replace(old,new,1)
c=c.replace(old_email,new_email,1)
c=c.replace(old_password,new_password,1)
c=c.replace(old_name,new_name,1)

# Add error display before the button
old_err='<Btn full onClick={handleAuth}'
new_err='{error&&<div style={{color:"#B71C1C",fontSize:13,marginBottom:12,padding:"10px 14px",background:"#FFEBEE",borderRadius:4}}>{error}</div>}\n          <Btn full onClick={handleAuth}'
c=c.replace(old_err,new_err,1)

with open('app/HHCApp.jsx','w',encoding='utf-8') as f:
    f.write(c)
print("Done!")