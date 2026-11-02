'use client'
import { useState, useEffect } from 'react'

// Founder photograph: set to e.g. '/photos/christine.jpg' once Christine's original photo is uploaded to public/photos.
// Left empty, the section shows a clearly marked placeholder (no stock or AI image).
const FOUNDER_PHOTO = ''

const G = {
  gold:"#C9A84C",goldLt:"#E2C97E",goldDk:"#9A7A2E",goldPale:"#F5EDD0",
  black:"#080808",charcoal:"#111",ink:"#1A1A1A",
  white:"#FFF",cream:"#F5F3EE",creamDk:"#EDE8DF",creamLt:"#FAF8F3",
  silver:"#999",smoke:"#CCC",muted:"#3A3A3A",dim:"#666",
}
const SR="'Georgia',serif"
const DP="'Trebuchet MS',sans-serif"
const BD="'Helvetica Neue',Helvetica,Arial,sans-serif"

const PKGS = [
  {
    id:"essential",name:"Essential",sub:"Club Access",price:39,disc:10,badge:null,
    tagline:"Quarterly maintenance, priority access and member savings.",
    included:["One full maintenance service every three months (treatment, wash and style, or weave/braids wash and refresh)","One complimentary add-on per membership year (e.g. colour, a weave or plaits)","Priority booking access","Members-only appointment slots","10% off styling and premium services","Professional healthy hair maintenance advice"],
    excluded:"Complimentary aftercare products are not included with Essential.",
    cta:"Choose Essential"
  },
  {
    id:"signature",name:"Signature",sub:"Care",price:99,disc:15,badge:"Most Popular",
    tagline:"One monthly maintenance service plus ongoing member benefits.",
    included:["One monthly maintenance service (treatment, wash and style, or weave/braids wash and refresh)","Two complimentary add-ons per membership year (e.g. colour, a weave or plaits)","Complimentary Aftercare Products Provided","Hair and scalp assessment","Shampoo and cleanse","Professional treatment selected according to hair needs","Sustenance, Olaplex or K18 where appropriate","Trim where required","Basic styling","Healthy hair maintenance advice","Priority booking","15% off selected premium services"],
    excluded:null,
    cta:"Choose Signature"
  },
  {
    id:"elite",name:"Elite",sub:"VIP",price:149,disc:20,badge:"Premium",
    tagline:"The highest level of care and flexibility.",
    included:["One monthly maintenance service (treatment, wash and style, or weave/braids wash and refresh)","Two complimentary add-ons per membership year (e.g. colour, a weave or plaits)","Complimentary Aftercare Products Provided","\u00A330 monthly premium styling credit",
"Gift your credit to family and friends","Priority appointments","Free consultations","Birthday Glam bonus","Exclusive member benefits"],
    excluded:null,
    cta:"Choose Elite"
  },
]

const TREATS = [
  {name:"Sustenance",icon:"💧",desc:"Designed to support moisture, softness and manageability as part of an ongoing healthy hair maintenance routine."},
  {name:"Olaplex",icon:"🔗",desc:"Used where appropriate to support the condition and structure of hair affected by chemical processing, colouring, heat or styling."},
  {name:"K18",icon:"✨",desc:"An advanced repair-focused option that may be selected for stressed or damaged hair to support its condition, softness and manageability."},
]

const BENEFITS = [
  {icon:"📅",title:"Priority Booking",desc:"Get earlier access to selected appointments and member-only availability."},
  {icon:"🌿",title:"Consistent Maintenance",desc:"Stay on top of your hair routine instead of waiting until your hair becomes difficult to manage."},
  {icon:"💆🏾‍♀️",title:"Professional Care",desc:"Receive appropriate maintenance advice and treatments according to your hair's needs."},
  {icon:"🏷️",title:"Member Savings",desc:"Receive discounts and benefits according to your membership level."},
  {icon:"🖤",title:"Ongoing Support",desc:"Healthy hair maintenance becomes an ongoing relationship rather than an occasional salon appointment."},
]

const STEPS = [
  {n:1,title:"Choose",desc:"Select the Healthy Hair Club membership that suits you."},
  {n:2,title:"Join",desc:"Create your account and activate your monthly membership."},
  {n:3,title:"Book",desc:"Access your eligible member appointments and priority availability."},
  {n:4,title:"Maintain",desc:"Stay consistent with professional support throughout the year."},
]

