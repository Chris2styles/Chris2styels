with open('app/HHCApp.jsx','r',encoding='utf-8') as f:
    c=f.read()
if 'import React from' not in c:
    c='import React from "react";\n'+c
    with open('app/HHCApp.jsx','w',encoding='utf-8') as f:
        f.write(c)
    print('Added React import')
else:
    print('Already there')