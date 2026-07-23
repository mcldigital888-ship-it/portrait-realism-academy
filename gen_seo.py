#!/usr/bin/env python3
# Generates the SEO/AEO sub-pages + sitemap.xml for portraitrealismacademy.com
# Money page (/) stays hand-authored (index.html). All facts verified; NO "best" claims, NO fake reviews.
import json, os

SITE = "https://portraitrealismacademy.com"
FEDERICO = SITE + "/#federico"
COURSE   = SITE + "/#course"
ACADEMY  = SITE + "/#academy"
WHITELAB = SITE + "/#whitelabel"
SOL      = SITE + "/#solstudios"
UPDATED  = "October 2026"

# ---- canonical schema nodes (reused by @id) ----
NODE_PERSON = {
  "@type":"Person","@id":FEDERICO,"name":"Federico Galliani","alternateName":"Portrait KID",
  "jobTitle":"Tattoo Artist","nationality":"Italian",
  "description":"Italian black & grey portrait-realism tattoo artist, co-owner of White Label Tattoo, award-winning on the U.S. tattoo convention circuit.",
  "knowsAbout":["black and grey tattooing","portrait realism tattoo","grey wash technique","healed tattoo longevity"],
  "worksFor":{"@id":WHITELAB},
  "award":["First place, U.S. tattoo convention, Baltimore","First place, U.S. tattoo convention, Chicago"],
  "image":SITE+"/assets/portfolio/instructor-federico.webp",
  "sameAs":["https://www.instagram.com/federicogallianitattoo/"]
}
NODE_WHITELAB = {"@type":"Organization","@id":WHITELAB,"name":"White Label Tattoo",
  "address":{"@type":"PostalAddress","addressLocality":"Cesano Maderno","addressRegion":"MB","addressCountry":"IT"}}
NODE_SOL = {"@type":"Place","@id":SOL,"name":"SOL Studios",
  "address":{"@type":"PostalAddress","streetAddress":"11000 W Janesville Rd","addressLocality":"Hales Corners","addressRegion":"WI","postalCode":"53130","addressCountry":"US"}}
NODE_ACADEMY = {"@type":"EducationalOrganization","@id":ACADEMY,"name":"Portrait Realism Academy",
  "url":SITE+"/","founder":{"@id":FEDERICO},"description":"A 3-day black & grey portrait-realism tattoo masterclass by Federico Galliani, Milwaukee, October 2026."}
NODE_COURSE = {"@type":"Course","@id":COURSE,"name":"Portrait Realism Academy by Federico Galliani",
  "description":"A 3-day hands-on black & grey portrait-realism tattoo masterclass for intermediate and advanced artists: grey-wash theory, live demo, and supervised practice.",
  "provider":{"@id":ACADEMY},"inLanguage":"en","educationalLevel":"Intermediate to advanced",
  "image":[SITE+"/assets/portfolio/hero-old-man.webp",SITE+"/assets/portfolio/hiphop-nyc-portrait.webp"],
  "hasCourseInstance":{"@type":"CourseInstance","courseMode":"in-person","startDate":"2026-10-06","endDate":"2026-10-08",
    "location":{"@id":SOL},"instructor":{"@id":FEDERICO},"maximumAttendeeCapacity":10,
    "offers":{"@type":"Offer","price":"2000","priceCurrency":"USD","availability":"https://schema.org/LimitedAvailability","url":SITE+"/apply/"}}}

def webpage(url,name,desc):
    return {"@type":"WebPage","@id":url+"#webpage","url":url,"name":name,"description":desc,"isPartOf":{"@id":SITE+"/#website"},"inLanguage":"en-US"}
def website():
    return {"@type":"WebSite","@id":SITE+"/#website","url":SITE+"/","name":"Portrait Realism Academy","inLanguage":"en-US"}
def crumb(url,name):
    return {"@type":"BreadcrumbList","itemListElement":[
        {"@type":"ListItem","position":1,"name":"Home","item":SITE+"/"},
        {"@type":"ListItem","position":2,"name":name,"item":url}]}

