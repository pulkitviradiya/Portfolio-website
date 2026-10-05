"""Build the standalone portfolio pages from stable legacy content.

Run without flags for concept previews; use --production for live filenames.
"""
from pathlib import Path
from html.parser import HTMLParser
from html import escape, unescape
import argparse
import json
import re

ROOT = Path(__file__).resolve().parent
LEGACY_ROOT = ROOT / 'legacy-source'
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--production', action='store_true', help='Write live HTML filenames and indexable metadata')
ARGS = parser.parse_args()
PREFIX = '' if ARGS.production else 'concept-'
PAGE_SLUGS = (
    'index', 'work', 'journey', 'about', 'education', 'cairo', 'research',
    'off-duty', 'candy-floss', 'pujan-energy', 'lenskart', 'ximivogue', 'ps-coffee',
)


class Node:
    def __init__(self, tag='', attrs=(), parent=None):
        self.tag, self.attrs, self.parent, self.children = tag, dict(attrs), parent, []

    def find(self, tag=None, cls=None):
        found = []
        for child in self.children:
            if isinstance(child, Node):
                if (tag is None or child.tag == tag) and (cls is None or cls in child.attrs.get('class', '').split()):
                    found.append(child)
                found.extend(child.find(tag, cls))
        return found

    def text(self):
        return ' '.join(''.join(c.text() if isinstance(c, Node) else c for c in self.children).split())

    def html(self):
        attrs = ''.join(f' {k}="{escape(v or "", quote=True)}"' for k, v in self.attrs.items())
        inner = ''.join(c.html() if isinstance(c, Node) else escape(c) for c in self.children)
        return f'<{self.tag}{attrs}>{inner}</{self.tag}>'


class Document(HTMLParser):
    voids = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr'}

    def __init__(self, filename):
        super().__init__(convert_charrefs=True)
        self.root = self.current = Node()
        self.feed((LEGACY_ROOT / filename).read_text())

    def handle_starttag(self, tag, attrs):
        node = Node(tag, attrs, self.current)
        self.current.children.append(node)
        if tag not in self.voids:
            self.current = node

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in self.voids:
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        node = self.current
        while node.parent:
            if node.tag == tag:
                self.current = node.parent
                break
            node = node.parent

    def handle_data(self, data):
        self.current.children.append(data)


icon_file = ROOT / 'concept-icons.json'
if not icon_file.exists():
    source = Path('/private/tmp/portfolio-design/node_modules/lucide-static/icons')
    names = ['arrow-up-right', 'arrow-right', 'arrow-down', 'sun-moon', 'menu', 'x', 'pause', 'plus', 'headphones', 'play', 'coffee']
    icon_file.write_text(json.dumps({n: (source / (n + '.svg')).read_text() for n in names}, indent=2))
ICONS = json.loads(icon_file.read_text())


def icon(name='arrow-up-right'):
    svg = ICONS[name]
    svg = svg[svg.index('<svg'):]
    return svg.replace('<svg', '<svg aria-hidden="true" focusable="false" class="icon"', 1)


def clean(html):
    html = html.replace('\u2014', ', ').replace('&mdash;', ', ')
    for name in ['index', 'journey', 'ps-coffee', 'pujan-energy', 'candy-floss', 'lenskart', 'ximivogue']:
        html = html.replace(f'href="{name}.html', f'href="concept-{name}.html')
    return html


def paras(values):
    return ''.join(f'<p>{s}</p>' for s in values)


def link(label, href, cls='text-link'):
    return f'<a class="{cls}" href="{href}">{label}{icon()}</a>'


def proof(items):
    return '<div class="proof">' + ''.join(f'<div class="proof-item"><div class="proof-number">{n}</div><div class="proof-label">{label}</div></div>' for n, label in items) + '</div>'


def filters(target, options):
    return f'<div class="filter-bar" data-filter-group="{target}" role="group" aria-label="Filter {target}">' + ''.join(f'<button type="button" data-filter="{key}" aria-pressed="{"true" if key == "all" else "false"}">{label}</button>' for key, label in options) + '</div>'


