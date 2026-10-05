"""Builds the Elia Living multi-page site into ./site from data.py."""
import html, os, json
from urllib.parse import quote
from data import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..") if os.path.basename(os.path.dirname(os.path.abspath(__file__))) == "_source" else os.path.join(os.path.dirname(__file__), "site")
E = html.escape

# ------------------------------------------------------------------ helpers
def cf(i, w=1600):
    return f"https://imagedelivery.net/{ACC}/{i}/w={w},quality=82,format=auto"
def cf_raw(i):
    return f"https://imagedelivery.net/{ACC}/{i}/format=auto"
def cdn(name):
    return CDN + quote(name)

FB = "onerror=\"if(this.dataset.fb){this.src=this.dataset.fb;this.removeAttribute('data-fb')}\""

def pimg(i, w=1600, alt="", cls="", lazy=True, extra=""):
    l = 'loading="lazy" ' if lazy else 'fetchpriority="high" '
    c = f' class="{cls}"' if cls else ""
    return f'<img src="{cf(i,w)}" data-fb="{cf_raw(i)}" {FB} alt="{E(alt)}" {l}decoding="async"{c} {extra}>'

def cimg(name, alt="", cls="", lazy=True, extra=""):
    l = 'loading="lazy" ' if lazy else 'fetchpriority="high" '
    c = f' class="{cls}"' if cls else ""
    return f'<img src="{cdn(name)}" alt="{E(alt)}" {l}decoding="async"{c} {extra}>'

ARROW = '<svg class="arrow" viewBox="0 0 22 10" aria-hidden="true"><path d="M0 5h20.5M16.5 1l4 4-4 4" fill="none" stroke="currentColor" stroke-width="1"/></svg>'
ARROW_L = '<svg viewBox="0 0 22 10" aria-hidden="true"><path d="M22 5H1.5M5.5 1l-4 4 4 4" fill="none" stroke="currentColor" stroke-width="1"/></svg>'
ARROW_R = '<svg viewBox="0 0 22 10" aria-hidden="true"><path d="M0 5h20.5M16.5 1l4 4-4 4" fill="none" stroke="currentColor" stroke-width="1"/></svg>'
EXT = '<svg viewBox="0 0 10 10" width="9" height="9" aria-hidden="true"><path d="M2 8 8 2M3.5 2H8v4.5" fill="none" stroke="currentColor" stroke-width="1"/></svg>'
CHAT = '<svg viewBox="0 0 20 20" aria-hidden="true"><path d="M10 2.2a7.8 7.8 0 0 0-6.7 11.8L2.2 17.8l3.9-1.1A7.8 7.8 0 1 0 10 2.2Z" fill="none" stroke="currentColor" stroke-width="1.2"/></svg>'

def eur(n): return "€" + f"{n:,}"
def wa(text=""): return f"https://wa.me/{WA}" + (f"?text={quote(text)}" if text else "")

def wordmark(tag=True):
    t = '<small>Trusted Real Estate Advisors</small>' if tag else ""
    return f'<span class="wordmark" aria-label="Elia Living"><b>ELIA LIVING</b>{t}</span>'

ICONS = {
 "bed": '<path d="M3 20v-9h22v9M3 16h22M6 11V7h7v4M15 11V7h7v4M3 20v2M25 20v2"/>',
 "bath": '<path d="M4 14h20v3a5 5 0 0 1-5 5H9a5 5 0 0 1-5-5v-3ZM7 14V6a2 2 0 0 1 4 0M8 22l-1 2M20 22l1 2"/>',
 "built": '<path d="M4 24V10l10-6 10 6v14H4ZM11 24v-7h6v7"/>',
 "plot": '<path d="M4 4h20v20H4zM4 10h4M20 24v-4M14 4v3"/>',
 "pool": '<path d="M3 19c2 0 3-1.4 5.5-1.4S11 19 14 19s3.5-1.4 5.5-1.4S22 19 25 19M3 23c2 0 3-1.4 5.5-1.4S11 23 14 23s3.5-1.4 5.5-1.4S22 23 25 23M9 16V5a2 2 0 0 1 4 0M17 16V5a2 2 0 0 1 4 0M9 9h8M9 13h8"/>',
 "sea": '<path d="M3 14c3 0 4-2 7-2s4 2 7 2 4-2 7-2M3 19c3 0 4-2 7-2s4 2 7 2 4-2 7-2M14 9a4 4 0 0 0-4-4M18 5l2-2M14 5V2"/>',
 "spa": '<path d="M14 24c-5 0-8-3-8-7 3 0 6 1.5 8 4 2-2.5 5-4 8-4 0 4-3 7-8 7ZM14 21c-2-3-2-7 0-11 2 4 2 8 0 11Z"/>',
 "lift": '<path d="M7 3h14v22H7zM12 9l2-2 2 2M12 19l2 2 2-2"/>',
 "garage": '<path d="M3 24V11l11-7 11 7v13M7 24v-9h14v9M7 18h14M7 21h14"/>',
 "solar": '<path d="M5 20 8 10h12l3 10H5ZM14 10v10M6.5 15h15M14 3v3M6 5l2 2M22 5l-2 2"/>',
}
AMEN_LABEL = {"pool":"Pool","sea":"Sea views","spa":"Spa","lift":"Lift","garage":"Garage","solar":"Solar energy"}
def icon(k): return f'<svg viewBox="0 0 28 28" aria-hidden="true">{ICONS[k]}</svg>'

NAV = [("properties.html","Properties","properties"),("services.html","Services","services"),("costa-blanca.html","Costa Blanca","costa"),("about.html","About","about"),("contact.html","Contact","contact")]

BOOT = """<script>(function(d){var r=d.documentElement;r.classList.add('js');if(!window.matchMedia('(prefers-reduced-motion: reduce)').matches){r.classList.add('motion');try{if(sessionStorage.getItem('el-nav'))r.classList.add('is-arriving');else if(r.dataset.page==='home'&&!sessionStorage.getItem('el-intro')){r.classList.add('is-arriving','intro');sessionStorage.setItem('el-intro','1')}}catch(e){}}})(document)</script>"""

def head(title, desc, page):
    return f"""<!doctype html>
<html lang="en" data-page="{page}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<meta name="theme-color" content="#0F1113">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preconnect" href="https://imagedelivery.net" crossorigin>
<link rel="preconnect" href="https://cdn-tesoro.fra1.digitaloceanspaces.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bodoni+Moda:ital,opsz,wght@0,6..96,400..600;1,6..96,400..500&family=Jost:wght@300..500&display=swap">
<link rel="stylesheet" href="assets/site.css">
{BOOT}
</head>"""

def header(active, tone):
    links = "".join(f'<a href="{h}"{" aria-current=\"page\"" if k==active else ""}>{t}</a>' for h,t,k in NAV)
    menu_items = [("index.html","Home","home","Welcome home"),("properties.html","Properties","properties","Residences for sale"),("services.html","Services","services","Find · build · design · live"),("costa-blanca.html","Costa Blanca","costa","Life on the coast"),("about.html","About","about","The people behind Elia"),("contact.html","Contact","contact","Book a consultation")]
    lis = "".join(f'<li><a href="{h}" data-preview="{k}" style="--i:{i}"{" aria-current=\"page\"" if k==active else ""}>{t}<span class="sub">{s}</span></a></li>' for i,(h,t,k,s) in enumerate(menu_items))
    lis += f'<li><a href="{GUIDES}" target="_blank" rel="noopener" style="--i:6" data-preview="guides">Guides <span class="sub">Buying in Spain ↗</span></a></li>'
    prev = [("home", pimg("15c0003e-49bf-49aa-af81-5a16178d2800", 900)), ("properties", pimg("0d1571a9-702b-4155-33b5-025b0ac2e200", 900)),
            ("services", cimg("PREMIUM-INFINITY-POOL-WITH-A-VIEW.jpg")), ("costa", cimg("Costa-Blanca-Hero-copy-scaled-1.jpg")),
            ("about", cimg("ac8d1e52-415e-4dc1-8ead-e4603c58ef16 (1).jpg")), ("contact", pimg("b0dfe48e-bd91-4d5f-2c7a-6b4c08e0f900", 900)),
            ("guides", cimg("Secondsection_villa_front.jpg"))]
    pv = "".join(x.replace("<img ", f'<img data-key="{k}" ' + ('class="on" ' if k==(active or "home") else ""), 1) for k,x in prev)
    return f"""<div class="curtain" aria-hidden="true">{wordmark(False)}</div>
<a class="sr-only" href="#main">Skip to content</a>
<header class="site-header">
 <div class="wrap site-header__inner">
  <a href="index.html" aria-label="Elia Living home">{wordmark()}</a>
  <nav class="nav" aria-label="Primary">{links}</nav>
  <div class="header-actions">
   <a class="btn header-cta" href="contact.html#consultation">Book a consultation</a>
   <button class="menu-btn" aria-expanded="false" aria-controls="menu"><span class="menu-btn__lines" aria-hidden="true"></span><span>Menu</span></button>
  </div>
 </div>
</header>
<div class="menu" id="menu" aria-hidden="true">
 <ul class="menu__links">{lis}</ul>
 <aside class="menu__aside">
  <div class="menu__preview">{pv}</div>
  <div class="menu__contact">
   <span class="label">Talk to us</span>
   <a href="tel:{PHONE_TEL}">{PHONE}</a>
   <a href="mailto:{EMAIL}">{EMAIL}</a>
   <a href="{wa()}" target="_blank" rel="noopener">WhatsApp</a>
   <span>{ADDRESS_LINES[0]}, Jávea</span>
  </div>
 </aside>
</div>
<main id="main">"""

