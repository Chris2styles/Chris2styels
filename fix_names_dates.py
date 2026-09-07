with open('app/HHCApp.jsx','r',encoding='utf-8') as f:
    c=f.read()

# Fix "Aisha" in booking confirmation
old='"You are all set!"'
new='{`You are all set, ${mem.name.split(" ")[0]}!`}'
print("Old confirm found:", old in c)
c=c.replace(old,new,1)

# Also fix any remaining hardcoded Aisha
c=c.replace('"You are all set, Aisha"','`You are all set!`')
c=c.replace("'You are all set, Aisha'","`You are all set!`")

# Fix the next appointment date to show today's date
import datetime
today = datetime.date.today()
next_month = today.replace(month=today.month+1) if today.month < 12 else today.replace(year=today.year+1, month=1)
next_date = next_month.strftime("%-d %b %Y") if hasattr(datetime.date, 'strftime') else next_month.strftime("%d %b %Y")

# Fix membership card date
old_next="next:'Contact salon to book',"
new_next=f"next:'Next billing: {next_month.strftime(\"%d %b %Y\")}',"
print("Next date found:", old_next in c)
c=c.replace(old_next, new_next, 1)

with open('app/HHCApp.jsx','w',encoding='utf-8') as f:
    f.write(c)
print("Done!")