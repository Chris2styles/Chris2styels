with open('app/HHCApp.jsx','r',encoding='utf-8') as f:
    c=f.read()
old='import React from "react";'
new='import React from "react";\nimport LandingPageComp from "./LandingPage.jsx";'
c=c.replace(old,new,1)
with open('app/HHCApp.jsx','w',encoding='utf-8') as f:
    f.write(c)
print("Done! LandingPageComp import added")