with open('app/HHCApp.jsx','r',encoding='utf-8') as f:
    c=f.read()

# Find and fix the login routing
old='if(cScr==="login") return <ClientLogin onLogin={(opts)=>setCS(opts&&opts.hasMembership?"dashboard":"packages")}/>;'
new='if(cScr==="login") return <ClientLogin onLogin={()=>setCS("dashboard")}/>;'

if old in c:
    c=c.replace(old,new,1)
    print("Fixed opts version!")
else:
    # Try original
    old2='if(cScr==="login") return <ClientLogin onLogin={()=>setCS("packages")}/>;'
    if old2 in c:
        c=c.replace(old2,new,1)
        print("Fixed original version!")
    else:
        print("Could not find - showing context:")
        idx=c.find('ClientLogin onLogin')
        print(c[idx:idx+100])

with open('app/HHCApp.jsx','w',encoding='utf-8') as f:
    f.write(c)
print("Done!")