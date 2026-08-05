with open('app/HHCApp.jsx','r',encoding='utf-8') as f:
    c=f.read()

addons_end=c.find('const ADDONS=[')
addons_close=c.find('];',addons_end)+2
insert='\nconst ACATS=[...new Set(ADDONS.map(a=>a.cat))];\n'
c=c[:addons_close]+insert+c[addons_close:]
print("ACATS added:",('const ACATS=' in c))
with open('app/HHCApp.jsx','w',encoding='utf-8') as f:
    f.write(c)
print("Done!")