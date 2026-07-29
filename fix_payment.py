with open('app/HHCApp.jsx','r',encoding='utf-8') as f:
    c=f.read()

old="""        {sel&&(
          <div style={{textAlign:"center"}}>
            <Btn onClick={()=>onSelect(sel)}>Continue to Payment</Btn>"""

new="""        {sel&&(
          <div style={{textAlign:"center"}}>
            {!showForm?(
              <Btn onClick={()=>setShowForm(true)}>Continue to Payment</Btn>
            ):(
              <div style={{background:"#111",borderRadius:8,padding:24,maxWidth:380,margin:"0 auto",textAlign:"left"}}>
                <div style={{color:"#C9A84C",fontSize:12,fontWeight:700,letterSpacing:2,textTransform:"uppercase",marginBottom:16}}>Your Details</div>
                <div style={{marginBottom:14}}>
                  <div style={{color:"#999",fontSize:11,fontWeight:700,letterSpacing:1.5,textTransform:"uppercase",marginBottom:6}}>Full Name</div>
                  <input value={name} onChange={e=>setName(e.target.value)} placeholder="Your full name" style={{width:"100%",padding:"12px 14px",background:"#272727",border:"1px solid #3A3A3A",borderRadius:4,color:"#FFF",fontSize:14,outline:"none",boxSizing:"border-box"}}/>
                </div>
                <div style={{marginBottom:20}}>
                  <div style={{color:"#999",fontSize:11,fontWeight:700,letterSpacing:1.5,textTransform:"uppercase",marginBottom:6}}>Email Address</div>
                  <input value={email} onChange={e=>setEmail(e.target.value)} placeholder="your@email.com" type="email" style={{width:"100%",padding:"12px 14px",background:"#272727",border:"1px solid #3A3A3A",borderRadius:4,color:"#FFF",fontSize:14,outline:"none",boxSizing:"border-box"}}/>
                </div>
                <button disabled={!name||!email} onClick={()=>onSelect(sel,email,name)} style={{width:"100%",padding:"14px 0",background:(!name||!email)?"#EEE":"linear-gradient(135deg,#E2C97E,#C9A84C)",color:(!name||!email)?"#AAA":"#1A1A1A",border:"none",borderRadius:8,fontWeight:700,fontSize:13,letterSpacing:1.5,textTransform:"uppercase",cursor:(!name||!email)?"not-allowed":"pointer"}}>Pay Now with Stripe</button>
              </div>
            )}"""

# Add showForm state
old_state="  const [showT,setShowT]=useState(false);\n  if(showT)"
new_state="  const [showT,setShowT]=useState(false);\n  const [showForm,setShowForm]=useState(false);\n  const [name,setName]=useState('');\n  const [email,setEmail]=useState('');\n  if(showT)"

# Fix App onSelect
old_select='if(cScr==="packages") return <ClientPackages onSelect={()=>setCS("dashboard")}/>;'
new_select='''if(cScr==="packages") return <ClientPackages onSelect={async(pkg,email,name)=>{
    try{
      const res=await fetch('/api/create-checkout',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({package:pkg,email:email,name:name})});
      const data=await res.json();
      if(data.url){window.location.href=data.url;}
      else{alert('Payment error: '+(data.error||'Unknown'));}
    }catch(err){alert('Connection error. Please try again.');}
  }}/>;'''

print("old state found:", old_state in c)
print("old select found:", old_select in c)
print("old btn found:", old in c)

c=c.replace(old_state,new_state,1)
c=c.replace(old_select,new_select,1)
c=c.replace(old,new,1)

with open('app/HHCApp.jsx','w',encoding='utf-8') as f:
    f.write(c)
print('Done!')