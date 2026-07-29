import re

print("Reading app file...")
with open('app/HHCApp.jsx', 'r', encoding='utf-8') as f:
    c = f.read()

# Fix Pill component
old_pill = '''function Pill({s}) {
  const d=SMAP[s]||SMAP.active;
  return React.createElement("span",{style:{background:d.bg,color:d.color,fontSize:11,fontWeight:700,padding:"3px 10px",borderRadius:2,fontFamily:BD}},d.label);
}'''
new_pill = '''function Pill({s}) {
  const d=SMAP[s]||SMAP.active;
  return <span style={{background:d.bg,color:d.color,fontSize:11,fontWeight:700,padding:"3px 10px",borderRadius:2,fontFamily:BD}}>{d.label}</span>;
}'''

# Fix PkgTag component
old_pkg = '''function PkgTag({p}) {
  const c={essential:G.silver,signature:G.gold,elite:G.goldLt}[p]||G.silver;
  return React.createElement("span",{style:{background:G.graphite,color:c,fontSize:11,fontWeight:700,padding:"3px 10px",borderRadius:2,textTransform:"uppercase",fontFamily:BD}},p);
}'''
new_pkg = '''function PkgTag({p}) {
  const c={essential:G.silver,signature:G.gold,elite:G.goldLt}[p]||G.silver;
  return <span style={{background:G.graphite,color:c,fontSize:11,fontWeight:700,padding:"3px 10px",borderRadius:2,textTransform:"uppercase",fontFamily:BD}}>{p}</span>;
}'''

# Fix Logo component
old_logo = '''function Logo({light,sz}) {
  sz=sz||26;
  return React.createElement("div",{style:{display:"flex",alignItems:"center",gap:12}},
    React.createElement("div",{style:{width:sz+4,height:sz+4,borderRadius:"50%",border:"1.5px solid "+G.gold,display:"flex",alignItems:"center",justifyContent:"center"}},
      React.createElement("span",{style:{fontFamily:SR,fontSize:sz*0.56,color:G.gold,fontStyle:"italic"}},"C")
    ),
    React.createElement("div",null,
      React.createElement("div",{style:{fontFamily:DP,fontSize:sz*0.6,color:light?G.white:"#1A1A1A",letterSpacing:2,textTransform:"uppercase",lineHeight:1}},"Chris 2 Styles"),
      React.createElement("div",{style:{fontFamily:BD,fontSize:sz*0.34,color:G.gold,letterSpacing:3,textTransform:"uppercase",marginTop:2}},"Healthy Hair Club")
    )
  );
}'''
new_logo = '''function Logo({light,sz}) {
  sz=sz||26;
  return (
    <div style={{display:"flex",alignItems:"center",gap:12}}>
      <div style={{width:sz+4,height:sz+4,borderRadius:"50%",border:"1.5px solid "+G.gold,display:"flex",alignItems:"center",justifyContent:"center"}}>
        <span style={{fontFamily:SR,fontSize:sz*0.56,color:G.gold,fontStyle:"italic"}}>C</span>
      </div>
      <div>
        <div style={{fontFamily:DP,fontSize:sz*0.6,color:light?G.white:"#1A1A1A",letterSpacing:2,textTransform:"uppercase",lineHeight:1}}>Chris 2 Styles</div>
        <div style={{fontFamily:BD,fontSize:sz*0.34,color:G.gold,letterSpacing:3,textTransform:"uppercase",marginTop:2}}>Healthy Hair Club</div>
      </div>
    </div>
  );
}'''

# Fix Btn component - find and replace entire function
btn_start = c.find("function Btn({children,onClick,full,ghost,danger,sm,disabled})")
btn_end = c.find("\nfunction TreatCard", btn_start)
old_btn = c[btn_start:btn_end]

new_btn = '''function Btn({children,onClick,full,ghost,danger,sm,disabled}) {
  const bg=disabled?"#EEE":danger?"#FFF0F0":ghost?"transparent":"linear-gradient(135deg,"+G.goldLt+","+G.gold+")";
  const co=disabled?"#AAA":danger?G.err:ghost?G.goldDk:"#1A1A1A";
  const brd=ghost?"1px solid "+G.gold:danger?"1px solid #FFCDD2":"none";
  return (
    <button onClick={disabled?undefined:onClick}
      style={{width:full?"100%":"auto",padding:sm?"9px 18px":"14px 28px",
        background:bg,color:co,border:brd,borderRadius:8,
        fontFamily:DP,fontWeight:700,fontSize:sm?11:13,letterSpacing:1.5,
        textTransform:"uppercase",cursor:disabled?"not-allowed":"pointer"}}>
      {children}
    </button>
  );
}'''

print("Fixing Pill:", old_pill[:30] in c)
print("Fixing PkgTag:", old_pkg[:30] in c)
print("Fixing Logo:", old_logo[:30] in c)
print("Fixing Btn:", "React.createElement" in old_btn)

c = c.replace(old_pill, new_pill, 1)
c = c.replace(old_pkg, new_pkg, 1)
c = c.replace(old_logo, new_logo, 1)
c = c[:btn_start] + new_btn + c[btn_end:]

remaining = c.count("React.createElement")
print(f"Remaining React.createElement: {remaining}")

with open('app/HHCApp.jsx', 'w', encoding='utf-8') as f:
    f.write(c)

print("DONE!")
