with open('app/HHCApp.jsx', 'r', encoding='utf-8') as f:
    c = f.read()

start = c.find('const ADDONS=[')
end = c.find('];', start) + 2

new = '''const ADDONS=[
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

c = c[:start] + new + c[end:]

with open('app/HHCApp.jsx', 'w', encoding='utf-8') as f:
    f.write(c)

print('Done!')