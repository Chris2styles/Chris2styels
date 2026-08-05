with open('app/HHCApp.jsx','r',encoding='utf-8') as f:
    c=f.read()

# Add supabase import at top
if 'supabase' not in c:
    old='import React from "react";'
    new='import React from "react";\nimport { createClient } from "@supabase/supabase-js";\nconst supabase = createClient(process.env.NEXT_PUBLIC_SUPABASE_URL, process.env.NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY);'
    c=c.replace(old,new,1)
    print("Added Supabase!")
else:
    print("Supabase already there")

with open('app/HHCApp.jsx','w',encoding='utf-8') as f:
    f.write(c)
print("Done!")