VENTURES = [
    dict(slug='candy-floss', name='Candy Floss', category='Consumer brand', filter='retail', years='2021 to 2026', role='Co-founder', location='Gujarat, India', color='#ded2ef', art='candy-art', art_title='Made here.<br>Built here.', subtitle='A supply-chain crisis became an 11-store brand.', metrics=[('11', 'Stores scaled'), ('200+', 'Domestic vendors'), ('~35 to ~70%', 'Gross margin expansion'), ('12,000', 'Sq ft warehouse')],
         description='When imports stopped, we built a brand of our own. A Made-in-India retail ecosystem, from product and positioning to eleven stores.', question='What if disruption became the starting point?',
         context='COVID disrupted the import-led model we had operated at Ximivogue. Waiting for the old supply chain to return would leave the business dependent on the same fragility. We chose to build closer to home.',
         decisions=[('Own the product, not just the shelf.', 'Built the name, positioning, identity, store design and product development. OEM and private-label SKUs connected customer insight directly to what we could design, source and sell.'), ('Make sourcing an operating advantage.', 'Developed a network of more than 200 domestic vendors, with backup suppliers, structured credit terms and inventory planning. Private-label development, BOM optimisation and pricing discipline helped expand gross margins from roughly 35% to 70%.'), ('Build a repeatable expansion model.', 'Scaled to 11 stores, including premium malls such as Phoenix, Palladium and Nexus. Designed franchise agreements, unit economics and onboarding, alongside Shopify D2C and marketplace distribution.')],
         takeaway='The shelf is the visible part. The business is everything behind it.', next='lenskart'),
    dict(slug='pujan-energy', name='Pujan Energy', category='Clean energy', filter='energy', years='2019 to present', role='Co-founder & operator', location='Jam Jodhpur, Gujarat', color='#d9f66f', image='pujan-solar.jpg', caption='Solar energy imagery from the existing portfolio; illustrative, not verified as the project site.', subtitle='Building for the long run, one reliable day at a time.', metrics=[('0.45 MW', 'Installed solar capacity'), ('450 kW', 'Owned capacity'), ('~99%', 'Reported plant uptime'), ('2019', 'Operating since')],
         description='Clean power for industrial Gujarat. A solar venture built from land identification to commissioning, and operated for the years that follow.', question='How do you turn infrastructure into a dependable business?',
         context='Industrial clients in Morbi needed clean, cost-competitive power. Open Access created a route to serve that demand, but making it work required land, equipment, regulation, commercial agreements and sustained operating discipline.',
         decisions=[('Own the whole execution chain.', 'Led land identification, feasibility, equipment selection and commissioning. Coordinated multiple vendors across panels, transformers, meters, breakers and cable networks.'), ('Treat compliance as part of operations.', 'Worked through MSME/Udyog Aadhaar, GETCO, SLDC, PGVCL and local approvals, alongside forecasting, scheduling and grid requirements.'), ('Design for dependable delivery.', 'Executed Wheeling and Power Sale Agreements for industrial consumers in the ceramic and paper sectors. Maintenance discipline and operational control support approximately 99% reported uptime.')],
         takeaway='Commissioning is a milestone. Reliability is the work.', next='ps-coffee'),
    dict(slug='lenskart', name='Lenskart', category='Retail franchise', filter='retail', years='2015 to 2026', role='Franchise partner', location='Surat & Gandhidham', color='#b9d6f4', image='lenskart-store.jpg', caption='Store archive from the Lenskart franchise chapter.', subtitle='Eleven years. A 290 sq ft store. A fivefold change.', metrics=[('53rd', 'Early franchise store'), ('5x', 'Monthly revenue growth'), ('290', 'Sq ft Surat flagship'), ('11 years', 'Franchise partnership')],
         description='An early franchise partnership that became an eleven-year education in retail. From the 53rd store to a second market in Gandhidham.', question='How much can you build inside 290 square feet?',
         context='I joined Lenskart in February 2015 as an early franchise partner. A compact Surat store meant every conversation, product decision and operating habit mattered.',
         decisions=[('Turn selling into customer education.', 'Used consultative selling, cross-selling and value-based product education to grow monthly revenue from Rs 3 lakh to more than Rs 15 lakh. Addressing customer pain points before purchase supported the customer experience.'), ('Keep the operation moving as the platform changes.', 'Managed P&L, hiring, training, SOPs, inventory and audits through the evolution from manual processes to iPad POS, digital CRM, order tracking and prescription records.'), ('Take the operating playbook to a new market.', 'Launched a second unit in Gandhidham in 2020, setting up the team, stock planning and store processes while establishing local presence.')],
         takeaway='Small footprint. Deep customer understanding. Compounding execution.', next='ximivogue'),
    dict(slug='ximivogue', name='Ximivogue', category='Lifestyle retail', filter='retail', years='2018 to 2021', role='Franchise partner & operator', location='Vadodara & Surat', color='#f6ac8c', art='ximi-art', art_title='Curiosity.<br>Converted.', subtitle='The chapter that turned consumer curiosity into a thesis.', metrics=[('2', 'Flagship stores'), ('~1,400', 'Sq ft per store'), ('2', 'Cities in Gujarat'), ('2018', 'First stores opened')],
         description='Bringing an international lifestyle format to Gujarat, and learning how discovery, merchandising and value shape a purchase.', question='What makes someone buy what they never came for?',
         context='A visit to a busy Delhi store ended with an unplanned Rs 2,500 purchase and a question that would shape my work: what had just happened in there? Ximivogue became the place to investigate that question through execution.',
         decisions=[('Act on the customer insight.', 'Brought the format to Gujarat through market research, brand onboarding, international sourcing and franchise execution. Opened Vadodara in August 2018 and Surat in November 2018.'), ('Treat the store as a connected experience.', 'Worked across category mix, eye-level placement, windows, island displays and pricing. Analysed sales by category, customer segment and seasonality to refine assortment and reduce dead stock.'), ('Learn the economics behind the experience.', 'Managed import pricing, currency impact and store-level economics alongside hiring, training, inventory and systems. Those lessons informed the later shift to domestic sourcing at Candy Floss.')],
         takeaway='A good retail experience makes discovery feel effortless. Building it is anything but.', next='candy-floss'),
    dict(slug='ps-coffee', name='P.S. Coffee', category='Specialty coffee', filter='coffee', years='Building in 2026', role='Building the venture', location='Ahmedabad, India', color='#d9f66f', image='concept-coffee.webp', caption='P.S. Coffee brand imagery. Proposed Pod format and launch plan remain pre-launch.', subtitle='Good coffee, inside an ordinary day.', metrics=[('5', 'Pods in the proposed launch fleet'), ('50 to 200', 'Sq ft planned Pod format'), ('100%', 'Arabica specialty coffee'), ('Pre-launch', 'Venture stage')],
         description='Specialty coffee designed around a daily habit. Compact, grab-and-go Pods where people already work, move and spend time.', question='Why should a good cup require a detour?',
         context='The venture thesis starts with a gap between specialty coffee as a sit-down occasion and coffee as an everyday routine. P.S. Coffee is being built to serve the latter in Ahmedabad.',
         decisions=[('Put distribution inside the routine.', 'The proposed 50 to 200 sq ft Pod format targets corporate campuses, co-working spaces, gyms and high-footfall corners. No seating and a tight menu keep the focus on convenience.'), ('Keep the product focused.', 'The proposition combines 100% Arabica specialty coffee with ceremonial-grade matcha, using a repeatable menu designed for speed and consistency.'), ('Prove the model before scaling it.', 'The launch plan proposes five Pods to test location types, throughput, menu performance and unit economics. The proof phase is designed to validate the format before a wider rollout.')],
         takeaway='Make quality part of the routine.', next='pujan-energy'),
]
BY_SLUG = {v['slug']: v for v in VENTURES}
SOURCES = {v['slug']: Document(v['slug'] + '.html').root for v in VENTURES}
JOURNEY = Document('journey.html').root.find(cls='t-item')


