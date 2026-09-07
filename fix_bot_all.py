with open('app/HHCApp.jsx','r',encoding='utf-8') as f:
    c=f.read()

bot_code='''function BotBtn({onClick}) {
  return (
    <button onClick={onClick} style={{position:"fixed",bottom:20,right:20,zIndex:999,width:56,height:56,borderRadius:"50%",background:"linear-gradient(135deg,#E2C97E,#C9A84C)",border:"none",boxShadow:"0 8px 24px rgba(201,168,76,0.4)",cursor:"pointer",display:"flex",alignItems:"center",justifyContent:"center",flexDirection:"column"}}>
      <span style={{fontSize:20,color:"#1A1A1A"}}>✦</span>
      <span style={{fontSize:8,color:"#1A1A1A",fontWeight:700}}>HELP</span>
    </button>
  );
}

function Bot({onClose}) {
  const [msgs,setMsgs]=React.useState([{r:"bot",t:"Hi! I am your Healthy Hair Club Assistant. Ask me about memberships, treatments, payments or bookings."}]);
  const [inp,setInp]=React.useState("");
  function send(text) {
    if(!text.trim())return;
    setMsgs(p=>[...p,{r:"user",t:text},{r:"bot",t:"Thank you for your message. Please contact the salon directly at 020 3754 7889 or christine.walker@hairdresser.net for personal assistance."}]);
    setInp("");
  }
  return (
    <div style={{position:"fixed",bottom:20,right:20,zIndex:1000,width:320,background:"#111",border:"1px solid #C9A84C55",borderRadius:8,boxShadow:"0 20px 60px rgba(0,0,0,0.7)",display:"flex",flexDirection:"column",maxHeight:"60vh"}}>
      <div style={{padding:"14px 18px",borderBottom:"1px solid #272727",display:"flex",justifyContent:"space-between",alignItems:"center",background:"#1A1A1A",borderRadius:"8px 8px 0 0"}}>
        <div style={{color:"#FFF",fontWeight:700,fontSize:14}}>HHC Assistant</div>
        <button onClick={onClose} style={{background:"none",border:"none",color:"#999",cursor:"pointer",fontSize:18}}>x</button>
      </div>
      <div style={{flex:1,overflowY:"auto",padding:14,display:"flex",flexDirection:"column",gap:10,minHeight:120}}>
        {msgs.map((m,i)=>(
          <div key={i} style={{display:"flex",justifyContent:m.r==="user"?"flex-end":"flex-start"}}>
            <div style={{maxWidth:"88%",padding:"10px 14px",borderRadius:8,background:m.r==="user"?"linear-gradient(135deg,#E2C97E,#C9A84C)":"#272727",color:m.r==="user"?"#1A1A1A":"#CCC",fontSize:13,lineHeight:1.65}}>{m.t}</div>
          </div>
        ))}
      </div>
      <div style={{padding:"10px 14px",borderTop:"1px solid #272727",display:"flex",gap:8}}>
        <input value={inp} onChange={e=>setInp(e.target.value)} onKeyDown={e=>e.key==="Enter"&&send(inp)} placeholder="Ask a question..." style={{flex:1,padding:"10px 12px",background:"#272727",border:"1px solid #3A3A3A",borderRadius:4,color:"#FFF",fontSize:13,outline:"none"}}/>
        <button onClick={()=>send(inp)} style={{background:"linear-gradient(135deg,#E2C97E,#C9A84C)",border:"none",borderRadius:4,padding:"10px 14px",cursor:"pointer",color:"#1A1A1A",fontWeight:700}}>→</button>
      </div>
    </div>
  );
}
'''

# Insert before ClientLogin function
idx=c.find('function ClientLogin(')
if idx>0:
    c=c[:idx]+bot_code+'\n'+c[idx:]
    print("Added Bot and BotBtn before ClientLogin!")
else:
    print("Could not find ClientLogin")

print("BotBtn in file:", 'function BotBtn' in c)
print("Bot in file:", 'function Bot({' in c)
with open('app/HHCApp.jsx','w',encoding='utf-8') as f:
    f.write(c)
print("Saved! Size:",len(c)//1024,"KB")