CSS = """*{margin:0;padding:0;box-sizing:border-box}html{scroll-behavior:smooth}
body{background:#0b0b0d;color:#eae7e1;font-family:'Inter',system-ui,-apple-system,sans-serif;font-weight:300;line-height:1.65;-webkit-font-smoothing:antialiased}
a{color:#c2a878}.serif{font-family:'Cormorant Garamond',Georgia,serif}
.wrap{max-width:820px;margin:0 auto;padding:0 22px}
nav{position:sticky;top:0;z-index:30;display:flex;justify-content:space-between;align-items:center;padding:14px 22px;background:rgba(11,11,13,.92);backdrop-filter:blur(10px);border-bottom:1px solid rgba(234,231,225,.12)}
nav .lg{font-family:'Cormorant Garamond',serif;font-size:15px;letter-spacing:3px;text-decoration:none;color:#eae7e1}
nav .ap{font-size:11px;letter-spacing:2px;text-transform:uppercase;text-decoration:none;color:#c2a878;border:1px solid rgba(194,168,120,.5);padding:8px 15px;border-radius:2px}
.bc{font-size:12px;color:#8c8a86;padding:20px 0 0}.bc a{text-decoration:none}
main{padding:22px 0 40px}
.kick{font-size:11px;letter-spacing:4px;text-transform:uppercase;color:#c2a878;margin:14px 0 12px}
h1{font-family:'Cormorant Garamond',serif;font-weight:600;font-size:clamp(30px,6vw,46px);line-height:1.06;margin-bottom:14px}
h2{font-family:'Cormorant Garamond',serif;font-weight:500;font-size:clamp(22px,4vw,30px);margin:34px 0 12px}
h3{font-size:16px;font-weight:600;margin:22px 0 6px;color:#eae7e1}
p{margin:0 0 15px;color:#cfccc5}p.lead{font-size:18px;color:#d7d4cd}
ul{margin:0 0 15px 20px;color:#cfccc5}li{margin:0 0 7px}
b,strong{color:#eae7e1;font-weight:500}
.card{border:1px solid rgba(234,231,225,.12);border-radius:12px;padding:22px 24px;background:#0e0e11;margin:18px 0}
.cta{display:inline-block;margin:8px 0;padding:15px 30px;background:#c2a878;color:#171308;font-weight:700;font-size:12px;letter-spacing:2px;text-transform:uppercase;text-decoration:none;border-radius:3px}
.meta{display:flex;flex-wrap:wrap;gap:8px 20px;font-size:13px;color:#8c8a86;margin:16px 0}
.meta b{color:#eae7e1}
details{border-bottom:1px solid rgba(234,231,225,.12)}
summary{cursor:pointer;list-style:none;padding:15px 0;font-family:'Cormorant Garamond',serif;font-size:18px}
summary::-webkit-details-marker{display:none}
details p{padding:0 0 15px;font-size:14.5px}
footer{border-top:1px solid rgba(234,231,225,.12);padding:30px 0;font-size:13px;color:#8c8a86}
footer a{text-decoration:none;margin-right:16px;display:inline-block;margin-bottom:6px}
.upd{font-size:12px;color:#6b6862;margin-top:26px}"""

FOOT_LINKS = [
 ("/","Home"),("/federico-galliani/","Federico Galliani"),
 ("/black-and-grey-portrait-realism/","The craft"),("/grey-wash-longevity/","Grey wash that heals"),
 ("/milwaukee-tattoo-arts-convention-2026/","Convention weekend"),
 ("/chicago-portrait-realism-masterclass/","From Chicago"),("/madison-portrait-realism-masterclass/","From Madison"),
 ("/minneapolis-portrait-realism-masterclass/","From Minneapolis"),("/apply/","Apply"),("/privacy/","Privacy"),
]