def art(v):
    photo = ' photo' if v.get('image') else ''
    body = f'<img src="{v["image"]}" alt="{escape(v.get("caption", v["name"]))}" loading="lazy" width="1920" height="928">' if v.get('image') else '<div class="art-grid" aria-hidden="true"></div>'
    title = 'Candy<br>Floss.' if v['slug'] == 'candy-floss' else 'Ximi<br>vogue.' if v['slug'] == 'ximivogue' else ''
    return f'<div class="work-art {v.get("art", "")}{photo}" style="--tile:{v["color"]}">{body}<span class="art-label">{v["category"]} / {v["years"]}</span><div class="art-copy">{title}</div><span class="art-foot">{v["name"] if not photo else ""}</span><span class="art-index">{icon()}</span></div>'


def work_items(ventures):
    stories = []
    for v in ventures:
        names = {'candy-floss':'Candy <em>Floss.</em>', 'pujan-energy':'Pujan <em>Energy.</em>', 'lenskart':'<em>Lens</em>kart.', 'ximivogue':'<em>Ximi</em>vogue.', 'ps-coffee':'P.S. <em>Coffee.</em>'}
        metrics = ''.join(f'<div><strong>{value}</strong><span>{label}</span></div>' for value, label in v['metrics'][:3])
        stories.append(f'<a class="reference-card reference-{v["slug"]} reveal" href="concept-{v["slug"]}.html" data-category="{v["filter"]}"><div class="reference-head"><span>{v["category"]}</span><span>{v["years"]}</span></div><h3>{names[v["slug"]]}</h3><p>{v["description"]}</p><div class="reference-stats">{metrics}</div><div class="reference-foot"><span>{v["role"]}</span><span>Read the story <i>{icon()}</i></span></div></a>')
    return ''.join(stories)


def hero(title, eyebrow, description='', meta='', cls='page-hero', color=None):
    style = f' style="--case:{color}"' if color else ''
    return f'<section class="{cls}"{style}><div class="wrap"><div class="eyebrow">{eyebrow}</div><h1>{title}</h1>{f"<p>{description}</p>" if description else ""}{meta}</div></section>'


NAV = [('index', 'Home'), ('work', 'Work'), ('journey', 'Journey'), ('about', 'About'), ('off-duty', 'Off duty')]
NIGHT_LYRICS = (
    '|| दिल है छोटा सा, छोटी सी आशा',
    'मस्ती भरे मन की, भोली सी आशा',
    'चाँद तारों को, छूने की आशा',
    'आसमानों में उड़ने की आशा ||',
)