const FAQS = [
  {q:"Which membership is right for me?",a:"Essential (£39) includes one full maintenance service every three months, priority booking and member discounts. Signature (£99) is our most popular — it includes one monthly maintenance service and Complimentary Aftercare Products Provided. Elite (£149) is for clients who want the highest level of care and flexibility, including a £30 monthly premium styling credit."},
  {q:"What is included in Signature?",a:"Signature includes one monthly maintenance service with hair and scalp assessment, shampoo and cleanse, a professional treatment selected according to your hair's needs, a trim where required, basic styling and healthy hair maintenance advice. You also receive two complimentary add-ons per membership year, Complimentary Aftercare Products Provided, priority booking and 15% off selected premium services."},
  {q:"Are all three treatments included every month?",a:"No. Sustenance, Olaplex and K18 are not all applied simultaneously. Your stylist will assess your hair at each appointment and select the most appropriate treatment according to your hair's condition and needs."},
  {q:"What happens if my payment fails?",a:"If your payment fails, your booking access is temporarily paused. You will receive a notification to update your payment details. Once resolved, your access is automatically restored."},
  {q:"Can I choose the date my payment comes out?",a:"Yes. When you join, you can choose any day from the 1st to the 28th for your monthly payment. Nothing is taken when you sign up; your first payment comes out on your chosen date and your membership starts from that day. You can book your appointments once your first payment has gone through."},
  {q:"Can I upgrade or downgrade?",a:"Yes. Please contact the salon to change your membership level. The change takes effect from your next payment date."},
  {q:"What can my maintenance service be?",a:"Your maintenance service is the care you get in between your main appointments, so your hair isn't left too long without attention. You choose what suits your hair at the time: a professional treatment (such as Sustenance, Olaplex or K18), a wash and style, a weave wash and refresh (washed, retied and maintained), or a braids wash and refresh. For example, if your weave lasts 6 to 8 weeks, you can come in part-way through to have it washed, retied and maintained."},
  {q:"Do unused appointments roll over?",a:"No. Maintenance services must be used within their period — each membership month for Signature and Elite, and each three-month period for Essential. Unused services do not roll over."},
  {q:"What is a complimentary add-on?",a:"Each complimentary add-on makes one add-on of your choice free on a visit — for example colour, a weave or plaits. Essential includes one per membership year; Signature and Elite include two. They reset each membership year and unused ones expire."},
  {q:"Can I gift my Elite credit?",a:"Yes. Elite members can gift some or all of their monthly £30 styling credit to anyone they like — family, friends or someone new to the salon — from their dashboard. Gifted credit must be used by the end of that membership month."},
  {q:"How do priority appointments work?",a:"Members receive earlier access to selected appointment slots before they are released to the general public. This means you are more likely to secure your preferred time with your stylist."},
  {q:"Can I cancel my membership?",a:"Yes. You can cancel anytime. Cancellations take effect at the end of your current billing month. There are no cancellation fees."},
  {q:"Can I speak directly to the salon?",a:"Yes. If you have a question that requires professional judgement or personal advice, you can always contact Chris 2 Styles Salon directly at 020 3754 7889 or christine.walker@hairdresser.net."},
]

function useUTM() {
  useEffect(() => {
    if(typeof window === 'undefined') return
    const params = new URLSearchParams(window.location.search)
    const utm = {
      source: params.get('utm_source') || 'direct',
      medium: params.get('utm_medium') || '',
      campaign: params.get('utm_campaign') || '',
      content: params.get('utm_content') || '',
    }
    sessionStorage.setItem('hhc_utm', JSON.stringify(utm))
    // Track landing page visit
    if(window.gtag) window.gtag('event','landing_page_view', utm)
  }, [])
}

function trackEvent(name, data={}) {
  try {
    const utm = JSON.parse(sessionStorage.getItem('hhc_utm') || '{}')
    if(window.gtag) window.gtag('event', name, {...data, ...utm})
    console.log('Track:', name, {...data, ...utm})
  } catch(e) {}
}