def page(slug,title,desc,kicker,h1,body,graph,noindex=False):
    canon=SITE+"/"+(slug+"/" if slug else "")
    foot="".join('<a href="%s">%s</a>'%(u,n) for u,n in FOOT_LINKS if u.strip("/")!=slug)
    robots='<meta name="robots" content="noindex,follow">' if noindex else '<meta name="robots" content="index,follow">'
    graph_full=[website()]+graph
    html=f"""<!DOCTYPE html><html lang="en-US"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
{robots}
<link rel="canonical" href="{canon}">
<meta name="geo.region" content="US-WI">
<meta property="og:title" content="{title}"><meta property="og:description" content="{desc}">
<meta property="og:type" content="website"><meta property="og:url" content="{canon}">
<meta property="og:image" content="{SITE}/assets/og-academy.jpg"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:image" content="{SITE}/assets/og-academy.jpg">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;1,500&family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<style>{CSS}</style>
<script type="application/ld+json">{json.dumps({"@context":"https://schema.org","@graph":graph_full},separators=(',',':'))}</script>
</head><body>
<nav><a class="lg" href="/" translate="no">PORTRAIT&nbsp;REALISM&nbsp;ACADEMY</a><a class="ap" href="/apply/">Apply</a></nav>
<div class="wrap"><div class="bc"><a href="/">Home</a> › {h1}</div></div>
<main class="wrap">
<div class="kick">{kicker}</div>
<h1>{h1}</h1>
{body}
<p class="upd">Last updated {UPDATED}.</p>
</main>
<footer class="wrap"><div>{foot}</div>
<p style="margin-top:14px">Portrait Realism Academy · Milwaukee · Oct 6–8, 2026 · <a href="https://www.instagram.com/federicogallianitattoo/">@federicogallianitattoo</a></p>
</footer></body></html>"""
    d=os.path.join(os.path.dirname(__file__), slug)
    os.makedirs(d,exist_ok=True)
    open(os.path.join(d,"index.html"),"w").write(html)
    return canon

CTA='<p><a class="cta" href="/apply/">Claim one of the 10 spots →</a></p>'
pages_built=[]

# 1) INSTRUCTOR ENTITY
body=f"""
<p class="lead">Federico Galliani — known as <b>"Portrait KID"</b> — is an Italian black &amp; grey portrait-realism tattoo artist and co-owner of <b>White Label Tattoo</b>. He teaches the Portrait Realism Academy in Milwaukee, October 6–8, 2026.</p>
<div class="meta"><span><b>12 years</b> tattooing</span><span><b>~20</b> U.S. conventions</span><span><b>First places</b>: Baltimore · Chicago</span><span><b>52K</b> on Instagram</span></div>
<h2>Background</h2>
<p>Federico has been tattooing for twelve years. He started in a studio in Seregno, in the Milan area — a six-month apprenticeship, after which he was selected among the studio's best interns and kept on for over two and a half years. He worked across several studios before opening his own in 2019, and today, for seven years, he has been co-owner and resident artist at White Label Tattoo.</p>
<h2>Style &amp; method</h2>
<p>His work is built on <b>realistic black &amp; grey portraits</b> using true <b>grey wash</b> — grey made from black ink diluted with water, not grey ink — with an obsessive attention to detail. His defining principle: a portrait is judged not by how it looks the day it's done, but by <b>how it holds and ages in the skin</b>. Longevity is central to everything he tattoos, and it is the core of what he teaches.</p>
<h2>Awards &amp; conventions</h2>
<ul>
<li>Award-winning on the U.S. convention circuit, with multiple <b>first-place</b> awards — including <b>Baltimore</b> and <b>Chicago</b> (a Female XL, a portrait of Sub-Zero from Mortal Kombat on a client's thigh).</li>
<li>Awards in Italy at <b>Milan</b> and <b>Bergamo</b>.</li>
<li>Roughly <b>twenty U.S. conventions</b>: Milwaukee, Chicago, Baltimore, Kansas City, Minneapolis, New York and more. In Europe: Brussels and Bern. In Italy: Milan, one of the world's biggest.</li>
</ul>
<h2>Press &amp; recognition</h2>
<ul>
<li><b>Global Tattoo Magazine</b> (2019)</li>
<li><b>Ink People</b> — Polish tattoo magazine, cover (2022)</li>
<li><b>iNKPPL</b> — "Ink, Passion and Patience" (2024)</li>
<li>Sponsored by <b>Eclipse Tattoo Ink</b></li>
</ul>
<p>He speaks English and Italian. See his portfolio on Instagram <a href="https://www.instagram.com/federicogallianitattoo/">@federicogallianitattoo</a>.</p>
{CTA}
"""
u=page("federico-galliani",
 "Federico Galliani — Black & Grey Portrait Realism Tattoo Artist (\"Portrait KID\")",
 "Federico Galliani (\"Portrait KID\") is an Italian black & grey portrait-realism tattoo artist, co-owner of White Label Tattoo, award-winning on the U.S. convention circuit (first places Baltimore & Chicago). Instructor of the Portrait Realism Academy, Milwaukee 2026.",
 "The instructor","Federico Galliani",body,
 [NODE_PERSON,NODE_WHITELAB,NODE_COURSE,NODE_ACADEMY,NODE_SOL,
  webpage(SITE+"/federico-galliani/","Federico Galliani — Portrait Realism Tattoo Artist","Bio, style, awards and conventions of Federico Galliani."),
  crumb(SITE+"/federico-galliani/","Federico Galliani")])