def page(slug, title, description, body):
    # Section labels need no ornamental numbering; historical figures stay intact.
    import re
    body = re.sub(r'(?<=>)0[1-5] / ', '', body)
    body = body.replace(' / 01 to 05', '')
    body = re.sub(r'<span>0[1-3]</span>', '<span aria-hidden="true">&#8599;</span>', body)
    nav = ''.join(f'<a href="concept-{key}.html" {"aria-current=page" if slug == key else ""}>{label}</a>' for key, label in NAV[1:])
    menu = ''.join(f'<a href="concept-{key}.html">{label}</a>' for key, label in NAV)
    night_display = ' <i class="night-divider">✦</i> '.join(escape(line) for line in NIGHT_LYRICS)
    night_copy = f'<span class="night-word-copy">{night_display} <i class="night-divider">✦</i></span>'
    night_copies = night_copy * 8
    night_accessible = escape(' '.join(NIGHT_LYRICS))
    css = (ROOT / 'concept-style.css').read_text() + '\n' + (ROOT / 'concept-editorial.css').read_text()
    js = (ROOT / 'concept-script.js').read_text() + '\n' + (ROOT / 'concept-editorial.js').read_text()
    robots = 'index, follow' if ARGS.production else 'noindex, nofollow'
    output = f'''<!DOCTYPE html>
<html lang="en" data-theme="light"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta http-equiv="Content-Security-Policy" content="default-src 'self'; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com; script-src 'self' 'unsafe-inline'; img-src 'self' data:; connect-src 'none'; base-uri 'self'; form-action 'none';">
<meta name="referrer" content="strict-origin-when-cross-origin"><meta http-equiv="Permissions-Policy" content="camera=(), microphone=(), geolocation=(), payment=()">
<link rel="icon" type="image/x-icon" href="favicon.ico"><link rel="icon" type="image/png" sizes="32x32" href="favicon-32x32.png"><link rel="apple-touch-icon" sizes="180x180" href="apple-touch-icon.png">
<meta name="robots" content="{robots}"><meta name="description" content="{escape(description, quote=True)}">
<meta name="color-scheme" content="light dark"><title>{title} | Pulkit Viradiya</title>
<style>{css}</style><script>document.documentElement.classList.add('has-js')</script></head><body class="page-{slug}">
<div class="site-intro" role="status" aria-live="polite" aria-label="अच्छी बातें वक़्त लेती हैं" lang="hi">
  <span class="site-intro-brand" aria-hidden="true">pulkit.</span>
  <div class="site-intro-stage">
    <span class="site-intro-line site-intro-first">अच्छी बातें वक़्त लेती हैं</span>
    <span class="site-intro-line site-intro-second" aria-hidden="true">सहज पके सो मीठा होय</span>
    <span class="site-intro-rule" aria-hidden="true"></span>
  </div>
</div>
<a href="#main" class="skip">Skip to content</a>
<header class="nav"><div class="wrap nav-inner"><a class="logo" href="concept-index.html" aria-label="Pulkit Viradiya, home">pulkit.<small>Founder &amp; operator</small></a><nav class="nav-links" aria-label="Primary">{nav}</nav><div class="nav-tools"><a class="nav-contact" href="mailto:pulkitviradiya@gmail.com">Let’s talk {icon()}</a><button class="icon-btn motion-toggle" type="button" aria-label="Pause motion" aria-pressed="false">{icon('pause')}</button><button class="icon-btn theme-toggle" type="button" aria-label="Switch to dark mode">{icon('sun-moon')}</button><button class="icon-btn mobile-menu" type="button" aria-label="Open navigation" aria-expanded="false" aria-controls="menu-dialog">{icon('menu')}</button></div></div><div class="progress" aria-hidden="true"></div></header>
<dialog class="menu-dialog" id="menu-dialog" aria-label="Navigation"><div class="menu-top"><span>pulkit. / Index</span><button class="icon-btn menu-close" aria-label="Close navigation" type="button">{icon('x')}</button></div><nav class="menu-list">{menu}<a href="mailto:pulkitviradiya@gmail.com">Let’s talk</a></nav></dialog>
<main id="main">{body}
<section class="contact-section" id="contact"><div class="wrap"><div class="eyebrow" lang="hi">अच्छी बातें वक़्त लेती हैं।</div><h2>Let’s <a href="mailto:pulkitviradiya@gmail.com"><span class="serif">talk.</span></a></h2><div class="contact-meta"><a href="mailto:pulkitviradiya@gmail.com">pulkitviradiya@gmail.com {icon()}</a><a href="https://www.linkedin.com/in/pulkitviradiya" target="_blank" rel="noopener noreferrer">LinkedIn {icon()}</a><span>Ahmedabad, India <span data-clock></span></span></div></div></section></main>
<section class="night-footer" aria-label="A quiet night of possibility">
  <div class="night-words" lang="hi">
    <span class="night-words-accessible">{night_accessible}</span>
    <div class="night-words-track" aria-hidden="true">{night_copies}</div>
  </div>
  <div class="night-scene">
    <img src="concept-night-footer.png" alt="Illustration of Pulkit resting beside a lake, looking toward the moon and stars" loading="lazy" width="1877" height="838">
    <div class="night-sparkles" aria-hidden="true">
      <span style="--x:17%;--y:20%;--delay:0s"></span><span style="--x:36%;--y:12%;--delay:1.5s"></span><span style="--x:58%;--y:23%;--delay:3s"></span><span style="--x:76%;--y:14%;--delay:.8s"></span><span style="--x:89%;--y:31%;--delay:2.2s"></span>
    </div>
  </div>
</section>
<div class="radhe-section"><hr class="radhe-rule"><span class="radhe-text" lang="hi">|| राधे राधे ||</span><hr class="radhe-rule"></div>
<footer class="footer"><div class="wrap"><span>&copy; <span data-year>2026</span> Pulkit Viradiya</span><a href="concept-work.html">A life in the making.</a><span>Stay curious. See you around, Pulkit.</span></div></footer>
<div class="page-wipe" aria-hidden="true"><span>Pulkit Viradiya.</span></div><div class="cursor-note" aria-hidden="true">Explore chapter &#8599;</div>
<script>{js}</script></body></html>'''
    output = output.replace(icon('pause'), f'<span class="motion-on">{icon("pause")}</span><span class="motion-off">{icon("play")}</span>', 1)
    if ARGS.production:
        for page_slug in PAGE_SLUGS:
            output = output.replace(f'href="concept-{page_slug}.html', f'href="{page_slug}.html')
    assert '\u2014' not in output
    (ROOT / f'{PREFIX}{slug}.html').write_text(output)


