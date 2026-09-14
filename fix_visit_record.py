with open('app/HHCApp.jsx','r',encoding='utf-8') as f:
    c=f.read()

# Add amount paid to the Log Visit form
old='''              <div style={{marginBottom:16}}>
                <div style={{fontSize:11,color:"#888",fontWeight:700,letterSpacing:1.5,textTransform:"uppercase",marginBottom:6}}>Notes</div>
                <textarea value={nv.note} onChange={e=>setNv(p=>({...p,note:e.target.value}))}'''

new='''              <div style={{marginBottom:14}}>
                <div style={{fontSize:11,color:"#888",fontWeight:700,letterSpacing:1.5,textTransform:"uppercase",marginBottom:6}}>Amount Paid for Add-ons Today (£)</div>
                <input type="number" value={nv.paid||""} onChange={e=>setNv(p=>({...p,paid:e.target.value}))} placeholder="e.g. 45.00"
                  style={{width:"100%",padding:"11px 12px",background:"#fff",border:"1px solid #DDD8CE",borderRadius:8,fontSize:13,fontFamily:BD,boxSizing:"border-box"}}/>
              </div>
              <div style={{marginBottom:16}}>
                <div style={{fontSize:11,color:"#888",fontWeight:700,letterSpacing:1.5,textTransform:"uppercase",marginBottom:6}}>Notes</div>
                <textarea value={nv.note} onChange={e=>setNv(p=>({...p,note:e.target.value}))}'''

print("Found:", old[:60] in c)
c=c.replace(old,new,1)

# Update visit display to show amount paid
old_visit_note='''                  {v.note&&(
                    <div>
                      <div style={{fontSize:11,color:"#AAA",fontWeight:700,letterSpacing:1.5,textTransform:"uppercase",marginBottom:8}}>Notes</div>
                      <div style={{background:"#fff",borderRadius:10,padding:"13px 16px",border:"1px solid "+G.creamDk,color:"#444",fontSize:13,lineHeight:1.8}}>{v.note}</div>
                    </div>
                  )}'''

new_visit_note='''                  {v.paid&&(
                    <div style={{marginBottom:12}}>
                      <div style={{fontSize:11,color:"#AAA",fontWeight:700,letterSpacing:1.5,textTransform:"uppercase",marginBottom:8}}>Amount Paid</div>
                      <div style={{background:G.goldPale,borderRadius:10,padding:"13px 16px",border:"1px solid "+G.gold+"44",color:G.goldDk,fontSize:20,fontWeight:700}}>£{v.paid}</div>
                    </div>
                  )}
                  {v.note&&(
                    <div>
                      <div style={{fontSize:11,color:"#AAA",fontWeight:700,letterSpacing:1.5,textTransform:"uppercase",marginBottom:8}}>Notes</div>
                      <div style={{background:"#fff",borderRadius:10,padding:"13px 16px",border:"1px solid "+G.creamDk,color:"#444",fontSize:13,lineHeight:1.8}}>{v.note}</div>
                    </div>
                  )}'''

print("Found visit note:", old_visit_note[:60] in c)
c=c.replace(old_visit_note,new_visit_note,1)

with open('app/HHCApp.jsx','w',encoding='utf-8') as f:
    f.write(c)
print("Done!")