def footer():
    soc = "".join(f'<li><a href="{u}" target="_blank" rel="noopener">{n}</a></li>' for n,u in SOCIAL)
    legal = "".join(f'<a href="{u}" target="_blank" rel="noopener">{n}</a>' for n,u in LEGAL)
    return f"""</main>
<footer class="site-footer">
 <div class="wrap">
  <div class="footer__big">
   <a class="display" href="contact.html">Let’s begin {ARROW}</a>
   <p class="lead" style="max-width:34ch">From the first viewing to your first night at home. Personal advice in English, Polish, Spanish, German and Dutch.</p>
  </div>
  <div class="footer__grid">
   <div>
    <h4>Contact</h4>
    <ul>
     <li><a href="tel:{PHONE_TEL}">{PHONE}</a></li>
     <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
     <li><a href="{wa()}" target="_blank" rel="noopener">WhatsApp</a></li>
    </ul>
   </div>
   <div>
    <h4>Office</h4>
    <p>{"<br>".join(ADDRESS_LINES)}</p>
    <p style="margin-top:12px">{HOURS}</p>
   </div>
   <div>
    <h4>Explore</h4>
    <ul>
     <li><a href="properties.html">Properties</a></li>
     <li><a href="services.html">Services</a></li>
     <li><a href="costa-blanca.html">Costa Blanca</a></li>
     <li><a href="about.html">About</a></li>
     <li><a href="{GUIDES}" target="_blank" rel="noopener">Guides {EXT}</a></li>
    </ul>
   </div>
   <div>
    <h4>Never miss an update</h4>
    <p>Exclusive news and market updates, by email.</p>
    <form data-form="newsletter" novalidate>
     <div class="newsletter field">
      <label class="sr-only" for="nl-email">Email address</label>
      <input id="nl-email" name="Email" type="email" placeholder="Your email address" required autocomplete="email">
      <button type="submit" aria-label="Subscribe">{ARROW}</button>
     </div>
     <label class="consent field"><input id="nl-consent" type="checkbox" name="Consent" value="yes" required><span>I accept the <a href="{LEGAL[1][1]}" target="_blank" rel="noopener" style="text-decoration:underline">privacy policy</a> and agree to receive commercial communications.</span></label>
    </form>
    <h4 style="margin-top:28px">Follow</h4>
    <ul style="grid-auto-flow:column;justify-content:start;gap:18px">{soc}</ul>
   </div>
  </div>
  <div class="footer__base">
   <span>© 2026 Elia Living · Trusted Real Estate Advisors · {API}</span>
   <div class="memberships" aria-label="Memberships">
    <img src="https://www.elialiving.es/assets/icons/nar-white.png" alt="REALTOR®" loading="lazy">
    <img src="https://www.elialiving.es/assets/icons/sira-white.png" alt="SIRA — Spanish International Realty Alliance" loading="lazy">
   </div>
   <nav aria-label="Legal">{legal}</nav>
  </div>
 </div>
</footer>
<a class="wa-fab" href="{wa('Hello Elia Living')}" target="_blank" rel="noopener">{CHAT} WhatsApp</a>
<script src="https://cdn.jsdelivr.net/npm/lenis@1.1.18/dist/lenis.min.js" defer></script>
<script src="assets/site.js" defer></script>
</body>
</html>"""

def page(fname, title, desc, pagekey, active, tone, content):
    doc = head(title, desc, pagekey) + f'\n<body data-header="{tone}">\n' + header(active, tone) + content + footer()
    with open(os.path.join(OUT, fname), "w", encoding="utf-8") as f:
        f.write(doc)

def specs_line(p):
    bits = [f"{p['beds']} bedrooms", f"{p['baths']} bathrooms"]
    if p["built"]: bits.append(f"{p['built']} m²")
    return "".join(f"<span>{b}</span>" for b in bits)

def pcard(p, w=1100, tag=True, cursor=True):
    t = f'<span class="pcard__tag">{E(p["status"])}</span>' if (tag and p.get("status")) else ""
    alt_img = pimg(p["imgs"][1], w, alt="", cls="alt") if len(p["imgs"]) > 1 else ""
    cur = ' data-cursor="View"' if cursor else ""
    return f"""<a class="pcard" href="property-{p['slug']}.html"{cur} data-loc="{p['loc']}" data-beds="{p['beds']}" data-price="{p['price']}" data-ref="{p['ref']}" data-name="{E(p['card'])}" data-order="{p['order']}">
 <div class="pcard__media">{t}{pimg(p['imgs'][0], w, alt=p['card'] + ', ' + p['town'], cls='main')}{alt_img}</div>
 <div class="pcard__body">
  <h3 class="pcard__name">{E(p['card'])}</h3>
  <span class="pcard__loc">{E(p['area'])}, {E(p['town'])} · {p['ref']}</span>
  <span class="pcard__price num">{eur(p['price'])}</span>
  <div class="pcard__specs num">{specs_line(p)}</div>
 </div>
</a>"""