hero_photo = 'concept-hero-daylight.png'
hero_class = 'hero' if hero_photo != 'pulkit.jpg' else 'hero hero-original'
home = f'''<section class="{hero_class}"><img class="hero-img" src="{hero_photo}" alt="Pulkit Viradiya" fetchpriority="high"><div class="hero-shade" aria-hidden="true"></div><div class="wrap"><div class="hero-top"><span class="eyebrow">Founder. Operator. Endlessly curious.</span><span>Independent by nature / Ahmedabad, India</span></div><div class="hero-name-block"><h1 class="hero-heading"><span class="hero-line"><span>Pulkit</span></span><span class="hero-line"><span class="serif">Viradiya.</span></span></h1><p class="hero-caption">Building businesses.<br>Understanding people.<br>Finding the extraordinary in the everyday.</p></div><div class="hero-rule" aria-hidden="true"></div><div class="hero-bottom"><div class="hero-disc"><a href="#opening" aria-label="Discover the portfolio">{icon('arrow-down')}</a><span>Scroll to<br>discover</span></div><div class="hero-location">Consumer brands. Retail. Clean energy.<small>Five ventures / One ongoing story</small></div></div></div><div class="hero-side" aria-hidden="true">A LIFE IN THE MAKING / 2026</div></section>
<div class="wrap ticker"><span><i class="ticker-dot"></i>Currently building P.S. Coffee</span><span>Consumer brands / Retail / Clean energy</span><span>01 / An ongoing story</span></div>
<section class="section wrap" id="opening"><div class="intro reveal"><div class="eyebrow">A little context</div><div><h2>A store. A supply chain.<br>A solar plant. <span class="serif">A daily ritual.</span><br>Different businesses.<br>The same curiosity.</h2><p>I’m a founder and operator who connects how people behave with how businesses run. My work spans eleven stores, a domestic vendor ecosystem, a solar venture, and a new bet on specialty coffee.</p></div></div>{proof([('11','Candy Floss stores scaled'),('200+','Domestic vendors built into the network'),('0.45 MW','Installed solar capacity'),('11 years','Lenskart franchise partnership')])}</section>
<div class="chapter-tape" aria-hidden="true"><div class="tape-track"><span>Observe. <b>✳</b> <em>Imagine.</em> <b>✳</b> Build. <b>✳</b> <em>Repeat.</em> <b>✳</b></span><span>Observe. <b>✳</b> <em>Imagine.</em> <b>✳</b> Build. <b>✳</b> <em>Repeat.</em> <b>✳</b></span></div></div>
<section class="section wrap" id="work"><div class="section-head reveal"><div><div class="eyebrow">Selected work / 01 to 05</div><h2>Ideas, <span class="serif">made real.</span></h2></div>{link('The complete index', 'concept-work.html')}</div><div class="work-grid">{work_items(VENTURES)}</div></section>
<section class="section dark-band"><div class="wrap"><div class="eyebrow">The thread through it all</div><h2 class="thesis reveal">Understand people.<br>Build the system.<br><span class="serif">Stay for the details.</span></h2><div class="process"><article><span>01 / OBSERVE</span><h3>Start on the ground.</h3><p>A queue outside a store. An industrial energy need. A coffee run that takes too long. The questions start in ordinary places.</p></article><article><span>02 / BUILD</span><h3>Connect the moving parts.</h3><p>Product, pricing, people, vendors and distribution. My role is to make them work as one business.</p></article><article><span>03 / OPERATE</span><h3>Make it work again tomorrow.</h3><p>The opening is only the beginning. The real work lives in consistent delivery, healthy economics and the details people feel.</p></article></div></div></section>
<section class="section wrap journey-strip"><img class="journey-image reveal" src="pulkit-right.jpg" alt="Pulkit looking to the right" loading="lazy" width="500" height="500"><div class="reveal"><div class="eyebrow">Not a straight line</div><h2>Mumbai. Gujarat.<br>Cairo. Macau.<br><span class="serif">Still curious.</span></h2><p>Before the businesses came classrooms, research and a summer in Egypt. Each chapter added a different way of seeing.</p>{link('Follow the journey', 'concept-journey.html')}<div class="chapter-list"><a class="chapter-row" href="concept-cairo.html"><span>2013</span><strong>Learning in Cairo</strong>{icon()}</a><a class="chapter-row" href="concept-research.html"><span>2014</span><strong>Questions without borders</strong>{icon()}</a><a class="chapter-row" href="concept-education.html"><span>1995+</span><strong>The early foundations</strong>{icon()}</a></div></div></section>
<section class="section off-duty-teaser"><div class="wrap"><div><div class="small-index">A person, not just a portfolio</div><h2>There’s always<br><span class="serif">another rabbit hole.</span></h2></div><div><p>Pour-over coffee in the morning. A brand worth breaking down. A new way to use AI. Curiosity doesn’t really clock out.</p>{link('Meet me off duty', 'concept-off-duty.html')}</div></div></section>'''
home = home.replace('<div class="hero-name-block">', '<div class="hero-name-block"><div class="hero-native-name"><span lang="gu">પુલકિત</span><span aria-hidden="true">·</span><span lang="hi">पुलकित</span></div>', 1)
page('index', 'Founder, operator, endlessly curious', 'Pulkit Viradiya builds consumer brands, retail businesses and clean energy infrastructure. Explore the work and the person behind it.', home)

backdrops = ''
chapter_links = ''
for i, venture in enumerate(VENTURES):
    media = f'<img src="{venture["image"]}" alt="" loading="lazy">' if venture.get('image') else f'<div class="backdrop-type {"ximi" if venture["slug"] == "ximivogue" else ""}">{venture["name"]}</div>'
    backdrops += f'<div data-backdrop="{venture["slug"]}" class="{"active" if i == 0 else ""}">{media}</div>'
    chapter_links += f'<a class="work-chapter" data-preview="{venture["slug"]}" href="concept-{venture["slug"]}.html"><strong>{venture["name"]}</strong><span>{venture["category"]}</span>{icon()}</a>'
work = f'<section class="work-opening"><div class="work-backdrops" aria-hidden="true">{backdrops}</div><div class="work-opening-top"><div><div class="eyebrow">Selected chapters / 01 to 05</div><h1>A body<br>of <span class="serif">work.</span></h1></div><p>Different industries. Different questions.<br>One instinct: understand deeply,<br>then build with intent.</p></div><nav class="work-chapters" aria-label="Venture chapters">{chapter_links}</nav><div class="work-opening-bottom"><span>Five businesses. One curious mind.</span><a href="#work-index">The full stories {icon("arrow-down")}</a></div></section>'
work += f'<section class="wrap section work-index-section">{filters("work-index", [("all","All ventures"),("retail","Retail & brands"),("energy","Clean energy"),("coffee","Coffee")])}<div class="timeline-counter" data-counter="work-index" aria-live="polite">5 ventures</div><div class="work-grid" id="work-index">{work_items(VENTURES)}</div></section>'
page('work', 'The work', 'Five venture chapters: Candy Floss, Pujan Energy, Lenskart, Ximivogue and P.S. Coffee.', work)

