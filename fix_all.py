with open('app/HHCApp.jsx','r',encoding='utf-8') as f:
    c=f.read()

# Add imports at the very top
imports='import React from "react";\nimport { useState } from "react";\nimport LandingPageComp from "./LandingPage.jsx";\n'

# Remove any existing duplicate imports
c=c.replace('import React from "react";\n','')
c=c.replace('import LandingPageComp from "./LandingPage.jsx";\n','')
c=c.replace('import { useState } from "react";\n','',1)

# Add clean imports at top
c=imports+c

print("Imports at top:")
print(c[:200])
print("LandingPageComp in file:",('LandingPageComp' in c))
print("Size:",len(c)//1024,"KB")

with open('app/HHCApp.jsx','w',encoding='utf-8') as f:
    f.write(c)
print("SAVED!")