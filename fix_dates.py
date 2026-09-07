from datetime import date, timedelta

today = date.today()
def fmt(d):
    return d.strftime("%a %d %b")

dates = [
    (fmt(today + timedelta(days=1)), "10:00am"),
    (fmt(today + timedelta(days=1)), "2:00pm"),
    (fmt(today + timedelta(days=2)), "11:00am"),
    (fmt(today + timedelta(days=2)), "3:30pm"),
    (fmt(today + timedelta(days=3)), "9:30am"),
    (fmt(today + timedelta(days=4)), "1:00pm"),
    (fmt(today + timedelta(days=5)), "10:30am"),
    (fmt(today + timedelta(days=5)), "4:00pm"),
]

with open('app/HHCApp.jsx','r',encoding='utf-8') as f:
    c=f.read()

old_slots='''const SLOTS=[
  {id:1,date:"Mon 16 Jun",time:"10:00am",avail:true},
  {id:2,date:"Mon 16 Jun",time:"2:00pm",avail:true},
  {id:3,date:"Tue 17 Jun",time:"11:00am",avail:true},
  {id:4,date:"Tue 17 Jun",time:"3:30pm",avail:false},
  {id:5,date:"Wed 18 Jun",time:"9:30am",avail:true},
  {id:6,date:"Thu 19 Jun",time:"1:00pm",avail:true},
  {id:7,date:"Fri 20 Jun",time:"10:30am",avail:true},
  {id:8,date:"Fri 20 Jun",time:"4:00pm",avail:false},
];'''

new_slots=f'''const SLOTS=[
  {{id:1,date:"{dates[0][0]}",time:"{dates[0][1]}",avail:true}},
  {{id:2,date:"{dates[1][0]}",time:"{dates[1][1]}",avail:true}},
  {{id:3,date:"{dates[2][0]}",time:"{dates[2][1]}",avail:true}},
  {{id:4,date:"{dates[3][0]}",time:"{dates[3][1]}",avail:false}},
  {{id:5,date:"{dates[4][0]}",time:"{dates[4][1]}",avail:true}},
  {{id:6,date:"{dates[5][0]}",time:"{dates[5][1]}",avail:true}},
  {{id:7,date:"{dates[6][0]}",time:"{dates[6][1]}",avail:true}},
  {{id:8,date:"{dates[7][0]}",time:"{dates[7][1]}",avail:false}},
];'''

print("Old slots found:", old_slots[:50] in c)
c=c.replace(old_slots,new_slots,1)

with open('app/HHCApp.jsx','w',encoding='utf-8') as f:
    f.write(c)
print("Done!")