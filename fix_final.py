with open('app/HHCApp.jsx','r',encoding='utf-8') as f:
    c=f.read()

# Find and fix the duplicate Btn
first=c.find('function Btn({children,onClick,full,ghost,danger,sm,disabled})')
second=c.find('function Btn({children,onClick,full,ghost,danger,sm,disabled})',first+10)
print(f"Btn occurrences - First:{first} Second:{second}")

if second>0:
    # Find end of second Btn function
    end=c.find('\nfunction TreatCard',second)
    good_btn='''function Btn({children,onClick,full,ghost,danger,sm,disabled}) {
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
    c=c[:first]+good_btn+c[end:]
    print("Fixed!")

# Verify
print("export default:",("export default function App" in c))
print("Btn count:",c.count("function Btn("))
print("Size:",len(c)//1024,"KB")

with open('app/HHCApp.jsx','w',encoding='utf-8') as f:
    f.write(c)
print("SAVED!")