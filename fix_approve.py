with open('app/HHCApp.jsx','r',encoding='utf-8') as f:
    c=f.read()

# Fix approve button
old='''                          <button style={{background:G.okBg,color:G.ok,border:"none",borderRadius:6,padding:"5px 12px",cursor:"pointer",fontSize:12,fontWeight:700}}>Approve</button>
                          <button style={{background:G.errBg,color:G.err,border:"none",borderRadius:6,padding:"5px 12px",cursor:"pointer",fontSize:12,fontWeight:700}}>Decline</button>'''

new='''                          <button onClick={async()=>{await supabase.from('bookings').update({status:'confirmed'}).eq('id',b.id);setRealBookings(p=>p.map(x=>x.id===b.id?{...x,status:'confirmed'}:x));}} style={{background:G.okBg,color:G.ok,border:"none",borderRadius:6,padding:"5px 12px",cursor:"pointer",fontSize:12,fontWeight:700}}>Approve</button>
                          <button onClick={async()=>{await supabase.from('bookings').update({status:'cancelled'}).eq('id',b.id);setRealBookings(p=>p.map(x=>x.id===b.id?{...x,status:'cancelled'}:x));}} style={{background:G.errBg,color:G.err,border:"none",borderRadius:6,padding:"5px 12px",cursor:"pointer",fontSize:12,fontWeight:700}}>Decline</button>'''

print("Found overview approve:", old[:50] in c)
c=c.replace(old,new,1)

# Fix bookings tab approve buttons
old2='''                      <button style={{background:G.okBg,color:G.ok,border:"none",borderRadius:6,padding:"7px 14px",cursor:"pointer",fontSize:12,fontWeight:700}}>Approve</button>
                          <button style={{background:G.errBg,color:G.err,border:"none",borderRadius:6,padding:"7px 14px",cursor:"pointer",fontSize:12,fontWeight:700}}>Decline</button>'''

new2='''                      <button onClick={async()=>{await supabase.from('bookings').update({status:'confirmed'}).eq('id',b.id);setRealBookings(p=>p.map(x=>x.id===b.id?{...x,status:'confirmed'}:x));}} style={{background:G.okBg,color:G.ok,border:"none",borderRadius:6,padding:"7px 14px",cursor:"pointer",fontSize:12,fontWeight:700}}>Approve</button>
                          <button onClick={async()=>{await supabase.from('bookings').update({status:'cancelled'}).eq('id',b.id);setRealBookings(p=>p.map(x=>x.id===b.id?{...x,status:'cancelled'}:x));}} style={{background:G.errBg,color:G.err,border:"none",borderRadius:6,padding:"7px 14px",cursor:"pointer",fontSize:12,fontWeight:700}}>Decline</button>'''

print("Found bookings approve:", old2[:50] in c)
c=c.replace(old2,new2,1)

with open('app/HHCApp.jsx','w',encoding='utf-8') as f:
    f.write(c)
print("Done!")