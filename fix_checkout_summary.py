with open('app/HHCApp.jsx','r',encoding='utf-8') as f:
    c=f.read()

# Add checkout summary to MemberDetail page
old='''        <div style={{background:"#fff",borderRadius:14,padding:22,border:"1px solid "+G.creamDk}}>
          <div style={{color:G.goldDk,fontSize:10,letterSpacing:2.5,textTransform:"uppercase",fontWeight:700,marginBottom:4}}>Next Visit Planner</div>'''

new='''        <div style={{background:"#fff",borderRadius:14,padding:22,marginBottom:14,border:"1px solid "+G.creamDk}}>
          <div style={{color:G.goldDk,fontSize:10,letterSpacing:2.5,textTransform:"uppercase",fontWeight:700,marginBottom:16}}>Appointment Checkout</div>
          <p style={{color:"#888",fontSize:13,margin:"0 0 16px",lineHeight:1.65}}>Select add-ons the client is paying for today. Discount applied automatically based on their membership.</p>
          {(()=>{
            const discMap={essential:10,signature:15,elite:20};
            const disc=discMap[data.pkg]||10;
            const [checkedAddons,setCheckedAddons]=React.useState([]);
            const toggle=(id)=>setCheckedAddons(p=>p.includes(id)?p.filter(x=>x!==id):[...p,id]);
            const total=ADDONS.filter(a=>checkedAddons.includes(a.id)).reduce((s,a)=>s+Math.round(a.price*(1-disc/100)),0);
            const fullTotal=ADDONS.filter(a=>checkedAddons.includes(a.id)).reduce((s,a)=>s+a.price,0);
            return (
              <div>
                <div style={{display:"flex",gap:8,flexWrap:"wrap",marginBottom:12}}>
                  {[...new Set(ADDONS.map(a=>a.cat))].map(cat=>(
                    <div key={cat}>
                      <div style={{color:G.goldDk,fontSize:10,fontWeight:700,letterSpacing:1.5,textTransform:"uppercase",marginBottom:6,marginTop:8}}>{cat}</div>
                      {ADDONS.filter(a=>a.cat===cat).map(a=>{
                        const checked=checkedAddons.includes(a.id);
                        const discPrice=Math.round(a.price*(1-disc/100));
                        return(
                          <label key={a.id} style={{display:"flex",gap:10,alignItems:"center",cursor:"pointer",padding:"6px 0",borderBottom:"1px solid "+G.creamDk}}>
                            <input type="checkbox" checked={checked} onChange={()=>toggle(a.id)} style={{accentColor:G.gold}}/>
                            <span style={{flex:1,color:"#333",fontSize:13}}>{a.name}</span>
                            <span style={{textDecoration:"line-through",color:"#AAA",fontSize:12,marginRight:4}}>£{a.price}</span>
                            <span style={{color:G.goldDk,fontWeight:700,fontSize:13}}>£{discPrice}</span>
                          </label>
                        );
                      })}
                    </div>
                  ))}
                </div>
                {checkedAddons.length>0&&(
                  <div style={{background:G.goldPale,borderRadius:10,padding:16,border:"1px solid "+G.gold+"44",marginTop:16}}>
                    <div style={{display:"flex",justifyContent:"space-between",marginBottom:8}}>
                      <span style={{color:"#666",fontSize:13}}>Full price</span>
                      <span style={{textDecoration:"line-through",color:"#AAA",fontSize:13}}>£{fullTotal}</span>
                    </div>
                    <div style={{display:"flex",justifyContent:"space-between",marginBottom:8}}>
                      <span style={{color:"#666",fontSize:13}}>{data.pkg} discount ({disc}% off)</span>
                      <span style={{color:G.ok,fontSize:13}}>-£{fullTotal-total}</span>
                    </div>
                    <div style={{display:"flex",justifyContent:"space-between",paddingTop:8,borderTop:"1px solid "+G.gold+"44"}}>
                      <span style={{fontWeight:700,color:"#1A1A1A",fontSize:16}}>Client pays today</span>
                      <span style={{fontWeight:700,color:G.goldDk,fontSize:22}}>£{total}</span>
                    </div>
                    <p style={{color:"#888",fontSize:11,margin:"8px 0 0",fontStyle:"italic"}}>Monthly membership fee collected separately by Stripe.</p>
                  </div>
                )}
              </div>
            );
          })()}
        </div>

        <div style={{background:"#fff",borderRadius:14,padding:22,border:"1px solid "+G.creamDk}}>
          <div style={{color:G.goldDk,fontSize:10,letterSpacing:2.5,textTransform:"uppercase",fontWeight:700,marginBottom:4}}>Next Visit Planner</div>'''

print("Found:", old[:60] in c)
c=c.replace(old,new,1)

with open('app/HHCApp.jsx','w',encoding='utf-8') as f:
    f.write(c)
print("Done!")