# ------------------------------------------------------------------ HOME
def build_home():
    hero = PROP_BY["eli893"]
    fx = PROP_BY["eli279"]
    order = ["eli893","cp40","eli1146","eli283","eli32","eli279"]
    cards = "".join(pcard(PROP_BY[s], 900) for s in order)
    towns = "".join(f'<li class="town"><a href="costa-blanca.html#towns" data-key="{t["key"]}"><span class="town__thumb">{cimg(t["img"], "")}</span><span class="town__name">{t["name"]}</span><span class="town__tag">{t["tag"]}</span></a></li>' for t in TOWNS)
    float_imgs = "".join(cimg(t["img"], "", extra=f'data-key="{t["key"]}"') for t in TOWNS)
    c = f"""
<section class="hero-scene" data-hero-end>
 <div class="hero">
  <div class="hero__media">{pimg(hero['imgs'][0], 2400, alt='Contemporary finca in Balcón al Mar, Jávea', lazy=False)}<div class="hero__shade"></div></div>
  <div class="hero__title">
   <h1 class="display split"><span class="l1" style="display:block">Welcome to your</span><span class="l2 it">Spanish dream.</span></h1>
  </div>
  <div class="hero__meta">
   <span class="where">Boutique real estate · Jávea &amp; the Costa Blanca</span>
   <a class="scroll" href="#intro"><i aria-hidden="true"></i>Scroll</a>
  </div>
  <div class="hero__after"><p class="display it">Elia Living. Welcome home.</p></div>
 </div>
</section>

<section class="statement wrap" id="intro">
 <p class="label" data-reveal>Who we are</p>
 <p class="statement__big" style="margin-top:28px">More than agents. Your personal real estate advisors on the Costa Blanca.</p>
 <div class="statement__cols">
  <div class="facts" data-reveal>
   <div class="fact"><span class="label">Based in</span><b>Jávea, Alicante</b></div>
   <div class="fact"><span class="label">Languages</span><b>EN · PL · ES · DE · NL</b></div>
   <div class="fact"><span class="label">Licensed</span><b>{API}</b></div>
   <div class="fact"><span class="label">Members</span><b>REALTOR® · SIRA</b></div>
  </div>
  <div class="body" data-reveal style="--d:120">
   <p>Elia Living is a premium, boutique agency on the Costa Blanca, where design and lifestyle come together. Founded by investors and experts, we help clients find homes that reflect their values and dreams.</p>
   <p>We guide every client with care, expertise and a personal touch, so each step feels clear, safe and inspiring.</p>
   <a class="link" href="about.html" style="margin-top:12px">Meet the team {ARROW}</a>
  </div>
 </div>
</section>

<section class="hscroll night" aria-label="Selected residences">
 <div class="hscroll__sticky">
  <div class="wrap hscroll__head">
   <div>
    <p class="label">Selected residences</p>
    <h2 class="display h-l" style="margin-top:14px">A lifestyle, <span class="it">not just a location.</span></h2>
   </div>
   <a class="link" href="properties.html">All residences {ARROW}</a>
  </div>
  <div class="hscroll__track">
   {cards}
   <div class="hscroll__end">
    <p class="display h-m">Homes with character and soul, personally selected.</p>
    <a class="btn btn--solid" href="properties.html">Explore properties {ARROW}</a>
   </div>
  </div>
  <div class="hscroll__progress" aria-hidden="true"><i></i></div>
 </div>
</section>

<section class="fx-scene" aria-label="Featured: {E(fx['name'])}">
 <div class="fx">
  <div class="fx__label" aria-hidden="true">
   <span class="a display it" style="position:absolute;top:7%;left:0;right:0">Sea views</span>
   <span class="b display" style="position:absolute;bottom:7%;left:0;right:0">from Racó de Galeno</span>
  </div>
  <div class="fx__img">{pimg(fx['imgs'][0], 2400, alt=fx['name'] + ', Benissa')}</div>
  <div class="fx__shade"></div>
  <div class="fx__caption on-image">
   <div>
    <p class="label" style="color:rgba(255,255,255,.8)">{fx['ref']} · {fx['town']}</p>
    <h2 class="display" style="margin-top:10px">{E(fx['name'])}</h2>
    <div class="meta num" style="margin-top:14px"><span>{eur(fx['price'])}</span><span>{fx['beds']} bedrooms</span><span>{fx['baths']} bathrooms</span><span>{fx['built']} m² built</span><span>{fx['plot']:,} m² plot</span></div>
   </div>
   <a class="btn btn--solid" href="property-{fx['slug']}.html">Discover the villa {ARROW}</a>
  </div>
 </div>
</section>

<section class="section wrap towns" aria-label="Where we work">
 <div style="display:flex;justify-content:space-between;align-items:flex-end;gap:24px;flex-wrap:wrap;margin-bottom:clamp(36px,5vw,70px)">
  <div>
   <p class="label" data-reveal>Where we work</p>
   <h2 class="display h-l split" style="margin-top:14px">The most beautiful corners <span class="it">of the Costa Blanca.</span></h2>
  </div>
  <a class="link" href="costa-blanca.html" data-reveal>Life on the coast {ARROW}</a>
 </div>
 <ul class="towns__list">{towns}</ul>
 <div class="towns__float" aria-hidden="true">{float_imgs}</div>
</section>

<section class="section stone" aria-label="Services">
 <div class="wrap">
  <div style="display:grid;grid-template-columns:repeat(12,1fr);gap:24px;margin-bottom:clamp(40px,6vw,80px)">
   <div style="grid-column:1/-1;max-width:900px">
    <p class="label" data-reveal>Signature service</p>
    <h2 class="display h-l split" style="margin-top:14px">Four ways we turn <span class="it">keys into dreams.</span></h2>
   </div>
  </div>
  <div class="svc4">
   <a href="services.html#properties" data-reveal><h3>Properties</h3><p>Handpicked homes, including off-market villas, with viewings, financing, legal and tax guidance.</p>{ARROW}</a>
   <a href="services.html#construction" data-reveal style="--d:90"><h3>Construction</h3><p>End-to-end project management, from permits and planning to final delivery.</p>{ARROW}</a>
   <a href="services.html#design" data-reveal style="--d:180"><h3>Design</h3><p>Turnkey interiors, home staging and architectural consultations.</p>{ARROW}</a>
   <a href="services.html#concierge" data-reveal style="--d:270"><h3>Concierge</h3><p>Relocation, schools, doctors and trusted services, from day one.</p>{ARROW}</a>
  </div>
 </div>
</section>

<section class="section wrap" aria-label="Client story">
 <div class="quote">
  <blockquote data-reveal>Moving to Spain felt calm and exciting thanks to Elia’s support. They took care of everything, from finding our dream home to helping us choose the right school for our kids.</blockquote>
  <cite data-reveal style="--d:150">Marek J., Warsaw</cite>
 </div>
</section>

<section class="invite on-image" aria-label="Book a consultation">
 <div class="invite__bg" data-parallax=".14">{cimg("Perfect_air_view_of_pool_area.jpg", "Aerial view of a villa pool area on the Costa Blanca")}</div>
 <div class="wrap">
  <p class="label" style="color:rgba(255,255,255,.75)" data-reveal>Vision &amp; mission</p>
  <h2 class="display h-xl split" style="margin:16px 0 24px;max-width:13ch">Your peace of mind. <span class="it">Our life’s work.</span></h2>
  <p class="lead" data-reveal style="margin-bottom:34px">Trust is everything. We are open and transparent from the first viewing to the final seal, because a sold home is not the end. It is the beginning of a new life.</p>
  <div class="btns" data-reveal>
   <a class="btn btn--solid" href="contact.html#consultation">Book a consultation {ARROW}</a>
   <a class="btn" href="{wa('Hello Elia Living, I would like to talk about a property.')}" target="_blank" rel="noopener">WhatsApp us</a>
  </div>
 </div>
</section>
"""
    page("index.html", "Elia Living", "Boutique real estate on the Costa Blanca. Villas, homes and apartments for sale in Jávea and Alicante, with personal advice in five languages.", "home", "home", "light", c)

# ------------------------------------------------------------------ PROPERTIES
def build_properties():
    cards = "".join(pcard(p, 1200) for p in sorted(PROPS, key=lambda x: x["order"]))
    locs = [("all","All areas")] + [(k, n) for k,n in [("javea","Jávea"),("moraira","Moraira"),("benissa","Benissa"),("benitachell","Benitachell")]]
    chips = "".join(f'<button class="chip" data-loc="{k}" aria-pressed="{"true" if k=="all" else "false"}">{n}</button>' for k,n in locs)
    c = f"""
<section class="opener wrap">
 <nav class="crumbs" aria-label="Breadcrumb"><a href="index.html">Home</a><span aria-hidden="true">/</span><span>Properties</span></nav>
 <div class="opener__row">
  <h1 class="display h-xxl split">Residences</h1>
  <div class="side" data-reveal style="--d:200">
   <p class="lead" style="font-size:1.08rem">We don’t believe in endless listings. We listen carefully, then handpick homes that truly fit your life.</p>
  </div>
 </div>
</section>

<div class="filters" role="region" aria-label="Filter residences">
 <div class="wrap filters__inner">
  <div class="chips" role="group" aria-label="Area">{chips}</div>
  <label class="field-inline" for="f-beds">Bedrooms
   <select id="f-beds"><option value="any">Any</option><option value="3">3+</option><option value="4">4+</option></select>
  </label>
  <label class="field-inline" for="f-sort">Sort
   <select id="f-sort"><option value="featured">Featured</option><option value="price-asc">Price, lowest first</option><option value="price-desc">Price, highest first</option></select>
  </label>
  <label class="field-inline" for="f-ref"><span class="sr-only">Search</span>
   <input id="f-ref" type="search" placeholder="Name or reference" autocomplete="off">
  </label>
  <span class="filters__count num" aria-live="polite">{len(PROPS)} residences</span>
 </div>
</div>

<section class="wrap" style="padding-bottom:clamp(90px,12vw,180px)">
 <div class="pgrid">
  {cards}
  <div class="pgrid__empty" hidden>
   <p class="display h-m">No residences match these filters.</p>
   <p class="muted" style="margin:14px 0 26px">Many homes are offered privately. Tell us what you are looking for.</p>
   <div class="btns" style="justify-content:center"><button class="btn" id="f-reset" type="button">Clear filters</button><a class="btn btn--solid" href="contact.html#consultation">Describe your search {ARROW}</a></div>
  </div>
 </div>
</section>

<section class="section night">
 <div class="wrap portfolio-note">
  <h2 class="display h-l split">Looking for something <span class="it">more specific?</span></h2>
  <div class="side" data-reveal>
   <p class="lead">Our wider portfolio holds homes across the Costa Blanca, including off-market villas and apartments in its most desirable locations. Tell us what matters to you and we will organise a personal viewing tour.</p>
   <div class="btns"><a class="btn btn--solid" href="contact.html#consultation">Start a tailored search {ARROW}</a></div>
  </div>
 </div>
</section>
"""
    page("properties.html", "Properties · Elia Living", "Villas, homes and apartments for sale in Jávea, Moraira, Benissa and Benitachell, selected by Elia Living.", "properties", "properties", "dark", c)