pages_built.append(("federico-galliani/","2026-10-01","0.8"))

# 2) PILLAR — the craft & curriculum
body=f"""
<p class="lead">Black &amp; grey portrait realism is the art of rebuilding a human face in the skin using only diluted black. This is what the Portrait Realism Academy teaches over three days — and how it's structured.</p>
<h2>What black &amp; grey portrait realism actually is</h2>
<p>No colour. Every tone — from the brightest catch-light to the deepest shadow — is built from <b>black ink and water</b>. The realism lives in the control of values: reading a reference correctly, mapping its tones, and laying them down so contrast stays readable once the tattoo heals and settles. Done well, a portrait looks like a photograph in the skin; done without a system, it flattens into grey within a couple of years.</p>
<h2>The three days</h2>
<h3>Day 1 — Foundations</h3>
<p>The grey-wash system from the ground up: reading reference, values and tone mapping, mixing black with water, machine and needle setup (mags, bugpins, shading order), and how to build contrast that survives healing.</p>
<h3>Day 2 — Live demonstration</h3>
<p>Federico tattoos a full portrait in front of the group, narrating every decision — layering, saturation, skin tones, highlights, and the details that separate a good portrait from a great one.</p>
<h3>Day 3 — Supervised practice</h3>
<p>You work under Federico's direct supervision, with real-time feedback on your dilution, needle angle and pressure. This hands-on day is the difference between a seminar you <em>watch</em> and a masterclass you <em>execute</em>.</p>
<h2>Who it's for</h2>
<p>Intermediate and advanced tattoo artists who already tattoo and want to specialize in black &amp; grey portrait realism. Taught in English. Ten spots only.</p>
<h2>Questions artists ask</h2>
<details><summary>What needles and machines does portrait realism use?</summary><p>Mostly magnum and bugpin configurations for smooth shading, with a disciplined shading order. Day 1 covers setup in detail; you bring your own machine.</p></details>
<details><summary>What is grey wash?</summary><p>Grey made by diluting black ink with water rather than using pre-mixed grey ink — it gives smoother, more controllable transitions and, mixed correctly, ages better. See <a href="/grey-wash-longevity/">grey wash that heals</a>.</p></details>
{CTA}
"""
page("black-and-grey-portrait-realism",
 "Black & Grey Portrait Realism — The Craft & 3-Day Curriculum | Portrait Realism Academy",
 "What black & grey portrait realism is, and the 3-day curriculum of the Portrait Realism Academy: grey-wash foundations, a full live demo, and supervised hands-on practice. Milwaukee, Oct 6–8 2026.",
 "The craft","Black &amp; grey portrait realism",body,
 [NODE_PERSON,NODE_COURSE,NODE_ACADEMY,NODE_SOL,
  {"@type":"TechArticle","@id":SITE+"/black-and-grey-portrait-realism/#article","headline":"Black & grey portrait realism — the craft and 3-day curriculum","author":{"@id":FEDERICO},"about":"black and grey portrait realism tattooing","inLanguage":"en"},
  webpage(SITE+"/black-and-grey-portrait-realism/","Black & grey portrait realism — craft & curriculum","The style, technique and 3-day curriculum."),
  crumb(SITE+"/black-and-grey-portrait-realism/","Black & grey portrait realism"),
  {"@type":"FAQPage","mainEntity":[
    {"@type":"Question","name":"What is grey wash in tattooing?","acceptedAnswer":{"@type":"Answer","text":"Grey wash is grey made by diluting black ink with water rather than using pre-mixed grey ink, giving smoother transitions that, mixed correctly, age better."}},
    {"@type":"Question","name":"Who is the black & grey portrait realism masterclass for?","acceptedAnswer":{"@type":"Answer","text":"Intermediate and advanced tattoo artists who want to specialize in black & grey portrait realism. Taught in English, 10 spots."}}]}])