for v in VENTURES:
    meta = '<div class="hero-meta">' + ''.join(f'<span>{escape(s)}</span>' for s in [v['role'],v['years'],v['location']]) + '</div>'
    if v['slug'] == 'ps-coffee':
        meta += f'<a class="text-link case-site-link" href="https://www.pscoffee.in/" target="_blank" rel="noopener noreferrer" aria-label="Visit the P.S. Coffee website (opens in a new tab)">www.pscoffee.in{icon()}</a>'
    body = hero(v['name'], v['category'] + ' / A chapter in practice', v['description'], meta, 'page-hero case-top', v['color'])
    if v.get('image'):
        body += f'<figure class="case-cover"><img src="{v["image"]}" alt="{escape(v["caption"])}" width="1920" height="928" fetchpriority="high"><figcaption>{v["caption"]}</figcaption></figure>'
    else:
        body += f'<div class="case-graphic" style="--case:{v["color"]}"><strong>{v["metrics"][0][0]}</strong><span>{"stores, built from a decision to begin again." if v["slug"] == "candy-floss" else "cities. A new way to understand the customer."}</span></div>'
    body += f'<div class="wrap"><nav class="case-nav" aria-label="In this case study"><a href="#context">The context</a><a href="#decisions">The decisions</a><a href="#detail">The detail</a><a href="#outcome">The takeaway</a></nav>{proof(v["metrics"])}'
    body += f'<section class="case-section" id="context"><div><div class="eyebrow">01 / The context</div><h2>{v["question"]}</h2></div><div class="prose"><p>{v["context"]}</p><div class="detail-list"><details><summary>The full background {icon("plus")}</summary>{clean("".join(p.html() for p in SOURCES[v["slug"]].find(cls="v-overview")[0].find(tag="p")))}</details></div></div></section>'
    body += '<section class="case-section" id="decisions"><div><div class="eyebrow">02 / The decisions</div><h2>Where I put<br>the <span class="serif">work.</span></h2></div><div class="prose">'
    for i, (heading, copy) in enumerate(v['decisions'], 1):
        body += f'<article class="decision reveal"><span>0{i}</span><h3>{heading}</h3><p>{copy}</p></article>'
    body += '</div></section><section class="case-section" id="detail"><div><div class="eyebrow">03 / The operating detail</div><h2>Behind the<br><span class="serif">headline.</span></h2></div><div class="detail-list prose">'
    for highlight in SOURCES[v['slug']].find(cls='v-highlight'):
        headings = highlight.find(tag='h3')
        if headings:
            body += f'<details><summary>{escape(headings[0].text())}{icon("plus")}</summary>{clean("".join(p.html() for p in highlight.find(tag="p")))}</details>'
    body += '</div></section></div>'
    body += f'<section class="section dark-band" id="outcome"><div class="wrap"><div class="eyebrow">04 / What stays with me</div><h2 class="thesis reveal">{v["takeaway"]}</h2>{link("Follow P.S. Coffee", "https://www.pscoffee.in/") if v["slug"] == "ps-coffee" else ""}</div></section>'
    nxt = BY_SLUG[v['next']]
    body += f'<section class="wrap next-chapter"><div class="eyebrow">Another chapter</div><a href="concept-{nxt["slug"]}.html">{nxt["name"]}{icon()}</a></section>'
    page(v['slug'], v['name'] + ' / ' + v['role'], v['description'], body)


def timeline_item(item, i):
    year_node = item.find(cls='t-year')[0]
    year = ''.join(c for c in year_node.children if isinstance(c, str)).strip()
    duration = year_node.find(cls='duration')[0].text().replace(', ', ' to ')
    category = item.find(cls='t-cat')[0].text()
    title_node = item.find(cls='t-title')[0]
    title = ''.join(c.html() if isinstance(c, Node) else escape(c) for c in title_node.children)
    category_filter = 'education' if category == 'Education' else 'experience' if category in ['Internship','Research'] else 'ventures'
    destination = 'education' if category == 'Education' else 'cairo' if category == 'Internship' else 'research' if category == 'Research' else 'about'
    title_text = title_node.text()
    for v in VENTURES:
        if v['name'] in title_text:
            destination = v['slug']
    descriptions = clean(''.join(p.html() for p in item.find(cls='t-desc')))
    if category == 'Today':
        title = 'Operating. Building. <em>Still learning.</em>'
        descriptions = '<p>Operating Pujan Energy while building the P.S. Coffee venture in Ahmedabad. Exploring AI as a practical tool for simplifying the work around both.</p>'
        destination = 'ps-coffee'
    color = 'var(--growth)' if destination in ['pujan-energy','ps-coffee'] else 'var(--invitation)' if destination in ['candy-floss','cairo','research'] else 'var(--curiosity)'
    state = ' is-current' if category == 'Today' else ' is-milestone' if category_filter != 'education' else ''
    return f'<article class="timeline-row reveal{state}" data-category="{category_filter}" style="--entry:{color}"><div class="timeline-year">{year}<small>{duration}</small></div><div class="timeline-body"><div class="eyebrow">{category}</div><h3>{clean(title)}</h3>{descriptions}{link("Explore this chapter", f"concept-{destination}.html")}</div></article>'


def skills_and_interests():
    groups = [
        ('Top skills', 'What I do, day to day.', [
            ('Brand Development', '0 to 1 build, positioning, identity'),
            ('Entrepreneurship', 'Multi-venture operating'),
            ('E-Commerce', 'Shopify, marketplaces, D2C'),
            ('Retail Operations', 'SOPs, P&L, store ops'),
            ('Private Label', 'OEM, BOM, vendor networks'),
            ('Supply Chain', '200+ vendor ecosystem')]),
        ('Outside work', 'Where the curiosity goes.', [
            ('Pour-over coffee', 'Black, every morning'),
            ('Coffee experimentation', 'Beans, methods, flavours'),
            ('Podcasts', 'Business, building, brands'),
            ('Brand teardowns', 'What works, what doesn’t, why'),
            ('AI experimentation', 'For workflow leverage'),
            ('Conversations', 'On building, scaling, new ideas')])]
    columns = ''
    for label, heading, items in groups:
        rows = ''.join(f'<li><h3>{escape(name)}</h3><p>{escape(detail)}</p></li>' for name, detail in items)
        columns += f'<div class="personal-column reveal"><div class="eyebrow">{label}</div><h2>{heading}</h2><ul>{rows}</ul></div>'
    return f'<section class="section wrap personal-details" aria-label="Skills and interests">{columns}</section>'


