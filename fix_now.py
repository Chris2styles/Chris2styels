with open('app/HHCApp.jsx','r',encoding='utf-8') as f:
    c=f.read()
f1=c.find('function Btn({children,onClick,full,ghost,danger,sm,disabled})')
f2=c.find('function Btn({children,onClick,full,ghost,danger,sm,disabled})',f1+10)
tc=c.find('\nfunction TreatCard',f2 if f2>0 else f1)
good='''function Btn({children,onClick,full,ghost,danger,sm,disabled}) {
  const bg=disabled?"#EEE":danger?"#FFF0F0":ghost?"transparent":"linear-gradient(135deg,"+G.goldLt+","+G.gold+")";
  const co=disabled?"#AAA":danger?G.err:ghost?G.goldDk:"#1A1A1A";
  const brd=ghost?"1px solid "+G.gold:danger?"1px solid #FFCDD2":"none";
  return (
    <button onClick={disabled?undefined:onClick}
      style={{width:full?"100%":"auto",padding:sm?"9px 18px":"14px 28px",background:bg,color:co,border:brd,borderRadius:8,fontFamily:DP,fontWeight:700,fontSize:sm?11:13,letterSpacing:1.5,textTransform:"uppercase",cursor:disabled?"not-allowed":"pointer"}}>
      {children}
    </button>
  );
}'''
c=c[:f1]+good+c[tc:]
print("export default:",("export default function App" in c))
print("size:",len(c)//1024,"KB")
print("Btn count:",c.count("function Btn("))
with open('app/HHCApp.jsx','w',encoding='utf-8') as f:
    f.write(c)
print("SAVED!")