pages_built.append(("black-and-grey-portrait-realism/","2026-10-01","0.7"))

# 3) GREY WASH LONGEVITY — citation bait
body=f"""
<p class="lead">The hardest part of black &amp; grey isn't making it look good on day one. It's making it still read in ten years. This is the method the Academy is built around.</p>
<h2>Why black &amp; grey portraits fade into grey</h2>
<p>A portrait that looks razor-sharp the day it's tattooed can turn into a soft grey smudge within a couple of years: the black lightens, the contrast collapses, and the features stop reading. The usual causes are contrast built too subtly to survive the skin's healing, and grey tones laid without enough separation between values.</p>
<h2>True grey wash — black and water</h2>
<p>Federico builds his greys from <b>black ink diluted with water</b> — not pre-mixed grey ink. Controlled dilution gives a wider, cleaner range of values and more predictable healing. The method is about <b>building contrast that survives</b>: holding the darkest darks opaque, protecting the highlights, and spacing the mid-tones so the face still separates after the tattoo settles.</p>
<h2>How to judge a black &amp; grey portrait</h2>
<ul>
<li>Not fresh — <b>healed</b>. Fresh work always looks contrasty; the real test is how it reads once it has settled.</li>
<li>Value separation: can you still tell the planes of the face apart from across the room?</li>
<li>Opaque darks and protected highlights — the two anchors that keep a portrait legible as it ages.</li>
</ul>
<p>This longevity-first approach is the throughline of all three days of the <a href="/black-and-grey-portrait-realism/">masterclass</a>.</p>
<h2>Questions</h2>
<details><summary>Does diluting ink with water make tattoos fade faster?</summary><p>Not when it's done with control — the point of the method is greys that heal predictably and hold their separation over time.</p></details>
<details><summary>Can you learn to make black &amp; grey heal better?</summary><p>Yes — it's a system of value control and contrast, not innate talent. That system is exactly what this masterclass teaches.</p></details>
{CTA}
"""
page("grey-wash-longevity",
 "Grey Wash That Heals — Black & Grey Tattoos Built to Last | Portrait Realism Academy",
 "Why black & grey portraits fade — and the true grey-wash method (black diluted with water) that keeps them readable as they heal and age. The longevity-first system taught at the Portrait Realism Academy.",
 "The method","Grey wash that heals",body,
 [NODE_PERSON,NODE_COURSE,NODE_ACADEMY,
  {"@type":"HowTo","@id":SITE+"/grey-wash-longevity/#howto","name":"How to build black & grey portraits that heal well","step":[
     {"@type":"HowToStep","name":"Dilute black with water","text":"Build greys from black ink diluted with water for a wider, cleaner range of values."},
     {"@type":"HowToStep","name":"Anchor the darks","text":"Keep the darkest darks opaque so the portrait keeps a reference point as it heals."},
     {"@type":"HowToStep","name":"Protect the highlights","text":"Preserve the brightest highlights untouched to hold contrast over time."},
     {"@type":"HowToStep","name":"Space the mid-tones","text":"Separate mid-values enough that the planes of the face still read after settling."}]},
  webpage(SITE+"/grey-wash-longevity/","Grey wash that heals","The longevity-first grey-wash method."),
  crumb(SITE+"/grey-wash-longevity/","Grey wash that heals"),
  {"@type":"FAQPage","mainEntity":[
    {"@type":"Question","name":"Why do black and grey tattoos fade into grey?","acceptedAnswer":{"@type":"Answer","text":"Usually because contrast was built too subtly to survive healing, or grey values were laid without enough separation. Opaque darks, protected highlights and spaced mid-tones keep a portrait legible as it ages."}},
    {"@type":"Question","name":"What is true grey wash?","acceptedAnswer":{"@type":"Answer","text":"Grey made from black ink diluted with water rather than pre-mixed grey ink — a wider, more controllable value range that, done correctly, heals more predictably."}}]}])
