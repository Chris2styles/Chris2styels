with open('app/HHCApp.jsx','r',encoding='utf-8') as f:
    c=f.read()

# Replace prototype inbox with empty array
old='  const [inbox,setInbox]=useState(['
end=c.find(']);', c.find('  const [inbox,setInbox]=useState(['))+2

old_full=c[c.find('  const [inbox,setInbox]=useState(['):end]
new_inbox='  const [inbox,setInbox]=useState([]'

print("Found inbox:", '  const [inbox,setInbox]=useState([' in c)
print("Length of old:", len(old_full))

c=c[:c.find('  const [inbox,setInbox]=useState([')]+new_inbox+c[end:]

with open('app/HHCApp.jsx','w',encoding='utf-8') as f:
    f.write(c)
print("Done!")