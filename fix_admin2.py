with open('app/HHCApp.jsx','r',encoding='utf-8') as f:
    c=f.read()

# Find the loadMembers function and add better error logging
old='''    async function loadMembers(){
      try {
        const {data:clients}=await supabase.from('clients').select('*');
        const {data:memberships}=await supabase.from('memberships').select('*');
        if(clients&&memberships){'''

new='''    async function loadMembers(){
      try {
        const {data:clients,error:e1}=await supabase.from('clients').select('*');
        const {data:memberships,error:e2}=await supabase.from('memberships').select('*');
        console.log('Clients:', clients, 'Error:', e1);
        console.log('Memberships:', memberships, 'Error:', e2);
        if(clients&&memberships){'''

print("Found:", old[:50] in c)
c=c.replace(old,new,1)
with open('app/HHCApp.jsx','w',encoding='utf-8') as f:
    f.write(c)
print("Done!")