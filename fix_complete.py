# Complete fix script
with open("app/HHCApp.jsx","r",encoding="utf-8") as f:
    c=f.read()
f1=c.find("function Btn({children,onClick,full,ghost,danger,sm,disabled})")
good_btn="""function Btn({children,onClick,full,ghost,danger,sm,disabled}) {
  const bg=disabled?"#EEE":danger?"#FFF0F0":ghost?"transparent":"linear-gradient(135deg,"+G.goldLt+","+G.gold+")";
  const co=disabled?"#AAA":danger?G.err:ghost?G.goldDk:"#1A1A1A";
  const brd=ghost?"1px solid "+G.gold:danger?"1px solid #FFCDD2":"none";
  return (
    <button onClick={disabled?undefined:onClick}
      style={{width:full?"100%":"auto",padding:sm?"9px 18px":"14px 28px",background:bg,color:co,border:brd,borderRadius:8,fontFamily:DP,fontWeight:700,fontSize:sm?11:13,letterSpacing:1.5,textTransform:"uppercase",cursor:disabled?"not-allowed":"pointer"}}>
      {children}
    </button>
  );
}"""
tail="""
function TreatCard({t}) {
  const [open,setOpen]=useState(false);
  return (
    <div style={{background:G.creamLt,borderRadius:10,border:"1px solid "+G.creamDk,overflow:"hidden"}}>
      <div onClick={()=>setOpen(!open)} style={{display:"flex",alignItems:"center",gap:12,padding:"13px 14px",cursor:"pointer"}}>
        <span style={{fontSize:22,flexShrink:0}}>{t.icon}</span>
        <div style={{flex:1}}><div style={{fontWeight:700,color:"#1A1A1A",fontSize:13}}>{t.name}</div><div style={{color:G.goldDk,fontSize:10,fontWeight:600,textTransform:"uppercase",marginTop:1}}>{t.tag}</div></div>
        <span style={{color:"#BBB",fontSize:16,display:"inline-block",transform:open?"rotate(90deg)":"none",transition:"transform 0.2s"}}>{">"}</span>
      </div>
      {open&&(
        <div style={{borderTop:"1px solid "+G.creamDk,padding:"12px 14px 14px"}}>
          <p style={{color:"#555",fontSize:13,lineHeight:1.7,margin:"0 0 8px"}}>{t.full}</p>
          <span style={{background:G.goldPale,color:G.goldDk,fontSize:11,fontWeight:600,padding:"3px 10px",borderRadius:20}}>{t.note}</span>
        </div>
      )}
    </div>
  );
}

function Terms({onBack,showAccept,onAccept}) {
  const [sec,setSec]=useState(null);
  const [ok,setOk]=useState(false);
  return (
    <div style={{minHeight:"100vh",background:G.cream,fontFamily:BD}}>
      <div style={{background:"#fff",borderBottom:"1px solid "+G.creamDk,padding:"14px 20px",display:"flex",alignItems:"center",gap:14,position:"sticky",top:0,zIndex:10}}>
        <button onClick={onBack} style={{background:G.creamLt,border:"1px solid "+G.creamDk,borderRadius:8,padding:"8px 16px",cursor:"pointer",fontSize:13,color:G.goldDk,fontWeight:700,fontFamily:BD}}>Back</button>
        <div style={{fontWeight:700,fontSize:15,color:"#1A1A1A"}}>Terms and Conditions</div>
      </div>
      <div style={{maxWidth:680,margin:"0 auto",padding:"24px 16px 80px"}}>
        <div style={{background:"linear-gradient(135deg,"+G.goldDk+","+G.gold+")",borderRadius:14,padding:"22px 24px",marginBottom:20}}>
          <div style={{color:"rgba(255,255,255,0.75)",fontSize:10,letterSpacing:3,textTransform:"uppercase",marginBottom:6}}>Healthy Hair Club</div>
          <div style={{fontFamily:SR,color:"#fff",fontSize:20,fontStyle:"italic",marginBottom:4}}>Membership Terms and Conditions</div>
          <div style={{color:"rgba(255,255,255,0.7)",fontSize:12}}>Chris 2 Styles Salon, Mitcham Lane, London SW16</div>
        </div>
        <div style={{background:"#fff",borderRadius:14,padding:22,marginBottom:16,border:"1px solid "+G.creamDk}}>
          <div style={{color:G.goldDk,fontSize:10,letterSpacing:2.5,textTransform:"uppercase",fontWeight:700,marginBottom:14}}>Key Points</div>
          {TCSUMMARY.map((item,i)=>(
            <div key={i} style={{display:"flex",gap:10,alignItems:"flex-start",marginBottom:8}}>
              <span style={{color:G.gold,fontSize:12,flexShrink:0,marginTop:2}}>✦</span>
              <span style={{color:"#444",fontSize:13,lineHeight:1.5}}>{item}</span>
            </div>
          ))}
        </div>
        {TCSECTIONS.map((s,i)=>(
          <div key={i} style={{background:"#fff",borderRadius:12,overflow:"hidden",marginBottom:10,border:"1px solid "+G.creamDk}}>
            <div onClick={()=>setSec(sec===i?null:i)} style={{display:"flex",justifyContent:"space-between",alignItems:"center",padding:"16px 18px",cursor:"pointer",background:sec===i?"#FDF8EC":"#fff"}}>
              <span style={{fontWeight:700,color:"#1A1A1A",fontSize:14}}>{s.t}</span>
              <span style={{color:sec===i?G.goldDk:"#CCC",fontSize:18,display:"inline-block",transform:sec===i?"rotate(90deg)":"none",transition:"transform 0.2s"}}>{">"}</span>
            </div>
            {sec===i&&(
              <div style={{padding:"4px 18px 18px",borderTop:"1px solid #F5F3EE",background:"#FDF8EC"}}>
                <p style={{color:"#444",fontSize:13,lineHeight:1.85,margin:"14px 0 0"}}>{s.b}</p>
              </div>
            )}
          </div>
        ))}
        {showAccept&&(
          <div style={{background:"#fff",borderRadius:14,padding:22,marginTop:10,border:"1px solid "+G.creamDk}}>
            <label style={{display:"flex",gap:14,alignItems:"flex-start",cursor:"pointer",marginBottom:18}}>
              <input type="checkbox" checked={ok} onChange={e=>setOk(e.target.checked)} style={{width:20,height:20,marginTop:2,flexShrink:0,accentColor:G.gold}}/>
              <span style={{color:"#444",fontSize:13,lineHeight:1.7}}>I have read and agree to the Healthy Hair Club Terms and Conditions. I understand my membership renews monthly and I can cancel anytime.</span>
            </label>
            <Btn full disabled={!ok} onClick={onAccept}>I Agree — Continue to Payment</Btn>
          </div>
        )}
      </div>
    </div>
  );
}

function ClientLogin({onLogin}) {
  const [tab,setTab]=useState("login");
  const [showT,setShowT]=useState(false);
  if(showT) return <Terms onBack={()=>setShowT(false)} showAccept={tab==="signup"} onAccept={()=>{setShowT(false);onLogin();}}/>;
  return (
    <div style={{minHeight:"100vh",position:"relative",fontFamily:BD,overflow:"hidden"}}>
      <img src={SALON_EXTERIOR} alt="salon" style={{position:"absolute",inset:0,width:"100%",height:"100%",objectFit:"cover"}}/>
      <div style={{position:"absolute",inset:0,background:"linear-gradient(160deg,rgba(0,0,0,0.88),rgba(10,6,0,0.82))"}}/>
      <div style={{position:"absolute",top:0,left:0,right:0,height:3,background:"linear-gradient(90deg,transparent,"+G.gold+",transparent)"}}/>
      <div style={{position:"relative",zIndex:1,minHeight:"100vh",display:"flex",flexDirection:"column",alignItems:"center",justifyContent:"center",padding:24}}>
        <div style={{textAlign:"center",marginBottom:44}}>
          <Logo light sz={30}/>
          <div style={{marginTop:28}}>
            <div style={{color:G.gold,fontSize:10,letterSpacing:4,textTransform:"uppercase",marginBottom:14}}>Mitcham Lane, London SW16</div>
            <h1 style={{fontFamily:SR,color:G.white,fontSize:34,fontWeight:400,margin:"0 0 10px",lineHeight:1.25,fontStyle:"italic"}}>The Healthy Hair Club</h1>
            <p style={{color:"rgba(255,255,255,0.6)",fontSize:14,maxWidth:320,margin:"0 auto",lineHeight:1.75}}>Priority booking. Exclusive care. Membership benefits all year round.</p>
          </div>
        </div>
        <div style={{background:G.charcoal,borderRadius:4,padding:36,width:"100%",maxWidth:380,border:"1px solid "+G.muted,boxShadow:"0 32px 80px rgba(0,0,0,0.6)"}}>
          <div style={{display:"flex",marginBottom:30,borderBottom:"1px solid "+G.muted}}>
            {["login","signup"].map(t=>(
              <button key={t} onClick={()=>setTab(t)} style={{flex:1,padding:"10px 0",background:"none",border:"none",cursor:"pointer",fontFamily:DP,fontSize:12,fontWeight:700,letterSpacing:2,textTransform:"uppercase",color:tab===t?G.gold:G.dim,borderBottom:"2px solid "+(tab===t?G.gold:"transparent"),marginBottom:-1}}>
                {t==="login"?"Sign In":"Join Now"}
              </button>
            ))}
          </div>
          {tab==="signup"&&(
            <div style={{marginBottom:16}}>
              <div style={{fontSize:10,color:G.silver,fontWeight:700,letterSpacing:2,textTransform:"uppercase",marginBottom:6}}>Full Name</div>
              <input placeholder="Your name" style={{width:"100%",padding:"13px 16px",background:G.graphite,border:"1px solid "+G.muted,borderRadius:3,boxSizing:"border-box",color:G.white,fontSize:14,fontFamily:BD,outline:"none"}}/>
            </div>
          )}
          <div style={{marginBottom:16}}>
            <div style={{fontSize:10,color:G.silver,fontWeight:700,letterSpacing:2,textTransform:"uppercase",marginBottom:6}}>Email Address</div>
            <input type="email" placeholder="you@email.com" style={{width:"100%",padding:"13px 16px",background:G.graphite,border:"1px solid "+G.muted,borderRadius:3,boxSizing:"border-box",color:G.white,fontSize:14,fontFamily:BD,outline:"none"}}/>
          </div>
          <div style={{marginBottom:24}}>
            <div style={{fontSize:10,color:G.silver,fontWeight:700,letterSpacing:2,textTransform:"uppercase",marginBottom:6}}>Password</div>
            <input type="password" placeholder="Enter password" style={{width:"100%",padding:"13px 16px",background:G.graphite,border:"1px solid "+G.muted,borderRadius:3,boxSizing:"border-box",color:G.white,fontSize:14,fontFamily:BD,outline:"none"}}/>
          </div>
          <Btn full onClick={()=>onLogin()}>{tab==="login"?"Sign In to My Account":"Create My Account"}</Btn>
          <p style={{textAlign:"center",fontSize:11,color:G.dim,marginTop:16,lineHeight:1.7}}>
            By joining you agree to our{" "}
            <span onClick={()=>setShowT(true)} style={{color:G.gold,cursor:"pointer",textDecoration:"underline"}}>Terms and Conditions</span>
          </p>
        </div>
      </div>
    </div>
  );
}

function ClientPackages({onSelect}) {
  const [sel,setSel]=useState(null);
  const [showT,setShowT]=useState(false);
  const [showForm,setShowForm]=useState(false);
  const [name,setName]=useState('');
  const [email,setEmail]=useState('');
  if(showT) return <Terms onBack={()=>setShowT(false)}/>;
  return (
    <div style={{minHeight:"100vh",background:G.black,fontFamily:BD}}>
      <div style={{position:"relative",height:200,overflow:"hidden"}}>
        <img src={SALON_WASHBAY} alt="salon" style={{width:"100%",height:"100%",objectFit:"cover",objectPosition:"center 60%",filter:"brightness(0.85)"}}/>
        <div style={{position:"absolute",inset:0,background:"linear-gradient(to bottom,rgba(0,0,0,0.4),rgba(8,8,8,1))"}}/>
        <div style={{position:"absolute",top:0,left:0,right:0,padding:"20px 24px"}}><Logo light sz={24}/></div>
        <div style={{position:"absolute",bottom:24,left:0,right:0,textAlign:"center"}}>
          <div style={{color:G.gold,fontSize:10,letterSpacing:4,textTransform:"uppercase",marginBottom:8}}>Choose Your Membership</div>
          <h2 style={{fontFamily:SR,color:G.white,fontSize:26,fontWeight:400,margin:0,fontStyle:"italic"}}>Join the Healthy Hair Club</h2>
        </div>
      </div>
      <div style={{maxWidth:960,margin:"0 auto",padding:"32px 20px 60px"}}>
        <div style={{display:"grid",gridTemplateColumns:"repeat(auto-fit,minmax(280px,1fr))",gap:20,marginBottom:32}}>
          {PKGS.map(pkg=>{
            const isSel=sel===pkg.id;
            return (
              <div key={pkg.id} onClick={()=>setSel(pkg.id)} style={{background:G.ink,borderRadius:4,overflow:"hidden",cursor:"pointer",position:"relative",border:"1px solid "+(isSel?G.gold:G.graphite),boxShadow:isSel?"0 0 0 1px "+G.gold:"none",transform:isSel?"translateY(-6px)":"none",transition:"all 0.25s"}}>
                {pkg.badge&&<div style={{position:"absolute",top:16,right:16,zIndex:2,background:"linear-gradient(135deg,"+G.goldLt+","+G.gold+")",color:G.black,fontSize:9,fontWeight:700,letterSpacing:2,textTransform:"uppercase",padding:"4px 10px",borderRadius:2}}>{pkg.badge}</div>}
                <div style={{height:170,overflow:"hidden",position:"relative"}}>
                  <img src={pkg.img} alt={pkg.name} style={{width:"100%",height:"100%",objectFit:"cover",objectPosition:"center top",filter:"brightness(0.85)"}}/>
                  <div style={{position:"absolute",inset:0,background:"linear-gradient(to top,rgba(26,26,26,0.9),transparent 60%)"}}/>
                  <div style={{position:"absolute",bottom:14,left:20}}>
                    <div style={{color:G.gold,fontSize:10,letterSpacing:3,textTransform:"uppercase",marginBottom:4}}>{pkg.sub}</div>
                    <div style={{fontFamily:SR,color:G.white,fontSize:22,fontStyle:"italic"}}>{pkg.name}</div>
                  </div>
                </div>
                <div style={{padding:"20px 20px 22px"}}>
                  <div style={{display:"flex",alignItems:"baseline",gap:4,marginBottom:6}}>
                    <span style={{fontFamily:DP,fontSize:34,color:G.gold,fontWeight:700}}>{"£"}{pkg.price}</span>
                    <span style={{color:G.dim,fontSize:13}}>/month</span>
                  </div>
                  <p style={{color:G.silver,fontSize:12,lineHeight:1.65,margin:"0 0 16px",fontStyle:"italic"}}>"{pkg.tagline}"</p>
                  <div style={{borderTop:"1px solid "+G.graphite,paddingTop:14}}>
                    {pkg.benefits.map((b,i)=>(
                      <div key={i} style={{display:"flex",gap:10,alignItems:"flex-start",marginBottom:7}}>
                        <span style={{color:G.gold,fontSize:12,flexShrink:0,marginTop:1}}>✦</span>
                        <span style={{color:G.smoke,fontSize:12,lineHeight:1.5}}>{b}</span>
                      </div>
                    ))}
                  </div>
                  <div style={{marginTop:16,padding:"11px 0",background:isSel?"linear-gradient(135deg,"+G.goldLt+","+G.gold+")":G.graphite,borderRadius:3,textAlign:"center"}}>
                    <span style={{fontFamily:DP,fontSize:11,fontWeight:700,letterSpacing:2,textTransform:"uppercase",color:isSel?G.black:G.silver}}>{isSel?"Selected":"Select Plan"}</span>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
        {sel&&(
          <div style={{textAlign:"center"}}>
            {!showForm?(
              <Btn onClick={()=>setShowForm(true)}>Continue to Payment</Btn>
            ):(
              <div style={{background:G.charcoal,borderRadius:8,padding:24,maxWidth:380,margin:"0 auto",textAlign:"left"}}>
                <div style={{color:G.gold,fontSize:12,fontWeight:700,letterSpacing:2,textTransform:"uppercase",marginBottom:16}}>Your Details</div>
                <div style={{marginBottom:14}}>
                  <div style={{color:G.silver,fontSize:11,fontWeight:700,letterSpacing:1.5,textTransform:"uppercase",marginBottom:6}}>Full Name</div>
                  <input value={name} onChange={e=>setName(e.target.value)} placeholder="Your full name"
                    style={{width:"100%",padding:"12px 14px",background:G.graphite,border:"1px solid "+G.muted,borderRadius:4,color:G.white,fontSize:14,fontFamily:BD,outline:"none",boxSizing:"border-box"}}/>
                </div>
                <div style={{marginBottom:20}}>
                  <div style={{color:G.silver,fontSize:11,fontWeight:700,letterSpacing:1.5,textTransform:"uppercase",marginBottom:6}}>Email Address</div>
                  <input value={email} onChange={e=>setEmail(e.target.value)} placeholder="your@email.com" type="email"
                    style={{width:"100%",padding:"12px 14px",background:G.graphite,border:"1px solid "+G.muted,borderRadius:4,color:G.white,fontSize:14,fontFamily:BD,outline:"none",boxSizing:"border-box"}}/>
                </div>
                <Btn full disabled={!name||!email} onClick={()=>onSelect(sel,email,name)}>Pay Now with Stripe</Btn>
              </div>
            )}
            <p style={{color:G.dim,fontSize:11,marginTop:12}}>
              Cancel anytime{" "}<span onClick={()=>setShowT(true)} style={{color:G.gold,cursor:"pointer",textDecoration:"underline"}}>Terms and Conditions</span>
            </p>
          </div>
        )}
      </div>
    </div>
  );
}

function ClientDashboard({onBook,onLogout}) {
  const mem={name:"Aisha Thompson",pkg:"signature",next:"16 Jul 2025",used:0,total:1};
  const pkg=PKGS.find(p=>p.id===mem.pkg);
  const myBkgs=BKGS.filter(b=>b.client===mem.name);
  const [chat,setChat]=useState(false);
  const [showT,setShowT]=useState(false);
  const [mOpen,setMOpen]=useState(false);
  const [sec,setSec]=useState(null);
  if(showT) return <Terms onBack={()=>setShowT(false)}/>;

  function S({id,icon,title,sub,children}) {
    const open=sec===id;
    return (
      <div style={{background:"#FFF",borderRadius:14,overflow:"hidden",marginBottom:14,boxShadow:"0 2px 12px rgba(0,0,0,0.05)",border:"1px solid "+G.creamDk}}>
        <div onClick={()=>setSec(open?null:id)} style={{display:"flex",alignItems:"center",justifyContent:"space-between",padding:"18px 20px",cursor:"pointer"}}>
          <div style={{display:"flex",alignItems:"center",gap:14}}>
            <div style={{width:38,height:38,borderRadius:10,background:open?G.goldPale:"#F7F3EC",display:"flex",alignItems:"center",justifyContent:"center",fontSize:18,flexShrink:0}}>{icon}</div>
            <div>
              <div style={{fontWeight:700,fontSize:15,color:"#1A1A1A"}}>{title}</div>
              {sub&&<div style={{fontSize:12,color:"#888",marginTop:1}}>{sub}</div>}
            </div>
          </div>
          <span style={{color:open?G.goldDk:"#BBB",fontSize:18,display:"inline-block",transform:open?"rotate(90deg)":"none",transition:"transform 0.2s"}}>{">"}</span>
        </div>
        {open&&<div style={{borderTop:"1px solid #F0EBE0"}}>{children}</div>}
      </div>
    );
  }

  return (
    <div style={{minHeight:"100vh",background:G.cream,fontFamily:BD}}>
      <div style={{position:"relative",height:210,overflow:"hidden"}}>
        <img src={SALON_INTERIOR} alt="salon" style={{width:"100%",height:"100%",objectFit:"cover",objectPosition:"center 30%"}}/>
        <div style={{position:"absolute",inset:0,background:"linear-gradient(to bottom,rgba(255,255,255,0),rgba(245,243,238,1))"}}/>
        <div style={{position:"absolute",top:0,left:0,right:0,padding:"16px 20px",display:"flex",justifyContent:"space-between",alignItems:"center"}}>
          <Logo light sz={22}/>
          <button onClick={onLogout} style={{background:"rgba(255,255,255,0.85)",border:"none",borderRadius:20,padding:"6px 16px",fontSize:12,color:"#555",cursor:"pointer",fontWeight:600}}>Sign Out</button>
        </div>
        <div style={{position:"absolute",bottom:16,left:20}}>
          <div style={{color:G.goldDk,fontSize:10,letterSpacing:3,textTransform:"uppercase",marginBottom:4}}>Welcome back</div>
          <div style={{fontFamily:SR,color:"#1A1A1A",fontSize:24,fontStyle:"italic"}}>{mem.name}</div>
        </div>
      </div>

      <div style={{maxWidth:680,margin:"0 auto",padding:"16px 16px 100px"}}>

        <div style={{background:"#FFF",borderRadius:16,overflow:"hidden",marginBottom:14,boxShadow:"0 2px 12px rgba(0,0,0,0.06)",border:"1px solid "+G.creamDk}}>
          <div onClick={()=>setMOpen(!mOpen)} style={{background:"linear-gradient(135deg,"+G.goldDk+","+G.gold+")",padding:"20px 20px 18px",cursor:"pointer"}}>
            <div style={{display:"flex",justifyContent:"space-between",alignItems:"flex-start"}}>
              <div>
                <div style={{color:"rgba(255,255,255,0.75)",fontSize:10,letterSpacing:3,textTransform:"uppercase",marginBottom:6}}>Healthy Hair Club</div>
                <div style={{fontFamily:SR,color:"#FFF",fontSize:22,fontStyle:"italic",marginBottom:2}}>Signature Care</div>
                <div style={{color:"rgba(255,255,255,0.85)",fontSize:13}}>{"£"}99 / month · Active</div>
              </div>
              <div style={{textAlign:"right"}}>
                <div style={{background:"rgba(255,255,255,0.2)",borderRadius:20,padding:"4px 12px",fontSize:11,color:"#fff",fontWeight:700,marginBottom:8}}>Active</div>
                <div style={{color:"rgba(255,255,255,0.75)",fontSize:11}}>Next: {mem.next}</div>
              </div>
            </div>
            <div style={{marginTop:16}}>
              <div style={{display:"flex",justifyContent:"space-between",marginBottom:6}}>
                <span style={{color:"rgba(255,255,255,0.75)",fontSize:11}}>Monthly session</span>
                <span style={{color:"#fff",fontSize:11,fontWeight:700}}>{mem.used}/{mem.total} used</span>
              </div>
              <div style={{height:5,background:"rgba(255,255,255,0.25)",borderRadius:4}}>
                <div style={{height:5,background:"#fff",borderRadius:4,width:(mem.total>0?(mem.used/mem.total)*100:0)+"%"}}/>
              </div>
            </div>
            <div style={{marginTop:12,color:"rgba(255,255,255,0.7)",fontSize:11}}>{mOpen?"Hide details":"Tap to see everything included"}</div>
          </div>

          {mOpen&&(
            <div style={{padding:"20px 20px 18px",borderTop:"1px solid "+G.creamDk}}>
              <div style={{color:G.goldDk,fontSize:10,letterSpacing:3,textTransform:"uppercase",marginBottom:14}}>What Is Included</div>
              <div style={{display:"grid",gridTemplateColumns:"1fr 1fr",gap:8,marginBottom:18}}>
                {pkg.benefits.map((b,i)=>(
                  <div key={i} style={{display:"flex",gap:8,alignItems:"flex-start"}}>
                    <span style={{color:G.gold,fontSize:13,flexShrink:0,marginTop:1}}>✦</span>
                    <span style={{color:"#444",fontSize:13,lineHeight:1.5}}>{b}</span>
                  </div>
                ))}
              </div>
              <div style={{background:G.creamLt,borderRadius:10,padding:16,marginBottom:14,border:"1px solid "+G.creamDk}}>
                <div style={{fontWeight:700,color:"#1A1A1A",fontSize:13,marginBottom:4}}>Monthly Maintenance Appointment</div>
                <p style={{color:"#666",fontSize:12,lineHeight:1.7,margin:"0 0 12px"}}>Your appointment is personalised to your hair needs. Your stylist selects the most suitable treatments from the options below.</p>
                <div style={{display:"grid",gridTemplateColumns:"1fr 1fr",gap:8}}>
                  {TREATS.map((t,i)=>(
                    <div key={i} style={{background:"#fff",borderRadius:8,padding:"10px 12px",border:"1px solid "+G.creamDk}}>
                      <div style={{fontSize:16,marginBottom:3}}>{t.icon}</div>
                      <div style={{fontWeight:700,color:"#1A1A1A",fontSize:12,marginBottom:2}}>{t.name}</div>
                      <div style={{color:G.goldDk,fontSize:10,marginBottom:4,fontWeight:600}}>{t.tag}</div>
                      <p style={{color:"#777",fontSize:11,lineHeight:1.55,margin:0}}>{t.short}</p>
                    </div>
                  ))}
                </div>
                <p style={{color:"#999",fontSize:11,marginTop:12,marginBottom:0,fontStyle:"italic"}}>Your stylist selects the best combination at each visit based on your hair condition.</p>
              </div>
              <div style={{background:"#F0EBE0",borderRadius:8,padding:"11px 14px",display:"flex",gap:10,alignItems:"flex-start"}}>
                <span style={{fontSize:16,flexShrink:0}}>💡</span>
                <p style={{color:"#5A4A2A",fontSize:12,margin:0,lineHeight:1.65}}>Your discount: 15% off selected premium services, applied automatically when you book.</p>
              </div>
            </div>
          )}
        </div>

        <button onClick={onBook} style={{width:"100%",padding:"17px 0",background:"linear-gradient(135deg,"+G.goldLt+","+G.gold+")",color:"#1A1A1A",border:"none",borderRadius:14,fontSize:15,fontWeight:700,fontFamily:DP,letterSpacing:1.5,textTransform:"uppercase",cursor:"pointer",marginBottom:14}}>
          Book My Appointment
        </button>

        {myBkgs.length>0&&(
          <S id="bkgs" icon="📋" title="Upcoming Appointments" sub={myBkgs.length+" scheduled"}>
            <div style={{padding:"0 20px 18px"}}>
              {myBkgs.map((b,i)=>(
                <div key={b.id} style={{paddingTop:14,borderTop:i>0?"1px solid #F0EBE0":"none"}}>
                  <div style={{display:"flex",justifyContent:"space-between",alignItems:"flex-start",marginBottom:4}}>
                    <div style={{fontWeight:700,color:"#1A1A1A",fontSize:14}}>{b.service}</div>
                    <Pill s={b.status}/>
                  </div>
                  <div style={{color:"#888",fontSize:12}}>{b.date} at {b.time}</div>
                  {b.addons.length>0&&<div style={{color:G.goldDk,fontSize:11,fontWeight:600,marginTop:3}}>+ {b.addons.join(", ")}</div>}
                </div>
              ))}
            </div>
          </S>
        )}

        <S id="maint" icon="🌿" title="Why Ongoing Maintenance Matters" sub="The secret to healthy-looking hair">
          <div style={{padding:"0 20px 20px"}}>
            <p style={{color:"#555",fontSize:13,lineHeight:1.85,margin:"16px 0 12px"}}>Healthy-looking hair is usually the result of consistency, not just one appointment. Regular maintenance helps keep the hair and scalp cleaner, more manageable and better supported over time.</p>
            <p style={{color:"#666",fontSize:13,lineHeight:1.85,margin:"0 0 16px",fontStyle:"italic",borderLeft:"3px solid "+G.gold,paddingLeft:14}}>By maintaining a consistent routine, you can stay on top of moisture, scalp care, trims and strengthening treatments before the hair becomes difficult to manage.</p>
            <div style={{display:"flex",flexDirection:"column",gap:8}}>
              {["Stay on top of moisture before hair becomes dry","Scalp care keeps the foundation healthy","Regular trims prevent split ends spreading","Right treatments applied at the right time","Ongoing advice tailored to your hair","Your hair stays easier to manage all year round"].map((b,i)=>(
                <div key={i} style={{display:"flex",gap:10,alignItems:"flex-start"}}>
                  <span style={{color:G.gold,fontSize:13,flexShrink:0}}>✦</span>
                  <span style={{color:"#555",fontSize:13,lineHeight:1.5}}>{b}</span>
                </div>
              ))}
            </div>
          </div>
        </S>

        <S id="treats" icon="💆🏾‍♀️" title="Your Treatments Explained" sub="Tap to learn what each treatment does">
          <div style={{padding:"0 20px 20px"}}>
            <p style={{color:"#888",fontSize:12,margin:"14px 0 16px",lineHeight:1.65}}>Your stylist selects the most suitable treatment at each visit. Not every treatment is applied every time.</p>
            <div style={{display:"flex",flexDirection:"column",gap:10}}>
              {TREATS.map((t,i)=><TreatCard key={i} t={t}/>)}
            </div>
          </div>
        </S>

        <S id="disc" icon="🏷️" title="Your Member Discounts" sub="See how your membership saves you money">
          <div style={{padding:"16px 20px 20px"}}>
            <div style={{background:G.creamLt,borderRadius:10,padding:16,border:"1px solid "+G.creamDk}}>
              <div style={{fontWeight:700,color:"#1A1A1A",fontSize:14,marginBottom:4}}>Signature Care — Your Discount</div>
              <div style={{color:G.goldDk,fontSize:22,fontWeight:700,marginBottom:2}}>15% off</div>
              <div style={{color:"#666",fontSize:12}}>Applied automatically on selected premium services. No codes needed.</div>
            </div>
          </div>
        </S>

        <S id="tc" icon="📄" title="Terms and Conditions" sub="Your membership agreement">
          <div style={{padding:"16px 20px 20px"}}>
            <p style={{color:"#666",fontSize:13,lineHeight:1.75,margin:"0 0 14px"}}>Your membership is governed by our Terms and Conditions, covering payment rights, booking rules, cancellation policy and session rules.</p>
            <div style={{display:"flex",flexDirection:"column",gap:8,marginBottom:18}}>
              {TCSUMMARY.map((item,i)=>(
                <div key={i} style={{display:"flex",gap:10,alignItems:"flex-start"}}>
                  <span style={{color:G.gold,fontSize:12,flexShrink:0,marginTop:2}}>✦</span>
                  <span style={{color:"#555",fontSize:13,lineHeight:1.5}}>{item}</span>
                </div>
              ))}
            </div>
            <Btn full onClick={()=>setShowT(true)}>Read Full Terms and Conditions</Btn>
          </div>
        </S>

        <div onClick={()=>setChat(true)} style={{background:"#FFF",borderRadius:14,padding:"16px 20px",display:"flex",alignItems:"center",gap:14,cursor:"pointer",border:"1px solid "+G.creamDk,marginBottom:14}}>
          <div style={{width:42,height:42,borderRadius:12,background:"linear-gradient(135deg,"+G.goldLt+","+G.gold+")",display:"flex",alignItems:"center",justifyContent:"center",fontSize:20,flexShrink:0}}>✦</div>
          <div style={{flex:1}}>
            <div style={{fontWeight:700,color:"#1A1A1A",fontSize:14}}>Got a question?</div>
            <div style={{color:"#888",fontSize:12,marginTop:2}}>Chat with our Healthy Hair Club Assistant</div>
          </div>
          <span style={{color:G.gold,fontSize:22,fontWeight:300}}>{">"}</span>
        </div>
      </div>
      {chat?<Bot onClose={()=>setChat(false)}/>:<BotBtn onClick={()=>setChat(true)}/>}
    </div>
  );
}

function ClientBooking({onBack}) {
  const [step,setStep]=useState(1);
  const [svc,setSvc]=useState(null);
  const [slot,setSlot]=useState(null);
  const [adds,setAdds]=useState([]);
  const [cat,setCat]=useState(ACATS[0]);
  const [chat,setChat]=useState(false);
  const disc=15;
  const svcs=SVCMAP.signature;

  function toggle(id) {setAdds(p=>p.includes(id)?p.filter(x=>x!==id):[...p,id]);}
  const total=ADDONS.filter(a=>adds.includes(a.id)).reduce((s,a)=>s+Math.round(a.price*(1-disc/100)),0);

  return (
    <div style={{minHeight:"100vh",background:G.cream,fontFamily:BD}}>
      <div style={{background:"#fff",borderBottom:"1px solid "+G.creamDk,padding:"16px 24px",display:"flex",alignItems:"center",gap:16}}>
        <button onClick={onBack} style={{background:"none",border:"none",cursor:"pointer",fontSize:20,color:"#666",padding:0}}>{"<"}</button>
        <Logo light={false} sz={22}/>
        <div style={{marginLeft:"auto",display:"flex",alignItems:"center",gap:12}}>
          <button onClick={()=>setChat(true)} style={{background:G.goldPale,border:"1px solid "+G.gold+"44",borderRadius:4,padding:"6px 14px",cursor:"pointer",color:G.goldDk,fontSize:11,fontWeight:700,fontFamily:DP,letterSpacing:1}}>Help</button>
          <span style={{color:G.goldDk,fontSize:11,letterSpacing:2,textTransform:"uppercase"}}>Book</span>
        </div>
      </div>
      <div style={{background:"#fff",borderBottom:"1px solid "+G.creamDk,padding:"0 24px"}}>
        <div style={{maxWidth:600,margin:"0 auto",display:"flex"}}>
          {["Service","Add-ons","Time","Confirm"].map((s,i)=>(
            <div key={s} style={{flex:1,textAlign:"center",padding:"14px 0",position:"relative"}}>
              <div style={{fontSize:11,fontWeight:700,fontFamily:DP,letterSpacing:1,textTransform:"uppercase",color:step===i+1?"#1A1A1A":step>i+1?G.gold:"#999"}}>{s}</div>
              {step===i+1&&<div style={{position:"absolute",bottom:0,left:0,right:0,height:2,background:G.gold}}/>}
            </div>
          ))}
        </div>
      </div>
      <div style={{maxWidth:600,margin:"0 auto",padding:"32px 20px 60px"}}>

        {step===1&&(
          <div>
            <h3 style={{fontFamily:SR,color:"#1A1A1A",fontSize:22,fontStyle:"italic",margin:"0 0 24px"}}>Choose your service</h3>
            {svcs.map(s=>(
              <div key={s} onClick={()=>setSvc(s)} style={{background:svc===s?G.creamLt:"#fff",border:"1px solid "+(svc===s?G.gold:G.creamDk),borderRadius:3,padding:"15px 20px",marginBottom:10,cursor:"pointer",display:"flex",justifyContent:"space-between",alignItems:"center"}}>
                <span style={{color:"#1A1A1A",fontWeight:svc===s?700:400,fontSize:14}}>{s}</span>
                {svc===s&&<span style={{color:G.gold,fontSize:14}}>✦</span>}
              </div>
            ))}
            <div style={{marginTop:24}}><Btn full disabled={!svc} onClick={()=>setStep(2)}>Next: Add-ons</Btn></div>
          </div>
        )}

        {step===2&&(
          <div>
            <h3 style={{fontFamily:SR,color:"#1A1A1A",fontSize:22,fontStyle:"italic",margin:"0 0 6px"}}>Enhance your visit</h3>
            <p style={{color:"#666",fontSize:13,margin:"0 0 20px"}}>As a Signature member you receive <span style={{color:G.goldDk,fontWeight:700}}>{disc}% off</span> all add-on services.</p>
            <div style={{display:"flex",gap:8,flexWrap:"wrap",marginBottom:16}}>
              {ACATS.map(c=>(
                <button key={c} onClick={()=>setCat(c)} style={{padding:"7px 14px",borderRadius:2,border:"1px solid "+(cat===c?G.goldDk:G.creamDk),background:cat===c?G.goldPale:"#fff",color:cat===c?G.goldDk:"#888",fontSize:11,fontWeight:700,fontFamily:DP,letterSpacing:1,textTransform:"uppercase",cursor:"pointer"}}>{c}</button>
              ))}
            </div>
            <div style={{marginBottom:16}}>
              {ADDONS.filter(a=>a.cat===cat).map(a=>{
                const isSel=adds.includes(a.id);
                const d=Math.round(a.price*(1-disc/100));
                return (
                  <div key={a.id} onClick={()=>toggle(a.id)} style={{background:isSel?G.creamLt:"#fff",border:"1px solid "+(isSel?G.gold:G.creamDk),borderRadius:3,padding:"14px 18px",marginBottom:8,cursor:"pointer",display:"flex",justifyContent:"space-between",alignItems:"center"}}>
                    <div style={{display:"flex",alignItems:"center",gap:12}}>
                      <div style={{width:22,height:22,borderRadius:2,border:"1.5px solid "+(isSel?G.gold:"#CCC"),background:isSel?G.gold:"transparent",display:"flex",alignItems:"center",justifyContent:"center",flexShrink:0}}>
                        {isSel&&<span style={{color:"#1A1A1A",fontSize:13,fontWeight:900}}>✓</span>}
                      </div>
                      <span style={{color:"#1A1A1A",fontSize:14}}>{a.name}</span>
                    </div>
                    <div style={{textAlign:"right",flexShrink:0,marginLeft:16}}>
                      <span style={{textDecoration:"line-through",color:"#AAA",fontSize:12,marginRight:8}}>{"£"}{a.price}</span>
                      <span style={{color:G.goldDk,fontWeight:700,fontSize:15}}>{"£"}{d}</span>
                    </div>
                  </div>
                );
              })}
            </div>
            {adds.length>0&&(
              <div style={{background:"#fff",border:"1px solid "+G.gold+"55",borderRadius:4,padding:"16px 20px",marginBottom:20}}>
                <div style={{display:"flex",justifyContent:"space-between",alignItems:"center",marginBottom:12}}>
                  <div style={{color:G.goldDk,fontSize:10,letterSpacing:3,textTransform:"uppercase"}}>Selected ({adds.length})</div>
                  <button onClick={()=>setAdds([])} style={{background:"none",border:"1px solid "+G.creamDk,color:"#AAA",borderRadius:2,padding:"3px 10px",cursor:"pointer",fontSize:11}}>Clear all</button>
                </div>
                {ADDONS.filter(a=>adds.includes(a.id)).map(a=>{
                  const d=Math.round(a.price*(1-disc/100));
                  return (
                    <div key={a.id} style={{display:"flex",justifyContent:"space-between",alignItems:"center",marginBottom:8,padding:"7px 0",borderBottom:"1px solid "+G.creamDk}}>
                      <span style={{color:"#555",fontSize:13}}>{a.name}</span>
                      <div style={{display:"flex",alignItems:"center",gap:12}}>
                        <span style={{textDecoration:"line-through",color:"#AAA",fontSize:12}}>{"£"}{a.price}</span>
                        <span style={{color:G.goldDk,fontWeight:700,fontSize:14}}>{"£"}{d}</span>
                        <button onClick={e=>{e.stopPropagation();toggle(a.id);}} style={{background:"none",border:"none",color:"#AAA",cursor:"pointer",fontSize:16,padding:"0 4px"}}>x</button>
                      </div>
                    </div>
                  );
                })}
                <div style={{display:"flex",justifyContent:"space-between",alignItems:"center",paddingTop:10}}>
                  <div style={{color:"#1A1A1A",fontWeight:700,fontSize:15}}>Add-ons total</div>
                  <span style={{color:G.goldDk,fontWeight:700,fontSize:20}}>{"£"}{total}</span>
                </div>
              </div>
            )}
            <div style={{display:"flex",gap:10}}>
              <Btn ghost onClick={()=>setStep(1)}>Back</Btn>
              <div style={{flex:1}}><Btn full onClick={()=>setStep(3)}>{adds.length>0?"Next: Time ("+adds.length+" add-on"+(adds.length>1?"s":"")+")":"Skip Add-ons"}</Btn></div>
            </div>
          </div>
        )}

        {step===3&&(
          <div>
            <h3 style={{fontFamily:SR,color:"#1A1A1A",fontSize:22,fontStyle:"italic",margin:"0 0 6px"}}>Select your time</h3>
            <p style={{color:"#666",fontSize:13,margin:"0 0 24px"}}>Members-only slots reserved exclusively for Healthy Hair Club members.</p>
            <div style={{display:"grid",gridTemplateColumns:"1fr 1fr",gap:10,marginBottom:24}}>
              {SLOTS.map(s=>(
                <div key={s.id} onClick={()=>s.avail&&setSlot(s.id)} style={{background:!s.avail?"#F5F5F5":slot===s.id?G.goldPale:"#fff",border:"1px solid "+(!s.avail?"#E0E0E0":slot===s.id?G.gold:G.creamDk),borderRadius:3,padding:16,cursor:s.avail?"pointer":"not-allowed",opacity:s.avail?1:0.4,textAlign:"center"}}>
                  <div style={{fontSize:12,color:slot===s.id?G.goldDk:"#888",marginBottom:4}}>{s.date}</div>
                  <div style={{fontSize:16,fontWeight:700,fontFamily:DP,color:slot===s.id?G.goldDk:"#1A1A1A"}}>{s.time}</div>
                  {!s.avail&&<div style={{fontSize:10,color:"#AAA",marginTop:4}}>BOOKED</div>}
                </div>
              ))}
            </div>
            <div style={{display:"flex",gap:10}}>
              <Btn ghost onClick={()=>setStep(2)}>Back</Btn>
              <div style={{flex:1}}><Btn full disabled={!slot} onClick={()=>setStep(4)}>Review Booking</Btn></div>
            </div>
          </div>
        )}

        {step===4&&(
          <div>
            <h3 style={{fontFamily:SR,color:"#1A1A1A",fontSize:22,fontStyle:"italic",margin:"0 0 24px"}}>Confirm your booking</h3>
            <div style={{background:"#fff",border:"1px solid "+G.creamDk,borderRadius:4,padding:24,marginBottom:16}}>
              {[["Service",svc],["Date and Time",(SLOTS.find(s=>s.id===slot)||{}).date+" at "+(SLOTS.find(s=>s.id===slot)||{}).time],["Membership","Signature Care"],["Service cost","Included"]].map((row,i)=>(
                <div key={i} style={{display:"flex",justifyContent:"space-between",alignItems:"center",padding:"11px 0",borderBottom:"1px solid "+G.creamDk}}>
                  <span style={{color:"#666",fontSize:13}}>{row[0]}</span>
                  <span style={{color:"#1A1A1A",fontWeight:600,fontSize:14}}>{row[1]}</span>
                </div>
              ))}
              {adds.length>0&&(
                <div style={{padding:"11px 0",borderBottom:"1px solid "+G.creamDk}}>
                  <div style={{color:"#666",fontSize:13,marginBottom:8}}>Add-ons ({adds.length})</div>
                  {ADDONS.filter(a=>adds.includes(a.id)).map(a=>{
                    const d=Math.round(a.price*(1-disc/100));
                    return (
                      <div key={a.id} style={{display:"flex",justifyContent:"space-between",marginBottom:4}}>
                        <span style={{color:"#555",fontSize:13}}>{a.name}</span>
                        <span>
                          <span style={{textDecoration:"line-through",color:"#AAA",marginRight:6,fontSize:13}}>{"£"}{a.price}</span>
                          <span style={{color:G.goldDk,fontWeight:700,fontSize:13}}>{"£"}{d}</span>
                        </span>
                      </div>
                    );
                  })}
                </div>
              )}
              {total>0&&(
                <div style={{display:"flex",justifyContent:"space-between",padding:"14px 0"}}>
                  <span style={{color:"#1A1A1A",fontWeight:700,fontSize:15}}>Add-ons total</span>
                  <span style={{color:G.goldDk,fontWeight:700,fontSize:18}}>{"£"}{total}</span>
                </div>
              )}
            </div>
            <div style={{background:G.creamLt,borderRadius:3,padding:14,marginBottom:20,border:"1px solid "+G.creamDk}}>
              <p style={{fontSize:12,color:"#666",margin:0,lineHeight:1.7}}>Your appointment will be confirmed by Christine once booked.</p>
            </div>
            <div style={{display:"flex",gap:10}}>
              <Btn ghost onClick={()=>setStep(3)}>Back</Btn>
              <div style={{flex:1}}><Btn full onClick={()=>setStep(5)}>Confirm Booking</Btn></div>
            </div>
          </div>
        )}

        {step===5&&(
          <div style={{textAlign:"center",paddingTop:32}}>
            <div style={{width:72,height:72,borderRadius:"50%",border:"2px solid "+G.gold,margin:"0 auto 24px",display:"flex",alignItems:"center",justifyContent:"center"}}>
              <span style={{color:G.gold,fontSize:28}}>✦</span>
            </div>
            <div style={{color:G.goldDk,fontSize:10,letterSpacing:4,textTransform:"uppercase",marginBottom:12}}>Booking Requested</div>
            <h3 style={{fontFamily:SR,color:"#1A1A1A",fontSize:26,fontWeight:400,fontStyle:"italic",margin:"0 0 12px"}}>You are all set, Aisha</h3>
            <p style={{color:"#666",fontSize:14,lineHeight:1.8,maxWidth:360,margin:"0 auto 32px"}}>Christine will confirm your appointment shortly.</p>
            <Btn onClick={onBack}>Back to Dashboard</Btn>
          </div>
        )}
      </div>
      {chat?<Bot onClose={()=>setChat(false)}/>:<BotBtn onClick={()=>setChat(true)}/>}
    </div>
  );
}

function MemberDetail({member,onBack,onLogout}) {
  const [noteVal,setNoteVal]=useState(member.notes||"");
  const [saved,setSaved]=useState(false);
  const [vOpen,setVOpen]=useState(null);
  const [logOpen,setLogOpen]=useState(false);
  const [data,setData]=useState(member);
  const [nv,setNv]=useState({date:"",service:"",treatments:[],note:""});

  function saveNote(){setData(p=>({...p,notes:noteVal}));setSaved(true);setTimeout(()=>setSaved(false),2500);}
  function addVisit(){if(!nv.date||!nv.service)return;setData(p=>({...p,visits:[{...nv},...(p.visits||[])]}));setNv({date:"",service:"",treatments:[],note:""});setLogOpen(false);}
  function togT(name){setNv(p=>({...p,treatments:p.treatments.includes(name)?p.treatments.filter(t=>t!==name):[...p.treatments,name]}));}

  return (
    <div style={{minHeight:"100vh",background:G.cream,fontFamily:BD}}>
      <div style={{background:"#fff",borderBottom:"1px solid "+G.creamDk,padding:"14px 20px",display:"flex",alignItems:"center",gap:14}}>
        <button onClick={onBack} style={{background:G.creamLt,border:"1px solid "+G.creamDk,borderRadius:8,padding:"8px 16px",cursor:"pointer",fontSize:13,color:G.goldDk,fontWeight:700,fontFamily:BD}}>Members</button>
        <Logo light={false} sz={22}/>
        <button onClick={onLogout} style={{marginLeft:"auto",background:G.creamLt,border:"1px solid "+G.creamDk,borderRadius:8,padding:"8px 14px",cursor:"pointer",fontSize:12,color:"#888"}}>Sign Out</button>
      </div>
      <div style={{maxWidth:760,margin:"0 auto",padding:"24px 16px 80px"}}>

        <div style={{background:"linear-gradient(135deg,"+G.goldDk+","+G.gold+")",borderRadius:16,padding:"24px 24px 22px",marginBottom:14}}>
          <div style={{display:"flex",justifyContent:"space-between",alignItems:"flex-start",marginBottom:18}}>
            <div style={{display:"flex",gap:16,alignItems:"center"}}>
              <div style={{width:56,height:56,borderRadius:"50%",background:"rgba(255,255,255,0.2)",border:"2px solid rgba(255,255,255,0.5)",display:"flex",alignItems:"center",justifyContent:"center",color:"#fff",fontWeight:700,fontSize:24,flexShrink:0}}>{data.name[0]}</div>
              <div>
                <div style={{fontFamily:SR,color:"#fff",fontSize:22,fontStyle:"italic",marginBottom:6}}>{data.name}</div>
                <div style={{display:"flex",gap:8}}><PkgTag p={data.pkg}/><Pill s={data.status}/></div>
              </div>
            </div>
            <div style={{textAlign:"right"}}>
              <div style={{color:"rgba(255,255,255,0.65)",fontSize:11,marginBottom:3}}>Member since</div>
              <div style={{color:"#fff",fontWeight:700,fontSize:14}}>{data.joined}</div>
            </div>
          </div>
          <div style={{display:"grid",gridTemplateColumns:"1fr 1fr 1fr",background:"rgba(255,255,255,0.12)",borderRadius:10,overflow:"hidden"}}>
            {[["Email",data.email],["Phone",data.phone],["Next Payment",data.next]].map((f,i)=>(
              <div key={f[0]} style={{padding:"12px 14px",borderRight:i<2?"1px solid rgba(255,255,255,0.15)":"none"}}>
                <div style={{color:"rgba(255,255,255,0.6)",fontSize:10,letterSpacing:1.5,textTransform:"uppercase",marginBottom:4}}>{f[0]}</div>
                <div style={{color:"#fff",fontSize:13,fontWeight:600,wordBreak:"break-all"}}>{f[1]}</div>
              </div>
            ))}
          </div>
          {data.pkg!=="essential"&&(
            <div style={{marginTop:14}}>
              <div style={{display:"flex",justifyContent:"space-between",marginBottom:5}}>
                <span style={{color:"rgba(255,255,255,0.7)",fontSize:11}}>Monthly sessions</span>
                <span style={{color:"#fff",fontSize:11,fontWeight:700}}>{data.used}/{data.total} used</span>
              </div>
              <div style={{height:5,background:"rgba(255,255,255,0.25)",borderRadius:4}}>
                <div style={{height:5,background:"#fff",borderRadius:4,width:(data.total>0?(data.used/data.total)*100:0)+"%"}}/>
              </div>
            </div>
          )}
        </div>

        {data.status==="payment_failed"&&(
          <div style={{background:G.errBg,border:"1px solid #FFCDD2",borderRadius:12,padding:18,marginBottom:14}}>
            <div style={{fontWeight:700,color:G.err,fontSize:14,marginBottom:6}}>Payment Failed — Booking Blocked</div>
            <p style={{color:G.err,fontSize:13,margin:"0 0 12px",lineHeight:1.65}}>Booking access is automatically blocked. A reminder has been sent.</p>
            <Btn danger sm>Send Another Reminder</Btn>
          </div>
        )}

        <div style={{background:"#fff",borderRadius:14,padding:20,marginBottom:14,border:"1px solid "+G.creamDk}}>
          <div style={{color:G.goldDk,fontSize:10,letterSpacing:2.5,textTransform:"uppercase",fontWeight:700,marginBottom:14}}>Manage Membership</div>
          <div style={{display:"grid",gridTemplateColumns:"1fr 1fr",gap:8}}>
            {[{l:"Mark as Active",bg:G.okBg,c:G.ok},{l:"Pause Membership",bg:G.warnBg,c:G.warn},{l:"Cancel Membership",bg:G.errBg,c:G.err},{l:"Change Package",bg:G.goldPale,c:G.goldDk}].map(a=>(
              <button key={a.l} style={{background:a.bg,color:a.c,border:"none",borderRadius:8,padding:"13px 14px",textAlign:"left",cursor:"pointer",fontSize:13,fontWeight:700,fontFamily:BD}}>{a.l}</button>
            ))}
          </div>
        </div>

        <div style={{background:"#fff",borderRadius:14,padding:22,marginBottom:14,border:"1px solid "+G.creamDk}}>
          <div style={{display:"flex",justifyContent:"space-between",alignItems:"center",marginBottom:12}}>
            <div>
              <div style={{color:G.goldDk,fontSize:10,letterSpacing:2.5,textTransform:"uppercase",fontWeight:700,marginBottom:2}}>Client Notes</div>
              <div style={{color:"#AAA",fontSize:12}}>Update anytime, after every appointment</div>
            </div>
            {saved&&<span style={{color:G.ok,fontSize:12,fontWeight:700,background:G.okBg,padding:"4px 12px",borderRadius:20}}>Saved</span>}
          </div>
          <textarea value={noteVal} onChange={e=>{setNoteVal(e.target.value);setSaved(false);}} placeholder="Notes about this client..." style={{width:"100%",padding:"13px 14px",background:G.creamLt,border:"1px solid "+G.creamDk,borderRadius:10,fontSize:13,fontFamily:BD,resize:"none",minHeight:100,boxSizing:"border-box",color:"#1A1A1A",lineHeight:1.75,outline:"none"}}/>
          <div style={{marginTop:10,display:"flex",gap:10,alignItems:"center"}}>
            <Btn sm onClick={saveNote}>Save Notes</Btn>
            <span style={{color:"#AAA",fontSize:12}}>Saved to this profile</span>
          </div>
        </div>

        <div style={{background:"#fff",borderRadius:14,overflow:"hidden",marginBottom:14,border:"1px solid "+G.creamDk}}>
          <div style={{padding:"18px 22px",display:"flex",justifyContent:"space-between",alignItems:"center",borderBottom:"1px solid #F5F3EE"}}>
            <div>
              <div style={{color:G.goldDk,fontSize:10,letterSpacing:2.5,textTransform:"uppercase",fontWeight:700,marginBottom:2}}>Visit History</div>
              <div style={{color:"#AAA",fontSize:12}}>{(data.visits||[]).length} visit{(data.visits||[]).length!==1?"s":""} recorded</div>
            </div>
            <button onClick={()=>setLogOpen(!logOpen)} style={{background:"linear-gradient(135deg,"+G.goldLt+","+G.gold+")",border:"none",borderRadius:8,padding:"9px 18px",cursor:"pointer",fontSize:12,fontWeight:700,fontFamily:DP,letterSpacing:1,textTransform:"uppercase",color:"#1A1A1A"}}>{logOpen?"Cancel":"+ Log Visit"}</button>
          </div>

          {logOpen&&(
            <div style={{padding:"20px 22px",background:G.creamLt,borderBottom:"1px solid "+G.creamDk}}>
              <div style={{color:G.goldDk,fontSize:10,letterSpacing:2,textTransform:"uppercase",fontWeight:700,marginBottom:16}}>Log New Visit</div>
              <div style={{display:"grid",gridTemplateColumns:"1fr 1fr",gap:12,marginBottom:14}}>
                <div>
                  <div style={{fontSize:11,color:"#888",fontWeight:700,letterSpacing:1.5,textTransform:"uppercase",marginBottom:6}}>Date</div>
                  <input type="date" value={nv.date} onChange={e=>setNv(p=>({...p,date:e.target.value}))} style={{width:"100%",padding:"11px 12px",background:"#fff",border:"1px solid #DDD8CE",borderRadius:8,fontSize:13,fontFamily:BD,boxSizing:"border-box"}}/>
                </div>
                <div>
                  <div style={{fontSize:11,color:"#888",fontWeight:700,letterSpacing:1.5,textTransform:"uppercase",marginBottom:6}}>Service</div>
                  <select value={nv.service} onChange={e=>setNv(p=>({...p,service:e.target.value}))} style={{width:"100%",padding:"11px 12px",background:"#fff",border:"1px solid #DDD8CE",borderRadius:8,fontSize:13,fontFamily:BD}}>
                    <option value="">Select service...</option>
                    {(SVCMAP[member.pkg]||SVCMAP.essential).map(s=><option key={s} value={s}>{s}</option>)}
                  </select>
                </div>
              </div>
              <div style={{marginBottom:14}}>
                <div style={{fontSize:11,color:"#888",fontWeight:700,letterSpacing:1.5,textTransform:"uppercase",marginBottom:8}}>Treatments Applied</div>
                <div style={{display:"grid",gridTemplateColumns:"1fr 1fr",gap:8}}>
                  {TREATS.map((t,i)=>{
                    const checked=nv.treatments.includes(t.name);
                    return (
                      <label key={i} style={{display:"flex",gap:10,alignItems:"flex-start",cursor:"pointer",background:checked?G.goldPale:"#fff",borderRadius:8,padding:"10px 12px",border:"1px solid "+(checked?G.gold:G.creamDk)}}>
                        <input type="checkbox" checked={checked} onChange={()=>togT(t.name)} style={{marginTop:2,flexShrink:0,accentColor:G.gold}}/>
                        <div>
                          <div style={{fontWeight:700,color:"#1A1A1A",fontSize:12}}>{t.icon} {t.name}</div>
                          <div style={{color:"#AAA",fontSize:11,marginTop:1}}>{t.tag}</div>
                        </div>
                      </label>
                    );
                  })}
                </div>
              </div>
              <div style={{marginBottom:16}}>
                <div style={{fontSize:11,color:"#888",fontWeight:700,letterSpacing:1.5,textTransform:"uppercase",marginBottom:6}}>Notes</div>
                <textarea value={nv.note} onChange={e=>setNv(p=>({...p,note:e.target.value}))} placeholder="e.g. Applied Olaplex. Hair responded well. Recommend K18 next visit." style={{width:"100%",padding:"12px 14px",background:"#fff",border:"1px solid #DDD8CE",borderRadius:8,fontSize:13,fontFamily:BD,resize:"none",minHeight:80,boxSizing:"border-box",color:"#1A1A1A",lineHeight:1.7}}/>
              </div>
              <Btn onClick={addVisit}>Save Visit Record</Btn>
            </div>
          )}

          {(data.visits||[]).length===0&&(
            <div style={{padding:"36px",textAlign:"center",color:"#AAA",fontSize:13,fontStyle:"italic"}}>No visits recorded yet. Tap Log Visit to add the first one.</div>
          )}

          {(data.visits||[]).map((v,i,arr)=>(
            <div key={i} style={{borderBottom:i<arr.length-1?"1px solid #F5F3EE":"none"}}>
              <div onClick={()=>setVOpen(vOpen===i?null:i)} style={{display:"flex",justifyContent:"space-between",alignItems:"center",padding:"15px 22px",cursor:"pointer",background:vOpen===i?G.creamLt:"#fff"}}>
                <div style={{display:"flex",gap:14,alignItems:"center"}}>
                  <div style={{width:40,height:40,borderRadius:10,background:vOpen===i?G.goldPale:"#F7F3EC",display:"flex",alignItems:"center",justifyContent:"center",flexShrink:0,fontSize:18}}>📋</div>
                  <div>
                    <div style={{fontWeight:700,color:"#1A1A1A",fontSize:14}}>{v.service}</div>
                    <div style={{color:"#888",fontSize:12,marginTop:1}}>{v.date}</div>
                  </div>
                </div>
                <div style={{display:"flex",gap:8,alignItems:"center"}}>
                  {(v.treatments||[]).length>0&&<span style={{background:G.goldPale,color:G.goldDk,fontSize:11,fontWeight:600,padding:"3px 10px",borderRadius:20}}>{v.treatments.length} treatment{v.treatments.length>1?"s":""}</span>}
                  <span style={{color:vOpen===i?G.goldDk:"#CCC",fontSize:20,display:"inline-block",transform:vOpen===i?"rotate(90deg)":"none",transition:"transform 0.2s"}}>{">"}</span>
                </div>
              </div>
              {vOpen===i&&(
                <div style={{padding:"4px 22px 20px",background:G.creamLt,borderTop:"1px solid #F5F3EE"}}>
                  {(v.treatments||[]).length>0&&(
                    <div style={{marginTop:14,marginBottom:14}}>
                      <div style={{fontSize:11,color:"#AAA",fontWeight:700,letterSpacing:1.5,textTransform:"uppercase",marginBottom:8}}>Treatments Applied</div>
                      <div style={{display:"flex",gap:8,flexWrap:"wrap"}}>
                        {v.treatments.map((t,ti)=>{
                          const td=TREATS.find(tr=>tr.name===t);
                          return <span key={ti} style={{background:"#fff",border:"1px solid "+G.creamDk,borderRadius:20,padding:"5px 13px",fontSize:12,fontWeight:600,color:"#333",display:"flex",alignItems:"center",gap:6}}><span>{td?td.icon:""}</span> {t}</span>;
                        })}
                      </div>
                    </div>
                  )}
                  {v.note&&(
                    <div>
                      <div style={{fontSize:11,color:"#AAA",fontWeight:700,letterSpacing:1.5,textTransform:"uppercase",marginBottom:8}}>Notes</div>
                      <div style={{background:"#fff",borderRadius:10,padding:"13px 16px",border:"1px solid "+G.creamDk,color:"#444",fontSize:13,lineHeight:1.8}}>{v.note}</div>
                    </div>
                  )}
                </div>
              )}
            </div>
          ))}
        </div>

        <div style={{background:"#fff",borderRadius:14,padding:22,border:"1px solid "+G.creamDk}}>
          <div style={{color:G.goldDk,fontSize:10,letterSpacing:2.5,textTransform:"uppercase",fontWeight:700,marginBottom:4}}>Next Visit Planner</div>
          <p style={{color:"#888",fontSize:12,margin:"0 0 14px",lineHeight:1.65}}>Tick treatments to consider at the next appointment.</p>
          {data.visits&&data.visits.length>0&&data.visits[0].note&&(
            <div style={{background:G.creamLt,borderRadius:10,padding:"12px 16px",border:"1px solid "+G.creamDk,marginBottom:14}}>
              <div style={{fontSize:11,color:"#AAA",fontWeight:700,letterSpacing:1,textTransform:"uppercase",marginBottom:6}}>Last Visit Note</div>
              <div style={{color:"#555",fontSize:13,lineHeight:1.7,fontStyle:"italic"}}>"{data.visits[0].note}"</div>
            </div>
          )}
          <div style={{display:"grid",gridTemplateColumns:"1fr 1fr",gap:8}}>
            {TREATS.map((t,i)=>(
              <label key={i} style={{display:"flex",gap:10,alignItems:"flex-start",cursor:"pointer",background:G.creamLt,borderRadius:8,padding:"10px 12px",border:"1px solid "+G.creamDk}}>
                <input type="checkbox" style={{marginTop:2,flexShrink:0,accentColor:G.gold}}/>
                <div>
                  <div style={{fontWeight:700,color:"#1A1A1A",fontSize:12}}>{t.icon} {t.name}</div>
                  <div style={{color:"#AAA",fontSize:11,marginTop:1}}>{t.tag}</div>
                </div>
              </label>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

function AdminLogin({onLogin}) {
  return (
    <div style={{minHeight:"100vh",position:"relative",fontFamily:BD,overflow:"hidden"}}>
      <img src={SALON_INTERIOR} alt="salon" style={{position:"absolute",inset:0,width:"100%",height:"100%",objectFit:"cover"}}/>
      <div style={{position:"absolute",inset:0,background:"rgba(0,0,0,0.88)"}}/>
      <div style={{position:"absolute",top:0,left:0,right:0,height:2,background:"linear-gradient(90deg,transparent,"+G.gold+",transparent)"}}/>
      <div style={{position:"relative",zIndex:1,minHeight:"100vh",display:"flex",flexDirection:"column",alignItems:"center",justifyContent:"center",padding:24}}>
        <div style={{textAlign:"center",marginBottom:36}}>
          <Logo light sz={28}/>
          <p style={{color:G.dim,fontSize:12,marginTop:12,letterSpacing:2,textTransform:"uppercase"}}>Admin Portal</p>
        </div>
        <div style={{background:G.charcoal,borderRadius:4,padding:36,width:"100%",maxWidth:380,border:"1px solid "+G.muted,boxShadow:"0 32px 80px rgba(0,0,0,0.7)"}}>
          <h3 style={{fontFamily:SR,color:G.white,fontSize:22,fontStyle:"italic",margin:"0 0 24px"}}>Christine Walker</h3>
          {["Email","Password"].map(label=>(
            <div key={label} style={{marginBottom:16}}>
              <div style={{fontSize:10,color:G.silver,fontWeight:700,letterSpacing:2,textTransform:"uppercase",marginBottom:6}}>{label}</div>
              <input type={label==="Password"?"password":"email"} defaultValue={label==="Email"?"christine@chris2styles.com":"password"} style={{width:"100%",padding:"13px 16px",background:G.graphite,border:"1px solid "+G.muted,borderRadius:3,boxSizing:"border-box",color:G.white,fontSize:14,fontFamily:BD,outline:"none"}}/>
            </div>
          ))}
          <div style={{marginTop:8}}><Btn full onClick={onLogin}>Sign In to Admin</Btn></div>
        </div>
      </div>
    </div>
  );
}

function AdminDashboard({onLogout}) {
  const [tab,setTab]=useState("overview");
  const [sel,setSel]=useState(null);
  const [filt,setFilt]=useState("all");
  const [openSec,setOpenSec]=useState(null);
  const [adds,setAdds]=useState(ADDONS);
  const [newA,setNewA]=useState({name:"",price:"",cat:ACATS[0]});
  const [aCat,setACat]=useState(ACATS[0]);
  const [inbox,setInbox]=useState([
    {id:1,client:"Monique James",type:"message",msg:"Hi Christine, I had a payment issue — is my membership still active?",time:"Today 9:42am",read:false},
    {id:2,client:"Priya Patel",type:"callback",msg:"Requested a callback about pausing her membership.",time:"Today 8:15am",read:false},
    {id:3,client:"Zoe Williams",type:"stylist question",msg:"Is a deep conditioning treatment suitable for fine hair?",time:"Yesterday 6:30pm",read:true},
  ]);
  const [replyT,setReplyT]=useState({});
  const [slots,setSlots]=useState([
    {id:1,sId:"s1",date:"2025-06-16",time:"09:00",dur:60,vip:true,booked:false},
    {id:2,sId:"s1",date:"2025-06-16",time:"10:00",dur:90,vip:true,booked:true},
    {id:3,sId:"s2",date:"2025-06-16",time:"09:30",dur:60,vip:true,booked:false},
    {id:4,sId:"s1",date:"2025-06-17",time:"10:00",dur:120,vip:true,booked:false},
  ]);
  const [nSlot,setNSlot]=useState({date:"",time:"",dur:60,vip:true,sId:"s1"});
  const stylists=[{id:"s1",name:"Christine",color:G.gold},{id:"s2",name:"Stylist 2",color:"#7EC8C8"}];
  const [selSt,setSelSt]=useState("all");

  const active=MEMBERS.filter(m=>m.status==="active").length;
  const failed=MEMBERS.filter(m=>m.status==="payment_failed").length;
  const paused=MEMBERS.filter(m=>m.status==="paused").length;
  const revenue=MEMBERS.filter(m=>m.status==="active").reduce((s,m)=>{const p=PKGS.find(pk=>pk.id===m.pkg);return s+(p?p.price:0);},0);
  const unread=inbox.filter(m=>!m.read).length;
  const filtered=filt==="all"?MEMBERS:MEMBERS.filter(m=>m.status===filt);

  function Card({id,icon,title,sub,children}) {
    const open=openSec===id;
    return (
      <div style={{background:"#FFF",borderRadius:14,overflow:"hidden",marginBottom:12,boxShadow:"0 2px 10px rgba(0,0,0,0.06)",border:"1px solid "+G.creamDk}}>
        <div onClick={()=>setOpenSec(open?null:id)} style={{display:"flex",alignItems:"center",justifyContent:"space-between",padding:"17px 20px",cursor:"pointer"}}>
          <div style={{display:"flex",alignItems:"center",gap:14}}>
            <div style={{width:40,height:40,borderRadius:10,background:open?G.goldPale:"#F7F3EC",display:"flex",alignItems:"center",justifyContent:"center",fontSize:20,flexShrink:0}}>{icon}</div>
            <div>
              <span style={{fontWeight:700,fontSize:15,color:"#1A1A1A"}}>{title}</span>
              {sub&&<div style={{fontSize:12,color:"#999",marginTop:1}}>{sub}</div>}
            </div>
          </div>
          <span style={{color:open?G.goldDk:"#CCC",fontSize:18,display:"inline-block",transform:open?"rotate(90deg)":"none",transition:"transform 0.2s"}}>{">"}</span>
        </div>
        {open&&<div style={{borderTop:"1px solid #F0EBE0"}}>{children}</div>}
      </div>
    );
  }

  if(tab==="members"&&sel) return <MemberDetail member={sel} onBack={()=>setSel(null)} onLogout={onLogout}/>;

  const TABS=[
    {id:"overview",label:"Overview"},
    {id:"members",label:"Members"},
    {id:"bookings",label:"Bookings"},
    {id:"addons",label:"Add-ons"},
    {id:"availability",label:"Availability"},
    {id:"inbox",label:"Messages"+(unread>0?" ("+unread+")":"")},
  ];

  return (
    <div style={{minHeight:"100vh",background:G.cream,fontFamily:BD}}>
      <div style={{background:"#fff",borderBottom:"1px solid "+G.creamDk,padding:"14px 20px",display:"flex",justifyContent:"space-between",alignItems:"center"}}>
        <Logo light={false} sz={24}/>
        <div style={{display:"flex",alignItems:"center",gap:12}}>
          <div style={{textAlign:"right"}}>
            <div style={{fontSize:13,fontWeight:700,color:"#1A1A1A"}}>Christine Walker</div>
            <div style={{fontSize:11,color:G.goldDk,fontWeight:600}}>Salon Owner</div>
          </div>
          <button onClick={onLogout} style={{background:G.creamLt,border:"1px solid "+G.creamDk,borderRadius:8,padding:"7px 14px",cursor:"pointer",fontSize:12,color:"#888"}}>Sign Out</button>
        </div>
      </div>
      <div style={{background:"#fff",borderBottom:"1px solid "+G.creamDk,padding:"0 20px",display:"flex",gap:0,overflowX:"auto"}}>
        {TABS.map(t=>(
          <button key={t.id} onClick={()=>{setTab(t.id);setOpenSec(null);}} style={{background:"none",border:"none",cursor:"pointer",padding:"14px 18px",whiteSpace:"nowrap",fontFamily:BD,fontSize:13,fontWeight:tab===t.id?700:500,color:tab===t.id?G.goldDk:"#888",borderBottom:"2px solid "+(tab===t.id?G.gold:"transparent")}}>
            {t.label}
          </button>
        ))}
      </div>

      <div style={{maxWidth:880,margin:"0 auto",padding:"24px 16px 80px"}}>

        {tab==="overview"&&(
          <div>
            <div style={{color:G.goldDk,fontSize:10,letterSpacing:3,textTransform:"uppercase",marginBottom:4}}>Dashboard</div>
            <h2 style={{fontFamily:SR,fontSize:24,color:"#1A1A1A",margin:"0 0 24px",fontStyle:"italic",fontWeight:400}}>Good morning, Christine</h2>
            <div style={{display:"grid",gridTemplateColumns:"repeat(4,1fr)",gap:12,marginBottom:16}}>
              {[{l:"Active Members",v:active,c:G.ok,bg:G.okBg,ic:"✅"},{l:"Monthly Revenue",v:"£"+revenue,c:G.goldDk,bg:G.goldPale,ic:"💷"},{l:"Failed Payment",v:failed,c:G.err,bg:G.errBg,ic:"⚠️"},{l:"Paused",v:paused,c:G.warn,bg:G.warnBg,ic:"⏸"}].map(s=>(
                <div key={s.l} style={{background:s.bg,borderRadius:12,padding:"16px 18px",border:"1px solid "+s.c+"22"}}>
                  <div style={{fontSize:22,marginBottom:6}}>{s.ic}</div>
                  <div style={{fontSize:26,fontWeight:700,color:s.c,fontFamily:DP}}>{s.v}</div>
                  <div style={{fontSize:12,color:"#777",marginTop:2}}>{s.l}</div>
                </div>
              ))}
            </div>
            {failed>0&&(
              <div style={{background:G.errBg,border:"1px solid #FFCDD2",borderRadius:12,padding:"14px 18px",marginBottom:14,display:"flex",alignItems:"center",gap:12}}>
                <span style={{fontSize:20}}>⚠️</span>
                <div style={{flex:1}}>
                  <div style={{fontWeight:700,color:G.err,fontSize:14}}>Payment Alert</div>
                  <div style={{color:G.err,fontSize:13}}>Monique James has a failed payment. Booking access is automatically blocked.</div>
                </div>
                <button onClick={()=>setTab("members")} style={{background:G.err,color:"#fff",border:"none",borderRadius:8,padding:"7px 16px",cursor:"pointer",fontSize:12,fontWeight:700}}>View</button>
              </div>
            )}
            <Card id="upcoming" icon="📅" title="Upcoming Bookings" sub={BKGS.length+" this week"}>
              <div style={{padding:"4px 0 8px"}}>
                {BKGS.map((b,i)=>(
                  <div key={b.id} style={{display:"flex",justifyContent:"space-between",alignItems:"center",padding:"13px 20px",borderBottom:i<BKGS.length-1?"1px solid #F5F3EE":"none"}}>
                    <div style={{display:"flex",gap:12,alignItems:"center"}}>
                      <div style={{width:38,height:38,borderRadius:"50%",background:G.goldPale,border:"1px solid "+G.gold+"44",display:"flex",alignItems:"center",justifyContent:"center",color:G.goldDk,fontWeight:700,fontSize:16,flexShrink:0}}>{b.client[0]}</div>
                      <div>
                        <div style={{fontWeight:700,color:"#1A1A1A",fontSize:14}}>{b.client}</div>
                        <div style={{color:"#888",fontSize:12}}>{b.service} · {b.date} {b.time}</div>
                        {b.addons.length>0&&<div style={{color:G.goldDk,fontSize:11,marginTop:2}}>+ {b.addons.join(", ")}</div>}
                      </div>
                    </div>
                    <div style={{display:"flex",gap:8,alignItems:"center"}}>
                      <PkgTag p={b.pkg}/><Pill s={b.status}/>
                      {b.status==="pending"&&(
                        <div style={{display:"flex",gap:6}}>
                          <button style={{background:G.okBg,color:G.ok,border:"none",borderRadius:6,padding:"5px 12px",cursor:"pointer",fontSize:12,fontWeight:700}}>Approve</button>
                          <button style={{background:G.errBg,color:G.err,border:"none",borderRadius:6,padding:"5px 12px",cursor:"pointer",fontSize:12,fontWeight:700}}>Decline</button>
                        </div>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </Card>
          </div>
        )}

        {tab==="members"&&!sel&&(
          <div>
            <div style={{display:"flex",justifyContent:"space-between",alignItems:"center",marginBottom:16}}>
              <div>
                <div style={{color:G.goldDk,fontSize:10,letterSpacing:3,textTransform:"uppercase",marginBottom:4}}>Directory</div>
                <h2 style={{fontFamily:SR,fontSize:22,color:"#1A1A1A",margin:0,fontStyle:"italic",fontWeight:400}}>Members</h2>
              </div>
              <div style={{display:"flex",gap:6,flexWrap:"wrap"}}>
                {["all","active","payment_failed","paused"].map(f=>(
                  <button key={f} onClick={()=>setFilt(f)} style={{padding:"6px 13px",borderRadius:20,border:"1px solid "+(filt===f?G.gold:"#DDD"),background:filt===f?G.goldPale:"#fff",color:filt===f?G.goldDk:"#888",fontSize:11,fontWeight:700,cursor:"pointer",fontFamily:BD}}>
                    {f==="payment_failed"?"Failed":f==="all"?"All":f.charAt(0).toUpperCase()+f.slice(1)}
                  </button>
                ))}
              </div>
            </div>
            <div style={{display:"flex",flexDirection:"column",gap:10}}>
              {filtered.map(m=>(
                <div key={m.id} onClick={()=>setSel(m)} style={{background:"#fff",borderRadius:12,padding:"16px 18px",display:"flex",alignItems:"center",gap:14,cursor:"pointer",border:"1px solid "+(m.status==="payment_failed"?"#FFCDD2":G.creamDk)}}>
                  <div style={{width:44,height:44,borderRadius:"50%",background:G.goldPale,border:"1px solid "+G.gold+"44",display:"flex",alignItems:"center",justifyContent:"center",color:G.goldDk,fontWeight:700,fontSize:18,flexShrink:0}}>{m.name[0]}</div>
                  <div style={{flex:1}}>
                    <div style={{fontWeight:700,color:"#1A1A1A",fontSize:15,marginBottom:2}}>{m.name}</div>
                    <div style={{color:"#AAA",fontSize:12}}>{m.email} · Joined {m.joined}</div>
                  </div>
                  <div style={{display:"flex",gap:8,alignItems:"center"}}>
                    <PkgTag p={m.pkg}/><Pill s={m.status}/>
                    <span style={{color:"#CCC",fontSize:20}}>{">"}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {tab==="bookings"&&(
          <div>
            <div style={{color:G.goldDk,fontSize:10,letterSpacing:3,textTransform:"uppercase",marginBottom:4}}>Appointments</div>
            <h2 style={{fontFamily:SR,fontSize:22,color:"#1A1A1A",margin:"0 0 20px",fontStyle:"italic",fontWeight:400}}>All Bookings</h2>
            <div style={{display:"flex",flexDirection:"column",gap:10}}>
              {BKGS.map(b=>(
                <div key={b.id} style={{background:"#fff",borderRadius:12,padding:"16px 18px",border:"1px solid "+G.creamDk}}>
                  <div style={{display:"flex",justifyContent:"space-between",alignItems:"flex-start"}}>
                    <div style={{display:"flex",gap:12,alignItems:"center"}}>
                      <div style={{width:42,height:42,borderRadius:"50%",background:G.goldPale,border:"1px solid "+G.gold+"44",display:"flex",alignItems:"center",justifyContent:"center",color:G.goldDk,fontWeight:700,fontSize:17,flexShrink:0}}>{b.client[0]}</div>
                      <div>
                        <div style={{fontWeight:700,color:"#1A1A1A",fontSize:14,marginBottom:2}}>{b.client}</div>
                        <div style={{color:"#888",fontSize:13}}>{b.service}</div>
                        <div style={{color:"#AAA",fontSize:12}}>{b.date} · {b.time}</div>
                        {b.addons.length>0&&<div style={{color:G.goldDk,fontSize:11,marginTop:3,fontWeight:600}}>Add-ons: {b.addons.join(", ")}</div>}
                      </div>
                    </div>
                    <div style={{display:"flex",flexDirection:"column",gap:8,alignItems:"flex-end"}}>
                      <div style={{display:"flex",gap:8}}><PkgTag p={b.pkg}/><Pill s={b.status}/></div>
                      {b.status==="pending"&&(
                        <div style={{display:"flex",gap:8}}>
                          <button style={{background:G.okBg,color:G.ok,border:"none",borderRadius:6,padding:"7px 14px",cursor:"pointer",fontSize:12,fontWeight:700}}>Approve</button>
                          <button style={{background:G.errBg,color:G.err,border:"none",borderRadius:6,padding:"7px 14px",cursor:"pointer",fontSize:12,fontWeight:700}}>Decline</button>
                        </div>
                      )}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {tab==="addons"&&(
          <div>
            <div style={{color:G.goldDk,fontSize:10,letterSpacing:3,textTransform:"uppercase",marginBottom:4}}>Services</div>
            <h2 style={{fontFamily:SR,fontSize:22,color:"#1A1A1A",margin:"0 0 6px",fontStyle:"italic",fontWeight:400}}>Add-on Services</h2>
            <p style={{color:"#888",fontSize:13,margin:"0 0 20px"}}>Discounts calculate automatically.</p>
            <div style={{background:"#fff",borderRadius:14,padding:22,marginBottom:16,border:"1px solid "+G.creamDk}}>
              <div style={{color:G.goldDk,fontSize:10,letterSpacing:2.5,textTransform:"uppercase",fontWeight:700,marginBottom:14}}>Add New Service</div>
              <div style={{display:"grid",gridTemplateColumns:"1fr 1fr 110px auto",gap:10,alignItems:"flex-end"}}>
                <div>
                  <div style={{fontSize:11,color:"#888",fontWeight:700,letterSpacing:1.5,textTransform:"uppercase",marginBottom:6}}>Service Name</div>
                  <input value={newA.name} onChange={e=>setNewA(p=>({...p,name:e.target.value}))} placeholder="e.g. Brazilian Blowout" style={{width:"100%",padding:"11px 14px",background:G.creamLt,border:"1px solid #DDD8CE",borderRadius:8,fontSize:13,fontFamily:BD,boxSizing:"border-box"}}/>
                </div>
                <div>
                  <div style={{fontSize:11,color:"#888",fontWeight:700,letterSpacing:1.5,textTransform:"uppercase",marginBottom:6}}>Category</div>
                  <select value={newA.cat} onChange={e=>setNewA(p=>({...p,cat:e.target.value}))} style={{width:"100%",padding:"11px 12px",background:G.creamLt,border:"1px solid #DDD8CE",borderRadius:8,fontSize:13,fontFamily:BD}}>
                    {ACATS.map(c=><option key={c} value={c}>{c}</option>)}
                  </select>
                </div>
                <div>
                  <div style={{fontSize:11,color:"#888",fontWeight:700,letterSpacing:1.5,textTransform:"uppercase",marginBottom:6}}>Price</div>
                  <input value={newA.price} type="number" onChange={e=>setNewA(p=>({...p,price:e.target.value}))} placeholder="0" style={{width:"100%",padding:"11px 12px",background:G.creamLt,border:"1px solid #DDD8CE",borderRadius:8,fontSize:13,fontFamily:BD,boxSizing:"border-box"}}/>
                </div>
                <Btn sm onClick={()=>{if(newA.name&&newA.price){setAdds(p=>[...p,{id:"c"+Date.now(),cat:newA.cat,name:newA.name,price:Number(newA.price)}]);setNewA({name:"",price:"",cat:ACATS[0]});}}}>Add</Btn>
              </div>
            </div>
            <div style={{display:"flex",gap:8,flexWrap:"wrap",marginBottom:14}}>
              {[...new Set(adds.map(a=>a.cat))].map(c=>(
                <button key={c} onClick={()=>setACat(c)} style={{padding:"7px 14px",borderRadius:20,border:"1px solid "+(aCat===c?G.gold:"#DDD"),background:aCat===c?G.goldPale:"#fff",color:aCat===c?G.goldDk:"#888",fontSize:11,fontWeight:700,cursor:"pointer",fontFamily:BD}}>{c}</button>
              ))}
            </div>
            <div style={{background:"#fff",borderRadius:14,overflow:"hidden",border:"1px solid "+G.creamDk}}>
              <div style={{display:"grid",gridTemplateColumns:"1fr 90px 90px 90px 90px 40px",padding:"10px 18px",background:G.creamLt,borderBottom:"1px solid "+G.creamDk}}>
                {["Service","Full","10%off","15%off","20%off",""].map((h,i)=><span key={i} style={{fontSize:10,color:"#AAA",fontWeight:700,letterSpacing:1.5,textTransform:"uppercase",textAlign:i>0?"right":"left"}}>{h}</span>)}
              </div>
              {adds.filter(a=>a.cat===aCat).map((a,i,arr)=>(
                <div key={a.id} style={{display:"grid",gridTemplateColumns:"1fr 90px 90px 90px 90px 40px",padding:"13px 18px",borderBottom:i<arr.length-1?"1px solid #F5F3EE":"none",alignItems:"center"}}>
                  <span style={{color:"#333",fontSize:14}}>{a.name}</span>
                  <span style={{textAlign:"right",fontWeight:700,color:"#1A1A1A",fontSize:15}}>{"£"}{a.price}</span>
                  <span style={{textAlign:"right",color:"#888",fontSize:13}}>{"£"}{Math.round(a.price*0.9)}</span>
                  <span style={{textAlign:"right",color:G.goldDk,fontSize:13}}>{"£"}{Math.round(a.price*0.85)}</span>
                  <span style={{textAlign:"right",color:G.goldDk,fontWeight:700,fontSize:15}}>{"£"}{Math.round(a.price*0.8)}</span>
                  <button onClick={()=>setAdds(p=>p.filter(x=>x.id!==a.id))} style={{background:"#FFF0F0",border:"1px solid #FFCDD2",color:G.err,borderRadius:6,padding:"4px 8px",cursor:"pointer",fontSize:12}}>x</button>
                </div>
              ))}
            </div>
          </div>
        )}

        {tab==="availability"&&(
          <div>
            <div style={{color:G.goldDk,fontSize:10,letterSpacing:3,textTransform:"uppercase",marginBottom:4}}>Scheduling</div>
            <h2 style={{fontFamily:SR,fontSize:22,color:"#1A1A1A",margin:"0 0 20px",fontStyle:"italic",fontWeight:400}}>Availability</h2>
            <div style={{background:"#fff",borderRadius:14,padding:22,marginBottom:16,border:"1px solid "+G.creamDk}}>
              <div style={{color:G.goldDk,fontSize:10,letterSpacing:2.5,textTransform:"uppercase",fontWeight:700,marginBottom:14}}>Add New Slot</div>
              <div style={{display:"flex",gap:10,flexWrap:"wrap",alignItems:"flex-end"}}>
                <div>
                  <div style={{fontSize:11,color:"#888",fontWeight:700,letterSpacing:1.5,textTransform:"uppercase",marginBottom:6}}>Date</div>
                  <input type="date" value={nSlot.date} onChange={e=>setNSlot(p=>({...p,date:e.target.value}))} style={{padding:"11px 12px",background:G.creamLt,border:"1px solid #DDD8CE",borderRadius:8,fontSize:13,fontFamily:BD}}/>
                </div>
                <div>
                  <div style={{fontSize:11,color:"#888",fontWeight:700,letterSpacing:1.5,textTransform:"uppercase",marginBottom:6}}>Time</div>
                  <input type="time" value={nSlot.time} onChange={e=>setNSlot(p=>({...p,time:e.target.value}))} style={{padding:"11px 12px",background:G.creamLt,border:"1px solid #DDD8CE",borderRadius:8,fontSize:13,fontFamily:BD}}/>
                </div>
                <div>
                  <div style={{fontSize:11,color:"#888",fontWeight:700,letterSpacing:1.5,textTransform:"uppercase",marginBottom:6}}>Duration</div>
                  <select value={nSlot.dur} onChange={e=>setNSlot(p=>({...p,dur:Number(e.target.value)}))} style={{padding:"11px 12px",background:G.creamLt,border:"1px solid #DDD8CE",borderRadius:8,fontSize:13,fontFamily:BD}}>
                    {[30,45,60,75,90,120,150,180].map(d=><option key={d} value={d}>{d} min</option>)}
                  </select>
                </div>
                <div>
                  <div style={{fontSize:11,color:"#888",fontWeight:700,letterSpacing:1.5,textTransform:"uppercase",marginBottom:6}}>Stylist</div>
                  <select value={nSlot.sId} onChange={e=>setNSlot(p=>({...p,sId:e.target.value}))} style={{padding:"11px 12px",background:G.creamLt,border:"1px solid #DDD8CE",borderRadius:8,fontSize:13,fontFamily:BD}}>
                    {stylists.map(s=><option key={s.id} value={s.id}>{s.name}</option>)}
                  </select>
                </div>
                <Btn sm onClick={()=>{if(nSlot.date&&nSlot.time){setSlots(p=>[...p,{id:Date.now(),sId:nSlot.sId,date:nSlot.date,time:nSlot.time,dur:nSlot.dur,vip:nSlot.vip,booked:false}]);setNSlot(p=>({...p,date:"",time:""}));}}}>Add</Btn>
              </div>
            </div>
            <div style={{display:"flex",gap:8,marginBottom:12}}>
              {["all",...stylists.map(s=>s.id)].map(id=>{
                const st=stylists.find(s=>s.id===id);
                return <button key={id} onClick={()=>setSelSt(id)} style={{padding:"6px 14px",borderRadius:20,border:"1px solid "+(selSt===id?(st?st.color:G.gold):"#DDD"),background:selSt===id?G.creamLt:"#fff",color:selSt===id?(st?st.color:G.goldDk):"#888",fontSize:11,fontWeight:700,cursor:"pointer",fontFamily:BD}}>{id==="all"?"All Stylists":(st?st.name:id)}</button>;
              })}
            </div>
            <div style={{background:"#fff",borderRadius:14,overflow:"hidden",border:"1px solid "+G.creamDk}}>
              {slots.filter(s=>selSt==="all"||s.sId===selSt).sort((a,b)=>a.date.localeCompare(b.date)||a.time.localeCompare(b.time)).map((slot,i,arr)=>{
                const st=stylists.find(s=>s.id===slot.sId);
                const tot=Number(slot.time.split(":")[0])*60+Number(slot.time.split(":")[1])+slot.dur;
                const et=String(Math.floor(tot/60)).padStart(2,"0")+":"+String(tot%60).padStart(2,"0");
                return (
                  <div key={slot.id} style={{display:"flex",gap:16,padding:"13px 18px",borderBottom:i<arr.length-1?"1px solid #F5F3EE":"none",alignItems:"center",background:slot.booked?G.creamLt:"#fff"}}>
                    <span style={{color:"#888",fontSize:12,width:70,flexShrink:0}}>{slot.date.slice(5).replace("-","/")}</span>
                    <span style={{fontWeight:700,color:"#1A1A1A",fontSize:13,width:55,flexShrink:0}}>{slot.time}</span>
                    <span style={{color:"#888",fontSize:12,width:110,flexShrink:0}}>{slot.dur}min → {et}</span>
                    <div style={{display:"flex",alignItems:"center",gap:6,width:90,flexShrink:0}}>
                      <div style={{width:7,height:7,borderRadius:"50%",background:st?st.color:G.gold}}/>
                      <span style={{color:"#555",fontSize:12}}>{st?st.name:""}</span>
                    </div>
                    <div onClick={()=>{if(!slot.booked)setSlots(p=>p.map(x=>x.id===slot.id?{...x,vip:!x.vip}:x));}} style={{cursor:slot.booked?"default":"pointer",flexShrink:0}}>
                      <span style={{fontSize:11,fontWeight:700,color:slot.vip?G.goldDk:"#AAA",background:slot.vip?G.goldPale:"#F5F3EE",border:"1px solid "+(slot.vip?G.gold:"#EEE"),padding:"3px 8px",borderRadius:20}}>{slot.vip?"Members":"Open"}</span>
                    </div>
                    <span style={{fontSize:12,fontWeight:700,color:slot.booked?G.err:G.ok,flexShrink:0,width:50}}>{slot.booked?"Booked":"Free"}</span>
                    {!slot.booked?<button onClick={()=>setSlots(p=>p.filter(x=>x.id!==slot.id))} style={{background:"#FFF0F0",color:G.err,border:"none",borderRadius:6,padding:"5px 10px",cursor:"pointer",fontSize:11,fontWeight:700}}>Remove</button>:<span style={{color:"#CCC",fontSize:11}}>Locked</span>}
                  </div>
                );
              })}
            </div>
          </div>
        )}

        {tab==="inbox"&&(
          <div>
            <div style={{color:G.goldDk,fontSize:10,letterSpacing:3,textTransform:"uppercase",marginBottom:4}}>Messages</div>
            <h2 style={{fontFamily:SR,fontSize:22,color:"#1A1A1A",margin:"0 0 20px",fontStyle:"italic",fontWeight:400}}>Client Messages</h2>
            <div style={{display:"flex",flexDirection:"column",gap:12}}>
              {inbox.map(msg=>(
                <div key={msg.id} style={{background:"#fff",borderRadius:14,padding:20,border:"1px solid "+(msg.read?G.creamDk:G.gold+"55"),borderLeft:"4px solid "+(msg.read?G.creamDk:G.gold)}}>
                  <div style={{display:"flex",justifyContent:"space-between",alignItems:"flex-start",marginBottom:12}}>
                    <div style={{display:"flex",gap:10,alignItems:"center"}}>
                      <div style={{width:40,height:40,borderRadius:"50%",background:G.goldPale,border:"1px solid "+G.gold+"44",display:"flex",alignItems:"center",justifyContent:"center",color:G.goldDk,fontWeight:700,fontSize:16}}>{msg.client[0]}</div>
                      <div>
                        <div style={{fontWeight:700,color:"#1A1A1A",fontSize:14}}>{msg.client}</div>
                        <div style={{display:"flex",gap:6,marginTop:3}}>
                          <span style={{background:G.goldPale,color:G.goldDk,fontSize:10,fontWeight:700,padding:"2px 8px",borderRadius:20,textTransform:"uppercase"}}>{msg.type}</span>
                          {!msg.read&&<span style={{background:G.creamLt,color:G.goldDk,fontSize:10,fontWeight:700,padding:"2px 8px",borderRadius:20}}>New</span>}
                        </div>
                      </div>
                    </div>
                    <span style={{color:"#AAA",fontSize:12}}>{msg.time}</span>
                  </div>
                  <p style={{color:"#555",fontSize:13,lineHeight:1.7,margin:"0 0 14px",padding:"12px 14px",background:G.creamLt,borderRadius:8,borderLeft:"2px solid "+G.gold+"44"}}>{msg.msg}</p>
                  <div style={{display:"flex",gap:8,alignItems:"center"}}>
                    <input value={replyT[msg.id]||""} onChange={e=>{const v=e.target.value;setReplyT(p=>({...p,[msg.id]:v}));}} placeholder="Type your reply..." style={{flex:1,padding:"10px 14px",background:G.creamLt,border:"1px solid "+G.creamDk,borderRadius:8,fontSize:13,fontFamily:BD,color:"#1A1A1A",outline:"none"}}/>
                    <Btn sm onClick={()=>{setInbox(p=>p.map(m=>m.id===msg.id?{...m,read:true}:m));setReplyT(p=>({...p,[msg.id]:""}));}}>Send</Btn>
                    {!msg.read&&<button onClick={()=>setInbox(p=>p.map(m=>m.id===msg.id?{...m,read:true}:m))} style={{background:G.creamLt,border:"1px solid "+G.creamDk,borderRadius:8,padding:"9px 14px",cursor:"pointer",color:"#888",fontSize:12}}>Mark read</button>}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default function App() {
  const [view,setView]=useState("home");
  const [cScr,setCS]=useState("login");
  const [aScr,setAS]=useState("login");

  if(view==="client"){
    if(cScr==="login") return <ClientLogin onLogin={()=>setCS("packages")}/>;
    if(cScr==="packages") return <ClientPackages onSelect={async(pkg,email,name)=>{
      try {
        const res = await fetch('/api/create-checkout', {
          method:'POST',
          headers:{'Content-Type':'application/json'},
          body:JSON.stringify({package:pkg, email:email, name:name})
        });
        const data = await res.json();
        if(data.url) { window.location.href = data.url; }
        else { alert('Payment error: ' + (data.error||'Unknown error')); }
      } catch(err) {
        alert('Connection error. Please try again.');
      }
    }}/>;
    if(cScr==="booking") return <ClientBooking onBack={()=>setCS("dashboard")}/>;
    return <ClientDashboard onBook={()=>setCS("booking")} onLogout={()=>{setView("home");setCS("login");}}/>;
  }
  if(view==="admin"){
    if(aScr==="login") return <AdminLogin onLogin={()=>setAS("dashboard")}/>;
    return <AdminDashboard onLogout={()=>{setView("home");setAS("login");}}/>;
  }

  return (
    <div style={{minHeight:"100vh",position:"relative",fontFamily:BD}}>
      <img src={SALON_EXTERIOR} alt="salon" style={{position:"absolute",inset:0,width:"100%",height:"100%",objectFit:"cover"}}/>
      <div style={{position:"absolute",inset:0,background:"linear-gradient(160deg,rgba(0,0,0,0.92),rgba(10,6,0,0.88))"}}/>
      <div style={{position:"absolute",top:0,left:0,right:0,height:2,background:"linear-gradient(90deg,transparent,"+G.gold+",transparent)"}}/>
      <div style={{position:"relative",zIndex:1,minHeight:"100vh",display:"flex",flexDirection:"column",alignItems:"center",justifyContent:"center",padding:24}}>
        <div style={{textAlign:"center",marginBottom:52}}>
          <Logo light sz={32}/>
          <h1 style={{fontFamily:SR,color:G.white,fontSize:30,fontWeight:400,fontStyle:"italic",margin:"28px 0 10px"}}>Healthy Hair Club App</h1>
          <p style={{color:"rgba(255,255,255,0.55)",fontSize:13,maxWidth:340,margin:"0 auto",lineHeight:1.8}}>Prototype — explore the client app and admin dashboard.</p>
        </div>
        <div style={{display:"flex",gap:20,flexWrap:"wrap",justifyContent:"center"}}>
          {[{label:"Client App",sub:"Sign up, membership, booking",icon:"👩🏾",action:()=>setView("client"),light:true},{label:"Admin Dashboard",sub:"Members, bookings, availability",icon:"💼",action:()=>setView("admin"),light:false}].map(card=>(
            <div key={card.label} onClick={card.action} style={{background:card.light?G.gold+"15":G.charcoal,border:"1px solid "+G.gold,borderRadius:4,padding:"32px 28px",width:240,cursor:"pointer",textAlign:"center"}}>
              <div style={{fontSize:42,marginBottom:16}}>{card.icon}</div>
              <div style={{fontFamily:DP,fontWeight:700,fontSize:14,letterSpacing:2,textTransform:"uppercase",color:G.white,marginBottom:10}}>{card.label}</div>
              <div style={{fontSize:12,color:G.silver,lineHeight:1.6,marginBottom:20}}>{card.sub}</div>
              <div style={{background:"linear-gradient(135deg,"+G.goldLt+","+G.gold+")",color:G.black,borderRadius:3,padding:"9px 0",fontFamily:DP,fontWeight:700,fontSize:11,letterSpacing:2,textTransform:"uppercase"}}>Open</div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
"""
c=c[:f1]+good_btn+tail
print("export default:",("export default function App" in c))
print("size:",len(c)//1024,"KB")
print("Btn count:",c.count("function Btn("))
with open("app/HHCApp.jsx","w",encoding="utf-8") as f:
    f.write(c)
print("SAVED!")
