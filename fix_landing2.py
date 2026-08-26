with open('app/HHCApp.jsx','r',encoding='utf-8') as f:
    c=f.read()

# Find and replace the landing view with proper LandingPage import
old='''  if(view==="landing"){
    const LandingPage = require('./HHCApp').LandingPage || (() => null);
    return <ClientPackages onSelect={async(pkg,email,name)=>{
      try {
        const res = await fetch('/api/create-checkout',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({package:pkg,email:email,name:name})});
        const data = await res.json();
        if(data.url){window.location.href=data.url;}
        else{alert('Payment error: '+(data.error||'Unknown error'));}
      } catch(err){alert('Connection error. Please try again.');}
    }} isLanding={true} onSignIn={()=>{setView("client");setCS("login");}}/>;
  }'''

new='''  if(view==="landing"){
    return <LandingPageComp 
      onJoin={(pkg)=>{setView("client");setCS("packages");}}
      onSignIn={()=>{setView("client");setCS("login");}}/>;
  }'''

print("Found:",old[:50] in c)
c=c.replace(old,new,1)

# Add LandingPageComp import at the top after React import
if 'LandingPageComp' not in c:
    old_import='import React from "react";'
    new_import='import React from "react";\nimport LandingPageComp from "./LandingPage.jsx";'
    c=c.replace(old_import,new_import,1)
    print("Added import!")

with open('app/HHCApp.jsx','w',encoding='utf-8') as f:
    f.write(c)
print("Done! Size:",len(c)//1024,"KB")