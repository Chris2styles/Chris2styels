import re

print("Reading app file...")
with open('app/HHCApp.jsx', 'r', encoding='utf-8') as f:
    c = f.read()

print(f"File size: {len(c)//1024}KB")

# Step 1: Add React import if missing
if 'import React from' not in c:
    c = 'import React from "react";\n' + c
    print("✓ Added React import")
else:
    print("✓ React import already there")

# Step 2: Fix React.createElement if any remain
count = c.count('React.createElement')
if count > 0:
    print(f"WARNING: {count} React.createElement calls found - these may cause errors")
else:
    print("✓ No React.createElement calls")

# Step 3: Add showForm state to ClientPackages if missing
if 'showForm' not in c:
    old = "  const [showT,setShowT]=useState(false);\n  if(showT)"
    new = "  const [showT,setShowT]=useState(false);\n  const [showForm,setShowForm]=useState(false);\n  const [name,setName]=useState('');\n  const [email,setEmail]=useState('');\n  if(showT)"
    if old in c:
        c = c.replace(old, new, 1)
        print("✓ Added showForm state")
    else:
        print("WARNING: Could not find state location")
else:
    print("✓ showForm already there")

# Step 4: Fix the payment button if missing
if 'Pay Now with Stripe' not in c:
    old_btn = """        {sel&&(
          <div style={{textAlign:"center"}}>
            <Btn onClick={()=>onSelect(sel)}>Continue to Payment</Btn>"""
    new_btn = """        {sel&&(
          <div style={{textAlign:"center"}}>
            {!showForm?(
              <Btn onClick={()=>setShowForm(true)}>Continue to Payment</Btn>
            ):(
              <div style={{background:"#111",borderRadius:8,padding:24,maxWidth:380,margin:"0 auto",textAlign:"left"}}>
                <div style={{color:"#C9A84C",fontSize:12,fontWeight:700,letterSpacing:2,textTransform:"uppercase",marginBottom:16}}>Your Details</div>
                <div style={{marginBottom:14}}>
                  <div style={{color:"#999",fontSize:11,fontWeight:700,letterSpacing:1.5,textTransform:"uppercase",marginBottom:6}}>Full Name</div>
                  <input value={name} onChange={e=>setName(e.target.value)} placeholder="Your full name" style={{width:"100%",padding:"12px 14px",background:"#272727",border:"1px solid #3A3A3A",borderRadius:4,color:"#FFF",fontSize:14,outline:"none",boxSizing:"border-box"}}/>
                </div>
                <div style={{marginBottom:20}}>
                  <div style={{color:"#999",fontSize:11,fontWeight:700,letterSpacing:1.5,textTransform:"uppercase",marginBottom:6}}>Email Address</div>
                  <input value={email} onChange={e=>setEmail(e.target.value)} placeholder="your@email.com" type="email" style={{width:"100%",padding:"12px 14px",background:"#272727",border:"1px solid #3A3A3A",borderRadius:4,color:"#FFF",fontSize:14,outline:"none",boxSizing:"border-box"}}/>
                </div>
                <button disabled={!name||!email} onClick={()=>onSelect(sel,email,name)} style={{width:"100%",padding:"14px 0",background:(!name||!email)?"#EEE":"linear-gradient(135deg,#E2C97E,#C9A84C)",color:(!name||!email)?"#AAA":"#1A1A1A",border:"none",borderRadius:8,fontWeight:700,fontSize:13,letterSpacing:1.5,textTransform:"uppercase",cursor:(!name||!email)?"not-allowed":"pointer"}}>Pay Now with Stripe</button>
              </div>
            )}"""
    if old_btn in c:
        c = c.replace(old_btn, new_btn, 1)
        print("✓ Added payment form")
    else:
        print("WARNING: Could not find button location")
else:
    print("✓ Payment button already there")

# Step 5: Fix App onSelect to call Stripe API
old_select = 'if(cScr==="packages") return <ClientPackages onSelect={()=>setCS("dashboard")}/>;'
new_select = '''if(cScr==="packages") return <ClientPackages onSelect={async(pkg,email,name)=>{
    try{
      const res=await fetch('/api/create-checkout',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({package:pkg,email:email,name:name})});
      const data=await res.json();
      if(data.url){window.location.href=data.url;}
      else{alert('Payment error: '+(data.error||'Unknown'));}
    }catch(err){alert('Connection error. Please try again.');}
  }}/>;'''

if 'create-checkout' not in c:
    if old_select in c:
        c = c.replace(old_select, new_select, 1)
        print("✓ Added Stripe API call")
    else:
        print("WARNING: Could not find onSelect location")
else:
    print("✓ Stripe API call already there")

