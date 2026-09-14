with open('app/HHCApp.jsx','r',encoding='utf-8') as f:
    c=f.read()

# Add Confirm Payment button to checkout section
old='''                    <p style={{color:"#888",fontSize:11,margin:"8px 0 0",fontStyle:"italic"}}>Monthly membership fee collected separately by Stripe.</p>
                  </div>
                )}
              </div>
            );
          })()}
        </div>'''

new='''                    <p style={{color:"#888",fontSize:11,margin:"8px 0 0",fontStyle:"italic"}}>Monthly membership fee collected separately by Stripe.</p>
                    <button onClick={async()=>{
                      const visitRecord={
                        date:new Date().toLocaleDateString('en-GB',{day:'numeric',month:'short',year:'numeric'}),
                        service:'Appointment',
                        treatments:checkedAddons.map(id=>ADDONS.find(a=>a.id===id)?.name||id),
                        paid:total,
                        note:'Add-ons charged: £'+total+' (after '+disc+'% member discount)',
                      };
                      setData(p=>({...p,visits:[visitRecord,...(p.visits||[])]}));
                      setCheckedAddons([]);
                      alert('Payment of £'+total+' recorded successfully!');
                    }} style={{width:"100%",marginTop:12,padding:"14px 0",background:"linear-gradient(135deg,#E2C97E,#C9A84C)",color:"#1A1A1A",border:"none",borderRadius:8,fontWeight:700,fontSize:14,cursor:"pointer",fontFamily:"Trebuchet MS,sans-serif",letterSpacing:1.5,textTransform:"uppercase"}}>
                      Confirm Payment — £{total}
                    </button>
                  </div>
                )}
              </div>
            );
          })()}
        </div>'''

print("Found:", old[:60] in c)
c=c.replace(old,new,1)

with open('app/HHCApp.jsx','w',encoding='utf-8') as f:
    f.write(c)
print("Done!")