export default function LandingPage({onJoin, onSignIn}) {
  useUTM()
  const [openFaq, setOpenFaq] = useState(null)
  const [storyOpen, setStoryOpen] = useState(false)

  function handleChoose(pkgId) {
    trackEvent('package_selected', {package: pkgId})
    onJoin(pkgId)
  }

  return (
    <div style={{fontFamily:BD, background:G.cream, minHeight:'100vh'}}>

      {/* NAV */}
      <nav style={{position:'sticky',top:0,zIndex:100,background:'rgba(8,8,8,0.96)',backdropFilter:'blur(10px)',borderBottom:'1px solid '+G.muted,padding:'14px 20px',display:'flex',justifyContent:'space-between',alignItems:'center'}}>
        <div>
          <div style={{fontFamily:DP,fontSize:13,color:G.white,letterSpacing:2,textTransform:'uppercase',lineHeight:1}}>Chris 2 Styles</div>
          <div style={{fontFamily:BD,fontSize:10,color:G.gold,letterSpacing:3,textTransform:'uppercase',marginTop:2}}>Healthy Hair Club</div>
        </div>
        <button onClick={()=>{trackEvent('signin_clicked');onSignIn()}}
          style={{background:'transparent',border:'1px solid '+G.gold,color:G.gold,borderRadius:4,padding:'8px 16px',fontSize:12,fontFamily:DP,fontWeight:700,letterSpacing:1.5,textTransform:'uppercase',cursor:'pointer'}}>
          Sign In
        </button>
      </nav>

      {/* HERO */}
      <section style={{background:'linear-gradient(160deg,#080808,#1A1A1A)',padding:'70px 20px 80px',textAlign:'center',position:'relative',overflow:'hidden'}}>
        <div style={{position:'absolute',top:0,left:0,right:0,height:2,background:'linear-gradient(90deg,transparent,'+G.gold+',transparent)'}}/>
        <div style={{maxWidth:600,margin:'0 auto'}}>
          <div style={{color:G.gold,fontSize:10,letterSpacing:5,textTransform:'uppercase',marginBottom:20}}>Chris 2 Styles Salon · Streatham SW16</div>
          <div style={{fontFamily:SR,color:G.white,fontSize:42,fontWeight:400,fontStyle:'italic',lineHeight:1.2,marginBottom:20}}>
            Your Hair.<br/>Maintained Consistently.
          </div>
          <p style={{color:'rgba(255,255,255,0.65)',fontSize:16,lineHeight:1.8,maxWidth:480,margin:'0 auto 32px'}}>
            Professional hair maintenance, priority booking and exclusive member benefits from Chris 2 Styles Salon.
          </p>
          <div style={{color:G.goldLt,fontSize:18,fontWeight:700,fontFamily:DP,marginBottom:32,letterSpacing:1}}>
            Memberships from £39/month
          </div>
          <div style={{display:'flex',gap:12,justifyContent:'center',flexWrap:'wrap'}}>
            <button onClick={()=>{trackEvent('explore_memberships_hero');document.getElementById('memberships').scrollIntoView({behavior:'smooth'})}}
              style={{background:'linear-gradient(135deg,'+G.goldLt+','+G.gold+')',color:G.black,border:'none',borderRadius:4,padding:'16px 32px',fontSize:14,fontFamily:DP,fontWeight:700,letterSpacing:2,textTransform:'uppercase',cursor:'pointer'}}>
              Explore Memberships
            </button>
            <button onClick={()=>{trackEvent('signin_clicked_hero');onSignIn()}}
              style={{background:'transparent',color:G.smoke,border:'1px solid '+G.muted,borderRadius:4,padding:'16px 24px',fontSize:13,fontFamily:BD,cursor:'pointer'}}>
              Already a member? Sign In
            </button>
          </div>
        </div>
      </section>

      {/* PROBLEM */}
      <section style={{background:G.white,padding:'64px 20px',textAlign:'center'}}>
        <div style={{maxWidth:580,margin:'0 auto'}}>
          <div style={{color:G.goldDk,fontSize:10,letterSpacing:4,textTransform:'uppercase',marginBottom:16}}>Why Healthy Hair Club</div>
          <h2 style={{fontFamily:SR,fontSize:30,color:G.ink,fontWeight:400,fontStyle:'italic',lineHeight:1.35,margin:'0 0 20px'}}>
            Healthy-looking hair isn't just about how your hair looks when you leave the salon.
          </h2>
          <p style={{color:G.dim,fontSize:16,lineHeight:1.85,margin:'0 0 16px'}}>
            Consistency matters. Healthy Hair Club was created for clients who want to stop leaving their hair maintenance until the last minute and instead have structured professional support throughout the year.
          </p>
          <p style={{color:G.dim,fontSize:15,lineHeight:1.85,margin:0,fontStyle:'italic',borderLeft:'3px solid '+G.gold,paddingLeft:20,textAlign:'left'}}>
            After more than 20 years of working with hair, I understand that what happens between appointments is just as important as the appointment itself.
          </p>
        </div>
      </section>

      {/* BENEFITS */}
      <section style={{background:G.creamLt,padding:'64px 20px'}}>
        <div style={{maxWidth:800,margin:'0 auto'}}>
          <div style={{textAlign:'center',marginBottom:40}}>
            <div style={{color:G.goldDk,fontSize:10,letterSpacing:4,textTransform:'uppercase',marginBottom:12}}>Member Benefits</div>
            <h2 style={{fontFamily:SR,fontSize:28,color:G.ink,fontWeight:400,fontStyle:'italic',margin:0}}>Why Join Healthy Hair Club</h2>
          </div>
          <div style={{display:'grid',gridTemplateColumns:'repeat(auto-fit,minmax(240px,1fr))',gap:16}}>
            {BENEFITS.map((b,i)=>(
              <div key={i} style={{background:G.white,borderRadius:12,padding:'24px 20px',border:'1px solid '+G.creamDk}}>
                <div style={{fontSize:28,marginBottom:12}}>{b.icon}</div>
                <div style={{fontWeight:700,color:G.ink,fontSize:15,marginBottom:8}}>{b.title}</div>
                <p style={{color:G.dim,fontSize:13,lineHeight:1.7,margin:0}}>{b.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* MEMBERSHIPS */}
      <section id="memberships" style={{background:G.black,padding:'70px 20px'}}>
        <div style={{maxWidth:960,margin:'0 auto'}}>
          <div style={{textAlign:'center',marginBottom:48}}>
            <div style={{color:G.gold,fontSize:10,letterSpacing:4,textTransform:'uppercase',marginBottom:12}}>Choose Your Membership</div>
            <h2 style={{fontFamily:SR,fontSize:32,color:G.white,fontWeight:400,fontStyle:'italic',margin:'0 0 12px'}}>Healthy Hair Club Memberships</h2>
            <p style={{color:'rgba(255,255,255,0.5)',fontSize:14,margin:0}}>Cancel anytime. No long-term contracts.</p>
          </div>
          <div style={{display:'grid',gridTemplateColumns:'repeat(auto-fit,minmax(280px,1fr))',gap:20}}>
            {PKGS.map(pkg=>{
              const isSig = pkg.id==='signature'
              return (
                <div key={pkg.id} style={{background:isSig?'linear-gradient(160deg,#1A1200,#2A1E00)':G.ink,borderRadius:4,overflow:'hidden',border:'1px solid '+(isSig?G.gold:G.muted),boxShadow:isSig?'0 0 0 1px '+G.gold+',0 20px 40px rgba(201,168,76,0.15)':'none',position:'relative',transform:isSig?'scale(1.02)':'none'}}>
                  {pkg.badge&&(
                    <div style={{position:'absolute',top:16,right:16,background:'linear-gradient(135deg,'+G.goldLt+','+G.gold+')',color:G.black,fontSize:9,fontWeight:700,letterSpacing:2,textTransform:'uppercase',padding:'4px 10px',borderRadius:2}}>
                      {pkg.badge}
                    </div>
                  )}
                  <div style={{padding:'28px 24px 0'}}>
                    <div style={{color:G.gold,fontSize:10,letterSpacing:3,textTransform:'uppercase',marginBottom:4}}>{pkg.sub}</div>
                    <div style={{fontFamily:SR,color:G.white,fontSize:26,fontStyle:'italic',marginBottom:16}}>{pkg.name}</div>
                    <div style={{display:'flex',alignItems:'baseline',gap:4,marginBottom:8}}>
                      <span style={{fontFamily:DP,fontSize:38,color:G.gold,fontWeight:700}}>£{pkg.price}</span>
                      <span style={{color:G.dim,fontSize:13}}>/month</span>
                    </div>
                    <p style={{color:'rgba(255,255,255,0.5)',fontSize:12,fontStyle:'italic',margin:'0 0 20px'}}>{pkg.tagline}</p>
                    <div style={{borderTop:'1px solid '+G.muted,paddingTop:20,marginBottom:20}}>
                      {pkg.included.map((item,i)=>(
                        <div key={i} style={{display:'flex',gap:10,alignItems:'flex-start',marginBottom:8}}>
                          <span style={{color:G.gold,fontSize:13,flexShrink:0,marginTop:1}}>✦</span>
                          <span style={{color:'rgba(255,255,255,0.75)',fontSize:13,lineHeight:1.5}}>{item}</span>
                        </div>
                      ))}
                      {pkg.excluded&&(
                        <div style={{marginTop:12,padding:'10px 12px',background:'rgba(255,255,255,0.05)',borderRadius:4,color:'rgba(255,255,255,0.4)',fontSize:12,lineHeight:1.5}}>
                          {pkg.excluded}
                        </div>
                      )}
                    </div>
                  </div>
                  <div style={{padding:'0 24px 28px'}}>
                    <button onClick={()=>handleChoose(pkg.id)}
                      style={{width:'100%',padding:'15px 0',background:isSig?'linear-gradient(135deg,'+G.goldLt+','+G.gold+')':'transparent',color:isSig?G.black:G.gold,border:isSig?'none':'1px solid '+G.gold,borderRadius:4,fontFamily:DP,fontWeight:700,fontSize:13,letterSpacing:1.5,textTransform:'uppercase',cursor:'pointer'}}>
                      {pkg.cta}
                    </button>
                  </div>
                </div>
              )
            })}
          </div>
          <p style={{textAlign:'center',color:'rgba(255,255,255,0.3)',fontSize:12,marginTop:24}}>
            By joining you agree to our <span style={{color:G.gold,cursor:'pointer'}} onClick={()=>document.getElementById('faqs').scrollIntoView({behavior:'smooth'})}>membership terms</span>. Cancel anytime.
          </p>
        </div>
      </section>

      {/* TREATMENTS */}
      <section style={{background:G.white,padding:'64px 20px'}}>
        <div style={{maxWidth:760,margin:'0 auto'}}>
          <div style={{textAlign:'center',marginBottom:40}}>
            <div style={{color:G.goldDk,fontSize:10,letterSpacing:4,textTransform:'uppercase',marginBottom:12}}>Professional Care</div>
            <h2 style={{fontFamily:SR,fontSize:28,color:G.ink,fontWeight:400,fontStyle:'italic',margin:'0 0 12px'}}>Professional Care, Selected For Your Hair</h2>
            <p style={{color:G.dim,fontSize:14,margin:0}}>Your stylist will determine the most appropriate treatment according to your hair's condition and needs.</p>
          </div>
          <div style={{display:'grid',gridTemplateColumns:'repeat(auto-fit,minmax(220px,1fr))',gap:16,marginBottom:24}}>
            {TREATS.map((t,i)=>(
              <div key={i} style={{background:G.creamLt,borderRadius:12,padding:'24px 20px',border:'1px solid '+G.creamDk}}>
                <div style={{fontSize:28,marginBottom:12}}>{t.icon}</div>
                <div style={{fontWeight:700,color:G.ink,fontSize:16,marginBottom:8}}>{t.name}</div>
                <p style={{color:G.dim,fontSize:13,lineHeight:1.7,margin:0}}>{t.desc}</p>
              </div>
            ))}
          </div>
          <div style={{background:G.creamLt,borderRadius:10,padding:'16px 20px',border:'1px solid '+G.creamDk,textAlign:'center'}}>
            <p style={{color:G.dim,fontSize:13,margin:0,lineHeight:1.7}}>
              <strong style={{color:G.ink}}>Important:</strong> Treatments are not all applied simultaneously. Your stylist selects the most suitable option at each appointment. No medical claims are made. Results may vary.
            </p>
          </div>
        </div>
      </section>

      {/* FOUNDER — approved story, exact wording */}
      <section id="founder" style={{background:G.creamLt,padding:'72px 20px'}}>
        <div style={{maxWidth:960,margin:'0 auto'}}>
          <div style={{textAlign:'center',marginBottom:40}}>
            <div style={{color:G.goldDk,fontSize:10,letterSpacing:4,textTransform:'uppercase',marginBottom:12}}>Our Founder</div>
            <h2 style={{fontFamily:SR,fontSize:30,color:G.ink,fontWeight:400,fontStyle:'italic',margin:0,lineHeight:1.3}}>Meet Christine — The Woman Behind Healthy Hair Club</h2>
          </div>
          <div style={{display:'grid',gridTemplateColumns:'repeat(auto-fit,minmax(280px,1fr))',gap:32,alignItems:'start'}}>
            <div style={{position:'relative',borderRadius:14,overflow:'hidden',border:'1px solid '+G.creamDk,background:G.white,aspectRatio:'4 / 5',maxWidth:420,width:'100%',margin:'0 auto'}}>
              {FOUNDER_PHOTO ? (
                <img src={FOUNDER_PHOTO} alt="Christine Walker, founder of Chris 2 Styles Salon and Healthy Hair Club" style={{width:'100%',height:'100%',objectFit:'cover',objectPosition:'center top',display:'block'}}/>
              ) : (
                <div style={{width:'100%',height:'100%',background:'linear-gradient(160deg,'+G.goldDk+','+G.gold+')',display:'flex',flexDirection:'column',alignItems:'center',justifyContent:'center',textAlign:'center',padding:24,boxSizing:'border-box'}}>
                  <div style={{width:88,height:88,borderRadius:'50%',border:'2px solid rgba(255,255,255,0.55)',display:'flex',alignItems:'center',justifyContent:'center',marginBottom:16}}>
                    <span style={{color:G.white,fontSize:36,fontFamily:SR,fontStyle:'italic'}}>C</span>
                  </div>
                  <div style={{color:G.white,fontSize:12,letterSpacing:2,textTransform:'uppercase'}}>Christine Walker</div>
                  <div style={{color:'rgba(255,255,255,0.75)',fontSize:11,marginTop:6}}>Founder photograph coming soon</div>
                </div>
              )}
            </div>
            <div style={{background:G.white,borderRadius:14,border:'1px solid '+G.creamDk,padding:'32px 28px'}}>
              <p style={{color:G.dim,fontSize:16,lineHeight:1.85,margin:'0 0 16px'}}>
                My journey in hairdressing began over 22 years ago, driven by a passion for creativity, beauty and helping people feel confident in themselves.
              </p>
              <p style={{color:G.dim,fontSize:16,lineHeight:1.85,margin:0}}>
                As an award-winning hairstylist, I've been fortunate to receive recognition within the hair and beauty industry, including the Black Hair and Beauty Awards, alongside nominations and finalist honours for Stylist of the Year and Styling Team of the Year. While these achievements mean a great deal to me, what has always mattered most is the difference I can make in the lives of the women who sit in my chair.
              </p>
              <div id="founder-story-more" hidden={!storyOpen} style={{marginTop:16}}>
                <p style={{color:G.dim,fontSize:16,lineHeight:1.85,margin:'0 0 16px'}}>
                  Over the years, I've had the privilege of working with countless clients, learning about their individual hair needs, challenges and goals. One thing I've come to understand is that beautiful, healthy hair isn't achieved through occasional appointments or following the latest trends. It's built through consistency, professional knowledge and personalised care.
                </p>
                <p style={{color:G.dim,fontSize:16,lineHeight:1.85,margin:'0 0 16px'}}>
                  When I opened Chris 2 Styles Salon in 2016, my vision was to create more than somewhere women came to have their hair styled. I wanted to create a community — a space where women could come together, feel at peace, be listened to, understood and genuinely cared for. Somewhere they could take time for themselves, feel a sense of belonging and, most importantly, feel at home.
                </p>
                <p style={{color:G.ink,fontSize:16,lineHeight:1.85,margin:'0 0 16px',fontWeight:700}}>
                  Healthy Hair Club was born from that same philosophy.
                </p>
                <p style={{color:G.dim,fontSize:16,lineHeight:1.85,margin:'0 0 16px'}}>
                  I wanted to bring together a community of women who value their hair health, understand the importance of regular maintenance and appreciate having a trusted professional supporting them throughout their hair journey.
                </p>
                <p style={{color:G.dim,fontSize:16,lineHeight:1.85,margin:'0 0 16px'}}>
                  Through Healthy Hair Club, my goal is to make consistent, personalised hair care more accessible, convenient and rewarding, while continuing to nurture the sense of community that has always been at the heart of my salon.
                </p>
                <p style={{color:G.ink,fontSize:17,lineHeight:1.8,margin:0,fontFamily:SR,fontStyle:'italic',borderLeft:'3px solid '+G.gold,paddingLeft:18}}>
                  Because to me, healthy hair is more than a service. It's about confidence, self-care, connection and belonging.
                </p>
              </div>
              <button type="button" aria-expanded={storyOpen} aria-controls="founder-story-more"
                onClick={()=>{if(!storyOpen)trackEvent('read_my_story');setStoryOpen(!storyOpen)}}
                style={{marginTop:24,background:'transparent',border:'1px solid '+G.gold,color:G.goldDk,borderRadius:4,padding:'12px 22px',fontSize:12,fontFamily:DP,fontWeight:700,letterSpacing:1.5,textTransform:'uppercase',cursor:'pointer'}}>
                {storyOpen?'Show Less':'Read My Story'}
              </button>
              <div style={{marginTop:24,paddingTop:20,borderTop:'1px solid '+G.creamDk}}>
                <div style={{color:G.ink,fontWeight:700,fontSize:15}}>Christine Walker</div>
                <div style={{color:G.goldDk,fontSize:13,marginTop:2,fontStyle:'italic'}}>Founder, Chris 2 Styles Salon &amp; Healthy Hair Club</div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* SOCIAL PROOF PLACEHOLDER */}
      <section style={{background:G.white,padding:'64px 20px'}}>
        <div style={{maxWidth:800,margin:'0 auto',textAlign:'center'}}>
          <div style={{color:G.goldDk,fontSize:10,letterSpacing:4,textTransform:'uppercase',marginBottom:12}}>Client Results</div>
          <h2 style={{fontFamily:SR,fontSize:28,color:G.ink,fontWeight:400,fontStyle:'italic',margin:'0 0 32px'}}>Real Results From Real Clients</h2>
          <div style={{display:'grid',gridTemplateColumns:'repeat(auto-fit,minmax(220px,1fr))',gap:16}}>
            {[1,2,3].map(i=>(
              <div key={i} style={{background:G.creamLt,borderRadius:12,height:200,display:'flex',alignItems:'center',justifyContent:'center',border:'2px dashed '+G.creamDk,flexDirection:'column',gap:8}}>
                <span style={{fontSize:28}}>📷</span>
                <span style={{color:G.smoke,fontSize:12}}>Before & After {i}</span>
                <span style={{color:G.smoke,fontSize:11}}>Coming soon</span>
              </div>
            ))}
          </div>
          <div style={{marginTop:32,background:G.creamLt,borderRadius:12,padding:'24px 20px',border:'1px solid '+G.creamDk}}>
            <div style={{display:'flex',justifyContent:'center',gap:4,marginBottom:12}}>
              {[1,2,3,4,5].map(i=><span key={i} style={{color:G.gold,fontSize:20}}>★</span>)}
            </div>
            <p style={{color:G.dim,fontSize:14,fontStyle:'italic',margin:'0 0 8px'}}>"Every time I leave the salon I feel both beautiful and special."</p>
            <div style={{color:G.silver,fontSize:12}}>— Google Review · Chris 2 Styles Salon</div>
          </div>
        </div>
      </section>

      {/* HOW IT WORKS */}
      <section style={{background:G.creamLt,padding:'64px 20px'}}>
        <div style={{maxWidth:700,margin:'0 auto'}}>
          <div style={{textAlign:'center',marginBottom:40}}>
            <div style={{color:G.goldDk,fontSize:10,letterSpacing:4,textTransform:'uppercase',marginBottom:12}}>Simple Process</div>
            <h2 style={{fontFamily:SR,fontSize:28,color:G.ink,fontWeight:400,fontStyle:'italic',margin:0}}>How It Works</h2>
          </div>
          <div style={{display:'flex',flexDirection:'column',gap:16}}>
            {STEPS.map((s,i)=>(
              <div key={i} style={{background:G.white,borderRadius:12,padding:'20px 24px',display:'flex',gap:20,alignItems:'flex-start',border:'1px solid '+G.creamDk}}>
                <div style={{width:44,height:44,borderRadius:'50%',background:'linear-gradient(135deg,'+G.goldLt+','+G.gold+')',display:'flex',alignItems:'center',justifyContent:'center',flexShrink:0,fontFamily:DP,fontWeight:700,fontSize:18,color:G.black}}>
                  {s.n}
                </div>
                <div>
                  <div style={{fontWeight:700,color:G.ink,fontSize:16,marginBottom:4}}>{s.title}</div>
                  <p style={{color:G.dim,fontSize:14,lineHeight:1.65,margin:0}}>{s.desc}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* FAQS */}
      <section id="faqs" style={{background:G.white,padding:'64px 20px'}}>
        <div style={{maxWidth:680,margin:'0 auto'}}>
          <div style={{textAlign:'center',marginBottom:40}}>
            <div style={{color:G.goldDk,fontSize:10,letterSpacing:4,textTransform:'uppercase',marginBottom:12}}>Questions</div>
            <h2 style={{fontFamily:SR,fontSize:28,color:G.ink,fontWeight:400,fontStyle:'italic',margin:0}}>Frequently Asked Questions</h2>
          </div>
          {FAQS.map((faq,i)=>(
            <div key={i} style={{borderBottom:'1px solid '+G.creamDk,overflow:'hidden'}}>
              <div onClick={()=>setOpenFaq(openFaq===i?null:i)}
                style={{display:'flex',justifyContent:'space-between',alignItems:'center',padding:'18px 0',cursor:'pointer'}}>
                <span style={{fontWeight:700,color:G.ink,fontSize:15,paddingRight:20}}>{faq.q}</span>
                <span style={{color:G.gold,fontSize:22,flexShrink:0,transform:openFaq===i?'rotate(45deg)':'none',transition:'transform 0.2s'}}>+</span>
              </div>
              {openFaq===i&&(
                <div style={{paddingBottom:18}}>
                  <p style={{color:G.dim,fontSize:14,lineHeight:1.8,margin:0}}>{faq.a}</p>
                </div>
              )}
            </div>
          ))}
        </div>
      </section>

      {/* FINAL CTA */}
      <section style={{background:'linear-gradient(135deg,'+G.goldDk+','+G.gold+')',padding:'70px 20px',textAlign:'center'}}>
        <div style={{maxWidth:560,margin:'0 auto'}}>
          <h2 style={{fontFamily:SR,fontSize:32,color:G.white,fontWeight:400,fontStyle:'italic',margin:'0 0 16px',lineHeight:1.3}}>
            Ready to make your hair maintenance more consistent?
          </h2>
          <p style={{color:'rgba(255,255,255,0.8)',fontSize:15,lineHeight:1.75,margin:'0 0 36px'}}>
            Join the Healthy Hair Club and choose the level of care that works for you.
          </p>
          <div style={{display:'flex',gap:12,justifyContent:'center',flexWrap:'wrap'}}>
            <button onClick={()=>{trackEvent('explore_memberships_footer');document.getElementById('memberships').scrollIntoView({behavior:'smooth'})}}
              style={{background:G.black,color:G.white,border:'none',borderRadius:4,padding:'16px 32px',fontSize:14,fontFamily:DP,fontWeight:700,letterSpacing:2,textTransform:'uppercase',cursor:'pointer'}}>
              Explore Memberships
            </button>
            <button onClick={()=>handleChoose('signature')}
              style={{background:'rgba(255,255,255,0.15)',color:G.white,border:'1px solid rgba(255,255,255,0.4)',borderRadius:4,padding:'16px 24px',fontSize:13,fontFamily:DP,fontWeight:700,letterSpacing:1.5,textTransform:'uppercase',cursor:'pointer'}}>
              Join Healthy Hair Club
            </button>
          </div>
          <p style={{color:'rgba(255,255,255,0.6)',fontSize:12,marginTop:20}}>
            Already a member? <span onClick={()=>{trackEvent('signin_clicked_footer');onSignIn()}} style={{color:G.white,cursor:'pointer',textDecoration:'underline'}}>Sign In</span>
          </p>
        </div>
      </section>

      {/* FOOTER */}
      <footer style={{background:G.black,padding:'32px 20px',textAlign:'center',borderTop:'1px solid '+G.muted}}>
        <div style={{color:G.white,fontFamily:DP,fontSize:13,letterSpacing:2,textTransform:'uppercase',marginBottom:4}}>Chris 2 Styles</div>
        <div style={{color:G.gold,fontSize:10,letterSpacing:3,textTransform:'uppercase',marginBottom:16}}>Healthy Hair Club</div>
        <p style={{color:G.dim,fontSize:12,margin:'0 0 8px'}}>87 Mitcham Lane, Streatham, London SW16 6LY</p>
        <p style={{color:G.dim,fontSize:12,margin:'0 0 16px'}}>020 3754 7889 · christine.walker@hairdresser.net</p>
        <p style={{color:G.muted,fontSize:11,margin:0}}>© 2026 Chris 2 Styles Ltd. All rights reserved.</p>
      </footer>

    </div>
  )
}