pages_built.append(("grey-wash-longevity/","2026-10-01","0.7"))

# 4) CONVENTION WEDGE
body=f"""
<p class="lead">The Portrait Realism Academy runs <b>October 6–8, 2026</b> in the Milwaukee area — the days right before the <b>Milwaukee Tattoo Arts Convention</b> (Villain Arts), October 9–11, 2026 at the Baird Center. Learn first, then work the floor.</p>
<div class="card">
<h3>The masterclass — Oct 6–8</h3>
<p>3 days, 10 spots, black &amp; grey portrait realism with Federico Galliani at SOL Studios, Hales Corners (SW Milwaukee metro). <a href="/">Details &amp; apply →</a></p>
</div>
<div class="card">
<h3>The convention — Oct 9–11</h3>
<p>The <b>Milwaukee Tattoo Arts Convention</b> is organized by <b>Villain Arts</b> at the Baird Center, downtown Milwaukee — around 400 artists, seminars and contests. It is an independent event; the Academy is not part of it and does not organize it. Official info: <a href="https://villainarts.com/shows/milwaukee-wi/" rel="nofollow noopener">villainarts.com</a>.</p>
</div>
<h2>Why the timing works for traveling artists</h2>
<p>One trip to Milwaukee covers both: three focused days of portrait-realism training, then a weekend on the convention floor. If you were already planning to attend the convention, the Academy is the reason to arrive a few days early.</p>
<div class="meta"><span>Venue: <b>SOL Studios</b>, Hales Corners WI</span><span>Airport: <b>MKE</b> ~10 mi / 20 min</span><span>Downtown Milwaukee: ~14 mi / 18 min</span></div>
{CTA}
"""
page("milwaukee-tattoo-arts-convention-2026",
 "Milwaukee Tattoo Arts Convention 2026 + Portrait Realism Masterclass (Oct 6–8)",
 "The Portrait Realism Academy runs Oct 6–8, 2026, the days before the Milwaukee Tattoo Arts Convention (Villain Arts, Oct 9–11). Learn black & grey portrait realism, then work the convention floor.",
 "Convention weekend","Milwaukee Tattoo Arts Convention 2026",body,
 [NODE_PERSON,NODE_COURSE,NODE_ACADEMY,NODE_SOL,
  {"@type":"Event","@id":SITE+"/milwaukee-tattoo-arts-convention-2026/#convention","name":"Milwaukee Tattoo Arts Convention","startDate":"2026-10-09","endDate":"2026-10-11","eventStatus":"https://schema.org/EventScheduled","organizer":{"@type":"Organization","name":"Villain Arts","url":"https://villainarts.com/"},"location":{"@type":"Place","name":"Baird Center","address":{"@type":"PostalAddress","addressLocality":"Milwaukee","addressRegion":"WI","addressCountry":"US"}},"sameAs":"https://villainarts.com/shows/milwaukee-wi/"},
  webpage(SITE+"/milwaukee-tattoo-arts-convention-2026/","Milwaukee Tattoo Arts Convention 2026 + masterclass","The masterclass runs the days before the convention."),
  crumb(SITE+"/milwaukee-tattoo-arts-convention-2026/","Milwaukee Tattoo Arts Convention 2026")])
pages_built.append(("milwaukee-tattoo-arts-convention-2026/","2026-10-01","0.7"))