journey = hero('A life in<br><span class="serif">the making.</span>', 'Now to 1995 / The journey', 'What I’m building today, and the chapters that brought me here. Work, questions and learning, traced back to the beginning.')
journey = journey.replace('</section>', '<div class="journey-route" aria-hidden="true"><svg viewBox="0 0 400 500" fill="none"><path class="route-base" d="M30 470V370Q30 320 90 320H265Q330 320 330 260V215Q330 165 265 165H165Q110 165 110 110V85Q110 35 170 35H365"/><path class="route-motion" d="M30 470V370Q30 320 90 320H265Q330 320 330 260V215Q330 165 265 165H165Q110 165 110 110V85Q110 35 170 35H365"/><circle cx="30" cy="470" r="7"/><circle cx="330" cy="260" r="7"/><circle cx="110" cy="110" r="7"/><circle cx="365" cy="35" r="7"/></svg></div></section>', 1)
journey += f'<section class="wrap" style="padding-bottom:70px">{filters("timeline",[("all","All chapters"),("ventures","Ventures"),("experience","Research & experience"),("education","Education")])}<div class="timeline-counter" data-counter="timeline" aria-live="polite">{len(JOURNEY)} chapters</div><div class="timeline" id="timeline">' + ''.join(timeline_item(item, i) for i,item in reversed(list(enumerate(JOURNEY)))) + '</div></section>'
journey += skills_and_interests()
page('journey', 'The journey', 'The full chronological journey of Pulkit Viradiya, from school and university to Cairo, research and five venture chapters.', journey)

about = hero('Curiosity is<br><span class="serif">the constant.</span>', 'The person behind the work', 'Founder. Retail operator. Clean-energy co-founder. Someone who asks how things work, then gets involved in making them work better.')
about += f'''<section class="wrap section portrait-section"><img src="pulkit.jpg" alt="Portrait of Pulkit Viradiya" loading="lazy" width="2784" height="4176"><div><div class="eyebrow">The story behind the thesis</div><blockquote class="quote">“What just happened in there?”</blockquote><p>In 2018, I walked into a Delhi store after seeing a queue outside. I had no plan to buy anything. I left with Rs 2,500 of products I hadn’t known I wanted.</p><p>That question led me into consumer behaviour, impulse buying and the design of retail experiences. It took shape in Ximivogue, grew into Candy Floss, and still shapes the way I look at a business.</p><p>Alongside retail, I co-founded Pujan Energy. Different industry, same discipline: connect the parts, understand the economics, and make the operation dependable.</p></div></section>
<section class="section dark-band"><div class="wrap"><div class="eyebrow">How I think about the work</div><h2 class="thesis">Businesses grow by<br>understanding <span class="serif">people.</span></h2><div class="process"><article><span>BRAND & PRODUCT</span><h3>From an insight to a shelf.</h3><p>Positioning, private label, product development and vendor relationships, grounded in what customers value.</p></article><article><span>OPERATIONS & ECONOMICS</span><h3>Make the parts add up.</h3><p>Store P&amp;L, supply chains, inventory, teams and repeatable processes across retail and infrastructure.</p></article><article><span>CURIOSITY & TOOLS</span><h3>Keep learning in public.</h3><p>Exploring AI to simplify daily workflows, studying brands, and bringing what I learn back into the work.</p></article></div></div></section>
<section class="section wrap"><div class="section-head"><div><div class="eyebrow">A wider perspective</div><h2>More than <span class="serif">one language.</span></h2></div></div><div class="languages"><span>Gujarati<small>Native</small></span><span>Hindi<small>Fluent</small></span><span>English<small>Professional</small></span><span>Marathi<small>Conversational</small></span></div><div class="chapter-list"><a class="chapter-row" href="concept-education.html"><span>01</span><strong>Education & foundations</strong>{icon()}</a><a class="chapter-row" href="concept-cairo.html"><span>02</span><strong>AIESEC in Cairo</strong>{icon()}</a><a class="chapter-row" href="concept-research.html"><span>03</span><strong>Research & presentations</strong>{icon()}</a></div></section>'''
about += skills_and_interests()
page('about', 'The person behind the work', 'The operating philosophy, curiosity and experience behind Pulkit Viradiya’s ventures.', about)

education = hero('The early<br><span class="serif">foundations.</span>', 'Education / 1995 to 2014', 'From Mumbai to Gujarat, then business administration and economics at Pandit Deendayal Energy University.')
education += '<section class="wrap section" style="padding-top:0">'
for item in JOURNEY:
    if item.find(cls='t-cat')[0].text() != 'Education':
        continue
    duration = item.find(cls='duration')[0].text().replace(', ', ' to ')
    title = item.find(cls='t-title')[0].text()
    sub = item.find(cls='t-sub')
    education += f'<article class="education-row"><span>{duration}</span><div><h3>{escape(title)}</h3>{f"<p>{escape(sub[0].text())}</p>" if sub else ""}{clean("".join(p.html() for p in item.find(cls="t-desc")))}</div></article>'
education += '</section><section class="section dark-band"><div class="wrap"><div class="eyebrow">2010 to 2014 / PDEU</div><h2 class="thesis">An analytical foundation.<br>A wider <span class="serif">worldview.</span></h2><p style="margin-top:30px">Business administration with an economics focus laid the groundwork for research, international experience and the operating decisions that followed.</p></div></section>'
education += f'<section class="wrap next-chapter"><div class="eyebrow">Beyond the classroom</div><a href="concept-cairo.html">A summer in Cairo {icon()}</a></section>'
page('education', 'Education & foundations', 'Pulkit Viradiya’s education from 1995 to 2014, including PDEU, P. P. Savani, Mumbai and Valsad schools.', education)

