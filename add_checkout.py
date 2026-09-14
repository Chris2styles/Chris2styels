with open('app/HHCApp.jsx','r',encoding='utf-8') as f:
    c=f.read()

# Find Next Visit Planner and add checkout before it
old='          <div style={{color:G.goldDk,fontSize:10,letterSpacing:2.5,textTransform:"uppercase",fontWeight:700,marginBottom:4}}>Next Visit Planner</div>'

new='''          <div style={{color:G.goldDk,fontSize:10,letterSpacing:2.5,textTransform:"uppercase",fontWeight:700,marginBottom:16}}>Appointment Checkout</div>
          <p style={{color:"#888",fontSize:13,margin:"0 0 16px"}}>Select add-ons the client is paying for today.</p>
          {(()=>{
            const discMap={essential:10,signature:15,elite:20};
            const disc=discMap[data.pkg]||10;
            const [ca,setCa]=React.useState([]);
            const tog=(id)=>setCa(p=>p.includes(id)?p.filter(x=>x!==id):[...p,id]);
            const tot=ADDONS.filter(a=>ca.includes(a.id)).reduce((s,a)=>s+Math.round(a.price*(1-disc/100)),0);
            const full=ADDONS.filter(a=>ca.includes(a.id)).reduce((s,a)=>s+a.price,0);
            return (
              <div>
                {ADDONS.map(a=>{
                  const chk=ca.includes(a.id);
                  return(
                    <label key={a.id} style={{display:"flex",gap:10,alignItems:"center",cursor:"pointer",padding:"7px 0",borderBottom:"1px solid "+G.creamDk}}>
                      <input type="checkbox" checked={chk} onChange={()=>tog(a.id)} style={{accentColor:G.gold}}/>
                      <span style={{flex:1,color:"#333",fontSize:13}}>{a.name}</span>
                      <span style={{textDecoration:"line-through",color:"#AAA",fontSize:12,marginRight:4}}>£{a.price}</span>
                      <span style={{color:G.goldDk,fontWeight:700,fontSize:13}}>£{Math.round(a.price*(1-disc/100))}</span>
                    </label>
                  );
                })}
                {ca.length>0&&(
                  <div style={{background:G.goldPale,borderRadius:10,padding:16,border:"1px solid "+G.gold+"44",marginTop:16}}>
                    <div style={{display:"flex",justifyContent:"space-between",marginBottom:6}}>
                      <span style={{color:"#666",fontSize:13}}>Full price</span>
                      <span style={{textDecoration:"line-through",color:"#AAA"}}>£{full}</span>
                    </div>
                    <div style={{display:"flex",justifyContent:"space-between",marginBottom:6}}>
                      <span style={{color:"#666",fontSize:13}}>{disc}% member discount</span>
                      <span style={{color:G.ok,fontSize:13}}>-£{full-tot}</span>
                    </div>
                    <div style={{display:"flex",justifyContent:"space-between",paddingTop:8,borderTop:"1px solid "+G.gold+"44",marginBottom:12}}>
                      <span style={{fontWeight:700,color:"#1A1A1A",fontSize:16}}>Client pays</span>
                      <span style={{fontWeight:700,color:G.goldDk,fontSize:22}}>£{tot}</span>
                    </div>
                    <button onClick={()=>{
                      setData(p=>({...p,visits:[{date:new Date().toLocaleDateString("en-GB",{day:"numeric",month:"short",year:"numeric"}),service:"Appointment",treatments:ca.map(id=>ADDONS.find(a=>a.id===id)?.name||id),paid:tot,note:"Add-ons charged: £"+tot+" (after "+disc+"% discount)"},...(p.visits||[])]}));
                      setCa([]);
                      alert("Payment of £"+tot+" recorded!");
                    }} style={{width:"100%",padding:"14px 0",background:"linear-gradient(135deg,#E2C97E,#C9A84C)",color:"#1A1A1A",border:"none",borderRadius:8,fontWeight:700,fontSize:14,cursor:"pointer",letterSpacing:1.5,textTransform:"uppercase"}}>
                      Confirm Payment — £{tot}
                    </button>
                    <p style={{color:"#888",fontSize:11,margin:"8px 0 0",textAlign:"center",fontStyle:"italic"}}>Monthly membership collected separately by Stripe.</p>
                  </div>
                )}
              </div>
            );
          })()}
        </div>

        <div style={{background:"#fff",borderRadius:14,padding:22,border:"1px solid "+G.creamDk}}>
          <div style={{color:G.goldDk,fontSize:10,letterSpacing:2.5,textTransform:"uppercase",fontWeight:700,marginBottom:4}}>Next Visit Planner</div>'''

print("Found:", old in c)
c=c.replace(old,new,1)

with open('app/HHCApp.jsx','w',encoding='utf-8') as f:
    f.write(c)
print("Done! Size:",len(c)//1024,"KB")