# 5-7) GEO SPOKES
def geo(slug,city,h1,dist_line,scene,extra,fa):
    body=f"""
<p class="lead">{dist_line}</p>
<h2>Getting to the masterclass from {city}</h2>
<p>{scene}</p>
<div class="meta"><span>Venue: <b>SOL Studios</b>, 11000 W Janesville Rd, Hales Corners WI 53130</span></div>
<h2>Why come from {city}</h2>
<p>{extra} And the masterclass opens the weekend of the <a href="/milwaukee-tattoo-arts-convention-2026/">Milwaukee Tattoo Arts Convention</a> (Oct 9–11) — one trip, both.</p>
<p>Three days, ten spots, black &amp; grey portrait realism with <a href="/federico-galliani/">Federico Galliani</a>. October 6–8, 2026.</p>
<details><summary>{fa[0][0]}</summary><p>{fa[0][1]}</p></details>
<details><summary>{fa[1][0]}</summary><p>{fa[1][1]}</p></details>
{CTA}
"""
    origin={"@type":"Place","name":city,"address":{"@type":"PostalAddress","addressLocality":city.split(",")[0],"addressCountry":"US"}}
    page(slug,
      f"Portrait Realism Tattoo Masterclass for {city} Artists — Milwaukee, Oct 6–8 2026",
      f"{dist_line} A 3-day black & grey portrait-realism masterclass with Federico Galliani at SOL Studios, Hales Corners WI — the weekend of the Milwaukee Tattoo Arts Convention.",
      f"Traveling in · {city}",h1,body,
      [NODE_PERSON,NODE_COURSE,NODE_ACADEMY,NODE_SOL,origin,
       webpage(SITE+"/"+slug+"/",f"Portrait realism masterclass for {city} artists","Travel details and the masterclass for artists from "+city+"."),
       crumb(SITE+"/"+slug+"/",f"From {city}"),
       {"@type":"FAQPage","mainEntity":[
         {"@type":"Question","name":fa[0][0],"acceptedAnswer":{"@type":"Answer","text":fa[0][1]}},
         {"@type":"Question","name":fa[1][0],"acceptedAnswer":{"@type":"Answer","text":fa[1][1]}}]}])
    pages_built.append((slug+"/","2026-10-01","0.6"))

geo("chicago-portrait-realism-masterclass","Chicago",
 "Portrait realism masterclass — for Chicago artists",
 "From Chicago, the Portrait Realism Academy is about a 90-minute drive north — roughly 87 miles up I-94 to Hales Corners, in the Milwaukee metro.",
 "It's an easy up-and-back or an overnight: about 87 miles / 90 minutes by car straight up I-94. O'Hare (ORD) is roughly 77 miles from the venue if you're connecting a flight.",
 "Chicago has one of the deepest black &amp; grey realism scenes in the Midwest — and Federico has taken a first-place award in Chicago.",
 [("How far is the masterclass from Chicago?","About 87 miles / roughly a 90-minute drive up I-94 from Chicago to SOL Studios in Hales Corners, WI."),
  ("Is it worth the trip from Chicago?","It's a short drive for three days of hands-on portrait-realism training, and it lands the weekend of the Milwaukee Tattoo Arts Convention.")])

geo("madison-portrait-realism-masterclass","Madison",
 "Portrait realism masterclass — for Madison artists",
 "From Madison, the Portrait Realism Academy is a straight shot east — about 78 miles / an hour and twenty minutes on I-94 to Hales Corners.",
 "Roughly 78 miles / 1 hour 20 minutes due east on I-94. Close enough to commute in daily or stay over for the three days.",
 "There's no dedicated portrait-realism intensive in Madison — this is the nearest serious black &amp; grey masterclass, with a Milwaukee-area venue.",
 [("How far is the masterclass from Madison?","About 78 miles / roughly 1 hour 20 minutes east on I-94 to SOL Studios in Hales Corners, WI."),
  ("Can I commute from Madison each day?","Yes — it's close enough to drive in daily, or stay near the venue for the three days.")])

geo("minneapolis-portrait-realism-masterclass","Minneapolis",
 "Portrait realism masterclass — for Minneapolis & Twin Cities artists",
 "From Minneapolis, the Portrait Realism Academy is a short nonstop flight — about 75 minutes MSP→MKE, then 15 minutes to the venue — or roughly a 5-hour drive.",
 "Fly MSP→MKE in about 75 minutes; Milwaukee Mitchell (MKE) is only ~10 miles / 20 minutes from SOL Studios. By car it's roughly 337 miles / about 5 hours.",
 "The Twin Cities are a strong stop on the convention circuit, and this is the closest 3-day portrait-realism masterclass to fly in for.",
 [("How do I get to the masterclass from Minneapolis?","Fly MSP→MKE (~75 min) then ~20 minutes to the venue, or drive ~337 miles (~5 hours)."),
  ("Is it a fly-in or a drive?","Either works — a quick nonstop to MKE is the easy option; the airport is ~20 minutes from SOL Studios.")])