# Step 6: Update prices
old_start = c.find('const ADDONS=[')
old_end = c.find('];', old_start) + 2
new_addons = '''const ADDONS=[
  {id:"a1",cat:"Styling Extras",name:"Silk Press",price:55},
  {id:"a2",cat:"Styling Extras",name:"Wash and Silk Press",price:74.50},
  {id:"a3",cat:"Styling Extras",name:"Wash Silk Press and Trim",price:92.50},
  {id:"a4",cat:"Styling Extras",name:"Blow Dry",price:15},
  {id:"a5",cat:"Styling Extras",name:"Wash and Roller Set",price:50},
  {id:"a6",cat:"Styling Extras",name:"Wash and Tong",price:45},
  {id:"a7",cat:"Styling Extras",name:"Silk Press and Semi Permanent Colour",price:110.50},
  {id:"a8",cat:"Styling Extras",name:"Silk Press and Treatment",price:110.50},
  {id:"a9",cat:"Styling Extras",name:"Silk Press Semi Permanent Colour Treatment and Trim",price:174.50},
  {id:"a10",cat:"Styling Extras",name:"Frytong",price:35},
  {id:"a11",cat:"Styling Extras",name:"Dry Styling",price:40},
  {id:"a12",cat:"Styling Extras",name:"Wash Cut and Style",price:65},
  {id:"a13",cat:"Styling Extras",name:"Dry Cut",price:37.50},
  {id:"a14",cat:"Styling Extras",name:"Fringe Trim",price:10},
  {id:"a15",cat:"Styling Extras",name:"Cut Ends 1-3 Inches",price:30},
  {id:"b1",cat:"Colour and Toning",name:"Permanent Colour with Blow Dry Short Hair",price:75},
  {id:"b2",cat:"Colour and Toning",name:"Permanent Colour with Blow Dry Medium Hair",price:95},
  {id:"b3",cat:"Colour and Toning",name:"Permanent Colour with Blow Dry Long Hair",price:130},
  {id:"b4",cat:"Colour and Toning",name:"Hairline Semi Permanent Colour",price:55},
  {id:"b5",cat:"Colour and Toning",name:"Half Head Highlights Short Hair",price:70},
  {id:"b6",cat:"Colour and Toning",name:"Half Head Highlights Medium Hair",price:85},
  {id:"b7",cat:"Colour and Toning",name:"Half Head Highlights Long Hair",price:95},
  {id:"b8",cat:"Colour and Toning",name:"Half Head Highlights with Cut",price:100},
  {id:"b9",cat:"Colour and Toning",name:"Ombre Colour Short Hair",price:45},
  {id:"b10",cat:"Colour and Toning",name:"Ombre Colour Medium Hair",price:55},
  {id:"b11",cat:"Colour and Toning",name:"Ombre Colour Long Hair",price:65},
  {id:"b12",cat:"Colour and Toning",name:"Roots Bleach and Tone",price:90},
  {id:"c1",cat:"Hair Treatments",name:"Olaplex Treatment",price:95},
  {id:"c2",cat:"Hair Treatments",name:"Oil Treatment with Blow Dry",price:65},
  {id:"c3",cat:"Hair Treatments",name:"Keratin Blow Dry Short Hair",price:200},
  {id:"c4",cat:"Hair Treatments",name:"Keratin Blow Dry Medium Hair",price:250},
  {id:"c5",cat:"Hair Treatments",name:"Keratin Blow Dry Long Hair",price:275},
  {id:"d1",cat:"Relaxer Services",name:"Relaxer",price:84.50},
  {id:"d2",cat:"Relaxer Services",name:"Relaxer and Treatment",price:115},
  {id:"d3",cat:"Relaxer Services",name:"Relaxer Treatment and Trim",price:140},
  {id:"d4",cat:"Relaxer Services",name:"Relaxer and Semi Permanent Colour",price:125},
  {id:"d5",cat:"Relaxer Services",name:"Relaxer Semi Permanent Colour and Trim",price:140},
  {id:"d6",cat:"Relaxer Services",name:"Relaxer Hairline",price:55},
  {id:"d7",cat:"Relaxer Services",name:"Texturizer Short Hair",price:55},
  {id:"d8",cat:"Relaxer Services",name:"Texturizer Long Hair",price:75},
  {id:"e1",cat:"Braids and Weaves",name:"Adult Cornrow Large",price:50},
  {id:"e2",cat:"Braids and Weaves",name:"Adult Cornrow Medium",price:65},
  {id:"e3",cat:"Braids and Weaves",name:"Feeding Knotless Ghana Braids",price:75},
  {id:"e4",cat:"Braids and Weaves",name:"Crochet Braids",price:85},
  {id:"e5",cat:"Braids and Weaves",name:"2 Jumbo Braids with Extension",price:35},
  {id:"e6",cat:"Braids and Weaves",name:"Base Cornrow",price:40},
  {id:"e7",cat:"Braids and Weaves",name:"Full Head Twist",price:57.50},
  {id:"e8",cat:"Braids and Weaves",name:"Full Head Weave with Leave Out",price:130},
  {id:"e9",cat:"Braids and Weaves",name:"Half Head Weave",price:100},
  {id:"e10",cat:"Braids and Weaves",name:"Hair Bonding Pieces",price:25},
  {id:"e11",cat:"Braids and Weaves",name:"Hair Weaving Per Row",price:20},
  {id:"e12",cat:"Braids and Weaves",name:"Wig Cap Bonding",price:100},
  {id:"e13",cat:"Braids and Weaves",name:"Weave Restyle",price:65},
  {id:"e14",cat:"Braids and Weaves",name:"Washing of Weave",price:20},
  {id:"e15",cat:"Braids and Weaves",name:"Weave Take Out",price:25},
  {id:"f1",cat:"Consultations",name:"Consultation",price:30},
]'''

if old_start > 0:
    c = c[:old_start] + new_addons + c[old_end:]
    print("✓ Updated prices")

print(f"\nFinal checks:")
print(f"  React import: {'import React from' in c}")
print(f"  showForm: {'showForm' in c}")
print(f"  Pay Now: {'Pay Now with Stripe' in c}")
print(f"  Stripe API: {'create-checkout' in c}")
print(f"  Silk Press: {'Silk Press' in c}")
print(f"  React.createElement: {c.count('React.createElement')}")
print(f"  Size: {len(c)//1024}KB")

with open('app/HHCApp.jsx', 'w', encoding='utf-8') as f:
    f.write(c)

print("\nALL DONE - File saved successfully!")
