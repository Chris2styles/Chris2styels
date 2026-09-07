with open('app/HHCApp.jsx','r',encoding='utf-8') as f:
    c=f.read()

if 'function BotBtn' not in c:
    # Add BotBtn before Bot function
    old='function Bot({'
    new='''function BotBtn({onClick}) {
  return (
    <button onClick={onClick} style={{position:"fixed",bottom:20,right:20,zIndex:999,width:56,height:56,borderRadius:"50%",background:"linear-gradient(135deg,#E2C97E,#C9A84C)",border:"none",boxShadow:"0 8px 24px rgba(201,168,76,0.4)",cursor:"pointer",display:"flex",alignItems:"center",justifyContent:"center",flexDirection:"column"}}>
      <span style={{fontSize:20,color:"#1A1A1A"}}>✦</span>
      <span style={{fontSize:8,color:"#1A1A1A",fontWeight:700}}>HELP</span>
    </button>
  );
}

function Bot({'''
    c=c.replace(old,new,1)
    print("Added BotBtn!")
else:
    print("BotBtn already there")

with open('app/HHCApp.jsx','w',encoding='utf-8') as f:
    f.write(c)
print("Done!")