# ------------------------------------------------------------------ PROPERTY
def build_property(p, idx):
    n = len(p["imgs"])
    adv = TEAM_BY.get(p["advisor"]) if p["advisor"] else None
    nxt = PROPS[(idx + 1) % len(PROPS)]
    rel = [q for q in PROPS if q["slug"] != p["slug"]]
    rel = sorted(rel, key=lambda q: (q["loc"] != p["loc"], abs(q["price"] - p["price"])))[:3]

    specs = [("Price", eur(p["price"]), "spec--price"), ("Bedrooms", str(p["beds"]), ""), ("Bathrooms", str(p["baths"]), "")]
    if p["built"]: specs.append(("Built", f"{p['built']} m²", ""))
    if p["plot"]: specs.append(("Plot", f"{p['plot']:,} m²", ""))
    specs.append(("Location", p["town"], ""))
    specs.append(("Reference", p["ref"], ""))
    specbar = "".join(f'<div class="spec {c}"><small>{k}</small><b class="num">{E(v)}</b></div>' for k,v,c in specs)

    slides = "".join(f'<div class="gallery__slide{" on" if i==0 else ""}">' + (pimg(im, 2000, alt=f"{p['card']}, photo {i+1} of {n}", lazy=(i>0)) if i < 2 else f'<img data-src="{cf(im,2000)}" data-fb="{cf_raw(im)}" {FB} alt="{E(p["card"])}, photo {i+1} of {n}" decoding="async">') + "</div>" for i, im in enumerate(p["imgs"]))
    thumbs = "".join(f'<button type="button" aria-label="Show photo {i+1}"{" class=\"on\"" if i==0 else ""}>{pimg(im, 240, alt="")}</button>' for i, im in enumerate(p["imgs"]))
    gnote = ""
    if p["photos_total"] > n:
        gnote = f'<p class="gallery__note">Showing {n} of the {p["photos_total"]} photographs in the current listing. The full set will be added.</p>'

    # chapters, interleaving a few photos (never the hero, never repeated)
    pool = p["imgs"][2:] if n > 4 else p["imgs"][1:]
    step = max(1, len(pool) // max(1, len(p["chapters"])))
    chap_html, nav = [], []
    for ci, (lab, title, paras, items) in enumerate(p["chapters"]):
        cid = f"ch{ci+1}"
        nav.append(f'<a href="#{cid}"><span class="n">{ci+1:02d}</span>{E(lab)}</a>')
        ps = "".join(f"<p>{E(x)}</p>" for x in paras)
        lis = ""
        if items:
            lis = "<ul>" + "".join(f"<li><b>{E(a)}</b><span>{E(b)}</span></li>" for a,b in items) + "</ul>"
        fig = ""
        if ci % 2 == 1:
            k = (ci // 2) * step
            if k < len(pool):
                fig = f'<div class="figure"><div class="ph mask" data-reveal data-cursor="Zoom">{pimg(pool[k], 1400, alt=p["card"])}</div></div>'
        chap_html.append(f'<article class="chapter" id="{cid}" data-reveal><h3><span class="n">{ci+1:02d} · {E(lab)}</span>{E(title)}</h3>{ps}{lis}{fig}</article>')
    summary = "<ul>" + "".join(f'<li class="plain">{E(s)}</li>' for s in p["summary"]) + "</ul>"
    nav.append(f'<a href="#ch-sum"><span class="n">—</span>In summary</a>')
    chap_html.append(f'<article class="chapter" id="ch-sum" data-reveal><h3><span class="n">In summary</span>What sets it apart</h3>{summary}</article>')

    amen = [("bed", str(p["beds"]), "Bedrooms"), ("bath", str(p["baths"]), "Bathrooms")]
    if p["built"]: amen.append(("built", f"{p['built']} m²", "Built area"))
    if p["plot"]: amen.append(("plot", f"{p['plot']:,} m²", "Plot"))
    for a in p["amen"]: amen.append((a, "", AMEN_LABEL[a]))
    amen_html = "".join(f'<div>{icon(k)}' + (f'<b class="num">{v}</b>' if v else "") + f'<span>{E(l)}</span></div>' for k,v,l in amen)

    status = f'<span class="status-pill"><i></i>{E(p["status"])}</span>' if p.get("status") else ""
    msg = f"Hello Elia Living, I'm interested in {p['card']} ({p['ref']})."
    adv_html = (f'<div class="advisor"><div class="advisor__img">{cimg(adv["img"], adv["name"])}</div><div><span class="label">Your advisor</span><b>{adv["name"]}</b><span style="color:var(--on-night-2);font-size:14px">{E(adv["role"])} · {adv["langs"]}</span></div></div>'
                if adv else f'<div><span class="label">Your advisors</span><p class="display h-s" style="margin-top:8px">The Elia Living sales team</p></div>')
    loc_img = p["imgs"][min(3, n-1)] if n > 1 else p["imgs"][0]

    c = f"""
<section class="p-open wrap">
 <nav class="crumbs" aria-label="Breadcrumb"><a href="index.html">Home</a><span aria-hidden="true">/</span><a href="properties.html">Properties</a><span aria-hidden="true">/</span><span>{p['ref']}</span></nav>
 <div class="p-open__row">
  <div>
   <h1 class="display p-title split">{E(p['name'])}</h1>
   <p class="p-sub" data-reveal style="--d:250">{E(p['sub'])}</p>
  </div>
  <div class="p-loc" data-reveal style="--d:350">
   {status}
   <span class="label">{E(p['kind'])} · {p['ref']}</span>
   <span>{E(p['area'])}, {E(p['town'])}</span>
   <span class="display" style="font-size:2rem;margin-top:6px">{eur(p['price'])}</span>
  </div>
 </div>
</section>

<section class="p-heroimg-scene" aria-label="Main photograph">
 <div class="p-heroimg"><div class="p-heroimg__clip">{pimg(p['imgs'][0], 2400, alt=p['card'] + ', ' + p['town'], lazy=False)}</div></div>
</section>

<div class="specbar">
 <div class="wrap specbar__inner">{specbar}<a class="btn btn--solid" href="#enquire">Arrange a viewing {ARROW}</a></div>
</div>

<section class="section wrap">
 <div class="p-intro">
  <p class="lead-big" data-reveal>{E(p['intro'])}</p>
  <aside data-reveal style="--d:150">
   <p class="body" style="margin:0">{E(p['lead_more'])}</p>
   <a class="link" href="#gallery">View the photographs {ARROW}</a>
  </aside>
 </div>
</section>

<section class="night section--tight" id="gallery" aria-label="Photo gallery">
 <div class="wrap gallery" data-gallery tabindex="-1">
  <div class="gallery__stage" data-cursor="Expand" role="group" aria-roledescription="carousel" aria-label="{E(p['card'])} photographs">{slides}</div>
  <div class="gallery__bar">
   <span class="gallery__count num"><b>01</b>/ {n:02d}</span>
   <div class="gbtns"><button class="gbtn gprev" type="button" aria-label="Previous photo">{ARROW_L}</button><button class="gbtn gnext" type="button" aria-label="Next photo">{ARROW_R}</button></div>
  </div>
  <div class="gallery__thumbs">{thumbs}</div>
  {gnote}
 </div>
</section>

<section class="section wrap" aria-label="About the home">
 <div class="story">
  <nav class="story__nav" aria-label="Chapters">{"".join(nav)}</nav>
  <div class="story__body">{"".join(chap_html)}</div>
 </div>
</section>

<section class="section--tight wrap" aria-label="Key facts">
 <p class="label" style="margin-bottom:20px">Key facts</p>
 <div class="amen" data-reveal>{amen_html}</div>
</section>

<section class="section wrap" aria-label="Location">
 <div class="ploc">
  <div class="ploc__text">
   <p class="label" data-reveal>Location</p>
   <h2 class="display h-l split">{E(p['area'])}, <span class="it">{E(p['town'])}</span></h2>
   <p class="body" data-reveal>{E(p['address'])}</p>
   <a class="link" data-reveal href="https://www.google.com/maps/search/?api=1&amp;query={p['maps']}" target="_blank" rel="noopener">Open the area in Google Maps {ARROW}</a>
   <a class="link" data-reveal href="costa-blanca.html">Life on the Costa Blanca {ARROW}</a>
  </div>
  <div class="ploc__card mask" data-reveal>{pimg(loc_img, 1400, alt=p['card'])}
   <div class="ploc__pin"><span class="label">{p['ref']}</span><b style="font-weight:400;font-family:var(--f-display);font-size:1.4rem">{E(p['card'])}</b><span class="muted" style="font-size:14px">{E(p['area'])} · {E(p['town'])}</span></div>
  </div>
 </div>
</section>

<section class="section night" id="enquire" aria-label="Enquire">
 <div class="wrap enquire">
  <div class="enquire__left">
   <p class="label">Enquire</p>
   <h2 class="display h-l split">Ready to make this <span class="it">your home?</span></h2>
   {adv_html}
   <div class="btns">
    <a class="btn btn--solid" href="{wa(msg)}" target="_blank" rel="noopener">{CHAT.replace('<svg ','<svg width="18" height="18" ')} WhatsApp</a>
    <a class="btn" href="tel:{PHONE_TEL}">{PHONE}</a>
   </div>
  </div>
  <form class="enquire__form form" data-form="enquiry" data-subject="Enquiry: {E(p['card'])} ({p['ref']})" novalidate>
   <input type="hidden" name="Property" value="{E(p['card'])} ({p['ref']})">
   <div class="field"><label for="e-name">Name</label><input id="e-name" name="Name" autocomplete="name" required><span class="err">Please add your name.</span></div>
   <div class="field"><label for="e-email">Email</label><input id="e-email" name="Email" type="email" autocomplete="email" required><span class="err">Please add a valid email.</span></div>
   <div class="field"><label for="e-phone">Phone</label><input id="e-phone" name="Phone" type="tel" autocomplete="tel"></div>
   <div class="field"><label for="e-when">I would like to</label><select id="e-when" name="Request"><option>Arrange a viewing</option><option>Receive more information</option><option>Book a video call</option></select></div>
   <div class="field full"><label for="e-msg">Message</label><textarea id="e-msg" name="Message">I'm interested in {E(p['card'])} ({p['ref']}).</textarea></div>
   <label class="consent field full"><input type="checkbox" id="e-consent" name="Consent" value="yes" required><span>I accept the <a href="{LEGAL[1][1]}" target="_blank" rel="noopener" style="text-decoration:underline">privacy policy</a>.</span><span class="err">Please accept to continue.</span></label>
   <div class="form__foot full"><button class="btn btn--solid" type="submit">Prepare my enquiry {ARROW}</button></div>
   <div class="form__ready" hidden><p class="display h-s" style="margin:0">Your enquiry is ready.</p><p style="margin:0;color:var(--on-night-2)">Choose how you would like to send it.</p><div class="btns"><a class="btn btn--solid ready-wa" href="#" target="_blank" rel="noopener">Send on WhatsApp</a><a class="btn ready-mail" href="#">Send by email</a></div></div>
  </form>
 </div>
</section>

<section class="section wrap" aria-label="Related residences">
 <div style="display:flex;justify-content:space-between;align-items:flex-end;gap:24px;flex-wrap:wrap;margin-bottom:clamp(32px,4vw,60px)">
  <h2 class="display h-l split">You may also <span class="it">love</span></h2>
  <a class="link" href="properties.html">All residences {ARROW}</a>
 </div>
 <div class="related">{"".join(pcard(q, 900) for q in rel)}</div>
</section>

<a class="next-prop" href="property-{nxt['slug']}.html" data-cursor="Next" aria-label="Next residence: {E(nxt['card'])}">
 {pimg(nxt['imgs'][0], 2000, alt='')}
 <div class="wrap"><span class="label" style="color:rgba(255,255,255,.8)">Next residence · {nxt['ref']}</span><span class="display h-xl">{E(nxt['card'])}</span><span style="display:flex;gap:24px;font-size:15px" class="num">{eur(nxt['price'])} · {E(nxt['town'])} {ARROW}</span></div>
</a>

<div class="lightbox" aria-hidden="true" role="dialog" aria-label="Photographs of {E(p['card'])}">
 <div class="lightbox__top"><span class="lightbox__count num"></span><button class="lightbox__close" type="button">Close <span aria-hidden="true">✕</span></button></div>
 <div class="lightbox__img"><img alt="{E(p['card'])}"></div>
 <div class="lightbox__bottom"><span class="muted" style="color:var(--on-night-2)">{E(p['card'])} · {p['ref']}</span><div class="gbtns"><button class="gbtn lbprev" type="button" aria-label="Previous photo">{ARROW_L}</button><button class="gbtn lbnext" type="button" aria-label="Next photo">{ARROW_R}</button></div></div>
</div>
"""
    title = f"{p['card']} · {p['town']} · Elia Living"
    desc = f"{p['kind']} for sale in {p['town']}: {p['beds']} bedrooms, {p['baths']} bathrooms" + (f", {p['built']} m² built" if p['built'] else "") + (f" on a {p['plot']:,} m² plot" if p['plot'] else "") + f". {eur(p['price'])}. Ref {p['ref']}."
    page(f"property-{p['slug']}.html", title, desc, "property", "properties", "dark", c)

# ------------------------------------------------------------------ ABOUT
def build_about():
    founders = [TEAM_BY["karina"], TEAM_BY["monika"]]
    team = [m for m in TEAM if m["key"] not in ("karina","monika")]
    def member(m, i):
        return f"""<article class="member" data-reveal style="--d:{(i%3)*100}">
 <div class="ph mask" data-reveal>{cimg(m['img'], m['name'] + ', ' + m['role'])}</div>
 <div class="member__head"><h3>{m['name']}</h3><span class="member__langs">{m['langs']}</span></div>
 <span class="member__role">{E(m['role'])}</span>
 <p class="member__bio">{E(m['bio'])}</p>
 <button class="member__more" type="button" aria-expanded="false">Read more</button>
</article>"""
    fpair = "".join(f'<figure>{"<div class=\"ph mask\" data-reveal>" + cimg(m["img"], m["name"]) + "</div>"}<figcaption><b style="font-weight:420">{m["name"]}</b><span class="muted">{E(m["role"])}</span></figcaption></figure>' for m in founders)
    clients = [("Second-home seekers","Choosing the Costa Blanca as a new way of living, close to nature, sun and tranquillity."),
               ("Holiday home owners","Families enjoying seasonal stays while making a future-oriented investment."),
               ("Professionals & remote workers","People blending a Mediterranean lifestyle with the freedom to work from anywhere."),
               ("Premium clients","Buyers seeking prestige, privacy and comfort in exclusive villas and apartments."),
               ("Investors","Focused on strong returns, from rentals to strategic developments.")]
    cl = "".join(f'<li data-reveal style="--d:{i*60}"><h3>{a}</h3><p>{b}</p></li>' for i,(a,b) in enumerate(clients))
    why = ["Only the best homes, personally selected","Local expertise, global standards","Creative interior design and renovation","Tailor-made, full service","Legal and financial advice","Long-term support beyond the sale","A strong partner network across the Costa Blanca","Multilingual experts: EN, PL, ES, DE, NL","Always available, even on WhatsApp"]
    c = f"""
<section class="wrap ab-open">
 <div class="ab-open__text">
  <nav class="crumbs" aria-label="Breadcrumb"><a href="index.html">Home</a><span aria-hidden="true">/</span><span>About</span></nav>
  <h1 class="display h-xxl split">Beyond <span class="it">real estate.</span></h1>
  <p class="lead" data-reveal style="--d:300;margin-top:28px">A boutique agency on the Costa Blanca, and your trusted partner to find and create your dream life in Spain.</p>
 </div>
 <div class="ab-open__arch mask" data-reveal style="--d:150">{cimg("ac8d1e52-415e-4dc1-8ead-e4603c58ef16 (1).jpg", "Elia Living on the Costa Blanca", lazy=False, extra='data-parallax=".08"')}</div>
</section>

<section class="section night" style="margin-top:clamp(80px,10vw,160px)">
 <div class="wrap">
  <p class="label" data-reveal>Mission &amp; vision</p>
  <h2 class="display h-l split" style="margin:14px 0 clamp(40px,5vw,70px)">Your peace of mind. <span class="it">Our purpose.</span></h2>
  <div class="mv">
   <div data-reveal><span class="label">Mission</span><p class="display">To help clients turn their dream of living or investing in Spain into reality, with trust, security and tailor-made service.</p></div>
   <div data-reveal style="--d:150"><span class="label">Vision</span><p class="display">To become the leading boutique agency in Spain, known for long-term relationships, personalised service and homes that enrich lives.</p></div>
  </div>
 </div>
</section>

<section class="section wrap">
 <div class="clients">
  <div class="clients__intro">
   <p class="label" data-reveal>Who we work with</p>
   <h2 class="display h-l split">Different clients. <span class="it">One dream.</span></h2>
   <p class="body" data-reveal>Our clients see a home as more than an address: a lifestyle, an investment and a new chapter. From families to investors, they share one desire, a life well lived on the Costa Blanca.</p>
  </div>
  <ul class="clients__list">{cl}</ul>
 </div>
</section>

<section class="section stone" id="our-people">
 <div class="wrap founders">
  <div class="founders__pair">{fpair}</div>
  <div class="founders__text">
   <p class="label" data-reveal>Our people</p>
   <h2 class="display h-l split">Meet the <span class="it">founders</span></h2>
   <p class="body" data-reveal>Karina and Monika created Elia Living with a shared passion for design, strategy and meaningful living. Their own experience as investors gives them a unique perspective: they know what it takes to make wise choices, revive homes with soul, and guide clients with clarity and care.</p>
   <p class="body" data-reveal style="font-size:15.5px">{E(TEAM_BY['karina']['bio'])}</p>
  </div>
 </div>
</section>

<section class="section wrap" id="team">
 <div style="display:grid;grid-template-columns:repeat(12,1fr);gap:24px;margin-bottom:clamp(50px,7vw,110px)">
  <div style="grid-column:1/span 7">
   <p class="label" data-reveal>The team</p>
   <h2 class="display h-l split" style="margin-top:14px">We speak <span class="it">your language.</span></h2>
  </div>
  <p class="body" data-reveal style="grid-column:1/-1;max-width:56ch">An international team of real estate advisors, designers and luxury marketing professionals who live, work and invest on the Costa Blanca. We have walked the same path as our clients, so we are with you from the first hello to the day you open your new door.</p>
 </div>
 <div class="team">{member(TEAM_BY['monika'],0)}{"".join(member(m, i+1) for i,m in enumerate(team))}</div>
</section>

<section class="section--tight wrap">
 <p class="label" data-reveal style="margin-bottom:22px">Why clients choose us</p>
 <ul class="why" data-reveal>{"".join(f"<li>{E(w)}</li>" for w in why)}</ul>
</section>

<section class="section wrap" style="text-align:center">
 <p class="label" data-reveal>What next?</p>
 <h2 class="display h-xl split" style="margin:18px auto 26px;max-width:14ch">Your new beginning <span class="it">starts here.</span></h2>
 <p class="lead" data-reveal style="margin:0 auto 34px">Whether you are looking for a second home, a safe investment or a complete lifestyle change, Elia Living is here to make it seamless.</p>
 <div class="btns" data-reveal style="justify-content:center"><a class="btn btn--solid" href="contact.html#consultation">Book a consultation {ARROW}</a></div>
</section>
"""
    page("about.html", "About · Elia Living", "The story, values and people behind Elia Living, a boutique real estate agency in Jávea on the Costa Blanca.", "about", "about", "dark", c)

# ------------------------------------------------------------------ SERVICES
def build_services():
    c = f"""
<section class="svc-hero on-image">
 <div class="svc-hero__bg" data-parallax=".12">{cimg("PREMIUM-INFINITY-POOL-WITH-A-VIEW.jpg", "Infinity pool overlooking the Mediterranean", lazy=False)}</div>
 <div class="wrap">
  <h1 class="display h-xxl split">Your vision. <span class="it">Our expertise.</span></h1>
  <p class="lead" data-reveal style="--d:400">Trusted advisors who hand-select the right homes, manage projects with precision, refine interiors with style, and make sure your life abroad begins seamlessly.</p>
 </div>
</section>

<nav class="svc-index" aria-label="Services">
 <div class="wrap svc-index__inner"><a href="#properties">Properties</a><a href="#construction">Construction &amp; investment</a><a href="#design">Design</a><a href="#concierge">Concierge</a></div>
</nav>

<section class="section wrap svc" id="properties">
 <div class="svc__head"><p class="label" data-reveal>Elia Living Properties</p><h2 class="display h-xl split">Finding your perfect home, <span class="it">made simple.</span></h2></div>
 <div class="svc-a">
  <div class="body" data-reveal>
   <p>We don’t believe in endless listings. Instead, we listen carefully, understand what matters to you, and handpick homes that truly fit your life.</p>
   <p>We guide you through the search with care and precision, from highlighting off-market villas and apartments in the Costa Blanca’s most desirable locations to organising personalised viewing tours.</p>
   <p>Our team handles the details, arranging schedules, advising on financing options and providing legal and tax guidance, so the process is transparent and stress-free.</p>
   <a class="link" href="properties.html" style="margin-top:10px">See current residences {ARROW}</a>
  </div>
  <ol class="steps" data-reveal style="--d:150">
   <li>We listen to what matters to you</li>
   <li>We handpick homes, including off-market</li>
   <li>We organise a personal viewing tour</li>
   <li>We guide financing, legal and tax steps</li>
  </ol>
 </div>
</section>

<section class="section night svc" id="construction">
 <div class="wrap">
  <div class="svc__head"><p class="label" data-reveal>Elia Living Construction &amp; Investments</p><h2 class="display h-xl split">From vision <span class="it">to value.</span></h2></div>
  <div class="svc-b">
   <div class="svc-b__imgs">
    <div class="ph mask" data-reveal>{cimg("Karina-Villa-pool.jpg", "Villa pool from an Elia Living project")}</div>
    <div class="ph mask" data-reveal style="--d:200">{cimg("LUXURY-HOME-COSTA-BLACA-WITH-RED_FLOAT-POOL-CROP.jpg", "Luxury home on the Costa Blanca")}</div>
   </div>
   <div class="svc-b__text">
    <p class="body" data-reveal style="margin:0">End-to-end project management, from permits and planning to full construction oversight and final delivery. We run our own developments and co-investments. You don’t need to be on site: we handle everything remotely, with full transparency.</p>
    <div class="figures" data-reveal>
     <div><b class="num">30%</b><span>Up to 30% return within 18 months on renovations</span></div>
     <div><b class="num">20–50%</b><span>Return on investment on new builds</span></div>
    </div>
    <p class="fineprint" data-reveal>Figures as published by Elia Living for its developments and co-investments. Returns vary by project.</p>
    <ol class="steps" data-reveal><li>Permits &amp; planning</li><li>Construction oversight</li><li>Final delivery</li></ol>
   </div>
  </div>
 </div>
</section>

<section class="section wrap svc" id="design">
 <div class="svc__head"><p class="label" data-reveal>Elia Living Design</p><h2 class="display h-xl split">Spaces that <span class="it">feel like home.</span></h2></div>
 <div class="svc-c">
  <div class="svc-c__text">
   <p class="body" data-reveal style="margin:0">We create interiors that combine luxury, functionality and timeless style. From complete turnkey projects to home staging that boosts property value, our designs make every space more attractive and market-ready.</p>
   <p class="body" data-reveal style="margin:0">We collaborate with leading local and international architects and offer architectural consultations to refine layouts, optimise flow and elevate style.</p>
   <div class="tags" data-reveal><span>Turnkey interiors</span><span>Home staging</span><span>Architectural consultations</span><span>Renovation design</span></div>
   <a class="link" href="about.html#team" data-reveal>Meet Jan, our Head of Design {ARROW}</a>
  </div>
  <div class="svc-c__imgs">
   <div class="ph mask" data-reveal>{cimg("Design 1.png", "Interior designed by Elia Living")}</div>
   <div class="ph mask" data-reveal style="--d:200">{cimg("Design 2.png", "Interior designed by Elia Living")}</div>
  </div>
 </div>
</section>

<section class="section stone svc" id="concierge">
 <div class="wrap">
  <div class="svc__head"><p class="label" data-reveal>Elia Living Concierge</p><h2 class="display h-xl split">Personal support, <span class="it">every step of the way.</span></h2></div>
  <div class="svc-d">
   <p class="lead" data-reveal>For us, buying a property is just the beginning. From day one, you feel at home on the Costa Blanca.</p>
   <div class="svc-d__list" data-reveal>
    <div><b>Relocation</b><span>Moving and settling in</span></div>
    <div><b>Transport</b><span>Arrangements on arrival and beyond</span></div>
    <div><b>Interior set-up</b><span>Ready to live in</span></div>
    <div><b>Schools</b><span>Finding the right one for your children</span></div>
    <div><b>Doctors</b><span>And other trusted services</span></div>
    <div><b>Day-to-day needs</b><span>A local insider to call</span></div>
    <div><b>Restaurants</b><span>Access to the best tables</span></div>
    <div><b>Culture &amp; clubs</b><span>Cultural events and private clubs</span></div>
   </div>
  </div>
 </div>
</section>

<section class="section night">
 <div class="wrap" style="display:grid;gap:30px;justify-items:start">
  <h2 class="display h-xl split" style="max-width:16ch">A dream, an investment, <span class="it">a fresh start.</span></h2>
  <p class="lead" data-reveal>Whatever brings you to the Costa Blanca, we are here to make it truly yours.</p>
  <div class="btns" data-reveal><a class="btn btn--solid" href="contact.html#consultation">Let’s talk {ARROW}</a><a class="btn" href="{wa('Hello Elia Living, I would like to know more about your services.')}" target="_blank" rel="noopener">WhatsApp</a></div>
 </div>
</section>
"""
    page("services.html", "Services · Elia Living", "Property search, construction and investment, interior design and concierge on the Costa Blanca.", "services", "services", "light", c)

# ------------------------------------------------------------------ COSTA BLANCA
def build_costa():
    nature = [("Endless sunshine","15-scaled-1.png",["Over 320 days of sun a year","Golden sunsets"]),
              ("Diverse landscapes","24-scaled-1.png",["Beaches and hidden coves","Mountains and high cliffs","Valleys of vineyards and olive groves"]),
              ("Montgó Natural Park","20-2-scaled-1.png",["Over 650 plant species","Rare birds of prey","Panoramic trails"]),
              ("A gentle microclimate","26-1-scaled-1.png",["Cooler summers, mild winters","Lush Mediterranean greenery"]),
              ("Blue Flag beaches","15-scaled-1.png",["Cala La Granadella, Jávea","Playa La Grava, Jávea"]),
              ("Active outdoors","19-2-scaled-1.png",["On the water: sailing, snorkelling, kayaking","On land: hiking, cycling, golf"])]
    nat = "".join(f'<article class="ncard"><div class="ph">{cimg(img, t)}</div><h3>{t}</h3><ul>{"".join(f"<li>{E(x)}</li>" for x in li)}</ul></article>' for t,img,li in nature)
    tabs = "".join(f'<button role="tab" type="button" data-key="{t["key"]}" data-cap="{t["name"]} · {t["tag"]}" aria-selected="{"true" if i==0 else "false"}"><b>{t["name"]}</b><span>{t["tag"]}</span></button>' for i,t in enumerate(TOWNS))
    timgs = "".join(cimg(t["img"], t["name"], cls="on" if i==0 else "", extra=f'data-key="{t["key"]}"') for i,t in enumerate(TOWNS))
    culture = [("Festivals","Moros y Cristianos, San Juan and year-round local fiestas."),("Arts & culture","Galleries, music, film festivals and a growing art scene in Jávea."),
               ("Wellness","From SHA Wellness Clinic to natural thermal spas."),("Yoga & Pilates","Sunrise sessions under the Mediterranean sky."),
               ("Gastronomy","Dénia is a UNESCO Creative City of Gastronomy."),("Origins of paella","Authentic rice dishes and fresh seafood traditions."),
               ("Michelin stars","Quique Dacosta in Dénia and BonAmb in Jávea."),("Wine & markets","Boutique vineyards of the Marina Alta and lively local markets.")]
    cu = "".join(f'<div data-reveal style="--d:{(i%4)*70}"><h3>{a}</h3><p>{b}</p></div>' for i,(a,b) in enumerate(culture))
    c = f"""
<section class="cb-hero on-image" data-hero-end>
 <div class="cb-hero__bg" data-parallax=".1">{cimg("Costa-Blanca-Hero-copy-scaled-1.jpg", "The Costa Blanca coastline", lazy=False)}</div>
 <div class="cb-hero__text wrap" style="padding-inline:0">
  <p class="label" style="color:rgba(255,255,255,.8)">Costa Blanca</p>
  <h1 class="display split">More than a place. <span class="it">A life shaped by light and sea.</span></h1>
 </div>
</section>

<section class="section wrap" id="nature">
 <div class="sun">
  <div class="sun__num num" data-reveal>320<small>days of sunshine a year</small></div>
  <div class="sun__text">
   <p class="label" data-reveal>Nature</p>
   <h2 class="display h-l split">Where sun <span class="it">meets sea.</span></h2>
   <p class="body" data-reveal>Over 320 days of sunshine a year and a famously mild, healthy climate. People come for the sun, and stay for the quality of life.</p>
  </div>
 </div>
</section>

<section class="night section--tight" aria-label="Nature highlights">
 <div class="wrap" style="display:flex;justify-content:space-between;align-items:flex-end;gap:20px;margin-bottom:34px;flex-wrap:wrap">
  <h2 class="display h-m">The landscape, <span class="it">in six notes</span></h2>
  <span class="label">Drag or scroll →</span>
 </div>
 <div class="nature" tabindex="0" aria-label="Nature highlights, scrollable">{nat}</div>
</section>

<section class="videoband" aria-label="Film of Jávea">
 <video autoplay muted loop playsinline preload="metadata" poster="{cdn('Costa-Blanca-Hero-copy-scaled-1.jpg')}"><source src="{cdn('javea-video-test.webm')}" type="video/webm"></video>
 <div class="videoband__cap"><span class="label" style="color:rgba(255,255,255,.8)">Jávea</span><span class="display h-l">The sea. The food. <span class="it">The nature.</span></span></div>
 <button class="vtoggle" type="button">Pause film</button>
</section>

<section class="section wrap" id="towns">
 <div style="margin-bottom:clamp(40px,5vw,70px);max-width:900px">
  <p class="label" data-reveal>Life &amp; culture</p>
  <h2 class="display h-l split" style="margin-top:14px">Mediterranean life <span class="it">at its best.</span></h2>
  <p class="body" data-reveal style="margin-top:20px">Gastronomy, tradition and modern living come together in coastal towns that each have their own charm, from historic streets and artisan shops to picturesque harbours.</p>
 </div>
 <div class="townx">
  <div class="townx__tabs" role="tablist" aria-label="Towns">{tabs}</div>
  <div class="townx__stage">{timgs}<span class="townx__cap">{TOWNS[0]['name']} · {TOWNS[0]['tag']}</span></div>
 </div>
</section>

<section class="section--tight wrap" aria-label="Culture">
 <div class="culture">{cu}</div>
</section>

<section class="section stone" id="practical">
 <div class="wrap">
  <div style="display:grid;grid-template-columns:repeat(12,1fr);gap:24px;margin-bottom:clamp(40px,6vw,80px);align-items:end">
   <div style="grid-column:1/span 7"><p class="label" data-reveal>Practical info</p><h2 class="display h-l split" style="margin-top:14px">Easy living. <span class="it">Smart choices.</span></h2></div>
   <p class="body" data-reveal style="grid-column:9/span 4;margin:0">Beyond the homes themselves, the Costa Blanca offers what international residents need for everyday comfort and long-term security.</p>
  </div>
  <div class="practical">
   <article data-reveal><div class="ph mask" data-reveal>{cimg("09d6f467e69b356db564e6d9f3406795.jpeg", "Costa Blanca coast")}</div><h3>Easy access</h3><ul><li><b>Airports.</b> Alicante and Valencia within 1 to 1.5 hours.</li><li><b>Balearics.</b> Ferries from Dénia reach Ibiza in about two hours.</li><li><b>Community.</b> Around half of Jávea’s residents are international.</li></ul></article>
   <article data-reveal style="--d:120"><div class="ph mask" data-reveal style="--d:120">{cimg("Portal-Marina_00_hres.jpeg", "Costa Blanca residential setting")}</div><h3>Sport, school &amp; health</h3><ul><li><b>Sport.</b> Tennis academies, golf, padel, sailing and 470 km of cycling routes.</li><li><b>Schools.</b> Lady Elizabeth School and Xàbia International College (UK and Spanish systems).</li><li><b>Healthcare.</b> Hospitals in Dénia and Alicante with international staff.</li></ul></article>
   <article data-reveal style="--d:240"><div class="ph mask" data-reveal style="--d:240">{cimg("Secondsection_villa_front.jpg", "Villa front on the Costa Blanca")}</div><h3>Everyday living</h3><ul><li><b>Cost of living.</b> Noticeably lower than in Western and Northern Europe.</li><li><b>Water.</b> Jávea’s modern desalination plant keeps gardens green and pools full year-round.</li><li><b>Safety.</b> A safe and welcoming community.</li></ul></article>
  </div>
 </div>
</section>

<section class="section wrap" style="text-align:center">
 <h2 class="display h-xl split" style="max-width:15ch;margin:0 auto 26px">Ready to find your place <span class="it">under the sun?</span></h2>
 <div class="btns" data-reveal style="justify-content:center"><a class="btn btn--solid" href="properties.html">Explore properties {ARROW}</a><a class="btn" href="contact.html#consultation">Book a consultation</a></div>
</section>
"""
    page("costa-blanca.html", "Costa Blanca · Elia Living", "Life on the Costa Blanca: Jávea, Moraira, Altea, Dénia and Calpe, nature, culture and practical information for international buyers.", "costa", "costa", "light", c)

# ------------------------------------------------------------------ CONTACT
def build_contact():
    c = f"""
<section class="wrap ct">
 <div class="ct__left">
  <div>
   <nav class="crumbs" aria-label="Breadcrumb"><a href="index.html">Home</a><span aria-hidden="true">/</span><span>Contact</span></nav>
   <h1 class="display h-xxl split">Let’s <span class="it">talk.</span></h1>
   <p class="lead" data-reveal style="--d:300;margin-top:24px">Ready to take the next step? Tell us about the life you want on the Costa Blanca. We reply personally, in your language.</p>
  </div>
  <ul class="ways" data-reveal style="--d:400" id="contact-detail">
   <li><span class="label">Phone</span><span class="v num"><a href="tel:{PHONE_TEL}">{PHONE}</a></span><button class="copy" type="button" data-copy="{PHONE}">Copy</button></li>
   <li><span class="label">WhatsApp</span><span class="v"><a href="{wa('Hello Elia Living')}" target="_blank" rel="noopener">Message us</a></span><button class="copy" type="button" data-copy="{PHONE}">Copy</button></li>
   <li><span class="label">Email</span><span class="v"><a href="mailto:{EMAIL}">{EMAIL}</a></span><button class="copy" type="button" data-copy="{EMAIL}">Copy</button></li>
  </ul>
 </div>
 <div class="ct__right" id="consultation">
  <form class="form" data-form="consultation" data-subject="Consultation request via elialiving.es" novalidate>
   <div class="field full"><span class="label" style="font-size:12px;letter-spacing:.16em">Book a consultation</span><p class="display h-m" style="margin:10px 0 0">How can we help?</p></div>
   <fieldset class="field full" style="border:0;padding:0;margin:0"><legend class="label" style="font-size:12px;letter-spacing:.16em;margin-bottom:10px;padding:0">I’m interested in</legend>
    <div class="choice">
     <label><input type="radio" name="Interest" value="Buying a home" checked><span>Buying a home</span></label>
     <label><input type="radio" name="Interest" value="Construction & investment"><span>Construction &amp; investment</span></label>
     <label><input type="radio" name="Interest" value="Interior design"><span>Interior design</span></label>
     <label><input type="radio" name="Interest" value="Concierge & relocation"><span>Concierge &amp; relocation</span></label>
    </div>
   </fieldset>
   <div class="field"><label for="c-name">Name</label><input id="c-name" name="Name" autocomplete="name" required><span class="err">Please add your name.</span></div>
   <div class="field"><label for="c-email">Email</label><input id="c-email" name="Email" type="email" autocomplete="email" required><span class="err">Please add a valid email.</span></div>
   <div class="field"><label for="c-phone">Phone</label><input id="c-phone" name="Phone" type="tel" autocomplete="tel"></div>
   <div class="field"><label for="c-lang">Preferred language</label><select id="c-lang" name="Language"><option>English</option><option>Polski</option><option>Español</option><option>Deutsch</option><option>Nederlands</option></select></div>
   <div class="field"><label for="c-area">Preferred area</label><select id="c-area" name="Area"><option>Not sure yet</option><option>Jávea</option><option>Moraira</option><option>Benitachell / Cumbre del Sol</option><option>Benissa</option><option>Altea</option><option>Dénia</option><option>Calpe</option></select></div>
   <div class="field"><label for="c-budget">Budget</label><select id="c-budget" name="Budget"><option>Prefer not to say</option><option>Up to €1,000,000</option><option>€1,000,000 – €2,000,000</option><option>€2,000,000 – €3,500,000</option><option>Above €3,500,000</option></select></div>
   <div class="field full"><label for="c-msg">Message</label><textarea id="c-msg" name="Message" placeholder="A few words about what you are looking for"></textarea></div>
   <label class="consent field full" style="color:var(--mute)"><input type="checkbox" id="c-consent" name="Consent" value="yes" required><span>I accept the <a href="{LEGAL[1][1]}" target="_blank" rel="noopener" style="text-decoration:underline">privacy policy</a>.</span><span class="err">Please accept to continue.</span></label>
   <div class="form__foot full"><button class="btn btn--solid" type="submit">Prepare my request {ARROW}</button></div>
   <div class="form__ready" hidden style="border-color:var(--line)"><p class="display h-s" style="margin:0">Your request is ready.</p><p class="muted" style="margin:0">Choose how you would like to send it.</p><div class="btns"><a class="btn btn--solid ready-wa" href="#" target="_blank" rel="noopener">Send on WhatsApp</a><a class="btn ready-mail" href="#">Send by email</a></div></div>
  </form>
 </div>
</section>

<section class="section night" style="margin-top:clamp(90px,12vw,180px)" aria-label="Office">
 <div class="wrap office">
  <address class="office__addr" data-reveal>{ADDRESS_LINES[0]}<br><span class="it">{ADDRESS_LINES[1]}</span><br>{ADDRESS_LINES[2]}</address>
  <div class="office__side" data-reveal style="--d:150">
   <p class="label">Office hours</p>
   <dl class="hours"><dt>Monday – Friday</dt><dd class="num">9:00 – 17:00</dd></dl>
   <a class="link" href="{MAPS_OFFICE}" target="_blank" rel="noopener">Get directions {ARROW}</a>
   <p class="label" style="margin-top:12px">{API} · REALTOR® · SIRA</p>
  </div>
 </div>
</section>

<section class="section--tight wrap" aria-label="Other ways to start">
 <div class="svc4" style="border-top:1px solid var(--line)">
  <a href="properties.html"><h3>Browse residences</h3><p>Start with a home that caught your eye.</p>{ARROW}</a>
  <a href="services.html"><h3>Our services</h3><p>Find, build, design and live.</p>{ARROW}</a>
  <a href="costa-blanca.html"><h3>Costa Blanca</h3><p>Towns, climate, schools and practical information.</p>{ARROW}</a>
  <a href="{GUIDES}" target="_blank" rel="noopener"><h3>Buying guides</h3><p>Read our guides to buying in Spain.</p>{ARROW}</a>
 </div>
</section>
"""
    page("contact.html", "Contact · Elia Living", "Contact Elia Living in Jávea: +34 645 05 41 02, info@elialiving.es, WhatsApp, or book a consultation.", "contact", "contact", "dark", c)

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    build_home(); build_properties(); build_about(); build_services(); build_costa(); build_contact()
    for i, p in enumerate(PROPS): build_property(p, i)
    print("built", sorted(f for f in os.listdir(OUT) if f.endswith(".html")))