# 8) APPLY
body=f"""
<p class="lead">Ten spots. $2,000. October 6–8, 2026, in the Milwaukee area. Apply below and we reply personally with availability and the deposit link.</p>
<div class="card">
<form action="https://formsubmit.co/marcoetingcrd@gmail.com" method="POST">
<input type="hidden" name="_subject" value="New Academy application (apply page)">
<input type="hidden" name="_template" value="table">
<input type="hidden" name="_captcha" value="false">
<input type="hidden" name="_next" value="https://portraitrealismacademy.com/thanks/">
<p><input name="first" placeholder="First name" required style="width:100%;padding:12px;margin:6px 0;background:#0a0a0c;border:1px solid rgba(234,231,225,.15);color:#eae7e1;border-radius:6px">
<input name="last" placeholder="Last name" required style="width:100%;padding:12px;margin:6px 0;background:#0a0a0c;border:1px solid rgba(234,231,225,.15);color:#eae7e1;border-radius:6px">
<input type="email" name="email" placeholder="Email" required style="width:100%;padding:12px;margin:6px 0;background:#0a0a0c;border:1px solid rgba(234,231,225,.15);color:#eae7e1;border-radius:6px">
<input name="instagram" placeholder="Instagram @handle" style="width:100%;padding:12px;margin:6px 0;background:#0a0a0c;border:1px solid rgba(234,231,225,.15);color:#eae7e1;border-radius:6px">
<textarea name="message" placeholder="Tell us about your work / why you're applying" style="width:100%;padding:12px;margin:6px 0;min-height:90px;background:#0a0a0c;border:1px solid rgba(234,231,225,.15);color:#eae7e1;border-radius:6px"></textarea></p>
<button class="cta" type="submit" style="border:0;cursor:pointer">Submit application</button>
</form>
</div>
<p style="font-size:12px;color:#8c8a86">A $500 deposit confirms your spot once your application is accepted. Spots are limited to 10.</p>
"""
page("apply",
 "Apply — Portrait Realism Academy (10 spots, Milwaukee Oct 6–8 2026)",
 "Apply for one of the 10 spots at the Portrait Realism Academy — a 3-day black & grey portrait-realism masterclass with Federico Galliani. Milwaukee, October 6–8, 2026. $2,000.",
 "Apply","Claim one of the 10 spots",body,
 [NODE_COURSE,NODE_ACADEMY,NODE_SOL,
  webpage(SITE+"/apply/","Apply for the Portrait Realism Academy","Application form for the masterclass."),
  crumb(SITE+"/apply/","Apply")])
pages_built.append(("apply/","2026-10-01","0.9"))

# 9) THANKS (noindex)
page("thanks",
 "Thanks — Portrait Realism Academy",
 "Your application has been received.",
 "Thank you","Application received",
 f'<p class="lead">Thanks — your application is in. We reply personally with availability and the deposit link.</p><p>In the meantime, meet <a href="/federico-galliani/">your instructor</a> or read about <a href="/grey-wash-longevity/">the grey-wash method</a>.</p>{CTA}',
 [webpage(SITE+"/thanks/","Thanks","Application received.")], noindex=True)

# ---- sitemap.xml (indexable pages only) ----
urls=[("/","2026-10-01","1.0")]+pages_built
sm=['<?xml version="1.0" encoding="UTF-8"?>','<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for loc,lm,pr in urls:
    sm.append(f"<url><loc>{SITE}/{loc.lstrip('/')}</loc><lastmod>{lm}</lastmod><priority>{pr}</priority></url>")
sm.append("</urlset>")
open(os.path.join(os.path.dirname(__file__),"sitemap.xml"),"w").write("\n".join(sm))
print("Built pages:",[u for u,_,_ in urls])
print("sitemap urls:",len(urls))
