import os, shutil

# Read the landing page
with open('app/HHCApp.jsx','r',encoding='utf-8') as f:
    app = f.read()

# Update the App function to show landing page for new visitors
old = 'export default function App({startAdmin=false}) {\n  const [view,setView]=useState(startAdmin?"admin":"client");'
new = '''export default function App({startAdmin=false}) {
  const [view,setView]=useState(startAdmin?"admin":"landing");'''

if old in app:
    app = app.replace(old, new, 1)
    print("Updated App initial view to landing")
else:
    print("WARNING: Could not find App function - checking alternative...")
    alt = 'export default function App({startAdmin=false}) {'
    if alt in app:
        print("Found App function")

# Update the App routing to include landing page
old_routing = '''  if(view==="client"){
    if(cScr==="login") return <ClientLogin onLogin={()=>setCS("packages")}/>;'''

new_routing = '''  if(view==="landing"){
    const LandingPage = require('./HHCApp').LandingPage || (() => null);
    return <ClientPackages onSelect={async(pkg,email,name)=>{
      try {
        const res = await fetch('/api/create-checkout',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({package:pkg,email:email,name:name})});
        const data = await res.json();
        if(data.url){window.location.href=data.url;}
        else{alert('Payment error: '+(data.error||'Unknown error'));}
      } catch(err){alert('Connection error. Please try again.');}
    }} isLanding={true} onSignIn={()=>{setView("client");setCS("login");}}/>;
  }

  if(view==="client"){
    if(cScr==="login") return <ClientLogin onLogin={()=>setCS("packages")}/>;'''

if old_routing in app:
    app = app.replace(old_routing, new_routing, 1)
    print("Added landing routing")
else:
    print("WARNING: Could not find routing section")

with open('app/HHCApp.jsx','w',encoding='utf-8') as f:
    f.write(app)

print("App updated!")
print("Size:", len(app)//1024, "KB")
