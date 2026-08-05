with open('app/HHCApp.jsx','r',encoding='utf-8') as f:
    c=f.read()

old='export default function App() {\n  const [view,setView]=useState("client");'
new='export default function App({startAdmin=false}) {\n  const [view,setView]=useState(startAdmin?"admin":"client");'

c=c.replace(old,new,1)
print("Fixed:",new in c)
with open('app/HHCApp.jsx','w',encoding='utf-8') as f:
    f.write(c)
print("Done!")