cairo = hero('Learning in<br><span class="serif">Cairo.</span>', 'AIESEC / Global Community Development Program', 'A summer outside the familiar. Cross-cultural work, tourism research and a closer look at an economy in transition.', '<div class="hero-meta"><span>May to June 2013</span><span>Cairo, Egypt</span><span>International internship</span></div>', 'page-hero case-top', '#bce1de')
cairo += '<section class="wrap case-section"><div><div class="eyebrow">01 / The assignment</div><h2>Explore Egypt.</h2></div><div class="prose"><p>Selected for AIESEC’s Global Community Development Program, I worked with a local NGO on the Explore Egypt tourism project. The work promoted cultural and tourism experiences across multiple Egyptian cities.</p><p>In a team spanning different nationalities, I created content, blogs and documentation for a centralised tourism database. The assignment brought research, communication and cross-cultural collaboration into the same daily practice.</p></div></section>'
cairo += '<section class="wrap case-section"><div><div class="eyebrow">02 / The questions</div><h2>An economy<br>in transition.</h2></div><div class="prose"><p>I also authored a research paper, <em>Political Crisis and its Impact on Egypt’s Economy</em>, looking at macroeconomic shifts in an evolving market.</p><p>This was early exposure to working in an unstructured environment and understanding emerging-market dynamics from the ground up. There was no familiar operating playbook to lean on.</p></div></section><section class="section dark-band"><div class="wrap"><div class="eyebrow">What the chapter added</div><h2 class="thesis">A different place.<br>A different <span class="serif">way of seeing.</span></h2></div></section>'
cairo += f'<section class="wrap next-chapter"><div class="eyebrow">Follow the questions</div><a href="concept-research.html">Research & presentations {icon()}</a></section>'
page('cairo', 'AIESEC, Cairo', 'Pulkit Viradiya’s 2013 AIESEC international internship, Explore Egypt tourism work and economic research.', cairo)

research = hero('Questions<br><span class="serif">without borders.</span>', 'Research & presentations / 2013 to 2014', 'Sustainability, economic development and the pressures of urbanisation. Early work in turning a complex question into a structured argument.')
research += '<section class="wrap case-section"><div><div class="eyebrow">December 2013</div><h2>Sustainable<br>development.</h2></div><div class="prose"><p>Presented research at national and international conferences on sustainability, governance and economic development.</p><p>Co-presented on sustainable rural development at Rajiv Gandhi National University of Law. In New Delhi, the research explored the role of the public and private sectors in sustainable development.</p></div></section>'
research += '<section class="wrap case-section"><div><div class="eyebrow">January 2014 / Macau</div><h2>ICCKS 2014.</h2></div><div class="prose"><p>Selected for an oral presentation at ICCKS 2014, representing India among participants from more than 20 countries.</p><h3 style="margin-top:28px">Challenges Posed by Rapid Urbanisation and Scarce Resources</h3><p>The paper focused on sustainability, infrastructure stress and future urban-development models. Discussions with researchers and academics broadened the context around economic development and policy.</p><p>The lasting skills were practical: analytical thinking, public speaking and making a structured case for an idea.</p></div></section>'
research += '<section class="section dark-band"><div class="wrap"><div class="eyebrow">From research to practice</div><h2 class="thesis">Learn to ask better.<br>Then build <span class="serif">with intent.</span></h2></div></section>'
research += f'<section class="wrap next-chapter"><div class="eyebrow">Into the operating years</div><a href="concept-lenskart.html">The Lenskart chapter {icon()}</a></section>'
page('research', 'Research & presentations', 'Research and international presentations on sustainable development, urbanisation and scarce resources.', research)

off = hero('Off <span class="serif">duty.</span><br>Still switched on.', 'A few things beyond the work', 'The morning ritual. The brands worth studying. The tools worth trying. A small window into where the curiosity goes.')
off += '<figure><img class="coffee-wide" src="concept-coffee.webp" alt="P.S. Coffee branded cups, from the brand’s image collection" loading="lazy" width="1672" height="944"></figure>'
off += '<section class="section wrap"><div class="interests"><article><span>01 / DAILY RITUAL</span><h3>Black coffee.<br>Every morning.</h3><p>Pour-over coffee is a daily constant. Experimenting with beans, brewing methods and flavours keeps the ritual interesting.</p></article><article><span>02 / ALWAYS STUDYING</span><h3>A brand is<br>a set of decisions.</h3><p>I break down brands to understand what works, what doesn’t and why. Product, price, distribution and customer behaviour rarely make sense in isolation.</p></article><article><span>03 / NEW TOOLS</span><h3>AI, put<br>to practical use.</h3><p>I’m experimenting with AI to simplify workflows and day-to-day operations. Curiosity and a willingness to learn are the starting point.</p></article></div></section>'
off += f'<section class="section wrap" style="padding-top:0"><div class="section-head"><div><div class="eyebrow">The personal shelf</div><h2>On repeat.<br><span class="serif">In progress.</span></h2></div></div><div class="listening"><article><div class="vinyl" aria-hidden="true"></div><h3>Listening room</h3><p>Music for the hours between ideas. The personal playlist is still being selected.</p><span class="status">Spotify selection coming soon</span></article><article><div style="height:275px;display:grid;place-items:center;background:var(--panel)"><span style="font-size:90px;font-family:Georgia;font-style:italic">Why?</span></div><h3 style="margin-top:35px">The learning queue</h3><p>Business, building and brands. A collection of favourite channels and conversations is taking shape.</p><span class="status">YouTube selections coming soon</span></article></div></section>'
off += '<section class="section off-duty-teaser"><div class="wrap"><h2>The best ideas<br>often start with<br><span class="serif">a conversation.</span></h2><div><p>Building something? Found a brand worth studying? Or just want to talk about a good cup of coffee?</p>' + link('Say hello', 'mailto:pulkitviradiya@gmail.com') + '</div></div></section>'
page('off-duty', 'Off duty, still curious', 'Pour-over coffee, brand teardowns, AI experiments and the interests beyond Pulkit Viradiya’s ventures.', off)

print(f'Built {len(PAGE_SLUGS)} standalone {"production" if ARGS.production else "concept"} pages.')
