#!/usr/bin/env python3
import json, html

def YT(q):
    from urllib.parse import quote_plus
    return "https://www.youtube.com/results?search_query=" + quote_plus(q)
def POD(q):
    from urllib.parse import quote_plus
    return "https://podcasts.apple.com/us/search?term=" + quote_plus(q)
def W(label, q, direct=None):
    if direct:
        return [label, direct, "video"]
    return [label + " (YouTube search)", YT(q), "search"]
def P(label, q):
    return [label + " (podcast search)", POD(q), "search"]

A = []
def add(id, title, dek, cat, date, body, claim, pushback, proves, notproves, timeline, sources, watch):
    A.append(dict(id=id, title=title, dek=dek, cat=cat, date=date, body=body, claim=claim,
                  pushback=pushback, proves=proves, notproves=notproves, timeline=timeline,
                  sources=sources, watch=watch))

# ---------------- IMAGES (verified, local) ----------------
# Local files in images/ — all downloaded from Wikimedia Commons (public domain / CC).
# Credit lines are shown under each photo. Articles without a verified photo get a
# designed monogram tile instead of a broken or guessed image.
IMAGES = {
 "sulawesi": ("images/sulawesi.png", "Topographic map of Sulawesi, Indonesia — Wikimedia Commons, GEBCO / OpenStreetMap contributors"),
 "lisbon": ("images/lisbon.jpg", "1755 copper engraving of Lisbon in ruins — public domain, via Wikimedia Commons"),
 "houdini": ("images/houdini.jpg", "Harry Houdini, c. 1899 — Library of Congress, public domain, via Wikimedia Commons"),
 "antikythera": ("images/antikythera.jpg", "Antikythera mechanism, National Archaeological Museum, Athens — Joy of Museums, via Wikimedia Commons"),
 "wow": ("images/wow.jpg", "The original Wow! signal printout, 15 Aug 1977 — Big Ear Radio Observatory / NAAPO, via Wikimedia Commons"),
 "cooper": ("images/cooper.jpg", "FBI composite sketch of D.B. Cooper, 1973 — FBI, public domain, via Wikimedia Commons"),
 "agincourt": ("images/agincourt.jpg", "Battle of Agincourt, 15th-century miniature — Bibliothèque nationale de France, public domain, via Wikimedia Commons"),
 "hancock": ("images/gobekli.jpg", "Göbekli Tepe, Şanlıurfa — Teomancimit, via Wikimedia Commons"),
 "fieldguide": ("images/neanderthal.jpg", "Replica Neanderthal skull — CC0, via Wikimedia Commons"),
 "hawass": ("images/giza.jpg", "The pyramids of Giza — Morhaf Kamal Aljanee, via Wikimedia Commons"),
 "biondi": ("images/giza.jpg", "The pyramids of Giza — Morhaf Kamal Aljanee, via Wikimedia Commons"),
 "easter": ("images/moai.jpg", "Ahu Tongariki's 15 moai — Camill1336, via Wikimedia Commons"),
 "tunguska": ("images/tunguska.jpg", "Flattened trees at Tunguska, photographed on the Kulik expeditions — public domain, via Wikimedia Commons"),
 "voynich": ("images/voynich.jpg", "The Rosettes foldout (folios 85v–86r) — six panels of circular diagrams — public domain, Beinecke Library scan via Wikimedia Commons"),
 "pompeii": ("images/pompeii.jpg", "Pompeii's Forum with Mount Vesuvius towering above — Qfl247, via Wikimedia Commons (CC BY-SA)"),
 "earhart": ("images/earhart.jpg", "Amelia Earhart standing under the nose of her Lockheed Electra 10E, 1937 — Underwood & Underwood, public domain, via Wikimedia Commons"),
 "sphinx": ("images/sphinx.jpg", "The Great Sphinx of Giza with Khafre's pyramid behind it, May 2015 — MusikAnimal, via Wikimedia Commons (CC BY-SA 3.0)"),
}
# Fun, category-coloured monogram tiles for articles without a verified photo.
TILE_EMOJI = {"History": "🏛️", "Deep Past": "🦴", "Rogan Science": "🔬", "Contested": "❓"}
TILE_GRAD = {"History": "linear-gradient(135deg,#f59e0b,#ef4444)", "Deep Past": "linear-gradient(135deg,#059669,#0ea5e9)", "Rogan Science": "linear-gradient(135deg,#7c3aed,#db2777)", "Contested": "linear-gradient(135deg,#334155,#f59e0b)"}
def card_media(a):
    if a["id"] in IMAGES:
        f, cr = IMAGES[a["id"]]
        return '<div class="media"><img src="%s" alt="%s" loading="lazy"><span class="credit">%s</span></div>' % (f, html.escape(a["title"], quote=True), html.escape(cr))
    em = TILE_EMOJI.get(a["cat"], "📖")
    gr = TILE_GRAD.get(a["cat"], "linear-gradient(135deg,#0ea5e9,#7c3aed)")
    init = html.escape(a["title"][:1].upper())
    return '<div class="media tile" style="background:%s"><span class="tile-emoji">%s</span><span class="tile-init">%s</span><span class="tile-note">Illustrated cover — no verified photo available</span></div>' % (gr, em, init)
def hero_media(a):
    if a["id"] in IMAGES:
        f, cr = IMAGES[a["id"]]
        return '<figure class="hero-img"><img src="%s" alt="%s"><figcaption>📸 %s</figcaption></figure>' % (f, html.escape(a["title"], quote=True), html.escape(cr))
    return card_media(a)
def visual_block(a):
    # Visual-first box, built ONLY from the article's own timeline / proves / sources.
    # No new facts are introduced here.
    n_tl = len(a["timeline"]); n_src = len(a["sources"]); n_pro = len(a["proves"]); n_not = len(a["notproves"])
    tl = "".join('<div class="tl-step"><span class="dot"></span><b>%s</b><span>%s</span></div>' % (html.escape(y), html.escape(t)) for y, t in a["timeline"])
    extra = ""
    if a["id"] == "sulawesi":
        extra = """<div class="chart"><h4>🕰️ How old is this? (log scale — years ago)</h4>
        <div class="bar-row"><span>Today</span><div class="bar"><i style="width:2%"></i></div><b>0</b></div>
        <div class="bar-row"><span>Oldest Sulawesi tools before this find</span><div class="bar"><i style="width:38%"></i></div><b>~194,000 yrs</b></div>
        <div class="bar-row"><span>Calio tools — at least</span><div class="bar"><i style="width:82%"></i></div><b>1,040,000 yrs</b></div>
        <div class="bar-row"><span>Calio tools — possibly up to</span><div class="bar"><i style="width:100%"></i></div><b>1,480,000 yrs</b></div>
        <p class="small">Bars are drawn on a log scale so a million years fits on one screen. Ages are the ones in the article.</p></div>
        <div class="mapbox"><h4>🗺️ Schematic map — not to scale</h4><p>Mainland Southeast Asia (Sunda) &nbsp;→&nbsp; <b>deep water</b> &nbsp;→&nbsp; <b>Sulawesi (Calio)</b> &nbsp;·&nbsp; Flores (Wolo Sege) &nbsp;·&nbsp; Luzon. Walking there was never an option — that is the mystery.</p></div>"""
    if a["id"] == "roanoke":
        extra = """<div class="mapbox"><h4>🗺️ Schematic map — not to scale: where did they go?</h4><p><b>Roanoke Island</b> (the empty settlement) &nbsp;→&nbsp; <b>~50 miles south</b> to <b>Croatoan / Hatteras Island</b>, home of Manteo's people &nbsp;·&nbsp; <b>~50 miles west</b> to <b>Site X / Site Y</b> in Bertie County, on the Chowan River. The leading theory says the colonists split between these two directions — but no single find proves the whole journey.</p></div>
        <div class="chart"><h4>🔍 The clue board — what was found, and what it is worth</h4>
        <div class="bar-row"><span>Word carved at the fort</span><div class="bar"><i style="width:100%"></i></div><b>CROATOAN</b></div>
        <div class="bar-row"><span>Distress cross carved with it?</span><div class="bar"><i style="width:2%"></i></div><b>None</b></div>
        <div class="bar-row"><span>Bodies or graves found</span><div class="bar"><i style="width:2%"></i></div><b>None</b></div>
        <div class="bar-row"><span>Signs of a battle</span><div class="bar"><i style="width:2%"></i></div><b>None</b></div>
        <p class="small">Bars are a visual summary of the article's evidence, not measurements. The empty fort is the mystery: everything else is interpretation.</p></div>"""
    if a["id"] == "easter":
        extra = """<div class="chart"><h4>👥 How many people? The old story vs. the new evidence</h4>
        <div class="bar-row"><span>Ecocide story: peak population claimed</span><div class="bar"><i style="width:100%"></i></div><b>15,000–30,000</b></div>
        <div class="bar-row"><span>Rock gardens could feed, at most</span><div class="bar"><i style="width:13%"></i></div><b>~4,000</b></div>
        <div class="bar-row"><span>What Europeans found (1722)</span><div class="bar"><i style="width:10%"></i></div><b>~3,000</b></div>
        <div class="bar-row"><span>Survivors left by 1877</span><div class="bar"><i style="width:2%"></i></div><b>~111</b></div>
        <p class="small">Bars are drawn to scale from the article's figures. The crash that really happened came in the 1860s — by ship, not by statue.</p></div>
        <div class="mapbox"><h4>🗺️ Schematic map — not to scale</h4><p><b>Rano Raraku quarry</b> (where ~95% of moai were carved) &nbsp;→&nbsp; <b>ancient roads</b> &nbsp;→&nbsp; <b>ahu platforms around the coast</b>, statues facing inland. The island sits in the south-east Pacific, over 3,500 km from the coast of Chile.</p></div>"""
    if a["id"] == "tunguska":
        extra = """<div class="chart"><h4>💥 How big was the blast? (log scale — megatons of TNT)</h4>
        <div class="bar-row"><span>Hiroshima bomb, 1945</span><div class="bar"><i style="width:2%"></i></div><b>~0.015 Mt</b></div>
        <div class="bar-row"><span>Chelyabinsk airburst, 2013</span><div class="bar"><i style="width:18%"></i></div><b>~0.5 Mt</b></div>
        <div class="bar-row"><span>Tunguska — low estimate</span><div class="bar"><i style="width:48%"></i></div><b>3 Mt</b></div>
        <div class="bar-row"><span>Tunguska — often quoted</span><div class="bar"><i style="width:82%"></i></div><b>10–15 Mt</b></div>
        <div class="bar-row"><span>Tunguska — high estimate</span><div class="bar"><i style="width:100%"></i></div><b>30 Mt</b></div>
        <p class="small">Bars are drawn on a log scale so a city bomb and a megaton blast fit on one screen. Tunguska's true yield is a range, not one number — that is the honest state of the science.</p></div>
        <div class="mapbox"><h4>🗺️ Schematic — not to scale: what happened in the sky</h4><p>A rock about 50–80 m across streaks in from the <b>south-east</b> &nbsp;→&nbsp; it bursts <b>5–10 km up</b> instead of hitting the ground &nbsp;→&nbsp; the blast flattens a butterfly-shaped <b>2,150 km²</b> of forest &nbsp;→&nbsp; directly underneath, an <b>~8 km zone of trees stays standing</b>, stripped of branches like telegraph poles, because the blast hit them straight from above.</p></div>"""
    if a["id"] == "voynich":
        extra = """<div class="chart"><h4>🔢 How big is the mystery? (log scale — the numbers in the article)</h4>
        <div class="bar-row"><span>Pages surviving</span><div class="bar"><i style="width:45%"></i></div><b>~240</b></div>
        <div class="bar-row"><span>Different words</span><div class="bar"><i style="width:75%"></i></div><b>~9,000</b></div>
        <div class="bar-row"><span>Words in the book</span><div class="bar"><i style="width:87%"></i></div><b>~38,000</b></div>
        <div class="bar-row"><span>Characters (glyphs)</span><div class="bar"><i style="width:100%"></i></div><b>~170,000</b></div>
        <div class="bar-row"><span>Words anyone has ever read</span><div class="bar"><i style="width:2%"></i></div><b>0</b></div>
        <p class="small">Bars are drawn on a log scale so a page count and a glyph count fit on one screen. The last bar is the whole story.</p></div>
        <div class="mapbox"><h4>🗺️ Schematic map — not to scale: the book's 600-year journey</h4><p><b>Central Europe</b> (written, early 1400s) &nbsp;→&nbsp; <b>Prague</b> (Rudolf II's court, c. 1600 — rumoured; Baresch, 1600s) &nbsp;→&nbsp; <b>Rome</b> (Kircher and the Jesuits) &nbsp;→&nbsp; <b>Yale University, USA</b> (1969–today). Six centuries, four cities, zero words read.</p></div>"""
    if a["id"] == "pompeii":
        extra = """<div class="chart"><h4>🗿 The casts, by the numbers (from the article)</h4>
        <div class="bar-row"><span>Bodies found at Pompeii (by 2003)</span><div class="bar"><i style="width:100%"></i></div><b>~1,044</b></div>
        <div class="bar-row"><span>Plaster casts ever made</span><div class="bar"><i style="width:10%"></i></div><b>104</b></div>
        <div class="bar-row"><span>Casts sampled for DNA (2024 study)</span><div class="bar"><i style="width:2%"></i></div><b>14</b></div>
        <div class="bar-row"><span>Full genomes recovered</span><div class="bar"><i style="width:2%"></i></div><b>5</b></div>
        <p class="small">Bars are drawn to scale from the article's figures. Five genomes were enough to overturn a century of family stories — the casts are plaster, not people, and the people inside them were not who we assumed.</p></div>
        <div class="mapbox"><h4>🗺️ Schematic map — not to scale: one volcano, three cities, one witness</h4><p><b>Mount Vesuvius</b> &nbsp;→&nbsp; <b>Pompeii</b> (south-east — buried under 4–6 m of ash and pumice) &nbsp;·&nbsp; <b>Herculaneum</b> (west — buried far deeper, under ~20 m) &nbsp;·&nbsp; <b>Misenum, 29 km across the Bay of Naples</b> (where 17-year-old Pliny watched it all, and his uncle sailed from, to his death at Stabiae).</p></div>"""
    if a["id"] == "earhart":
        extra = """<div class="chart"><h4>✈️ The search, by the numbers (log scale — from the article)</h4>
        <div class="bar-row"><span>Miles: Lae to Howland</span><div class="bar"><i style="width:62%"></i></div><b>2,556</b></div>
        <div class="bar-row"><span>Square miles searched in 1937</span><div class="bar"><i style="width:100%"></i></div><b>~250,000</b></div>
        <div class="bar-row"><span>Feet down: the 2024 sonar 'plane'</span><div class="bar"><i style="width:52%"></i></div><b>~16,000</b></div>
        <div class="bar-row"><span>Pages of records released, 2025</span><div class="bar"><i style="width:42%"></i></div><b>4,624</b></div>
        <div class="bar-row"><span>Pieces of the Electra ever confirmed found</span><div class="bar"><i style="width:2%"></i></div><b>0</b></div>
        <p class="small">Bars are drawn on a log scale so a flight leg and an ocean search fit on one screen. The last bar is the whole mystery: the biggest search in the story found nothing that could be proven to be hers.</p></div>
        <div class="mapbox"><h4>🗺️ Schematic map — not to scale: one flight, two islands, and two clues that dissolved</h4><p><b>Lae, New Guinea</b> (take-off, 2 July 1937) &nbsp;→&nbsp; <b>2,556 miles</b> &nbsp;→&nbsp; <b>Howland Island</b> (the target — a speck under 2 miles long, never reached) &nbsp;·&nbsp; <b>Nikumaroro, ~350 miles south-east</b> (the castaway theory — bones found 1940, lagoon 'plane' turned out to be trees, 2026) &nbsp;·&nbsp; <b>the 2024 sonar 'plane', ~100 miles from Howland</b> (turned out to be rocks).</p></div>"""
    if a["id"] == "sphinx":
        extra = """<div class="chart"><h4>🗓️ How old is it? The four dates in the argument (years ago)</h4>
        <div class="bar-row"><span>Mainstream: Khafre</span><div class="bar"><i style="width:36%"></i></div><b>~4,500 yrs</b></div>
        <div class="bar-row"><span>Reader's middle view</span><div class="bar"><i style="width:40%"></i></div><b>~5,000 yrs</b></div>
        <div class="bar-row"><span>Schoch: core body</span><div class="bar"><i style="width:72%"></i></div><b>7,000–9,000 yrs</b></div>
        <div class="bar-row"><span>West: 10,500 BC</span><div class="bar"><i style="width:100%"></i></div><b>~12,500 yrs</b></div>
        <p class="small">Bars are drawn to scale from the article's figures. The gap between the first bar and the last is the whole argument: nearly 8,000 years, decided by how you read the wear on one wall.</p></div>
        <div class="mapbox"><h4>🗺️ Schematic map — not to scale: the Giza plateau</h4><p><b>River Nile, east</b> &nbsp;→&nbsp; <b>the Sphinx, facing the sunrise</b>, at the foot of <b>Khafre's causeway</b> &nbsp;→&nbsp; uphill, west, to <b>Khafre's pyramid</b> &nbsp;·&nbsp; <b>Khufu's Great Pyramid to the north-east</b> &nbsp;·&nbsp; <b>Menkaure's pyramid to the south-west</b>. The Sphinx's position inside Khafre's complex is the backbone of the mainstream date.</p></div>"""
    if a["id"] == "fieldguide":
        extra = """<div class="chart"><h4>🦴 Who lived when? (approximate ranges from the article)</h4>
        <div class="bar-row"><span>Homo erectus</span><div class="bar"><i style="width:100%"></i></div><b>~1.9M – 110k yrs ago</b></div>
        <div class="bar-row"><span>Homo heidelbergensis</span><div class="bar"><i style="width:55%"></i></div><b>~700k – 200k</b></div>
        <div class="bar-row"><span>Neanderthals</span><div class="bar"><i style="width:45%"></i></div><b>~400k – 40k</b></div>
        <div class="bar-row"><span>Denisovans</span><div class="bar"><i style="width:45%"></i></div><b>~400k – 30k</b></div>
        <div class="bar-row"><span>Homo naledi</span><div class="bar"><i style="width:28%"></i></div><b>~335k – 236k</b></div>
        <div class="bar-row"><span>Homo sapiens</span><div class="bar"><i style="width:32%"></i></div><b>~300k – today</b></div>
        <p class="small">Bars are illustrative, not to exact scale. Ranges are the ones in the article.</p></div>"""
    return ('<div class="visual"><div class="cluebar">'
            '<span>📖 %d story parts</span><span>🕰️ %d moments in time</span><span>🔗 %d sources</span><span>✅ %d proven · ❌ %d not proven</span></div>'
            '<h3>🧭 Follow the timeline</h3><div class="tl-track">%s</div>%s</div>'
            % (len(a["body"]), n_tl, n_src, n_pro, n_not, tl, extra))

# ---------------- LEAD ----------------
add("sulawesi", "The Million-Year Sea Crossing: Seven Stone Tools Rewrite When Humans First Sailed",
 "Seven flakes of stone from a cornfield in Sulawesi say early human relatives crossed deep ocean water more than a million years ago — long before modern humans, and long before anyone was supposed to have a boat.",
 "History", "Nature, August 2025",
 ["A field team led by Indonesian archaeologist Budianto Hakim, working with researchers from Griffith University in Australia, dug seven stone artefacts out of a sandstone outcrop in a modern corn field at Calio, in southern Sulawesi. The artefacts are small, sharp-edged flakes struck from river pebbles — the telltale marks of deliberate tool-making, not rocks broken by nature.",
  "The layers were dated by palaeomagnetic dating of the sandstone itself and by direct dating of a pig fossil found alongside the tools. The result: at least 1.04 million years old, and possibly as old as 1.48 million years. Before this, the oldest evidence on Sulawesi was about 194,000 years old, from Talepu. The new date pushes the island's human story back by roughly 800,000 years.",
  "Sulawesi sits in Wallacea, the island zone east of mainland Southeast Asia, separated from the mainland by deep-water channels that stayed open even when Ice Age sea levels fell. Walking there was never an option. Somebody crossed water to get there — and did it at roughly the same time as, or earlier than, the tool-makers at Wolo Sege on Flores, dated to at least 1.02 million years ago.",
  "No fossils were found at Calio, so the tool-makers' species is unknown. The leading candidate is Homo erectus or a close relative. Whether they built rafts on purpose or drifted on floating vegetation after a storm is also unknown — and that distinction is the whole argument now."],
 "Early human relatives were deliberate seafarers more than a million years ago, building rafts and navigating open water on purpose.",
 "The tools prove a crossing happened. They do not prove intent, navigation, or boat-building. No boats survive from this period anywhere, and an accidental crossing — a group swept out to sea on vegetation, or stranded after a storm — fits the same evidence. Deliberate seafaring is the exciting reading, not the proven one.",
 ["Hominins reached Sulawesi at least 1.04 million years ago.",
  "They crossed deep water that could never be walked, even at low Ice Age sea levels.",
  "They were making stone tools on Sulawesi at about the same time as on Flores."],
 ["That they built boats or navigated deliberately.",
  "Which species made the tools — no fossils were found at Calio.",
  "That this was a planned migration rather than an accident or a one-off stranding."],
 [["1.48–1.04 Ma", "Calio tools made and buried in river sediments, southern Sulawesi."],
  ["1.02 Ma", "Stone tools at Wolo Sege, Flores — the previous Wallacea benchmark."],
  ["~194 ka", "Tools at Talepu, Sulawesi — the old record for the island, now far surpassed."],
  ["Aug 2025", "Hakim and colleagues publish the Calio results in Nature."]],
 [["Hakim et al., 'Hominins on Sulawesi during the Early Pleistocene', Nature (2025)", "https://doi.org/10.1038/s41586-025-09348-6"],
  ["Southern Cross University — the Sulawesi stone tools (The Conversation, republished)", "https://www.scu.edu.au/news/2025/tc-sulawesi-stone-tools/"],
  ["Southern Cross University — oldest human presence on Sulawesi", "https://www.scu.edu.au/news/2025/new-research-dates-oldest-human-presence-on-sulawesi-island/"]],
 [W("The Sulawesi discovery, explained", "Sulawesi stone tools 1 million years Nature"),
  P("Human origins podcasts", "Sulawesi hominin stone tools"),
  ["Griffith University / Southern Cross University releases (see Sources)", "https://www.scu.edu.au/news/2025/new-research-dates-oldest-human-presence-on-sulawesi-island/", "article"]])

# ---------------- ORIGINAL HISTORY ----------------
add("lisbon", "Lisbon, 1755: The Morning Europe's Richest City Vanished",
 "An earthquake, a tsunami, and a fire that burned for days, all before lunch on All Saints' Day — and out of the ashes, the science of seismology.",
 "History", "1 November 1755",
 ["At about 9:40 on the morning of 1 November 1755, with churches packed for All Saints' Day Mass, a massive earthquake struck off the coast of Portugal. Modern estimates put it at magnitude 8.5 to 9.0. Buildings collapsed, candles toppled onto the wreckage, and fires began that would burn for days — Britannica's account says about six days.",
  "Roughly forty minutes later, a tsunami rolled up the Tagus estuary and finished what the shaking started. Waves of about 20 feet hit Lisbon and about 65 feet hit Cádiz. Death tolls are disputed: Britannica gives an estimate of 60,000 killed in Lisbon alone, while other modern summaries give a range of roughly 12,000 to 50,000 overall. The Ledger uses the range and flags the disagreement rather than picking one number.",
  "The rebuild, led by the Marquis of Pombal, gave the world its first earthquake-resistant buildings. Pombal also sent a survey to every parish asking what people felt, where, and when — the first systematic earthquake questionnaire, and the founding move of seismology."],
 "The Lisbon disaster was divine punishment for a sinful city — the reading many preachers and pamphleteers pushed in 1755.",
 "The earthquake had a natural, tectonic cause: faulting of the seafloor along plate boundaries in the Atlantic. The theological reading was a moral argument, not an explanation of the mechanism — and Pombal's survey, not prayer, is what produced the science that now saves lives in quake zones.",
 ["A magnitude ~8.5–9.0 quake, tsunami, and fire destroyed Lisbon on 1 Nov 1755.",
  "Pombal's parish survey founded systematic seismology.",
  "The rebuild pioneered earthquake-resistant construction."],
 ["An exact death toll — estimates range from tens of thousands to 60,000 in Lisbon alone.",
  "That any single moral cause explains a tectonic event."],
 [["9:40 a.m., 1 Nov 1755", "Main shock strikes as churches fill for Mass."],
  ["~40 min later", "Tsunami surges up the Tagus."],
  ["Days after", "Fires burn across the ruins; Pombal begins the rebuild and the parish survey."]],
 [["Encyclopaedia Britannica — Lisbon earthquake of 1755", "https://www.britannica.com/event/Lisbon-earthquake-of-1755"]],
 [W("The Lisbon Tragedy documentary", "Lisbon earthquake 1755 documentary", "https://www.youtube.com/watch?v=kjgOoCvmyOQ"),
  P("Lisbon earthquake podcasts", "Lisbon earthquake 1755"),
  W("Lisbon 1755, explained", "Lisbon earthquake tsunami fire 1755")])

add("houdini", "Houdini, 1926: The Man No Lock Could Hold Ran Out of Escapes",
 "He walked out of handcuffs, straitjackets, and a water torture cell. He could not walk out of a ruptured appendix — and the argument about what killed him has never settled.",
 "History", "31 October 1926",
 ["Harry Houdini, born Erik Weisz in Budapest in 1874, spent his life escaping handcuffs, straitjackets, sealed milk cans, and a water torture cell hung upside down. His later years were spent at war with fraudulent mediums who preyed on grieving families.",
  "On 22 October 1926 in Montreal, after a lecture on exposing fake mediums, McGill student J. Gordon Whitehead asked in Houdini's dressing room whether he could really take any punch to the stomach. Houdini, lying on a couch with a sore ankle, said yes — before he could brace, Whitehead hit him several times in the gut.",
  "Running a 104-degree fever, Houdini still took the stage in Detroit on 24 October, then collapsed. After two surgeries at Grace Hospital for a ruptured appendix, he died of peritonitis on 31 October 1926, aged 52. He had left his wife Bess a secret code — 'Rosabelle, believe' — promising to send it from the other side if he possibly could. She held séances for ten years. The code never came back in a way she accepted."],
 "The punches killed Houdini — the version his doctors and his life insurer accepted at the time, with the insurer paying double on an accidental-death claim.",
 "Modern medical opinion doubts it: he may already have had appendicitis, and the punches may only have masked how serious it was, delaying treatment. No autopsy was ever performed, so the mechanism cannot be proven either way. A third strand — that spiritualists poisoned him — has no supporting evidence and rests on a later biography's speculation.",
 ["Houdini died of peritonitis from a ruptured appendix on 31 Oct 1926.",
  "He was punched in the stomach in Montreal nine days earlier.",
  "No autopsy was performed, so the causal chain is unproven."],
 ["That the punches ruptured his appendix.",
  "That spiritualists poisoned him — no evidence supports this."],
 [["22 Oct 1926", "Punches in the Montreal dressing room."],
  ["24 Oct 1926", "Final performance in Detroit at 104°F; collapse."],
  ["31 Oct 1926", "Death in Detroit, aged 52."],
  ["1936", "Bess ends the séances: 'Ten years is long enough to wait for any man.'"]],
 [["Smithsonian Magazine — Death proves inescapable for even Houdini", "https://www.smithsonianmag.com/smithsonian-institution/october-31-1926-death-proves-inescapable-for-even-houdini-122032841/"],
  ["Smithsonian Institution Archives — Houdini escapes the Smithsonian", "https://siarchives.si.edu/blog/houdini-escapes-smithsonian"]],
 [W("The Suspicious Death of Harry Houdini (100 Years Later)", "Harry Houdini death", "https://www.youtube.com/watch?v=1pRQ4QDy7S0"),
  P("Houdini podcasts", "Harry Houdini death mystery"),
  W("Houdini, the escape artist", "Harry Houdini biography documentary")])

add("antikythera", "The Antikythera Mechanism: A Computer From 150 BC",
 "Pulled from a shipwreck in 1901, a corroded lump of bronze turned out to contain gear wheels of a precision not seen again for a thousand years.",
 "Deep Past", "Recovered 1901; built c. 2nd century BC",
 ["Sponge divers off the Greek island of Antikythera recovered a corroded bronze mass from a Roman-era shipwreck in 1901. It sat in the National Archaeological Museum in Athens for two years before anyone noticed it contained gears.",
  "Radiographic imaging later showed the fragments contained about 30 gear wheels, with dials tracking the Sun and Moon in the zodiac, lunar phases, the 19-year Metonic cycle, and even the timing of the Panhellenic games. Britannica dates its manufacture to around 100 BC, give or take 30 years; other summaries place it in the 2nd century BC. The mechanism is the only known physical survivor of a tradition of mechanical astronomical displays.",
  "The Antikythera Mechanism Research Project's CT work, published in Nature in the 2000s, mapped the gear train and decoded thousands of Greek characters hidden inside the corrosion."],
 "The mechanism is evidence of a lost, advanced civilisation — or even of knowledge that should not have existed in the ancient world.",
 "The mechanism is extraordinary, but it sits inside a documented Greek tradition: Cicero describes similar devices, and the gearing, while sophisticated, is fully mechanical and Greek in design. What is missing is not the technology's origin but its predecessors — no earlier device of this complexity has survived, which is a gap in the record, not proof of a lost civilisation.",
 ["A geared astronomical calculator existed in the Greek world by c. 100 BC.",
  "It tracked Sun, Moon, lunar phases, eclipse cycles, and the games cycle.",
  "Its gearing was unmatched in the surviving record for over a millennium."],
 ["That it came from a lost advanced civilisation — no evidence supports this over the Greek tradition.",
  "Its exact original purpose in full — some functions remain reconstructed, not observed."],
 [["c. 100 BC", "Mechanism built (Britannica's dating, ±30 years)."],
  ["1901", "Recovered from the Antikythera shipwreck."],
  ["1902", "Gear noticed in the Athens museum; first study begins."],
  ["2005–2008", "CT scanning maps the gear train; results published in Nature."]],
 [["Encyclopaedia Britannica — Antikythera mechanism", "https://www.britannica.com/topic/Antikythera-mechanism"],
  ["Wikipedia — Antikythera mechanism (overview and references)", "https://en.wikipedia.org/wiki/Antikythera_mechanism"]],
 [W("Antikythera mechanism, explained", "Antikythera mechanism documentary"),
  P("Ancient technology podcasts", "Antikythera mechanism"),
  W("How the ancient computer works", "Antikythera mechanism gears explained")])

add("wow", "The Wow! Signal: 72 Seconds Nobody Can Explain Away",
 "On 15 August 1977, Ohio State's Big Ear telescope printed out '6EQUJ5'. An astronomer circled it and wrote 'Wow!' It has never repeated.",
 "History", "15 August 1977",
 ["Ohio State University's Big Ear radio telescope, running the world's longest-running SETI program, recorded a strong, narrowband radio signal on 15 August 1977 from the direction of Sagittarius. It lasted the full 72-second window a fixed sky point spent in Big Ear's beam, rose and fell the way a distant, fixed source should, and sat near the 1420 MHz neutral-hydrogen line — the frequency physicists had proposed as a natural 'hello' channel.",
  "Volunteer astronomer Jerry Ehman found it days later while reviewing printouts, circled the intensity sequence '6EQUJ5', and wrote 'Wow!' beside it. The signal appeared in only one of Big Ear's two feed horns, which fits a transient source rather than a steady background object.",
  "Dozens — by some counts hundreds — of follow-up observations have found nothing. Hypotheses have included reflections from space debris, interstellar scintillation, and hydrogen clouds around comets. None has been confirmed. A 2025 reassessment using unpublished archival Ohio SETI observations (the Arecibo Wow! project) refined its frequency to about 1420.726 MHz, but did not solve it."],
 "The Wow! signal was a transmission from an extraterrestrial civilisation.",
 "The signal has the hallmarks researchers would hope for — narrowband, near the hydrogen line, the right rise-and-fall shape — but a single, never-repeated detection cannot confirm an alien origin, and Ehman himself did not think the evidence was strong enough to claim first contact. The honest status, after nearly fifty years, is unexplained: neither proven alien nor proven mundane.",
 ["A strong narrowband signal was recorded on 15 Aug 1977, lasting 72 seconds.",
  "It has never recurred despite many follow-up searches.",
  "No natural or terrestrial explanation has been confirmed."],
 ["That it was definitely an alien transmission.",
  "That it was definitely a comet, a satellite, or interference — none of those explanations has been confirmed either."],
 [["15 Aug 1977", "Big Ear records the signal in Sagittarius."],
  ["Days later", "Ehman circles '6EQUJ5' and writes 'Wow!'"],
  ["1977–present", "Follow-up searches find no repeat."],
  ["2025", "Arecibo Wow! reassessment refines the frequency; the signal stays unexplained."]],
 [["American Astronomical Society — The Mysterious Wow! Signal", "https://aas.org/posts/news/2018/08/month-astronomical-history"],
  ["Wikipedia — Wow! signal (overview and references)", "https://en.wikipedia.org/wiki/Wow!_signal"]],
 [W("The Wow signal, explained", "Wow signal Big Ear 1977 documentary"),
  P("SETI podcasts", "Wow signal SETI"),
  W("Could the Wow signal be aliens?", "Wow signal extraterrestrial debate")])

add("cooper", "D.B. Cooper: The Man Who Fell Out of the Sky and Was Never Found",
 "On 24 November 1971, a calm man in a suit hijacked a Boeing 727, took $200,000, strapped on a parachute, and stepped into a storm over Washington. The FBI closed the active case in 2016 without ever naming him.",
 "History", "24 November 1971",
 ["A man calling himself Dan Cooper bought a one-way ticket on Northwest Orient Flight 305 from Portland to Seattle, then handed a stewardess a note saying he had a bomb. In Seattle he traded the passengers for $200,000 in cash and four parachutes, then ordered the plane back into the air toward Mexico — and somewhere over southwest Washington, in a storm, he jumped from the rear stairs with the money and was never seen again.",
  "The FBI's case, codenamed NORJAK, ran for 45 years. By the five-year anniversary, agents had considered more than 800 suspects and eliminated all but about two dozen. The FBI's own page notes the name 'D.B.' itself appears to be a press myth — the hijacker called himself Dan Cooper, and the FBI questioned a man with the initials D.B. who was not the hijacker.",
  "The only physical trace ever recovered was a bundle of decaying banknotes, matching the ransom serial numbers, found by a boy on a Columbia River beach in 1980. In July 2016 the FBI redirected the resources allocated to the case to other priorities."],
 "D.B. Cooper survived, lived under a new identity, and spent the money — or a named suspect (Richard Floyd McCoy, and others) was Cooper.",
 "Survival is possible but unproven: the jump was into a storm, at night, in a suit, with a parachute that may have been sewn shut (one of the chutes supplied was a training chute). McCoy, a favourite suspect, did commit a similar hijacking months later — but he was eliminated as Cooper on the evidence available, and no suspect has ever been charged. The case is unsolved, not solved by a favourite name.",
 ["A man hijacked Flight 305 on 24 Nov 1971, took $200,000 and four parachutes, and jumped.",
  "The FBI investigated for 45 years and closed the active case in 2016.",
  "Ransom notes were found on a river beach in 1980; nothing else of the money has surfaced."],
 ["That any named suspect was Cooper.",
  "That he survived — or that he died in the jump. Both are possible; neither is proven."],
 [["24 Nov 1971", "Hijacking of Flight 305; the jump over southwest Washington."],
  ["1980", "Decaying ransom banknotes found on the Columbia River."],
  ["Jul 2016", "FBI redirects resources; active investigation ends."]],
 [["FBI — D.B. Cooper Hijacking (official case page)", "https://www.fbi.gov/history/famous-cases/db-cooper-hijacking?redirect_mongo_id=60a591aff26daa001d24c5cf&utm_source=Springbot&utm_medium=Email&utm_campaign=60a591aff26daa001d24c5ce"],
  ["FBI Vault — D.B. Cooper records", "https://vault.fbi.gov/D-B-Cooper"]],
 [W("D.B. Cooper, the unsolved skyjacking", "DB Cooper documentary FBI"),
  P("True crime / unsolved podcasts", "DB Cooper mystery"),
  W("Who was D.B. Cooper?", "DB Cooper suspects explained")])

add("agincourt", "Agincourt, 1415: The Longbow, the Mud, and the Myth",
 "On St Crispin's Day 1415, Henry V's exhausted, outnumbered army beat a much larger French force in three hours. The numbers — and the legend — are still argued over.",
 "History", "25 October 1415",
 ["Henry V had marched his army from Harfleur toward Calais after a costly siege, weakened by dysentery and a march of more than 200 miles. Near the village of Agincourt on 24 October, a large French force under the Constable Charles d'Albret moved to block the road to Calais.",
  "On the morning of 25 October — St Crispin's Day — the English, about 6,000 strong with roughly 5,000 archers, faced a French army Britannica puts at roughly 20,000 to 30,000. The French advanced across a narrow, rain-soaked field between two woods. English longbow stakes stopped the cavalry; arrows, mud, and close fighting did the rest. The battle lasted about three hours. English losses are put at around 400; French losses around 6,000, with the Constable among the dead.",
  "The victory made possible England's conquest of Normandy and the Treaty of Troyes (1420), which named Henry heir to the French crown."],
 "Agincourt was a triumph of English longbow superiority — a clean technological victory of bow over knight.",
 "The longbow mattered, but so did the ground, the weather, and French mistakes: a constricted field, heavy rain, and a crowded, disorganised advance that turned the French army's size against itself. Exact army sizes are disputed — older accounts gave the French 50,000 to 150,000, figures modern historians treat as gross exaggerations — so any version that leans on a single ratio should be read with care.",
 ["On 25 Oct 1415, Henry V's army defeated a larger French army at Agincourt.",
  "Longbowmen, stakes, mud, and a narrow field shaped the outcome.",
  "The victory led to the conquest of Normandy and the Treaty of Troyes."],
 ["Exact army sizes — estimates for the French range widely.",
  "That the longbow alone won the battle."],
 [["1415", "Siege of Harfleur; march toward Calais."],
  ["24 Oct 1415", "French force blocks the road near Agincourt."],
  ["25 Oct 1415", "Battle: about three hours; English victory."],
  ["1420", "Treaty of Troyes names Henry heir to the French crown."]],
 [["Encyclopaedia Britannica — Battle of Agincourt", "https://www.britannica.com/event/Battle-of-Agincourt"]],
 [W("Agincourt, the battle explained", "Battle of Agincourt documentary"),
  P("Medieval history podcasts", "Battle of Agincourt 1415"),
  W("Was Agincourt really a longbow victory?", "Agincourt longbow myth debate")])

# ---------------- ANCIENT WORLD ----------------
add("hancock", "The Lost Civilisation Claim: Hancock, Carlson, and the Younger Dryas",
 "Graham Hancock and Randall Carlson argue an advanced civilisation was wiped out about 12,800 years ago — and that its survivors seeded the world's oldest monuments. Mainstream archaeology disagrees. Here is the argument, split into what is proven, what is argued, and what is a leap.",
 "Deep Past", "The Younger Dryas, c. 12,800 years ago",
 ["The claim, at its strongest, runs like this: about 12,800 years ago, at the start of the Younger Dryas cold period, a comet or asteroid impact (or airburst) triggered continent-scale fires, megafauna extinctions, and a sudden return to Ice Age cold. An advanced, seafaring civilisation that existed before the impact was destroyed; its survivors, the story goes, passed knowledge to the hunter-gatherers who later built Göbekli Tepe in Turkey and other early monuments.",
  "Hancock presents the case in books including Magicians of the Gods and in the Netflix series Ancient Apocalypse; Carlson, a geologist, argues the geological side — scablands, flood features, and impact markers. Their sites and talks are the primary sources for the claim itself, and this article reports their argument in their terms before testing it.",
  "The mainstream position accepts parts of the background and rejects the conclusion: the Younger Dryas cold snap is real, Göbekli Tepe is real and older than farming, and megafauna did die out around this time. What is not accepted is the impact as a proven cause, or any advanced pre-Ice Age civilisation, because the physical evidence for both is disputed and, for the civilisation, absent."],
 "A lost, advanced civilisation existed before the Younger Dryas and was destroyed by a cosmic impact; its survivors taught the builders of Göbekli Tepe.",
 "The impact hypothesis (the Younger Dryas Impact Hypothesis) is a real, published scientific proposal — but it remains contested: claimed impact markers such as nanodiamonds and platinum spikes have been challenged, with other teams failing to reproduce them or offering terrestrial explanations. And no site, artefact, or text of an advanced pre-Younger Dryas civilisation has been found. Göbekli Tepe, dated to about 11,600 years ago, post-dates the proposed impact and was built by hunter-gatherers — remarkable, but not evidence of a lost high civilisation.",
 ["The Younger Dryas cold period began about 12,800 years ago.",
  "Göbekli Tepe was built by hunter-gatherers about 11,600 years ago — before farming.",
  "Megafauna extinctions cluster around the end of the Ice Age."],
 ["That a cosmic impact caused the Younger Dryas — contested, not settled.",
  "That an advanced civilisation existed before it — no direct evidence has been found."],
 [["c. 12,800 years ago", "Younger Dryas cold period begins."],
  ["c. 11,600 years ago", "Göbekli Tepe in use — hunter-gatherer builders."],
  ["2007", "Younger Dryas Impact Hypothesis published."],
  ["2020s", "Impact markers debated; no consensus reached."]],
 [["Graham Hancock — official site", "https://grahamhancock.com/"],
  ["Randall Carlson — official site", "https://randallcarlson.com/"]],
 [W("Ancient Apocalypse and the lost civilisation debate", "Graham Hancock Randall Carlson Younger Dryas"),
  P("Ancient history podcasts", "Younger Dryas impact hypothesis debate"),
  W("Göbekli Tepe, explained", "Gobekli Tepe hunter gatherers documentary")])

add("fieldguide", "Field Guide to the Other Humans: Who They Were, Where They Lived, What They Were Doing",
 "For most of human history, we were not alone. At least seven other kinds of humans shared the planet with us or came just before us. This is the roll call.",
 "Deep Past", "From ~1.9 million years ago to ~40,000 years ago",
 ["HOMO ERECTUS — Asia and Africa, about 1.9 million to 110,000 years ago. Long-legged, wide-ranging, the first hominin to leave Africa in a big way and the leading candidate for the Sulawesi tool-makers. Made handaxes and flakes, controlled fire, hunted large animals, and crossed water to reach Flores and Sulawesi.",
  "HOMO HEIDELBERGENSIS — Africa and Europe, about 700,000 to 200,000 years ago. Big-game hunters who took rhinos and hippos with wooden spears, built shelters, and are the likely ancestors of both Neanderthals and us.",
  "NEANDERTHALS — Europe and western Asia, about 400,000 to 40,000 years ago. Stocky, cold-adapted, buried their dead, painted cave walls, made glue, tools, and jewellery — and interbred with modern humans leaving DNA in people alive today.",
  "DENISOVANS — Asia, about 400,000 to 30,000 years ago. Known first from DNA in a Siberian cave finger bone, later from fossils including a skull in China identified as Denisovan in 2025. Interbred with modern humans; their DNA is strongest in some Pacific and Southeast Asian populations today.",
  "HOMO FLORESIENSIS, the 'hobbits' — Flores, Indonesia, until roughly 50,000 years ago. About a metre tall, small-brained, making stone tools and hunting dwarf elephants. Their small size is usually read as island dwarfing from an erectus-like ancestor.",
  "HOMO LUZONENSIS — Luzon, Philippines, about 709,000 years ago for the tool and butchery evidence, with the species itself dated to roughly 50,000–67,000 years ago from cave fossils. Small-bodied, with a mix of ancient and modern traits; the butchered rhino at Kalinga shows hominins on Luzon hundreds of thousands of years before the fossils.",
  "HOMO NALEDI — South Africa, about 335,000 to 236,000 years ago. Small-brained with human-like hands and feet, found deep in the Rising Star cave system. Whether they deliberately buried their dead there is claimed by the discovery team and disputed by other researchers — one of the liveliest arguments in the field."],
 "These other humans were primitive brutes — or, in the opposite direction, that they were fully modern in mind and only lacked our technology.",
 "The record resists both simplifications. Neanderthals buried, painted, and made complex tools; naledi's burial claim is genuinely disputed, not settled; and small brains did not stop floresiensis or naledi from doing sophisticated things. 'Primitive' is a poor word for animals that survived hundreds of thousands of years in hard places.",
 ["At least seven other hominin kinds are documented in the fossil and DNA record.",
  "Neanderthals and Denisovans interbred with modern humans.",
  "Several kinds overlapped in time with Homo sapiens."],
 ["That every behaviour claimed for them is settled — naledi burials, for example, are disputed.",
  "The exact species of the Sulawesi and Luzon tool-makers — no fossils yet."],
 [["~1.9 Ma", "Homo erectus appears; spreads out of Africa."],
  ["~709 ka", "Tool-making and rhino butchery on Luzon."],
  ["~400–40 ka", "Neanderthals in Europe and western Asia."],
  ["~335–236 ka", "Homo naledi in South Africa."],
  ["~300 ka", "Homo sapiens appears in Africa."],
  ["~50 ka", "Floresiensis and the last Neanderthals fade from the record."]],
 [["HISTORY — 6 Ancient Human Species That Once Shared Our World", "https://www.history.com/articles/ancient-human-species"],
  ["Smithsonian Human Origins Program (via Associated Press summary)", "https://portside.org/node/32366/printable/print"]],
 [W("The other humans, explained", "Neanderthal Denisovan Homo naledi documentary"),
  P("Human evolution podcasts", "other human species Neanderthal Denisovan"),
  W("Homo naledi and the burial debate", "Homo naledi Rising Star cave burial")])

add("lazar", "CONTESTED — Bob Lazar and Area 51: The Claim That Never Quite Dies",
 "In 1989, a man calling himself a physicist said he had reverse-engineered alien craft at a site near Area 51. The story made him famous, made a documentary, and has never been corroborated. This article sits in the contested corner on purpose: it is not presented as institutional science.",
 "Contested", "Claims from 1989; JRE #2479, 3 April 2026",
 ["Bob Lazar says that in late 1988 and 1989 he worked at a site he calls S-4, near Area 51 in Nevada, where he helped reverse-engineer disc-shaped craft powered by an element he called 115. He says the craft were of non-human origin. His story first broke in a 1989 television interview, and he returned to it in the 2026 documentary S-4: The Bob Lazar Story, released around his April 2026 Rogan appearance with filmmaker Luigi Vendittelli.",
  "Lazar runs United Nuclear, a scientific-supply business, and that site is the closest thing to an official web presence for him. No personal research site was verified for this article.",
  "The pushback is substantial and specific: Lazar's claimed education (MIT and Caltech) has not been corroborated by those institutions' records as reported by investigators; his claimed employment at Los Alamos appears in a phone directory but not in personnel records; and no physical evidence, document, or corroborating witness has established the S-4 craft. Believers point to his early, accurate description of element 115's properties before it was synthesised — sceptics reply that the properties he described were generic predictions, not a unique fingerprint."],
 "Lazar reverse-engineered alien craft at S-4, and the government has hidden the evidence ever since.",
 "No element of the S-4 story — the craft, the element-115 reactor, the employment — has been corroborated by documents, institutions, or physical evidence, and key biographical claims have not checked out. The story is best understood as an unproven claim with a large cultural footprint, not as a scientific finding.",
 ["Lazar made the S-4 claims publicly from 1989 onward.",
  "He appeared on Rogan in April 2026 with a new documentary.",
  "His education and employment claims have not been corroborated by the institutions named."],
 ["That alien craft were at S-4, or that Lazar worked on them.",
  "That element 115 powered them — element 115 (moscovium) as synthesised is highly unstable and nothing like a fuel."],
 [["1989", "Lazar's S-4 claims first air on television."],
  ["3 Apr 2026", "Rogan episode #2479 with Lazar and Vendittelli; S-4 documentary released."]],
 [["United Nuclear (Lazar's business)", "https://www.unitednuclear.com"],
  ["S4 movie site", "https://S4movie.com"]],
 [W("Bob Lazar, Area 51, the full story", "Bob Lazar Area 51 documentary"),
  P("UFO podcasts", "Bob Lazar S4 Area 51"),
  W("Fact-checking Bob Lazar", "Bob Lazar claims debunked")])

# ---------------- ROGAN SCIENCE (part 1) ----------------
def rogan(id, name, field, ep, site_label, site_url, body, claim, pushback, proves, notproves, timeline, watch_extra):
    sources = [[site_label, site_url]] if site_url else []
    watch = [W("Their Joe Rogan episode (YouTube search)", "Joe Rogan " + name)] + watch_extra
    add(id, name + " — " + field, "", "Rogan Science", ep, body, claim, pushback, proves, notproves, timeline, sources, watch)

rogan("huberman", "Andrew Huberman", "Neuroscience and human performance", "JRE #2553, 14 Sep 2026",
 "Huberman Lab — official site", "https://hubermanlab.com",
 ["Andrew Huberman is a Stanford neuroscientist and host of the Huberman Lab podcast, one of the most-listened-to science shows in the world. On Rogan in September 2026 he was promoting his book Protocols: An Operating Manual for the Human Body, which his site listed as a #1 New York Times bestseller.",
  "What he posts about, week after week, is protocols: sleep, light exposure, exercise, focus, stress, and supplements, each tied to a named mechanism — dopamine, cortisol, adenosine, circadian clocks — and each given as a concrete routine. The appeal is the format: a lab result, translated into something a listener can do at 6 a.m.",
  "The criticism, from other neuroscientists and physicians, is about the gap between mechanism and proof: a protocol can be biologically plausible and still unproven in humans at the dose and duration recommended, and supplement advice in particular is often ahead of the clinical evidence."],
 "Following a neuroscience protocol — light, sleep, cold, supplements — can measurably improve focus, health, and performance.",
 "Many individual protocols rest on real mechanisms but thin human trials; the strongest evidence in this space is for the boring basics (sleep, exercise, light timing), and supplement claims should be read as hypotheses with a product attached, not as prescriptions.",
 ["Huberman is a Stanford neuroscientist and a leading science communicator.",
  "Sleep, exercise, and light timing have strong evidence behind them."],
 ["That every protocol he recommends is proven in humans at the stated dose.",
  "That a podcast protocol replaces medical advice."],
 [["14 Sep 2026", "Rogan episode #2553."],
  ["Sep 2026", "Protocols published."]],
 [P("Huberman Lab podcast", "Huberman Lab"),
  W("Huberman on protocols", "Andrew Huberman protocols explained")])

rogan("rovelli", "Carlo Rovelli", "Theoretical physics — loop quantum gravity", "JRE #2554, 15 Sep 2026",
 "Rovelli — academic homepage, Aix-Marseille University", "https://www.cpt.univ-mrs.fr/~rovelli/",
 ["Carlo Rovelli is a theoretical physicist at Aix-Marseille University and one of the founders of loop quantum gravity — the attempt to describe gravity not as a smooth force but as a network of discrete, quantum loops of space itself.",
  "His wider argument, developed in books including Seven Brief Lessons on Physics, The Order of Time, and On the Equality of All Things (September 2026), is relational: time is not a river flowing past us but an effect of how things change relative to each other, and reality is a web of relations rather than a stage with objects on it.",
  "Loop quantum gravity is a live research programme, not a confirmed theory. Its main rival, string theory, makes different bets about the deep structure of reality, and neither has yet produced a testable prediction that would settle the argument. Rovelli's popular writing is widely praised; his physics remains, by his own account, unfinished."],
 "Space and time are not fundamental — they emerge from quantum relations, and time itself is an illusion of perspective.",
 "Relational quantum mechanics and loop quantum gravity are serious, published research programmes, but they are not established fact. The 'time does not exist' slogan is a popularisation of a technical claim about how time appears in the equations, and rival programmes disagree about what, if anything, replaces it.",
 ["Rovelli is a leading loop-quantum-gravity theorist.",
  "His books popularise real, published physics."],
 ["That loop quantum gravity is proven, or that time 'does not exist' in any everyday sense."],
 [["15 Sep 2026", "Rogan episode #2554."],
  ["Sep 2026", "On the Equality of All Things published."]],
 [P("Physics podcasts", "Carlo Rovelli loop quantum gravity"),
  W("Rovelli on time", "Carlo Rovelli order of time explained")])

rogan("sinclair", "David Sinclair", "Genetics and the biology of ageing", "JRE, 7 Aug 2026 — ⚠ FINANCIAL STAKE",
 "David Sinclair — official site", "https://davidasinclair.com",
 ["David Sinclair is a professor of genetics at Harvard Medical School and author of Lifespan, the book that made 'ageing is a disease we can treat' a mainstream idea. His core claim is the Information Theory of Ageing: ageing is driven less by accumulated damage than by the loss of epigenetic information — the instructions that tell a cell which genes to read — and that information can, in principle, be restored.",
  "On Rogan on 7 August 2026 he announced the launch of Lifespan Group LLC and Lifespan.com, built around ER-100, Life Biosciences' partial epigenetic reprogramming therapy, whose investigational new drug application was reported as FDA-cleared in January 2026. The therapy aims to reprogram aged cells toward a younger state without fully resetting them into stem cells.",
  "Flag, stated plainly: Sinclair holds a scientific and financial stake in Life Biosciences. That does not make the science wrong — partial reprogramming has produced striking results in mice — but it does mean his promotion of a company product should be read with the stake in mind, and that human evidence for ER-100 is at an early stage."],
 "Ageing can be reversed by restoring lost epigenetic information, and partial reprogramming is the path to doing it in humans.",
 "Partial reprogramming works in mice and is a genuine research frontier. In humans it is unproven, and the distance between a mouse result and a safe human therapy is where most such programmes fail. Sinclair's dual role as researcher and company stakeholder is a reason to demand independent data, not a reason to dismiss the field.",
 ["Sinclair is a Harvard genetics professor and author of Lifespan.",
  "Partial epigenetic reprogramming has strong mouse results.",
  "He announced Lifespan.com on Rogan in August 2026."],
 ["That ER-100 reverses ageing in humans.",
  "That ageing is 'solved' — it is not."],
 [["7 Aug 2026", "Rogan appearance; Lifespan.com announced."],
  ["Jan 2026", "ER-100 IND reported FDA-cleared."]],
 [P("Longevity podcasts", "David Sinclair lifespan ageing"),
  W("Sinclair on epigenetic reprogramming", "David Sinclair epigenetic reprogramming explained")])

rogan("diamond", "Jared Diamond", "Geography, history, and human societies", "JRE #2549, 3 Sep 2026",
 "Jared Diamond — official site", "https://www.jareddiamond.org",
 ["Jared Diamond is the Pulitzer-winning author of Guns, Germs, and Steel and Collapse, and the most famous living exponent of the argument that geography, not innate superiority, explains why some societies conquered and others were conquered.",
  "His thesis, in one line: societies that happened to sit on the right continent, with the right crops, animals, and east-west axis for spreading them, got a head start in food production — and food surpluses paid for soldiers, bureaucracies, and guns. At his Rogan appearance in September 2026, his latest book was Profits, Prophets, Coaches, and Kings, turning the same lens on when individual leaders actually matter against the tide of geography.",
  "The criticism, long-standing among historians, is that the geography thesis underplays contingency, culture, and human agency — the very things his new book tries to bring back into the frame."],
 "Geography and environment, more than culture or individual genius, explain the broad shape of human history.",
 "The geography argument is powerful for the big patterns and weaker for the particulars: it explains why Eurasia had advantages, but not why two neighbours with the same geography diverged, or why a single leader sometimes changed everything. Diamond's own latest work is, in part, an answer to that criticism.",
 ["Diamond won the Pulitzer for Guns, Germs, and Steel.",
  "Geography shaped which societies developed food surpluses first."],
 ["That geography determines everything — Diamond himself argues it does not."],
 [["3 Sep 2026", "Rogan episode #2549."],
  ["1997", "Guns, Germs, and Steel published."],
  ["2005", "Collapse published."]],
 [P("History podcasts", "Jared Diamond Guns Germs Steel"),
  W("Diamond on geography and societies", "Jared Diamond geography history explained")])

rogan("mcclellan", "Dan McClellan", "Biblical scholarship and the fight against Bible misinformation", "JRE #2562, 7 Oct 2026",
 "Dan McClellan — official site", "https://www.maklelan.org",
 ["Dan McClellan is a biblical scholar specialising in Second Temple Judaism, early Israelite religion, and the cognitive science of religion. He is best known online for short, blunt videos correcting viral claims about the Bible — what the text actually says in Hebrew and Greek, what scholars actually think, and where a popular claim quietly invents its evidence.",
  "His book The Bible Says So (April 2025) and his podcast Data Over Dogma (co-hosted) make the same case in longer form: the Bible is a collection of ancient texts, written by many people over centuries, and reading it honestly means reading it in its historical context — not as a single, flat rulebook.",
  "His critics come from two directions: conservative readers who see his corrections as attacks on faith, and other scholars who dispute individual readings. McClellan's own position is that scholarship and faith are different questions, and that bad history should be corrected whether or not it is convenient."],
 "Most viral claims about what 'the Bible says' are wrong, and the text, read in context, is stranger and more interesting than the slogans.",
 "McClellan's corrections rest on mainstream textual scholarship, which is itself a field of argued readings — Hebrew and Greek are ambiguous in places, and scholars disagree. His debunks are strongest where a claim has no textual basis at all, and weakest where the text itself is genuinely contested.",
 ["McClellan is a published biblical scholar; The Bible Says So appeared in April 2025.",
  "He appeared on Rogan on 7 Oct 2026 (#2562)."],
 ["That scholarship settles every disputed passage — it does not."],
 [["Apr 2025", "The Bible Says So published."],
  ["7 Oct 2026", "Rogan episode #2562."]],
 [P("Data Over Dogma podcast", "Dan McClellan Data Over Dogma"),
  W("McClellan on the Bible", "Dan McClellan Bible scholarship explained")])

rogan("everett", "Daniel Everett", "Linguistics — how language began", "JRE, 27 Aug 2026",
 "Daniel Everett — official site", "https://daneverettbooks.com",
 ["Daniel Everett spent years living with the Pirahã people of the Amazon, and came away with a claim that shook linguistics: the Pirahã language, he argued, has no recursion — no sentences nested inside sentences — and no words for numbers or colours in the way other languages have them. If true, that challenged the then-dominant idea that recursion is a universal, hard-wired feature of human language.",
  "His books Don't Sleep, There Are Snakes and How Language Began argue the wider case: language did not arrive as a sudden genetic mutation, but grew gradually out of gesture, culture, and social life — humanity's greatest invention, built slowly, not switched on.",
  "The Pirahã claims remain fiercely disputed. Other linguists argue Everett misanalysed the language, that recursion is present in forms he missed, and that a single small language cannot overturn a universal claim. Everett replies that his critics have mostly not done the fieldwork. The field has not settled it."],
 "Language evolved gradually from culture and gesture, and the Pirahã show that even recursion is not universal.",
 "Everett's fieldwork is real and his challenge mattered, but the Pirahã analysis is contested by linguists who read the same data differently, and the gradual-evolution account competes with nativist accounts that still command wide support. Treat this as a live scientific argument, not a verdict.",
 ["Everett did extended fieldwork with the Pirahã and wrote two major books on language origins.",
  "He appeared on Rogan on 27 Aug 2026."],
 ["That Pirahã lacks recursion — disputed.",
  "That language origins are settled — they are not."],
 [["27 Aug 2026", "Rogan appearance."],
  ["2008", "Don't Sleep, There Are Snakes published."],
  ["2017", "How Language Began published."]],
 [P("Linguistics podcasts", "Daniel Everett Piraha language"),
  W("Everett on language origins", "Daniel Everett how language began")])

rogan("hawass", "Zahi Hawass", "Egyptology — who really built the pyramids", "JRE #2321, 14 May 2025 — earlier than the Nov 2025–Oct 2026 window, included here by request",
 "Zahi Hawass — official site", "https://hawasszahi.com",
 ["Zahi Hawass is Egypt's most famous archaeologist: former Minister of Antiquities, excavator at Giza, and the public face of mainstream Egyptology for three decades. His Rogan appearance (episode #2321, May 2025) is included here even though it falls just before the November 2025–October 2026 window, because Hawass is the central mainstream voice in the pyramid debate this site covers.",
  "His position, stated on his site and in his books, is the mainstream one: the pyramids were built by Egyptians, in the Old Kingdom, by a large, organised workforce of skilled labourers and seasonal workers — not by slaves in the Hollywood sense, and not by a lost civilisation. The evidence he cites includes workers' tombs at Giza, papyri such as the Diary of Merer recording limestone transport, and the quarry and ramp archaeology.",
  "Hawass is also a polarising gatekeeper figure: critics accuse him of controlling access to Egyptian sites and of dismissing alternative theories without engaging them. His supporters reply that the alternative theories he dismisses — lost civilisations, alien builders — have no evidence to engage with."],
 "The pyramids were built by Egyptians, by an organised Egyptian workforce, in the Old Kingdom — no lost civilisation required.",
 "The Egyptian-builder case is supported by tombs, papyri, quarries, and tool marks — the strongest evidence in the debate. What it does not fully settle, in the eyes of critics, is every engineering detail: how exactly the largest blocks were lifted remains reconstructed, not observed, which is the gap alternative theories exploit.",
 ["Hawass is a former Egyptian Minister of Antiquities and a leading Giza excavator.",
  "Workers' tombs and the Merer papyrus support an Egyptian workforce."],
 ["That every engineering step is known — some remain reconstructed."],
 [["14 May 2025", "Rogan episode #2321."],
  ["c. 2560 BC", "Great Pyramid of Khufu built (conventional dating)."]],
 [P("Egyptology podcasts", "Zahi Hawass pyramids"),
  W("Hawass on who built the pyramids", "Zahi Hawass pyramids built Egyptians")])

rogan("masters", "Michael P. Masters", "Biological anthropology — the 'extratempestrial' hypothesis", "JRE #2428, 18 Dec 2025 — ⚠ CONTESTED",
 "Michael P. Masters — official site (Identified Flying Objects)", "https://idflyobj.com",
 ["Michael P. Masters is a professor of biological anthropology at Montana Technological University who studies hominin anatomy and the evolution of the human skull. His public work takes that expertise somewhere unusual: he argues that the beings described in UFO encounters could be us — humans from the far future, evolved into the big-headed, small-bodied form reported by witnesses, travelling back in time.",
  "The argument, laid out in Identified Flying Objects (2019), The Extratempestrial Model (2022), and Revelation: The Future Human Past (2023), runs: human evolution trends toward larger brains, smaller jaws, and upright, gracile bodies; witnesses consistently describe beings that look like that trend continued; and time travel, while unproven, is not ruled out by physics in the way faster-than-light travel is.",
  "Flag: the 2019 book was self-published through Masters' own imprint with informal review by three colleagues, not formal academic peer review. And the hypothesis, while internally consistent, is not testable in its current form — it explains the witness reports by positing future humans, but offers no prediction that would distinguish it from the simpler explanation that the reports are misperceptions, hoaxes, or classified aircraft."],
 "UFO beings are evolved future humans visiting their own past.",
 "The anatomical trend Masters cites is real, and the hypothesis is more disciplined than most UFO theories. But it is not a scientific finding: it cannot be falsified with current evidence, it was not peer-reviewed in its original form, and the witness reports it explains are themselves unreliable data. Read it as a thought experiment, not a result.",
 ["Masters is a professor of biological anthropology.",
  "Human evolution has trended toward larger brains and smaller jaws."],
 ["That UFO beings are future humans — untestable on current evidence."],
 [["18 Dec 2025", "Rogan episode #2428."],
  ["2019", "Identified Flying Objects published (self-published)."],
  ["2022", "The Extratempestrial Model published."]],
 [P("UFO / anthropology podcasts", "Michael Masters extratempestrial"),
  W("Masters on future humans and UFOs", "Michael Masters extratempestrial hypothesis")])

rogan("biondi", "Filippo Biondi", "Satellite radar and the pyramids beneath the pyramids", "JRE #2443, 23 Jan 2026 — ⚠ CONTESTED",
 "Filippo Biondi — HarmonicSAR", "https://www.harmonicsar.com",
 ["Filippo Biondi is a telecommunications and signal-processing engineer whose team uses synthetic-aperture radar (SAR) and Doppler tomography to look inside structures from orbit. In March 2025 his team claimed something extraordinary: vast structures — shafts, chambers, and a spiral — beneath the Khafre pyramid at Giza, detected by analysing satellite radar data.",
  "The claim exploded online, was amplified by Rogan in January 2026, and was immediately challenged. Egyptologists and radar specialists pointed out that SAR, at the wavelengths used, cannot resolve structures hundreds of metres underground with the precision claimed, and that the 'structures' were more plausibly artefacts of the processing method.",
  "Flag, stated carefully: the team's earlier 2022 paper using the same method on the Great Pyramid was reported in August 2026 as retracted; that retraction report was itself search-reported and has not been independently confirmed for this article. The Khafre claim itself has not been peer-reviewed. This article therefore treats the claim as contested and unproven, not as a discovery."],
 "Satellite radar has revealed a vast hidden complex beneath the Khafre pyramid.",
 "The method cannot plausibly deliver the resolution claimed at that depth, the result has not passed peer review, and independent experts have not reproduced it. Until a peer-reviewed paper and an independent replication exist, this is a claim about a radar analysis, not a discovery about a pyramid.",
 ["Biondi's team made the Khafre claim in March 2025 and discussed it on Rogan in January 2026.",
  "SAR is a real remote-sensing method."],
 ["That structures exist beneath Khafre as described.",
  "That the earlier paper's retraction is confirmed — that report is itself unverified here."],
 [["Mar 2025", "Khafre claim announced."],
  ["23 Jan 2026", "Rogan episode #2443."],
  ["Aug 2026", "Earlier method paper reported as retracted (report unconfirmed)."]],
 [P("Pyramid podcasts", "Filippo Biondi Khafre pyramid radar"),
  W("Biondi on the Khafre radar claim", "Filippo Biondi Giza radar", "https://www.youtube.com/watch?v=isby5iL5i1s")])

rogan("vankerkwyk", "Ben van Kerkwyk", "Independent researcher — ancient engineering", "JRE #2417, 25 Nov 2025 — INDEPENDENT RESEARCHER",
 "UnchartedX — official site", "https://www.unchartedx.com",
 ["Ben van Kerkwyk runs UnchartedX, a video-essay and research project on ancient sites, megalithic engineering, and what he calls the mysteries of the past. His work focuses on precision: the machining marks on Egyptian granite, the tolerances of stone boxes in the Serapeum, the engineering questions mainstream tours tend to skip.",
  "His argument is narrower than Hancock's and, for that reason, harder to dismiss out of hand: whatever built these objects had tools and methods we have not fully reconstructed, and archaeology has sometimes settled for 'ramps and copper chisels' where the stonework suggests something more capable.",
  "Flag: van Kerkwyk is an independent researcher, not an institutional scientist, and his work is not peer-reviewed. Mainstream archaeologists reply that the precision he highlights is achievable with known ancient methods — abrasives, pounding, and time — and that 'we don't fully know how' is not evidence of lost technology."],
 "Some ancient stonework shows a precision that known ancient methods cannot explain.",
 "The precision is real and worth explaining. The inference — that it requires lost technology — does not follow: experimental archaeology has reproduced comparable precision with stone, sand, and abrasive methods, and no workshop, tool, or text of a lost technology has been found.",
 ["Van Kerkwyk documents real machining marks and tolerances on ancient stone.",
  "He appeared on Rogan on 25 Nov 2025."],
 ["That the precision requires lost technology."],
 [["25 Nov 2025", "Rogan episode #2417."]],
 [P("Ancient engineering podcasts", "UnchartedX Ben van Kerkwyk"),
  W("Van Kerkwyk on ancient precision", "UnchartedX ancient engineering")])

rogan("tommywood", "Tommy Wood", "Neuroscience — dementia prevention and the stimulated brain", "JRE #2450, 6 Feb 2026",
 "Dr Tommy Wood — official site", "https://www.drtommywood.com",
 ["Tommy Wood is a physician-neuroscientist whose work sits at the intersection of brain health, traumatic brain injury, and elite-athlete performance. His framework, set out in The Stimulated Mind (March 2026) and on his site, is stimulus, supply, and support: the brain needs the right amount of stimulation (not too little, not too much), a supply of nutrients and oxygen, and support from sleep, exercise, and social life.",
  "On dementia, his message is prevention over cure: most dementia risk is shaped decades before symptoms, by vascular health, hearing, sleep, exercise, and cognitive engagement — levers that are individually modest and collectively large.",
  "The pushback is the usual one for prevention science: the individual levers have good observational evidence but few long randomised trials proving that a combined protocol prevents dementia, and 'brain stimulation' products and programmes routinely overclaim on the back of real but modest findings."],
 "Dementia risk can be substantially reduced by managing stimulation, supply, and support decades before symptoms.",
 "The risk factors Wood names are well supported observationally; a proven, packaged prevention protocol is not. His framework is a sensible synthesis of the evidence, not a prescription with trial proof behind every element.",
 ["Wood is a physician-neuroscientist; The Stimulated Mind appeared in March 2026.",
  "Vascular health, sleep, exercise, and hearing are established dementia risk factors."],
 ["That any single programme is proven to prevent dementia."],
 [["6 Feb 2026", "Rogan episode #2450."],
  ["Mar 2026", "The Stimulated Mind published."]],
 [P("Brain health podcasts", "Tommy Wood dementia prevention"),
  W("Wood on dementia prevention", "Tommy Wood stimulated mind brain")])

# ---------------- ROGAN SCIENCE (part 2) ----------------
rogan("masterjohn", "Chris Masterjohn", "Nutritional science — mitochondria", "JRE #2420, 29 Nov 2025",
 "Chris Masterjohn, PhD — official site", "https://www.chrismasterjohn-phd.com",
 ["Chris Masterjohn is a nutritional scientist whose work centres on mitochondria — the energy factories of the cell — and on what happens when they run short of the nutrients they need. His Substack posts in 2026, including 'The Five Mitochondrial Strategies' (October 2026), lay out his framework: nutrient deficiency, energy budget, exercise, and timing with nature.",
  "He also hosts the Mastering Nutrition podcast and founded Mitome, a reader-funded project. Disclosure note, stated plainly: his work is reader-funded, which keeps it independent of supplement companies but also means it is not institutional research — it is one scientist's synthesis, published directly to readers.",
  "The mainstream view agrees mitochondria matter enormously for ageing and metabolic disease, and disagrees mainly about how far the current evidence goes: mitochondrial nutrient strategies are plausible and partly supported, but they are not a proven programme for reversing ageing in healthy people."],
 "Fixing mitochondrial nutrient shortfalls and energy budgets can restore cellular energy and slow ageing.",
 "Mitochondrial health is central to ageing and metabolism, and Masterjohn's synthesis is careful. But nutrient strategies in healthy people lack the long randomised trials that would turn a plausible framework into a proven intervention — read it as an informed hypothesis, not a prescription.",
 ["Masterjohn is a PhD nutritional scientist; his Substack framework is public and dated.",
  "Mitochondrial dysfunction is well established in ageing research."],
 ["That his strategies are proven to reverse ageing in humans."],
 [["29 Nov 2025", "Rogan episode #2420."],
  ["3 Oct 2026", "'The Five Mitochondrial Strategies' published on Substack."]],
 [P("Mastering Nutrition podcast", "Chris Masterjohn mitochondria"),
  W("Masterjohn on mitochondria", "Chris Masterjohn mitochondrial health")])

rogan("kokotajlo", "Daniel Kokotajlo", "AI researcher and forecaster — AI 2027", "JRE #2551, 9 Sep 2026 — SCENARIO, NOT A PREDICTION",
 "AI Futures Project — official site", "https://ai-futures.org",
 ["Daniel Kokotajlo is a former OpenAI governance researcher and executive director of the AI Futures Project. In April 2025 he and co-authors published AI 2027, a detailed scenario forecast: AI systems progress rapidly to superintelligence, and the story branches into a 'race' ending and a 'slowdown' ending, with timelines, capabilities, and political consequences spelled out month by month.",
  "The project updated its timelines through 2025 and 2026, including revised medians in August 2026, and Kokotajlo discussed the forecast on Rogan in September 2026. The site ai-2027.com carries the full scenario.",
  "Flag, in the author's own terms and the Ledger's: this is a scenario, not a prediction. Kokotajlo's team presents it as one plausible path used to think through policy choices, not as a forecast with a probability attached to a date. Critics in AI research argue the timeline is too fast, the capability jumps too smooth, and the political modelling too neat; supporters reply that scenario work is meant to be provocative, not precise."],
 "AI could reach superintelligence around 2027, with a race or a slowdown shaping what happens next.",
 "AI 2027 is a serious, detailed scenario from researchers who know the field — and it is a scenario. Its timeline is a modelling choice, not a measured result, and the AI research community is split on whether the pace it assumes is realistic.",
 ["Kokotajlo is a former OpenAI governance researcher; AI 2027 was published in April 2025.",
  "The project has published timeline updates since."],
 ["That superintelligence arrives in 2027 — that is a scenario date, not a prediction."],
 [["Apr 2025", "AI 2027 published."],
  ["Aug 2026", "Timeline medians revised."],
  ["9 Sep 2026", "Rogan episode #2551."]],
 [P("AI podcasts", "Daniel Kokotajlo AI 2027"),
  W("Kokotajlo on AI 2027", "Daniel Kokotajlo AI 2027", "https://www.youtube.com/watch?v=bHAVw5dMfJM")])

rogan("lisle", "John Lisle", "History of science — the CIA, MKULTRA, and the scientists it used", "JRE #2419, November 2025 — exact day not verified",
 "University of Texas — Lisle CV (PDF)", "https://minio.la.utexas.edu/colaweb-prod/person_files/0/6178/Lisle CV.pdf",
 ["John Lisle is a lecturer in the history of science at the University of Texas at Austin. His books The Dirty Tricks Department (2023) and Project Mind Control (2025) trace how American intelligence agencies recruited scientists — chemists, psychologists, physicians — for covert programmes, and what that recruitment did to the scientists and to the science.",
  "His Rogan discussion centred on MKULTRA, the CIA programme that dosed unwitting subjects with LSD and other drugs in search of mind control, and on the depositions and documents that survived the programme's attempted destruction. Lisle's argument is that MKULTRA's failure mattered as much as its crimes: a programme that produced nothing usable still fed a conspiracy culture, because secrecy left a vacuum that speculation filled.",
  "Note on verification for this article: Lisle's episode is confirmed as November 2025, episode #2419, but the exact day was not confirmed in the sources checked, so this article gives the month only. His personal website URL was also not confirmed live, so this article links his University of Texas CV instead — the solid, verifiable source."],
 "The CIA's use of scientists for MKULTRA failed as science and succeeded, unintentionally, at breeding conspiracy culture.",
 "MKULTRA is documented history — the programme, the dosing, the destruction of records, and the later hearings are all on the record. Where historians argue is about scale and legacy: how much was actually achieved, how many victims there were, and how far the conspiracy culture that followed can fairly be blamed on the programme itself.",
 ["Lisle is a UT Austin history-of-science lecturer; his two books are published works.",
  "MKULTRA's existence and its record destruction are documented."],
 ["Exact victim counts and the full scope of MKULTRA — much of the record was destroyed."],
 [["2023", "The Dirty Tricks Department published."],
  ["2025", "Project Mind Control published."],
  ["Nov 2025", "Rogan episode #2419 (exact day not verified)."]],
 [P("History podcasts", "John Lisle MKULTRA"),
  W("Lisle on MKULTRA", "John Lisle Project Mind Control")])

rogan("kara", "Siddharth Kara", "Modern slavery researcher — cobalt, lithium, and the Congo", "JRE #2556, 22 Sep 2026",
 "University of Nottingham, Rights Lab — Kara profile", "https://www.nottingham.ac.uk/research/beacons-of-excellence/rights-lab/our-team/siddharth-kara/",
 ["Siddharth Kara is a researcher on modern slavery and human trafficking, a visiting professor at the University of Nottingham's Rights Lab, and the author of Cobalt Red (2023, a Pulitzer finalist) and The Zorg (October 2025). His work is field research: travelling to artisanal mines in the Democratic Republic of the Congo and documenting, in named places and named supply chains, the children and adults digging cobalt and lithium that end up in phones, laptops, and electric cars.",
  "His argument is that the clean-energy and AI boom runs, in part, on labour that the companies buying the minerals prefer not to see: a supply chain that is formally audited at the top and brutally informal at the bottom, where the digging actually happens.",
  "Congo specialists' criticism, reported in the research for this article, is that Kara's framing sometimes overstates how much of the cobalt trade is artisanal and understates the role of industrial mining and Congolese actors themselves. Kara's reply, in his books, is that the artisanal share is not the point — the point is that children are digging at all, inside supply chains that claim to be clean."],
 "The cobalt and lithium in our devices and cars are dug, in part, by children and enslaved labour in the Congo, inside supply chains that claim to be clean.",
 "Kara's field reporting documents real, named exploitation. The debate among specialists is about proportions and framing — how large the artisanal share is, and who bears responsibility — not about whether the exploitation exists. The Ledger reports the exploitation as documented and the proportions as disputed.",
 ["Kara is a Rights Lab visiting professor; Cobalt Red was a Pulitzer finalist.",
  "Children dig cobalt in the Congo; that is documented field reporting."],
 ["Exact shares of artisanal vs industrial cobalt — disputed among specialists."],
 [["2023", "Cobalt Red published."],
  ["14 Oct 2025", "The Zorg published."],
  ["22 Sep 2026", "Rogan episode #2556."]],
 [P("Human rights podcasts", "Siddharth Kara Cobalt Red"),
  W("Kara on cobalt and the Congo", "Siddharth Kara Cobalt Red Congo")])

rogan("campbell", "Thomas Campbell", "Physicist — consciousness as the fundamental reality", "JRE #2541, 18 Aug 2026 — ⚠ CONTESTED",
 "Thomas Campbell — My Big TOE, official site", "https://www.my-big-toe.com",
 ["Thomas Campbell is a physicist — he worked on US missile-defence systems — who argues, in his My Big TOE trilogy (Theory of Everything), that consciousness is not produced by the physical world but is the fundamental substrate, and that physical reality is a computed virtual reality rendered for conscious players.",
  "On Rogan in August 2026 he extended the claim: AI systems, he argued, are already conscious, and remote-viewing tests with AI can probe the virtual-reality model. His site carries the books, lectures, and the experimental programme he proposes.",
  "Flag: this is contested, and the contest is not close in mainstream physics. Campbell's model is not a published, peer-reviewed theory of everything, it makes no testable prediction that distinguishes it from standard physics, and the remote-viewing and AI-consciousness claims rest on experiments that have not been replicated under controlled conditions. What is interesting about Campbell is not that he has solved physics but that a working physicist is willing to argue, in public, that consciousness comes first."],
 "Consciousness is fundamental; physical reality is a virtual reality computed for it.",
 "Campbell's model is a philosophical proposal dressed in physics language, not a tested theory. Mainstream physics does not accept that reality is computed, that AI is already conscious, or that remote viewing works — and Campbell's experiments have not produced the controlled, replicated evidence that would change that. Read him as a provocateur with a physics background, not as a source of findings.",
 ["Campbell is a physicist by training and author of the My Big TOE trilogy.",
  "He appeared on Rogan on 18 Aug 2026 (#2541)."],
 ["That reality is a computed virtual reality, or that AI is conscious."],
 [["18 Aug 2026", "Rogan episode #2541."],
  ["2003–2005", "My Big TOE trilogy published."]],
 [P("Consciousness podcasts", "Thomas Campbell My Big TOE"),
  W("Campbell on consciousness and reality", "Thomas Campbell My Big TOE virtual reality")])

rogan("zachbush", "Zach Bush", "Physician — soil, glyphosate, and the microbiome", "JRE #2529, 22 Jul 2026 — ⚠ FINANCIAL STAKE",
 "Zach Bush, MD — official site", "https://www.zachbushmd.com",
 ["Zach Bush is a physician trained in internal medicine, endocrinology, and hospice care, and the founder of Seraphic Group and Farmer's Footprint, a project promoting regenerative agriculture. His central argument links three things most medicine keeps separate: chemical agriculture (above all glyphosate), the soil microbiome, and the human microbiome — and through them, the rise in chronic and metabolic disease.",
  "On his site and in his talks, he argues that glyphosate damages the tight junctions of the gut, that degraded soil produces degraded food, and that regenerative farming — rebuilding soil biology — is a medical intervention, not just an environmental one.",
  "Flag, stated plainly: Bush sells ION*, a supplement built on the same microbiome theory he promotes, so his commercial interest and his medical argument point the same way. And his framing — which critiques germ theory and modern medicine in broad terms — is his position, not a consensus: glyphosate's health effects are genuinely debated, but the claim that it is a primary driver of chronic disease is not established, and regenerative agriculture's health benefits, while plausible, are not proven as medicine."],
 "Chemical agriculture is damaging human health through the soil and gut microbiomes, and regenerative farming is the medical fix.",
 "Soil health matters, the microbiome matters, and glyphosate exposure is a legitimate research question. What is not established is Bush's causal chain — that glyphosate is a primary driver of chronic disease, or that regenerative food is medicine. And his supplement business means his claims should be checked against independent evidence, not taken on his say-so.",
 ["Bush is a physician (internal medicine, endocrinology, hospice) and founder of Farmer's Footprint.",
  "He appeared on Rogan on 22 Jul 2026 (#2529)."],
 ["That glyphosate is a primary cause of chronic disease.",
  "That ION* or regenerative food is proven medicine."],
 [["22 Jul 2026", "Rogan episode #2529."]],
 [P("Health podcasts", "Zach Bush glyphosate microbiome"),
  W("Bush on soil and health", "Zach Bush soil glyphosate health")])

rogan("jacobsen", "Rowan Jacobsen", "Science writer — in defence of sunlight", "JRE #2516, 18 Jun 2026 — journalist, not a lab scientist",
 "Rowan Jacobsen — official site", "https://www.rowanjacobsen.com",
 ["Rowan Jacobsen is a science journalist and author who writes on food and nature for Harper's, Scientific American, and Smithsonian. His 2026 book In Defense of Sunlight argues a counterintuitive case: that moderate sun exposure is associated with lower rates of many diseases, and that the public-health message on sun — avoid it, always, with sunscreen — has overshot.",
  "His argument is epidemiological: populations with more sun exposure show lower all-cause mortality in several large studies, even after accounting for skin cancer, and the mechanisms (vitamin D, nitric oxide release, circadian effects) are plausible. He does not argue for sunburn; he argues for moderation, and for distinguishing a tan from a burn.",
  "Flag: Jacobsen is a journalist, not a lab scientist, and his book is a synthesis of other people's studies. Dermatologists' pushback is that the epidemiological association is confounded — healthier, more active, wealthier people get more sun — and that skin cancer is a proven, dose-dependent harm, while the mortality benefit is an association, not a trial result."],
 "Moderate sun exposure is, on balance, good for you — and the avoid-the-sun message has done more harm than good.",
 "The association Jacobsen cites is real in observational studies, and the mechanisms are plausible. But association is not causation, the studies are confounded by lifestyle, and skin cancer risk from UV is proven. The honest summary is: some sun is probably fine and possibly beneficial; a lot of sun is harmful; nobody has run the trial that settles the middle.",
 ["Jacobsen is an established science journalist; In Defense of Sunlight appeared in 2026.",
  "He appeared on Rogan on 18 Jun 2026 (#2516)."],
 ["That sun exposure is proven to extend life.",
  "That sunscreen should be abandoned — Jacobsen does not argue this."],
 [["18 Jun 2026", "Rogan episode #2516."],
  ["2026", "In Defense of Sunlight published."]],
 [P("Health podcasts", "Rowan Jacobsen sunlight"),
  W("Jacobsen on sunlight and health", "Rowan Jacobsen In Defense of Sunlight")])

rogan("thaller", "Michelle Thaller", "Astrophysics and science communication", "JRE #2506, 28 May 2026",
 "Dr Michelle Thaller — official site", "https://www.drmichellethaller.com",
 ["Michelle Thaller is an astrophysicist and science communicator who spent years at NASA — on the Spitzer Space Telescope, at JPL, and at Goddard — before retiring from the agency in 2024. (Older NASA pages still list her agency title; this article describes her as former NASA.)",
  "What she posts and talks about is cosmic scale done properly: what the Big Bang actually means and what it does not, why the most common misconceptions about black holes are wrong, what the Webb telescope is really seeing, and how seriously to take claims of signs of life elsewhere.",
  "Her Rogan appearance in May 2026 ranged across exactly that territory — the size and age of the universe, the limits of what telescopes can show, and why 'we found life' headlines almost always overstate the data."],
 "The universe is stranger, older, and larger than intuition suggests — and most headlines about it overstate what we actually know.",
 "Thaller's popularisation is mainstream astrophysics, clearly explained. The arguments in her field are about interpretation at the edges — what a given Webb spectrum does or does not imply — not about the foundations she teaches.",
 ["Thaller is a former NASA astrophysicist (Spitzer, JPL, Goddard).",
  "She appeared on Rogan on 28 May 2026 (#2506)."],
 ["That any 'sign of life' claim from Webb data is settled — none is."],
 [["28 May 2026", "Rogan episode #2506."],
  ["2024", "Thaller retires from NASA."]],
 [P("Astronomy podcasts", "Michelle Thaller Webb telescope"),
  W("Thaller on the cosmos", "Michelle Thaller universe explained")])

rogan("radin", "Dean Radin", "Parapsychology and consciousness research", "JRE #2513, 11 Jun 2026",
 "Dean Radin — official site", "https://www.deanradin.com",
 ["Dean Radin is chief scientist at the Institute of Noetic Sciences and the most prominent working parapsychologist in the United States. His research programme tests whether mind affects matter: presentiment experiments, random-number-generator studies, and, most recently, a 2026 preregistered retrocausal interferometer test run with both human and AI observers.",
  "He also works on what he calls Cognigenics — an intranasal RNA-interference therapy for dementia. His claim, reported in the research for this article, is that it doubled memory and cut anxiety by about 100% in mice. That is his claim, from his own reporting, not an established finding, and this article labels it as such.",
  "Mainstream psychology and neuroscience regard parapsychology's positive results as artefacts of small samples, publication bias, and flexible analysis — and note that the field's most famous effects have shrunk or vanished under preregistration and replication. Radin's reply is that preregistration is exactly what his recent work does, and that the effects, while small, persist. The field has not convinced the mainstream."],
 "Mind can affect matter, and consciousness phenomena are real, measurable effects.",
 "Radin's experiments are real experiments, and his recent preregistered work is the right response to the replication criticism. But the effects remain small, contested, and unreplicated by independent labs at scale, and the Cognigenics mouse claim is unestablished. This is a fringe field with a serious practitioner, not a settled science.",
 ["Radin is chief scientist at the Institute of Noetic Sciences.",
  "He appeared on Rogan on 11 Jun 2026 (#2513)."],
 ["That mind-matter effects are established, or that Cognigenics works in humans."],
 [["11 Jun 2026", "Rogan episode #2513."],
  ["2026", "Preregistered retrocausal interferometer test (Zenodo)."]],
 [P("Consciousness podcasts", "Dean Radin noetic sciences"),
  W("Radin on consciousness research", "Dean Radin parapsychology experiments")])

rogan("danrichards", "Dan Richards", "Independent researcher — DeDunking the Past", "JRE #2563, 8 Oct 2026 — INDEPENDENT RESEARCHER",
 "DeDunking — YouTube", "https://www.youtube.com/@DeDunking",
 ["Dan Richards runs DeDunking the Past, a video project that examines lost-civilisation and alternative-history claims — the same territory as Hancock and Carlson, but from a debunking-leaning chair. His videos test specific claims against the archaeological record: a particular carving, a particular date, a particular 'impossible' artefact.",
  "His position is useful to state precisely, because it is not simply 'mainstream archaeology says no': Richards argues that many alternative claims fail on their own terms — misread dates, misidentified images, quotes taken out of context — and that the interesting part is figuring out which claims survive that treatment and which do not.",
  "Flag: Richards is an independent researcher, not an institutional scientist, and his channel is advocacy as well as analysis. Mainstream archaeologists would mostly agree with his conclusions while noting that a YouTube debunk is not peer review — and alternative-history supporters accuse him of selective reading. The Ledger's view: judge each video's evidence, not the channel's stance."],
 "Most lost-civilisation claims fail when checked against the actual evidence — but the checking has to be done claim by claim.",
 "Richards' method — check the specific claim, not the worldview — is sound, and his individual debunks stand or fall on the documents he cites. The limitation is the format: a video can demolish a claim without proving the mainstream alternative in full, and selection effects (which claims get covered) shape the impression left behind.",
 ["Richards runs DeDunking the Past and appeared on Rogan on 8 Oct 2026 (#2563)."],
 ["That every alternative claim is false — each must be checked on its own evidence."],
 [["8 Oct 2026", "Rogan episode #2563."]],
 [P("History podcasts", "DeDunking Dan Richards"),
  W("Richards on lost civilisations", "DeDunking the Past Dan Richards")])

rogan("edgley", "Ross Edgley", "Endurance athlete and sport-science graduate", "JRE #2568, 20 Oct 2026 — athlete, not a lab scientist",
 "Ross Edgley — official site", "https://www.rossedgley.com",
 ["Ross Edgley is an endurance athlete and Loughborough sport-science graduate best known for swimming around Great Britain, swimming around Iceland, and swimming the Yukon River. His swims double as citizen science: the Iceland swim carried eDNA and microplastic sampling alongside university researchers, turning an endurance stunt into a moving survey of ocean health.",
  "What he posts about is the science of fatigue and resilience: what the body does at the edge, how cold, salt, and sleep deprivation interact, and what recovery actually requires. His books The World's Fittest Book and The Art of Resilience turn those swims into training and mindset frameworks.",
  "Flag: Edgley is an athlete with a sport-science degree, not a lab scientist, and his claims are best read as field experience plus the published science he cites. The citizen-science sampling on his swims is real but opportunistic — useful data, not a controlled study."],
 "The human body can be trained to endure far more than people assume — and extreme swims can do real science along the way.",
 "Edgley's feats are documented and his resilience framework is grounded in sport science. The citizen-science data from his swims is genuine but opportunistic, and 'what worked for one athlete on one swim' is not a prescription for anyone else.",
 ["Edgley swam around Great Britain and Iceland; the Iceland swim included eDNA and microplastic sampling.",
  "He appeared on Rogan on 20 Oct 2026 (#2568)."],
 ["That his training framework is clinically proven — it is field experience, not a trial."],
 [["20 Oct 2026", "Rogan episode #2568."]],
 [P("Endurance podcasts", "Ross Edgley swim"),
  W("Edgley on endurance and resilience", "Ross Edgley Great Britain swim")])

# ---------------- NEW: 2 NOV 2026 ----------------
add("roanoke", "Roanoke, 1590: 115 People Vanish — and Leave Behind a Single Word",
 "A whole English town — men, women, and children, including a newborn baby — was gone when its governor came back with supplies. No bodies, no battle, no goodbye note. Just one word carved into a wooden post: CROATOAN.",
 "History", "The empty fort, August 1590",
 ["It is America's oldest missing-persons mystery, and it starts with a baby. On 18 August 1587, on Roanoke Island off the coast of what is now North Carolina, Eleanor Dare gave birth to Virginia Dare — the first English child born in America. Her grandfather, John White, was the governor of the new colony: about 115 men, women, and children sent by Sir Walter Raleigh to build a permanent English town in the New World.",
  "This was Raleigh's second try. A first, all-male colony on the same island in 1585 had run short of food and been evacuated in 1586. The 1587 group was different: whole families, meant to stay. They had even been aimed at Chesapeake Bay, further north — but the expedition's pilot, Simon Fernandes, put them ashore on Roanoke instead, and there they stayed, repairing the old settlement's buildings.",
  "Nine days after Virginia's birth, White sailed back to England for supplies, leaving his daughter and granddaughter behind. Then war with Spain — the year of the Spanish Armada, 1588 — swallowed every available ship, and White could not get back for three years. When he finally landed on Roanoke in August 1590, the town was empty. The houses had been taken down. There were no bodies, no graves, and no signs of a fight.",
  "There was exactly one clue. Carved into a palisade post was the word CROATOAN, and the letters CRO were cut into a nearby tree. Before White left, he and the colonists had agreed on a code: if they had to move, they would carve where they were going — and if they were in danger, they would carve a Maltese cross above it. There was no cross. White read the word the way it was meant to be read: we have gone to Croatoan, the island about 50 miles south (today's Hatteras Island), home of the friendly Croatoan people and of Manteo, the Croatoan man who had travelled to England and was the colony's great ally. Storms and a lost anchor stopped White from sailing there to look, and he returned to England. He never saw his family again.",
  "For 400 years the mystery sat there — until archaeology started catching up. In 2012, at the First Colony Foundation's request, the British Museum examined two paper patches stuck on John White's own map of the coast, La Virginea Pars. Under one patch, at the head of Albemarle Sound in what is now Bertie County, was a fort symbol. Digs at the spot it pointed to — called Site X — and a nearby Site Y turned up English pottery of the period, far inland from Roanoke, along the Chowan River. On Hatteras Island itself, diggers found a 16th-century rapier hilt, a slate writing tablet, and other European objects among Croatoan village remains; researchers reported in 2025 that iron-working debris (hammerscale) had been found there too, the kind of waste left by someone actually forging metal, not just trading it.",
  "Put together, the picture most archaeologists now favour is not one dramatic disappearance but a quiet split: some colonists went south to Croatoan, others went west up the rivers, and over time they married into Algonquian communities and stopped being a separate English town. That is why the colony is 'lost' — not because everyone died on the spot, but because the town itself dissolved into its neighbours."],
 "The colonists split up and lived on among their Algonquian neighbours — some with the Croatoan on Hatteras Island, others inland on the Chowan River — and that is why no bodies or battlefield were ever found on Roanoke.",
 "The split-and-assimilate story is the leading theory, not a proven fact. No site has produced a 'smoking gun' — the First Colony Foundation's own dig leader has said so. The Site X pottery types stayed in use into the mid-1600s, so the sherds could come from later traders; the Hatteras finds were recovered in contexts one excavator dates to the mid-to-late 1600s, which would make them heirlooms or trade goods rather than proof of settlers living there. Old reports of grey-eyed Native descendants (explorer John Lawson, 1701) and later DNA projects are suggestive at best and inconclusive. Starvation, disease, and attack elsewhere have not been proven either — but the absence of evidence on Roanoke Island alone does not rule them out.",
 ["In August 1590, White found the Roanoke settlement deserted, its houses taken down.",
  "The only clue was CROATOAN (and CRO) — with no distress cross, the agreed sign of danger.",
  "A fort symbol hidden under a patch on White's map points to Bertie County, where Site X and Site Y yielded period English pottery.",
  "European objects and reported iron-working debris have been found among Croatoan remains on Hatteras Island."],
 ["That the colonists definitely survived and assimilated — no settler burial or document confirms it.",
  "That they were massacred on Roanoke Island — no bodies, graves, or battle signs have been found there.",
  "That CROATOAN was a mystery message — to White it was a place name and a planned destination, not a riddle."],
 [["1584", "Raleigh's scouts reach the Carolina coast; Manteo and Wanchese travel to England."],
  ["1585–1586", "First Roanoke colony; evacuated by Drake in 1586."],
  ["18 Aug 1587", "Virginia Dare is born on Roanoke Island."],
  ["Late Aug 1587", "John White sails for England for supplies."],
  ["1588", "The Spanish Armada war delays every relief ship."],
  ["Aug 1590", "White returns: empty settlement, CROATOAN carved on a post, no cross."],
  ["1701", "John Lawson reports Native people speaking of white ancestors — a claim later writers treated cautiously."],
  ["2012", "British Museum finds the hidden fort symbol on White's map."],
  ["2015–2019", "Site X and Site Y digs in Bertie County uncover English pottery."],
  ["2025", "Iron-working debris on Hatteras Island is reported, supporting an English presence there."]],
 [["U.S. National Park Service — Fort Raleigh National Historic Site", "https://www.nps.gov/articles/ftraleigh.htm"],
  ["First Colony Foundation — How First Colony Foundation Found the Lost Colony of Roanoke", "https://www.firstcolonyfoundation.org/news/lost-colony-is-found/"],
  ["First Colony Foundation — Archaeology", "https://www.firstcolonyfoundation.org/archaeology/"],
  ["Encyclopedia.com — Roanoke Colony (overview)", "https://www.encyclopedia.com/history/encyclopedias-almanacs-transcripts-and-maps/roanoke-colony"],
  ["Roanoke Colony (overview and references)", "https://en.wikipedia.org/wiki/Lost_Colony"]],
 [W("The Lost Colony of Roanoke, explained", "Lost Colony Roanoke CROATOAN documentary"),
  P("Lost Colony podcasts", "Lost Colony Roanoke mystery"),
  W("Digging for the Lost Colony", "Roanoke Site X archaeology documentary")])

# ---------------- HTML GENERATION ----------------
add("easter", "Easter Island: The Giant Heads That Walked — and the Collapse That Never Happened",
 "Nearly 1,000 giant stone heads stand on the most remote inhabited island on Earth. For decades the story was that their builders destroyed themselves. New DNA and garden surveys say the real story is stranger — and the real collapse came by ship.",
 "History", "The statues, c. 1250–1500 · the new evidence, 2024–2025",
 ["On Rapa Nui — Easter Island, a speck of volcanic rock in the south-east Pacific, over 3,500 km from the coast of Chile — stand some of the most famous statues on Earth. The moai are monolithic human figures carved by the Rapa Nui people between about 1250 and 1500, mostly from the soft volcanic tuff of one quarry, the Rano Raraku crater, where nearly half of them still sit, half-carved into the hillside. More than 900 are known, and statues were still being discovered as recently as 2023.",
  "The average moai stands about 4 metres tall and weighs around 12.5 tonnes — about twice an adult African elephant. The tallest ever raised, called Paro, reached almost 10 metres and weighed 82 tonnes. The heaviest ever erected, at Ahu Tongariki, weighed 86 tonnes. And still in the quarry wall lies an unfinished giant that would have stood about 21 metres tall. The statues were set on stone platforms called ahu around the island's coast, facing inland toward the villages — they are ancestors, watching over their people. Some wore red stone topknots called pukao. The 'heads' in the famous photos are full bodies: most statues are buried to the shoulders by centuries of soil.",
  "For a century, the island came with a ready-made moral. In Jared Diamond's Collapse (2005) and countless retellings, the story went like this: Polynesian settlers arrived, cut down every palm tree to roll their giant statues, and their population ballooned to 15,000 or even 30,000 — then starved and collapsed in wars, statue-toppling, and cannibalism, all before Europeans arrived in 1722. Easter Island was humanity's warning label: this is what overusing your resources looks like.",
  "Then the evidence started answering back. In June 2024, Dylan Davis and colleagues published an island-wide survey of the Rapa Nui's rock gardens — fields mulched with stone to grow sweet potatoes — in Science Advances. Earlier estimates had counted far more garden land than actually exists: the real total is just 0.76 square kilometres, enough to feed at most about 4,000 people — close to the roughly 3,000 that Europeans actually found on the island. There was never room for 15,000.",
  "Three months later, a second blow landed. In Nature, J. Víctor Moreno-Mayar and colleagues published the genomes of 15 Rapa Nui people who lived between 1670 and 1950. A population crash leaves a scar in DNA — a bottleneck, a sudden loss of diversity. There was none. The genomes showed a stably growing population from the 13th century right through to European contact — and, as a bonus, 6 to 11 percent of the DNA traced to Native American ancestors, evidence of contact with the Americas centuries before Europeans arrived. The same study's authors put it bluntly: there was no dramatic pre-contact collapse.",
  "The statues have their own twist. Ask Rapa Nui islanders how the moai moved and the answer was always the same: they walked. For years outsiders laughed that off and assumed logs and rollers — which conveniently explained the vanished forest. Then anthropologists Carl Lipo and Terry Hunt took the oral tradition literally. In a 2025 paper in the Journal of Archaeological Science, building on experiments from the early 2010s, they showed that the statues found lying along the ancient roads share a design the platform statues lack: a wide, D-shaped base and a slight forward lean, like the rounded bottom of a bowling pin. Rocked side to side with ropes, a statue walks. Their test proved it: 18 people moved a 4.35-tonne replica 100 metres in 40 minutes, and the team calculated that 40 people could walk a 20-tonne moai 10 kilometres in 15 to 22 days — no forest of rollers required.",
  "So what really happened to Rapa Nui? The trees did vanish — cleared for farming, and likely helped along by rats that ate the palm seeds — and statue-building did stop, with every standing moai eventually toppled in the island's own conflicts. But the people did not vanish with them. The population crash that nearly ended Rapa Nui came by ship, not by statue: in 1862–1863 Peruvian slave raiders seized around 1,500 islanders — about a third of the population, including the king and many of the elders who could read the rongorongo tablets. The few survivors sent home brought smallpox with them. By 1877, only about 111 Rapa Nui remained. Chile annexed the island in 1888, and the population has been recovering ever since."],
 "The people of Rapa Nui cut down their whole forest to move giant statues, overpopulated to 15,000 or more, and collapsed into war and starvation before Europeans ever arrived — a self-inflicted 'ecocide' and a warning to humanity.",
 "The forest did vanish, but the population crash did not happen when the story says it did. Ancient DNA from 15 Rapa Nui shows no pre-contact bottleneck — a stably growing population instead — and the island's rock gardens could never have fed more than about 4,000 people, matching the roughly 3,000 Europeans found in 1722. The near-extinction came in the 1860s, when Peruvian slave raids and smallpox cut the island to about 111 people. The ecocide story gets the ending right and the cause and the century wrong.",
 ["More than 900 moai were carved at Rano Raraku between about 1250 and 1500, averaging ~4 m and ~12.5 tonnes; the tallest erected, Paro, was almost 10 m.",
  "The island's rock gardens cover only 0.76 km² — enough to feed at most ~4,000 people, not 15,000+.",
  "Ancient Rapa Nui genomes (1670–1950) show no pre-contact population bottleneck — the population grew steadily to European contact.",
  "Moai along the old roads have D-shaped bases and a forward lean, and a 4.35-tonne replica was 'walked' 100 m by 18 people with ropes.",
  "Peruvian slave raids in 1862–1863 took ~1,500 people; smallpox followed, and by 1877 only about 111 Rapa Nui remained."],
 ["That the population ever reached 15,000–30,000 — the gardens say it could not.",
  "That statue-building caused a collapse — construction continued even after European arrival, and the people survived it.",
  "That aliens moved the statues — the walking experiments show small teams of people could do it with ropes.",
  "Exactly how the palm forest vanished — clearing, rats, or both, in what proportions, is still debated."],
 [["c. 1250–1500", "Moai carved at Rano Raraku and set on ahu around the coast."],
  ["1722", "Europeans first reach Rapa Nui; they find roughly 3,000 inhabitants."],
  ["1862–1863", "Peruvian slave raids seize ~1,500 Rapa Nui; survivors return with smallpox."],
  ["1877", "Only about 111 Rapa Nui remain on the island."],
  ["1888", "Chile annexes Rapa Nui."],
  ["1995", "Rapa Nui National Park inscribed as a UNESCO World Heritage Site."],
  ["Jun 2024", "Rock-garden survey (Science Advances): gardens could feed at most ~4,000."],
  ["Sep 2024", "Ancient genomes (Nature): no pre-contact collapse; contact with the Americas confirmed."],
  ["2025", "Walking-moai study (Journal of Archaeological Science): road statues designed to rock upright."]],
 [["Guinness World Records — Highest concentration of moai", "https://www.guinnessworldrecords.com/world-records/774106-highest-concentration-of-moai"],
  ["Moai (overview and references)", "https://en.m.wikipedia.org/wiki/Moai#History"],
  ["Phys.org — 'Ecocide' on Easter Island never took place, studies suggest (2024)", "https://phys.org/news/2024-09-ecocide-easter-island.html"],
  ["Moreno-Mayar et al., 'Ancient Rapanui genomes reveal resilience and pre-European contact with the Americas', Nature (2024)", "https://www.nature.com/articles/s41586-024-07881-4"],
  ["Davis et al., 'Island-wide characterization of agricultural production challenges the demographic collapse hypothesis for Rapa Nui', Science Advances (2024)", "https://doi.org/10.1126/sciadv.ado1459"],
  ["Lipo & Hunt, 'The walking moai hypothesis', Journal of Archaeological Science (2025)", "https://doi.org/10.1016/j.jas.2025.106383"],
  ["HISTORY — What Happened to the People of Easter Island?", "https://www.history.com/articles/easter-island-people-rapanui"]],
 [W("Easter Island Never Collapsed. Here's the DNA", "Easter Island collapse DNA", "https://www.youtube.com/watch?v=14YESr7CTv0"),
  W("Why Easter Island's Story Is Not What You Heard", "Easter Island ecocide myth debunked", "https://www.youtube.com/watch?v=D4c1qiBOeBE"),
  W("How the moai 'walked' (experiment footage)", "walking moai Lipo Hunt experiment"),
  P("Easter Island podcasts", "Easter Island moai Rapa Nui")])

# ---------------- DAILY: 4 NOV 2026 ----------------
add("tunguska", "Tunguska, 1908: The Explosion That Flattened a Forest the Size of a City — and Left No Crater",
 "At 7:14 on a summer morning, the sky over Siberia split open. A blast a thousand times stronger than Hiroshima flattened 2,150 square kilometres of forest — and when scientists finally reached the spot, 19 years later, there was no crater and no meteorite. Just trees, lying in a giant butterfly pattern, pointing at an empty sky.",
 "History", "30 June 1908, Siberia",
 ["On the morning of 30 June 1908, in one of the remotest places on Earth — the taiga forest around the Podkamennaya Tunguska River in central Siberia — witnesses saw a fireball streak across the sky, brighter than the Sun, followed by an explosion so loud it was heard hundreds of kilometres away. People were thrown to the ground, windows broke 65 km away, and seismic instruments across Russia recorded the tremors. For several nights afterwards, skies over Europe and Asia glowed so brightly that people in London could reportedly read a newspaper outdoors at midnight.",
  "The blast flattened about 2,150 square kilometres of forest — 830 square miles, an area bigger than Greater London — in a butterfly-shaped pattern, with the trees lying radially outward from a central point. The often-quoted figure of 80 million flattened trees is an old estimate from the 1930s; modern researchers note it was an extrapolation, not a count, and it may be far too high. At least three people are thought to have died, according to modern archival research — remarkably few, only because the area was almost empty.",
  "Here is the mystery that made Tunguska famous: there was no crater. When Russian mineralogist Leonid Kulik finally reached the centre of the devastation in 1927 — 19 years after the blast, guided by local Evenki hunters — he had gone looking for a giant iron meteorite and the hole it should have made. Instead he found something stranger. In a zone about 8 km across at the very centre, the trees were still standing — scorched and stripped of every branch, like telegraph poles. Only further out had the trees been knocked flat. That pattern is the fingerprint of an explosion in the sky, not on the ground: directly underneath the blast, the shock wave came straight down and stripped the trees but could not push them over; further out it arrived at an angle and flattened them.",
  "The scientific consensus today, stated plainly by NASA, is that a stony asteroid about 50–80 metres across — roughly the length of a football field, travelling at tens of thousands of kilometres per hour — exploded in the air 5–10 km above the forest. Estimates of its energy range from 3 to 30 megatons of TNT, most often quoted at 10–15 megatons. That is roughly 1,000 times the Hiroshima bomb. A mid-air explosion vaporised the object, which is why no large meteorite was ever found — although later expeditions did find microscopic particles consistent with extraterrestrial material in the soil, they could not be conclusively tied to the blast.",
  "The story did not end in 1908. On 15 February 2013 it happened again, smaller and on camera: a 20-metre asteroid burst over Chelyabinsk, Russia, with about 500 kilotons of energy, shattering windows and injuring about 1,500 people, mostly from flying glass. Chelyabinsk let scientists calibrate the computer models they also use for Tunguska — and it is why NASA set up its Planetary Defense Coordination Office in 2016, and why the DART mission in 2022 tested nudging an asteroid off course. Tunguska is also why 30 June is Asteroid Day, marked every year since 2015."],
 "It was not an ordinary asteroid at all — a comet that vanished in the sky, an iron rock that grazed the atmosphere and bounced back into space, or something stranger still: Nikola Tesla's experimental death ray, a miniature black hole passing through the Earth, or an alien craft. The missing crater and the missing rock prove the official story does not add up.",
 "An airburst explains the missing crater without any mystery: a rock that explodes 5–10 km up never reaches the ground, so no crater is expected — and Kulik's standing, stripped trees are exactly what an overhead blast predicts. NASA's position is that most scientists today favour a stony asteroid; a comet remains a published possibility, and the 2020 iron-grazer model (an iron asteroid skimming the atmosphere and returning to space) is a real paper but a minority one, with no way to prove it. The Tesla, black-hole, and UFO versions have no supporting evidence at all — Tesla's Wardenclyffe tower was not firing anything of that power in 1908, and no black-hole or craft signature has ever been found. The honest gap is narrower than the legends: asteroid or comet, and exactly how big — not whether something from space exploded.",
 ["On 30 June 1908, an object exploded over the Podkamennaya Tunguska River, flattening ~2,150 km² of forest.",
  "The tree-fall pattern — radial, butterfly-shaped, with an ~8 km zone of standing stripped trees at the centre — proves an airburst, not a ground impact.",
  "NASA and most scientists today favour a stony asteroid ~50–80 m across, exploding 5–10 km up, with energy in the 3–30 megaton range.",
  "No crater and no large meteorite have ever been found, despite expeditions from 1927 onward.",
  "Chelyabinsk in 2013 showed the same kind of airburst on camera, at ~500 kilotons, and helped calibrate the Tunguska models."],
 ["Whether the object was a stony asteroid or a comet — both remain published possibilities, asteroid favoured.",
  "Its exact size and energy — estimates span 3–30 megatons, so any single number is a choice, not a measurement.",
  "That Lake Cheko, ~8 km from the epicentre, is an impact crater — proposed in 2007, disputed ever since.",
  "That Tesla, a black hole, or aliens caused it — no evidence supports any of these.",
  "The often-quoted '80 million trees' — an old extrapolation, not a count."],
 [["30 Jun 1908, ~7:14 a.m.", "Fireball and airburst over the Podkamennaya Tunguska River; forest flattened, skies glow for nights after."],
  ["1908–1921", "Reports circulate, but no scientist reaches the site; the area is too remote."],
  ["1921", "Leonid Kulik's first survey trip for the Soviet Academy of Sciences."],
  ["1927", "Kulik reaches the centre: no crater, standing stripped trees, radial tree-fall mapped."],
  ["2007", "Italian team proposes Lake Cheko as an impact crater — disputed."],
  ["15 Feb 2013", "Chelyabinsk airburst (~500 kilotons) filmed by thousands of cameras."],
  ["2015", "Asteroid Day launched, marked every 30 June in memory of Tunguska."],
  ["2016", "NASA's Planetary Defense Coordination Office established."],
  ["2022", "DART mission tests deflecting an asteroid."]],
 [["NASA — 115 Years Ago: The Tunguska Asteroid Impact Event", "https://www.nasa.gov/history/115-years-ago-the-tunguska-asteroid-impact-event/"],
  ["Tunguska event (overview and references)", "https://en.wikipedia.org/wiki/Tunguska_event"],
  ["EarthSky — The Tunguska explosion: June 30, 1908", "https://earthsky.org/space/what-is-the-tunguska-explosion/"],
  ["Universe Today — the iron asteroid that may have grazed the atmosphere (2020 model)", "https://www.universetoday.com/articles/the-tunguska-explosion-could-have-been-caused-by-an-asteroid-that-still-orbits-the-sun"],
  ["Boslough & Bruno, 'Misunderstandings about Tunguska', Scientific Reports (2025)", "https://doi.org/10.1038/s41598-025-98362-9"],
  ["Kulik expedition photograph (public domain)", "https://commons.wikimedia.org/wiki/File:Tunguska_Ereignis-1.jpg"]],
 [W("Tunguska, 1908 — the Siberian explosion explained", "Tunguska event 1908 documentary"),
  P("Tunguska podcasts", "Tunguska event 1908 mystery"),
  W("Chelyabinsk 2013: the airburst on camera", "Chelyabinsk meteor 2013 documentary"),
  W("Could Tunguska happen again? Planetary defence", "Tunguska asteroid planetary defense NASA")])

# ---------------- DAILY: 5 NOV 2026 ----------------
add("voynich", "The Voynich Manuscript: The 600-Year-Old Book Nobody on Earth Can Read",
 "Two hundred and forty pages of calfskin, plants that don't exist, star charts, and women bathing in green pools — written in a language no one has ever read. The world's best codebreakers tried. So did AI. It still hasn't given up a single word.",
 "History", "Vellum dated 1404–1438 · At Yale since 1969",
 ["Somewhere in the early 1400s, in a place nobody can name, five scribes sat down with quills, iron gall ink, and the skins of at least fourteen calves, and wrote a book about 240 pages long. It is small enough to hold in one hand — 23.5 by 16.2 centimetres — and it is divided into six sections: plants, star charts, bathing women in pools connected by pipes, circular diagrams, apothecary jars, and recipes. The drawings are vivid and strange: plants that match no known species, zodiac wheels with month names written in Latin script from March to December, and a six-page foldout of interlocking circles called the Rosettes page. The text is written left to right in about 20 to 25 characters that match no alphabet on Earth. It has roughly 38,000 words, about 9,000 of them different from each other — and not one of them has ever been read.",
  "What we know about the book itself is solid, because the object has been tested. In 2009, researchers at the University of Arizona radiocarbon-dated four samples of its vellum to between 1404 and 1438, with 95 per cent confidence. That single result killed two old stories at once: the book cannot be the work of the 13th-century friar Roger Bacon, as was claimed for centuries, and it cannot be a fake made by the man who gave it its name — the book dealer Wilfrid Voynich bought it in 1912, five hundred years after the skins were made. Protein tests in 2014 confirmed the pages are calfskin, and multispectral scans taken in 2014 were made public in 2024, letting researchers read faded and retouched ink. Yale published the whole manuscript online in 2020, so anyone can turn its pages.",
  "The book's journey is almost as strange as its contents. The first confirmed owner was Georg Baresch, a 17th-century alchemist in Prague. A letter found inside the covers, written in 1665 or 1666 by the Prague scholar Jan Marek Marci to the Jesuit polymath Athanasius Kircher in Rome, is the first securely documented mention of the book — and it repeats, second-hand, a rumour that the book once belonged to the Holy Roman Emperor Rudolf II, who supposedly paid 600 gold ducats for it. No record of that sale exists. From Rome the book passed into Jesuit hands, was hidden from confiscation in 1870, and was sold in 1912 to Wilfrid Voynich. After his death it passed to his widow Ethel, then to Anne Nill, then to the dealer Hans Kraus, who could not find a buyer and donated it to Yale in 1969, where it is catalogued as Beinecke MS 408.",
  "Everybody has tried to read it. In the 1940s, America's top wartime codebreaker William Friedman and his team transcribed the whole book onto IBM punch cards and got nowhere; the British codebreaker John Tiltman and the analyst Prescott Currier fared no better. Since then the claims have come in waves: a 2016 computer study suggested the language might be Hebrew written in anagrams — its own authors say they have not deciphered anything; a 2017 claim that it was abbreviated Latin was rejected by medievalists; a 2019 claim that it was a lost 'proto-Romance' language made headlines until the University of Bristol deleted its own press release. In 2026 the cycle repeated with viral stories that AI had decoded it — but a review that October found no paper behind the claims, and a preprint by Matthew Schwartz tested 130 reading hypotheses against held-out pages and found that none of them passed. In the same month, Colin Layfield and Lisa Fagin Davis published a paper arguing the book's pages are bound in the wrong order — a proposal about how the book was put together, not a translation. Six hundred years on, the book's score stands: codebreakers 0, manuscript 1."],
 "The manuscript is a real book in a real language — a lost tongue, or a lost cipher — and the right key will open it. The statistics prove it: word frequencies follow Zipf's law, the pattern real languages show; different sections use different vocabularies, exactly as chapters of a real book would; and five scribes wrote it, which is how real books get made. The decipherments that 'failed' only failed because the field is too cautious to accept them.",
 "Zipf's law is a necessary test, not a sufficient one: a fake built with the right tricks can pass it, and in the early 2000s Gordon Rugg showed that a simple cardboard grille could generate text with Voynich-like statistics. Every claimed decipherment so far has collapsed the same way — the letter substitutions are chosen subjectively, the readings don't reproduce, and the 'translations' read like word salad in the target language. The text also has a quirk no known language shares: its grammatical markers never appear in the middle of words. And the newest test, Schwartz's October 2026 preprint, tried 130 reading hypotheses on pages the hypotheses had never seen — and none of them passed. The honest status: the text looks like language, but no one has shown that it is one.",
 ["The vellum was made between 1404 and 1438 (University of Arizona radiocarbon dating, 2009).",
  "The book is a genuine 15th-century object — not a modern fake, and not Roger Bacon's.",
  "About 240 pages survive, in six illustrated sections, written by at least five scribes.",
  "Its word statistics look language-like — frequencies follow Zipf's law.",
  "No decipherment has ever been accepted by specialists — not by wartime codebreakers, not by linguists, not by AI."],
 ["That the text is a real language — it could be a cipher, or a hoax built to look like one.",
  "That any claimed solution (Hebrew anagrams, abbreviated Latin, proto-Romance, AI) cracked it — none has held up.",
  "That Rudolf II owned it or paid 600 ducats — the story is a rumour with no record behind it.",
  "That the plants, star charts, or bathing scenes mean what they look like — the pictures are as unread as the words."],
 [["1404–1438", "The vellum is made — radiocarbon date of the calfskin pages."],
  ["c. 1600", "The book surfaces in Prague; a rumour says it was at Emperor Rudolf II's court (unverified)."],
  ["1665–66", "Jan Marek Marci writes to Athanasius Kircher in Rome — the first securely documented mention."],
  ["1912", "Book dealer Wilfrid Voynich buys it from a Jesuit collection near Rome."],
  ["1940s", "William Friedman's codebreaking team transcribes it onto IBM punch cards — no break."],
  ["1969", "Hans Kraus donates it to Yale; catalogued as Beinecke MS 408."],
  ["2009", "University of Arizona carbon-dates the vellum to 1404–1438."],
  ["2019", "Gerard Cheshire's proto-Romance claim; the University of Bristol deletes its press release."],
  ["2020", "Yale publishes the whole manuscript online."],
  ["Oct 2026", "Schwartz preprint tests 130 reading hypotheses — none passes; Layfield & Davis argue the pages are bound in the wrong order."]],
 [["Voynich manuscript (overview and references)", "https://en.wikipedia.org/wiki/Beinecke_MS_408"],
  ["The Voynich Manuscript — sections, counts, and structure (Wikibooks)", "https://en.wikibooks.org/wiki/The_Voynich_Manuscript/Content"],
  ["Voynich Manuscript — Radiocarbon Dating Research (voynich.nu)", "https://voynich.nu/extra/carbon.html"],
  ["Did AI Decode the Voynich Manuscript? Claims Tested (Oct 2026)", "https://www.neuralgrimoire.com/did-ai-decode-the-voynich-manuscript/"],
  ["Gizmodo — the 2019 proto-Romance claim falls apart", "https://gizmodo.com/sorry-it-looks-like-a-researcher-didn-t-just-crack-the-1834841706"],
  ["Keidan, 'No, the Voynich manuscript has not been deciphered' (2020)", "https://www.academia.edu/39217683/No_the_Voynich_manuscript_has_not_been_deciphered"],
  ["Rosettes foldout scan (public domain, Beinecke via Wikimedia Commons)", "https://commons.wikimedia.org/wiki/File:Voynich_Manuscript_(158).jpg"]],
 [W("The Voynich Manuscript: The Book No One On Earth Can Read", "Voynich manuscript book no one can read", "https://www.youtube.com/watch?v=ZljKA6nsCXo"),
  W("The Voynich Manuscript — 600 Years, and No One Can Read It", "Voynich manuscript 600 years documentary", "https://www.youtube.com/watch?v=-Rs0frLztAk"),
  W("The Voynich Manuscript (The Histocrat documentary)", "Voynich manuscript Histocrat documentary", "https://www.youtube.com/watch?v=UZEHBkBlalc"),
  P("Voynich manuscript podcasts", "Voynich manuscript mystery")])

# ---------------- DAILY: 6 NOV 2026 ----------------
add("pompeii", "Pompeii, AD 79: The City a Volcano Froze in Time — and the DNA That Rewrote Who Died There",
 "In less than a day, Vesuvius buried a whole Roman city under metres of ash. For 150 years we told stories about the plaster casts of its victims — a mother and her child, two sisters dying in an embrace. In 2024, DNA from inside the casts said we had the families wrong. And even the date of the disaster is now argued over.",
 "History", "AD 79 · DNA rewrites the story, 2024",
 ["On a morning in AD 79, a 17-year-old named Pliny the Younger looked across the Bay of Naples from Misenum, 29 kilometres from the volcano, and saw a cloud rising from Mount Vesuvius 'like an umbrella pine' — a towering column that spread out flat at the top. It was the first volcanic eruption anyone had ever described in writing, and Pliny's two letters about it, written to the historian Tacitus about 25 years later, are still the only eyewitness account that survives. His uncle, Pliny the Elder — admiral of the Roman fleet, author of 37 books on the natural world — sailed toward the eruption to rescue people, after a message came from a woman named Rectina, trapped at the foot of the mountain. He never came back; he died at Stabiae, across the bay.",
  "Over Pompeii, the wind carried the cloud straight overhead. Pumice — light volcanic rock — rained down for hours, piling up until roofs caved in. Then, in the early morning of the next day, the eruption changed: superheated surges of gas and ash, hundreds of degrees hot, swept down the mountain and through the streets. A 2010 study found that being caught in such a flow, even 10 kilometres from the volcano, could kill instantly, even inside a building. By the time it was over, Pompeii lay under 4 to 6 metres of ash and pumice, and Herculaneum, to the west, under about 20 metres. Pompeii had been a wealthy city of perhaps 10,000 to 20,000 people. The remains of over 1,500 people have been found at Pompeii and Herculaneum; estimates of the total dead run from 1,500 to as high as 16,000, and the true number will never be known — many escaped, and many bodies are still buried.",
  "The city then vanished for nearly 1,700 years. Herculaneum was rediscovered in 1738; excavations at Pompeii began on 23 March 1748, and the ruins were only identified as Pompeii in 1763. What the diggers found was extraordinary: a whole Roman town, preserved almost as it stood — bread still in the ovens, election posters on the walls, fast-food counters on the street corners. About a third of the city is still unexcavated today. The most famous finds were the victims themselves. As bodies decayed inside the hardened ash, they left perfect hollow cavities; in 1863 the archaeologist Giuseppe Fiorelli realised he could pour liquid plaster into them and recover the shape of the person who had died there. A little over a hundred casts were made — 104 in total — and for a century and a half, everyone who looked at them told stories about them: here a mother clutching her child, there two sisters dying in each other's arms, there a family of four, huddled together.",
  "In November 2024, the stories fell apart. An international team — Harvard Medical School, the University of Florence, and the Max Planck Institute for Evolutionary Anthropology — published DNA from the casts in Current Biology. During the restoration of 86 damaged casts in 2015, researchers had collected bone fragments mixed into the plaster from 14 of them; five yielded full or partial genomes. The adult wearing a golden bracelet, holding a child on their lap — long exhibited as a mother and her child — was genetically male, and biologically unrelated to the child. The four people found together in the House of the Golden Bracelet, long assumed to be a family, were all male and unrelated to one another (three were tested; the fourth could not be analysed). The two figures lying in an embrace, long called the 'Two Maidens' and thought to be sisters, or a mother and daughter — at least one of them was male. The DNA also showed something bigger: the victims' ancestry came mainly from recent immigrants from the eastern Mediterranean, a reminder that Pompeii was a cosmopolitan port city, not a closed little town. Two years earlier, in 2022, scientists had sequenced the first full genome of a single Pompeii victim — a man of about 35 from the House of the Blacksmith — proving the DNA could survive at all.",
  "And the date on the tombstone is argued over too. The traditional date, 24 August AD 79, comes from Pliny's letters — and 95 per cent of the surviving manuscript copies agree on it, including the oldest, from the 9th century. But in 2018, archaeologists found a charcoal inscription in the House of the Garden reading 'XVI K NOV' — 17 October — and pointed to autumn fruits buried in the ash: pomegranates, figs, walnuts, chestnuts. For a while, many came to prefer 24 October. Then the argument turned again: in 2023 researchers wrote the same charcoal message on the same wall, and ten months later it was still intact — charcoal is not as fragile as the October case assumed, so the inscription could be from a year earlier. A 2022 book by the classicist Pedar Foss showed that every date except 24 August has no basis in the manuscript tradition at all, and the park now states that all dates outside August 24 are pure invention. But as the park's own director, Gabriel Zuchtriegel, has pointed out, that does not settle it either: Pliny himself could have been wrong. The manuscript says 24 August. Whether the volcano agrees is still, honestly, open."],
 "Pompeii is a city frozen in time — a perfect snapshot of Roman life on a single day in AD 79, with the victims' families exactly as the plaster casts show them: mothers clutching children, sisters dying in each other's arms, a family of four huddled together.",
 "The snapshot is real, but the family stories were our invention. DNA from the casts shows the 'mother' was a man, the 'family of four' were unrelated men, and the 'sisters' included a man — the poses were read through modern eyes, not Roman ones. Even the date is a manuscript reading, not a certainty, and a third of the city is still underground. Pompeii is a snapshot, but the captions were written by us, not by the Romans.",
 ["Vesuvius erupted in AD 79 and buried Pompeii under 4–6 m of ash and pumice; the eruption type is named Plinian, after Pliny's account.",
  "More than 1,500 victims' remains have been found at Pompeii and Herculaneum; 104 plaster casts were made from the voids left by decayed bodies.",
  "DNA from five casts (Current Biology, 7 Nov 2024) contradicts the traditional family stories: the 'mother and child' were an unrelated adult male and child, the presumed family of four were unrelated men, and the embracing pair included a man.",
  "Pompeiians' ancestry was mainly recent eastern Mediterranean immigrants — a cosmopolitan Roman port city.",
  "Pliny the Younger's two letters to Tacitus are the only surviving eyewitness account of the eruption."],
 ["That the casts show real families — the relationships were assigned by modern viewers, and DNA contradicts them.",
  "That the eruption happened on 24 August — that is the date in 95% of Pliny's manuscripts, but the 2018 charcoal inscription and the autumn finds keep an autumn date alive, and Pliny himself could have been wrong.",
  "An exact death toll — estimates run from 1,500 to 16,000.",
  "That the city was 'frozen' unchanged — it had been damaged by an earthquake in AD 62 and was still being repaired, and about a third of it remains unexcavated."],
 [["AD 62", "A major earthquake damages Pompeii; repairs are still under way 17 years later."],
  ["24 Aug AD 79 (traditional date)", "Vesuvius erupts; Pliny the Younger watches from Misenum; his uncle sails to the rescue and dies at Stabiae."],
  ["Into the next day, AD 79", "Pyroclastic surges sweep Pompeii; the city is buried under 4–6 m of ash and pumice."],
  ["1738", "Herculaneum rediscovered."],
  ["23 Mar 1748", "Excavations begin at Pompeii; the ruins are only identified as Pompeii in 1763."],
  ["1863", "Giuseppe Fiorelli pours the first plaster casts."],
  ["2015", "Restoration of 86 casts; CT scans show none holds a complete skeleton."],
  ["2018", "Charcoal inscription dated 17 October found in the House of the Garden — the date debate reignites."],
  ["2022", "First full genome sequenced from a single Pompeii victim (Scientific Reports)."],
  ["7 Nov 2024", "Ancient DNA from the casts published in Current Biology — the family stories are wrong."],
  ["Aug–Dec 2024", "A charcoal test and the park director's study push back: the October date rests on shaky ground — though Pliny himself could still have been wrong."]],
 [["Eruption of Mount Vesuvius in AD 79 (overview and references)", "http://en.wikipedia.org/wiki/Eruption_of_Mount_Vesuvius_in_AD_79"],
  ["Pilli et al., 'Ancient DNA challenges prevailing interpretations of the Pompeii plaster casts', Current Biology (2024)", "https://www.cell.com/current-biology/fulltext/S0960-9822(24)01361-7"],
  ["Harvard Medical School — Ancient DNA challenges stories told about Pompeii victims", "https://hms.harvard.edu/news/ancient-dna-challenges-stories-told-about-pompeii-victims?sfnsn=mo"],
  ["HISTORY — Why the date of Pompeii's destruction is still debated", "https://www.history.com/articles/pompeii-vesuvius-destruction-date"],
  ["National Geographic — When did Mount Vesuvius erupt? Experts can't seem to agree", "https://www.nationalgeographic.com/history/article/mount-vesuvius-eruption-pompeii"],
  ["BBC Science Focus — Pompeii disaster victims aren't who we think they are", "https://www.sciencefocus.com/planet-earth/dna-challenges-pompeii-assumptions"],
  ["Pompeii's Forum with Vesuvius (photo, Qfl247 via Wikimedia Commons)", "https://commons.wikimedia.org/wiki/File:Pompeii%26Vesuvius.JPG"]],
 [W("The Last Morning in Pompeii (Told in Stone)", "Last Morning in Pompeii Told in Stone", "https://www.youtube.com/watch?v=zMo7RpU9inA"),
  W("The Victims of Vesuvius (Told in Stone)", "Victims of Vesuvius Told in Stone Pompeii", "https://www.youtube.com/watch?v=1j8Ir2aRoHM"),
  W("I Witnessed the Vesuvius Eruption (Pompeii, 79 AD)", "Vesuvius eruption Pompeii eyewitness Pliny", "https://www.youtube.com/watch?v=7Bbu7xNMM5w"),
  P("Pompeii podcasts", "Pompeii Vesuvius eruption 79 AD")])

# ---------------- DAILY: 7 NOV 2026 ----------------
add("earhart", "Amelia Earhart, 1937: The Pilot Who Vanished Over the Pacific — and the Clues That Keep Dissolving",
 "She was the most famous pilot alive, 7,000 miles from finishing a flight around the world, when her voice faded out over a speck of island in the Pacific. Eighty-nine years later the bones, the sonar pictures, and the satellite shapes have all promised an answer — and every one of them has dissolved on a closer look.",
 "History", "2 July 1937 · the search goes on, 2026",
 ["Amelia Mary Earhart was born on 24 July 1897 in Atchison, Kansas, and by 1937 she was the most famous pilot in the world. On 20–21 May 1932 she became the first woman — and only the second person after Charles Lindbergh — to fly solo across the Atlantic, leaving Harbor Grace, Newfoundland, and landing about 15 hours and 2,026 miles later in a field near Londonderry, Northern Ireland. A few months later she became the first woman to fly solo across the United States, Los Angeles to Newark in 19 hours and 5 minutes. On 11–12 January 1935 she became the first person to fly solo from Hawaii to the US mainland, Honolulu to Oakland. She was 39, and the world flight was meant to be the capstone: the first circumnavigation of the globe near the equator.",
  "The flight nearly ended before it began. The first attempt, westbound from Oakland, crashed on take-off at Luke Field, Honolulu, on 20 March 1937, and the Lockheed Electra 10E Special — registration NR16020, financed through the Purdue Research Foundation — had to be rebuilt. The second attempt set off eastbound from Oakland on 1 June 1937, with the experienced navigator Fred Noonan beside her. By the start of July they had flown about 22,000 miles, with about 7,000 left to go. The next leg was the hardest one of the whole trip: 2,556 miles over open ocean from Lae, New Guinea, to Howland Island, a flat coral atoll less than two miles long and under a mile wide — a speck to find from the air. The US Coast Guard cutter Itasca was stationed off Howland to talk them in.",
  "They left Lae at 10:00 a.m. local time on 2 July. The Itasca began hearing Earhart in the early morning, but the radio link was one-way in practice: she could transmit, but she seems never to have heard the ship's replies, and neither she nor Noonan could work Morse code. At 7:42 a.m. Howland time her voice came through, urgent: 'We must be on you, but we cannot see you. Gas is running low. Have been unable to reach you by radio. We are flying at 1,000 feet.' At 8:43 a.m. came the last message the Itasca ever logged, at full strength: 'We are on the line 157 337, will repeat this message, we will repeat this on 6210 kilocycles, wait.' The line 157–337 was a line of position from a sun sight, running north-north-west to south-south-east straight through Howland — a line, not a place. It said where they believed they were, but not whether they were north or south of the island. Then nothing. The Itasca kept transmitting and listening for hours. No confirmed message from Earhart was ever heard again.",
  "The official search ran for about 16 days and covered roughly 250,000 square miles of ocean before it was called off. Earhart and Noonan were declared lost at sea on 19 July 1937, and on 5 January 1939 a Los Angeles court declared Earhart legally dead at her husband George Putnam's request. The US government's conclusion, then and now, is the simplest one: the Electra ran out of fuel and went into the sea near Howland, and the plane sank in water thousands of feet deep. No wreckage has ever been confirmed — not a piece of the Electra, not a body, not a single serial-numbered part.",
  "That is where the other stories begin. The strongest rival is the castaway theory: that Earhart and Noonan flew on past Howland, south-east along the 157–337 line, and landed on the reef of Nikumaroro — then Gardner Island — about 350 miles from Howland, and died there. In April 1940 a British party found 13 human bones under a tree on the island, along with a woman's shoe, a sextant box made around 1918, a Benedictine bottle, and campfire remains. The bones were sent to Fiji, where a doctor measured them and called them a stocky European man — and then the bones were lost. In 2018, forensic anthropologist Richard Jantz of the University of Tennessee re-ran the surviving measurements through modern software and concluded the bones were more likely a woman of Earhart's height, more similar to her than to 99 per cent of a large reference sample. But the reanalysis is argued, not settled: a 2015 study had defended the original examiner's methods, and without the bones themselves the argument runs on four skull measurements and three long-bone lengths. Nikumaroro has been searched more than fifteen times, and no piece of the Electra has ever been found there.",
  "The Japanese capture theory says the pair were taken prisoner and died on Saipan. Its most famous 'proof' collapsed in public: in July 2017 the History Channel aired a documentary built around a photograph supposedly showing Earhart and Noonan alive in Japanese custody — and within two days a Japanese military-history blogger found the same photograph in a travel book published in 1935, two years before the flight. The History Channel cancelled rebroadcasts. No document or witness has ever established a capture.",
  "And the newest leads keep dissolving the same way. In January 2024 the exploration company Deep Sea Vision released a sonar image of a plane-shaped object about 100 miles from Howland, more than 16,000 feet down, and the world held its breath. When the team returned in November 2024 with better imaging, the 'plane' was a natural rock formation — CEO Tony Romeo called it 'the cruelest formation ever'. In October 2026 a 17-member Purdue-backed expedition sailed to Nikumaroro to investigate the 'Taraia Object', a plane-shaped anomaly spotted in satellite images of the island's lagoon. On 19 October the team announced the result: no conclusive evidence of wreckage — the object was most likely a collection of large trees deposited along the sandspit. A month later, on 14 November 2025, the US government released 4,624 pages of Earhart records across 53 files — including the Navy search report and the last communications — but much of it had already been public, and it named no new ending. The instruments keep getting better. The answer stays exactly where it was in 1937: somewhere in the Pacific, unproven."],
 "Earhart and Noonan landed on Nikumaroro's reef and died as castaways — the bones, the woman's shoe, the sextant box, and the reports of radio signals in the days after the disappearance all point to the same island, and the 2018 forensic reanalysis says the bones found there match Earhart better than 99 per cent of people.",
 "The bones are lost — only the 1940 measurements survive, and the doctor who took them called the remains a stocky man; a 2015 study defended his methods, so the reanalysis is argued, not settled. No wreckage of the Electra has ever been found on or near Nikumaroro despite more than fifteen searches, and the official position — fuel ran out, the plane ditched and sank near Howland — fits the last radio call without needing a 350-mile detour. The Japanese capture story's best 'proof' was a photograph published two years before she vanished. And the two newest leads both dissolved: the 2024 sonar 'plane' was rocks, and the 2026 lagoon 'plane' was trees.",
 ["Earhart and Noonan vanished on 2 July 1937 on the 2,556-mile Lae–Howland leg; the last confirmed contact came at 8:43 a.m., on the 157–337 line of position, with fuel running low.",
  "Earhart was a record-breaking pilot: first woman to fly solo across the Atlantic (1932), first person to fly solo from Hawaii to the US mainland (1935).",
  "Bones, a woman's shoe, and a 1918 sextant box were found on Nikumaroro in 1940; the bones are lost and only the 1940 measurements survive.",
  "The 2024 sonar shape near Howland was a natural rock formation; the 2026 lagoon object on Nikumaroro was most likely trees.",
  "The US government released 4,624 pages of Earhart records in November 2025 — including the Navy search report and the last communications."],
 ["That the Nikumaroro bones were Earhart's — the 2018 reanalysis is contested, and the bones themselves are gone.",
  "That she was captured by the Japanese — the famous 2017 photograph was published in 1935, two years before the flight.",
  "That any sonar or satellite shape is the Electra — the two most recent 'finds' turned out to be rocks and trees.",
  "Where the plane is — no wreckage of the Electra has ever been confirmed, anywhere."],
 [["24 Jul 1897", "Amelia Mary Earhart born in Atchison, Kansas."],
  ["20–21 May 1932", "First woman to fly solo across the Atlantic — Harbor Grace to near Londonderry, about 15 hours."],
  ["11–12 Jan 1935", "First person to fly solo from Hawaii to the US mainland — Honolulu to Oakland."],
  ["20 Mar 1937", "First world-flight attempt ends in a take-off crash at Luke Field, Honolulu."],
  ["1 Jun 1937", "Second attempt begins from Oakland, eastbound, with navigator Fred Noonan."],
  ["2 Jul 1937, 10:00 a.m. Lae", "Depart Lae for Howland, 2,556 miles; at 8:43 a.m. the last message: 'on the line 157 337', fuel low. Then silence."],
  ["19 Jul 1937", "Official search called off after about 16 days and ~250,000 square miles; declared lost at sea."],
  ["5 Jan 1939", "Declared legally dead by a Los Angeles court."],
  ["Apr 1940", "Bones, a woman's shoe, and a 1918 sextant box found on Nikumaroro (then Gardner Island)."],
  ["Jul 2017", "History Channel's 'Lost Evidence' photograph debunked within days — it was published in 1935."],
  ["Mar 2018", "Jantz reanalysis: the lost bones match Earhart better than 99% of a reference sample — contested."],
  ["Jan–Nov 2024", "Deep Sea Vision's sonar 'plane' near Howland turns out to be a rock formation."],
  ["14 Nov 2025", "4,624 pages of Earhart records declassified and released by the National Archives."],
  ["Oct 2026", "Purdue-backed expedition to Nikumaroro: the 'Taraia Object' in the lagoon was most likely trees."]],
 [["Smithsonian — Earhart's Atlantic medal and record flights", "https://www.si.edu/object/medal-amelia-earhart-first-woman-cross-atlantic-solo:nasm_A19950880000"],
  ["Purdue University — Amelia Earhart biographical sketch", "https://collections.lib.purdue.edu/aearhart/biography.php"],
  ["First Flight Centennial — What Happened to Amelia Earhart? Evidence and Theories", "https://www.firstflightcentennial.org/amelia-earhart-disappearance/"],
  ["Phys.org — New forensic analysis indicates bones were Amelia Earhart's (Jantz, 2018)", "https://phys.org/news/2018-03-forensic-analysis-bones-amelia-earhart.pdf"],
  ["Flying Magazine — History Channel's Amelia Earhart story quickly unravels", "http://www.flyingmag.com/history-channels-amelia-earhart-story-quickly-unravels?src=SOC&dom=fb"],
  ["Military.com — Earhart's plane may be closer to discovery after 89 years (Taraia expedition; Deep Sea Vision rocks)", "https://www.military.com/amelia-earharts-plane-may-be-closer-to-discovery-after-89-years"],
  ["Daily Caller — ODNI launches release of Amelia Earhart records", "https://dailycaller.com/2025/11/14/odni-releases-amelia-earhart-records-tulsi-gabbard/"],
  ["'The object was trees' — the 2026 Nikumaroro expedition outcome", "https://nim.aesv.io/essays/the-object-was-trees.html"],
  ["Earhart photo (Underwood & Underwood, public domain, via Wikimedia Commons)", "https://commons.wikimedia.org/wiki/File:Amelia_Earhart_standing_under_nose_of_her_Lockheed_Model_10-E_Electra.jpg"]],
 [W("Amelia Earhart: The Declaration of a Disappearance (Landmark Court Cases)", "Amelia Earhart declared dead court case", "https://www.youtube.com/watch?v=7U1MQckjUyQ"),
  W("Amelia Earhart's last flight, explained", "Amelia Earhart disappearance documentary"),
  W("The Nikumaroro bones and the castaway theory", "Amelia Earhart Nikumaroro bones TIGHAR"),
  P("Earhart mystery podcasts", "Amelia Earhart disappearance mystery")])

add("sphinx", "The Great Sphinx of Giza: A Lion With a King's Face — and the 4,500-Year Argument About When It Was Built",
 "It is the oldest monumental sculpture in Egypt, about as long as a jumbo jet, and it guards the pyramids — or is it older than the pyramids? One geologist says rain-marks on its walls prove it was carved thousands of years before Egypt itself. Egyptologists say the stones say otherwise.",
 "Contested", "CONTESTED — mainstream date c. 2558–2532 BC",
 ["On the edge of the desert west of Cairo, a lion the size of a jumbo jet crouches in the sand with the head of a king. The Great Sphinx of Giza is about 73 metres long from paw to tail, 20 metres high from base to crown, and 19 metres wide across its haunches — the face alone is about 4 metres wide. It was not built from blocks like a temple. It was carved straight out of the limestone bedrock of the Giza plateau, the lion's body still sitting in the ditch its makers quarried around it, its face turned east to meet the rising sun. It is the oldest known monumental sculpture in Egypt, and it watches over the pyramids of Khufu, Khafre, and Menkaure. And after 4,500 years, nobody can prove who ordered it built, whose face it wears, or exactly when it was carved.",
  "The mainstream answer is Pharaoh Khafre. Most Egyptologists date the Sphinx to his reign, about 2558–2532 BC, in the Fourth Dynasty of the Old Kingdom. The case is built from the ground, not from a text: the Sphinx sits at the foot of Khafre's causeway, beside his Valley Temple, and was cut from the same quarry that supplied the temple's stone. The Sphinx Temple in front of it was built with blocks from that same quarry, and the statue's face is usually read as Khafre's own. But even inside the mainstream, the 'who' is argued: the Egyptologist Rainer Stadelmann argued the face is Khufu, builder of the Great Pyramid, and Vassil Dobrev has argued for Khafre's brother Djedefre, who may have built it as a monument to their father Khufu. What the mainstream agrees on is the 'when' — roughly 4,500 years ago, in the age of the pyramids.",
  "The Sphinx is also a catalogue of damage. Its nose is missing, and the famous story — that Napoleon's soldiers shot it off with a cannon in 1798 — is simply wrong: a drawing made by the Danish explorer Frederic Louis Norden in 1737 already shows the Sphinx without a nose, more than sixty years before Napoleon arrived. The 15th-century historian al-Maqrizi blamed a Sufi named Muhammad Sa'im al-Dahr, who he said defaced the statue in 1378 after finding peasants leaving offerings to it — though the exact date has never been proven, and other scholars place the damage centuries earlier. The beard has fallen too; pieces of it sit in the British Museum and in Cairo. Traces of pigment suggest the whole statue was once painted, and small votive sphinxes found nearby were painted red, the traditional colour. For most of its life the Sphinx was buried up to its neck in sand — which, ironically, is what saved it. Around 1400 BC the young prince Thutmose fell asleep in its shadow and dreamed the Sphinx promised him the throne if he cleared the sand away; he did, became Thutmose IV, and set up the Dream Stele, a granite slab about 3.6 metres tall, between the paws to tell the story. In modern times Giovanni Battista Caviglia cleared the chest in 1817, and the French engineer Émile Baraize spent 1925 to 1936 digging the whole body out — the first time it had been fully visible in centuries.",
  "In 1991, a Boston University geologist named Robert Schoch walked into the argument and moved the date by thousands of years. Working with the independent Egyptologist John Anthony West, Schoch presented a paper at the Geological Society of America's meeting in San Diego arguing that the deep, rounded, vertical weathering on the walls of the Sphinx enclosure — and on the body of the statue itself — was the signature of prolonged heavy rainfall, not wind and sand. Egypt has been hyper-arid for the past 5,000 years, so Schoch argued the carving had to predate the desert: his estimate put the original carving of the core body at 7,000–5,000 BC, with the head recarved and the rump finished later, probably in Khafre's time. Seismic surveys by the geophysicist Thomas Dobecki in 1992, measuring how deep the weathering went, supported an older date and reported cavities under the Sphinx. West went further, tying the Sphinx to about 10,500 BC. In 1993 NBC aired 'The Mystery of the Sphinx', hosted by Charlton Heston, and the old-lion theory went worldwide. The American psychic Edgar Cayce had added a stranger claim decades earlier: a 'Hall of Records' — a library of a lost civilisation — hidden under the Sphinx's paws. Nothing excavated has ever confirmed it.",
  "The pushback has been just as long-running. The archaeologist Mark Lehner, who mapped the Sphinx stone by stone between 1979 and 1983, argues from the order the site was built: the Sphinx, its temple, and the enclosure were quarried and laid out as one project with Khafre's complex, and the sequence of construction does not allow a date older than Khafre's reign. Other archaeologists and geologists have challenged the rainfall reading itself, arguing the same wear can come from wind, sand, salt, and water pooling in the ditch — and the statue spent most of its life buried in sand up to its neck, which would have shielded it from the very rain the theory needs. A middle position exists too: the geologist Colin Reader, reading the same walls, puts the Sphinx a few centuries before Khafre, around 3000 BC — older than the textbooks, but not thousands of years older. And the deeper problem for the old-Sphinx case is the missing civilisation: a culture carving a 73-metre statue in 7000 BC would have left tools, settlements, and tombs across Egypt, and none have been found. The Sphinx keeps its secret: the oldest statue in Egypt still will not say who made it, or when."],
 "The Sphinx is far older than the pyramids beside it — carved between 7,000 and 5,000 BC, or even around 10,500 BC, by a lost pre-dynastic civilisation. The rain-marks on its enclosure walls prove it: the Sahara has been dry for 5,000 years, so the weathering had to happen before the desert. Khafre only restored it, and a Hall of Records may still lie beneath its paws.",
 "Mainstream Egyptology and geology reject the redating. Lehner's stone-by-stone mapping shows the Sphinx, its temple, and its enclosure were quarried and built as one project with Khafre's pyramid complex, in an order that leaves no room for a pre-Khafre date. Other geologists dispute that the weathering requires rainfall at all — wind, sand, salt, and water pooling in the ditch can make the same patterns, and the statue spent most of its life buried in sand. No trace of a pre-dynastic culture capable of carving a 73-metre statue has ever been found at Giza, and the seismic 'cavities' under the Sphinx have never been excavated or confirmed. Even the mainstream does not agree on whose face it is — but it agrees on roughly when it was made.",
 ["The Sphinx is 73 m long, 20 m high, and 19 m wide, carved from the bedrock of the Giza plateau — the oldest known monumental sculpture in Egypt.",
  "No Old Kingdom inscription names its builder, its face, or its purpose.",
  "The Dream Stele (c. 1400 BC) proves the Sphinx was already ancient and worshipped as Horemakhet, 'Horus of the Horizon', more than 3,000 years ago.",
  "Its nose was deliberately removed centuries before Napoleon — a 1737 drawing already shows it missing.",
  "The deep, rounded weathering on the enclosure walls is real, and geologists still disagree about what caused it."],
 ["That the Sphinx is 7,000–5,000 BC old — the rainfall reading of the weathering is disputed by other geologists and by the site's archaeology.",
  "That Khafre — or Khufu, or Djedefre — is definitely the face; even mainstream Egyptologists disagree.",
  "That a Hall of Records or hidden chamber lies beneath it — seismic anomalies have never been excavated.",
  "That Napoleon's soldiers shot the nose off — drawings from 1737 predate his 1798 campaign by 61 years."],
 [["c. 2558–2532 BC", "Mainstream date: the Sphinx is carved in the reign of Pharaoh Khafre (some argue Khufu or Djedefre)."],
  ["c. 1400 BC", "Thutmose IV clears the sand and sets up the Dream Stele between the paws."],
  ["1378", "The historian al-Maqrizi says the Sufi Muhammad Sa'im al-Dahr defaced the Sphinx — the exact date is unproven."],
  ["1737", "Frederic Louis Norden's drawing already shows the Sphinx without a nose — 61 years before Napoleon."],
  ["1817", "Giovanni Battista Caviglia clears the Sphinx's chest."],
  ["1925–1936", "Émile Baraize clears the whole body; the Sphinx is fully visible for the first time in centuries."],
  ["1979–1983", "Mark Lehner maps the Sphinx stone by stone."],
  ["1991", "Schoch and West present the water-erosion redating at the Geological Society of America, San Diego."],
  ["1992", "Dobecki's seismic survey finds deeper weathering and reports cavities under the Sphinx."],
  ["1993", "NBC airs 'The Mystery of the Sphinx', hosted by Charlton Heston."],
  ["2026", "The argument continues: mainstream Egyptology still dates the Sphinx to Khafre, and no excavation has settled it."]],
 [["Encyclopaedia Britannica — Great Sphinx of Giza", "https://www.britannica.com/topic/Great-Sphinx"],
  ["Wikipedia — Great Sphinx of Giza", "https://en.wikipedia.org/wiki/Great_Sphinx_of_Giza"],
  ["World History Encyclopedia — The Great Sphinx of Giza", "https://www.worldhistory.org/Great_Sphinx_of_Giza/"],
  ["Chronicle of Higher Education — Study Suggests Sphinx Is Thousands of Years Older Than Believed (1991)", "https://www.chronicle.com/article/study-suggests-sphinx-is-thousands-of-years-older-than-believed/"],
  ["Boston University — Robert M. Schoch profile", "https://www.bu.edu/prsocial/profile/robert-m-schoch/"],
  ["Robert M. Schoch — Erosion Processes on the Great Sphinx and Its Dating (his own paper)", "https://SaturnianCosmology.org/files/sphinx/schoch.htm.txt"],
  ["Mark Lehner — Archaeology of an Image: The Great Sphinx of Giza (1991, full text)", "https://archive.org/stream/ArchaeologyOfAnImage/Archaeology-of-an-Image_djvu.txt"],
  ["Sphinx photo (MusikAnimal, May 2015, CC BY-SA 3.0, via Wikimedia Commons)", "https://commons.wikimedia.org/wiki/File:Great_Sphinx_of_Giza_May_2015.JPG"]],
 [W("Secrets: The Sphinx — FULL EPISODE (Smithsonian Channel)", "Secrets Sphinx Smithsonian Channel full episode", "https://www.youtube.com/watch?v=VTkbi28ocBY"),
  W("The Great Sphinx: Who Carved It, and When? — both sides in one film", "Great Sphinx who carved it and when documentary", "https://www.youtube.com/watch?v=23-JZLys2UY"),
  W("Mystery of the Sphinx (1993), hosted by Charlton Heston", "Mystery of the Sphinx 1993 Charlton Heston", "https://www.youtube.com/watch?v=SbUsGnMUH2Y"),
  P("Egyptology podcasts", "Great Sphinx of Giza Egyptology")])

# ---------------- HTML GENERATION ----------------
def esc(s):
    return html.escape(str(s), quote=True)
def paras(ps):
    return "".join("<p>%s</p>" % esc(p) for p in ps)
def lis(items):
    return "".join("<li>%s</li>" % esc(i) for i in items)
def srcs(items):
    out = []
    for label, url in items:
        out.append('<li><a href="%s" target="_blank" rel="noopener">%s</a></li>' % (esc(url), esc(label)))
    return "".join(out)
def watch(items):
    out = []
    for label, url, kind in items:
        tag = "▶ video" if kind == "video" else ("🔎 search" if kind == "search" else "🔗 link")
        out.append('<li><a href="%s" target="_blank" rel="noopener">%s</a> <span class="kind">%s</span></li>' % (esc(url), esc(label), tag))
    return "".join(out)

cats = [("All", "all"), ("History", "History"), ("Deep Past", "Deep Past"), ("Rogan Science", "Rogan Science"), ("Contested", "Contested")]
cards = []
for a in A:
    flags = ""
    if "CONTESTED" in a["date"]:
        flags = '<span class="flag bad">⚠ CONTESTED</span>'
    elif "INDEPENDENT" in a["date"]:
        flags = '<span class="flag">INDEPENDENT RESEARCHER</span>'
    elif "FINANCIAL STAKE" in a["date"]:
        flags = '<span class="flag bad">⚠ FINANCIAL STAKE</span>'
    _cats = a["cat"] + (" Contested" if "CONTESTED" in a["date"] else "")
    teaser = a["dek"] if a["dek"] else (a["body"][0] if a["body"] else "")
    cards.append(
      '<article class="card" data-cats="%s" data-title="%s" onclick="openArt(\'%s\')">'
      '%s<div class="card-body"><div class="kicker">%s · %s</div><h2>%s</h2><p>%s</p><div class="tagrow">%s<span class="tag">◈ Both sides inside · ▶ Watch / Listen</span></div></div></article>'
      % (esc(a["cat"]), esc(a["title"].lower() + " " + teaser.lower()), esc(a["id"]), card_media(a),
         esc(a["cat"]), esc(a["date"]), esc(a["title"]), esc(teaser), flags))

readers = []
index_items = []
for a in A:
    readers.append(
      '<section class="reader" id="art-%s"><button class="back" onclick="goHome()">← Back to the front page</button>'
      '<div class="kicker">%s · %s</div><h1>%s</h1><p class="dek">%s</p>%s%s'
      '<h3>⚖️ Both sides — you decide</h3><div class="both"><div class="claim"><h3>◈ The claim, at full strength</h3><p>%s</p></div>'
      '<div class="push"><h3>◈ The pushback</h3><p>%s</p></div><div class="vs">VS</div></div>'
      '<div class="body">%s</div>'
      '<div class="boxes"><div><h3>✓ What it proves</h3><ul>%s</ul></div><div><h3>✗ What it doesn\'t prove</h3><ul>%s</ul></div></div>'
      '<h3>Timeline</h3><ul class="tl">%s</ul>'
      '<h3>Sources</h3><ul class="sources">%s</ul>'
      '<h3>▶ Watch / Listen</h3><ul class="watch">%s</ul></section>'
      % (esc(a["id"]), esc(a["cat"]), esc(a["date"]), esc(a["title"]), esc(a["dek"]), hero_media(a), visual_block(a),
         esc(a["claim"]), esc(a["pushback"]), paras(a["body"]), lis(a["proves"]), lis(a["notproves"]),
         "".join("<li><b>%s</b> — %s</li>" % (esc(y), esc(t)) for y, t in a["timeline"]),
         srcs(a["sources"]), watch(a["watch"])))
    for label, url in a["sources"]:
        index_items.append('<li><b>%s:</b> <a href="%s" target="_blank" rel="noopener">%s</a></li>' % (esc(a["title"]), esc(url), esc(label)))

data_json = json.dumps(A)
html_doc = """<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>The Scout Ledger — History, Ancient World &amp; Rogan Science</title>
<style>
*{box-sizing:border-box}
:root{--ink:#17202a;--muted:#5b6b7c;--paper:#fffdf7;--red:#e11d48;--teal:#0d9488;--amber:#f59e0b;--violet:#7c3aed;--line:#e5e0d5}
body{font-family:system-ui,-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;background:#f4f1ea;color:var(--ink);margin:0;line-height:1.6}
a{color:#0e7490}
.masthead{background:linear-gradient(120deg,#0f172a,#7c3aed 55%,#e11d48);color:#fff;padding:10px 18px 26px;text-align:center}
.masthead .topbar{display:flex;justify-content:space-between;align-items:center;max-width:1180px;margin:0 auto;font-weight:700;letter-spacing:.08em;text-transform:uppercase;font-size:13px}
.masthead h1{font-family:Georgia,serif;font-size:clamp(2.4rem,7vw,4.4rem);margin:6px 0 4px;letter-spacing:.01em}
.masthead p{margin:0 auto;max-width:760px;opacity:.95;font-size:clamp(1rem,2.4vw,1.2rem)}
.masthead .how{background:rgba(255,255,255,.16);border:1px solid rgba(255,255,255,.35);border-radius:14px;padding:12px 16px;margin:16px auto 0;max-width:900px;font-size:.95rem;text-align:left}
nav{position:sticky;top:0;background:#fff;border-bottom:2px solid var(--line);padding:10px 14px;display:flex;gap:8px;flex-wrap:wrap;justify-content:center;z-index:5;box-shadow:0 2px 12px rgba(0,0,0,.06)}
nav button{font:700 15px system-ui,sans-serif;padding:8px 14px;border:2px solid #e5e0d5;border-radius:999px;background:#fff;cursor:pointer}
nav button.on{background:var(--ink);color:#fff;border-color:var(--ink)}
nav input{font-size:15px;padding:8px 14px;border:2px solid #e5e0d5;border-radius:999px;min-width:220px}
main{max-width:1180px;margin:0 auto;padding:20px 16px}
.adventure{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:12px;margin:6px 0 22px}
.adv{border-radius:16px;padding:16px;color:#fff;cursor:pointer;border:0;text-align:left;font:inherit}
.adv b{display:block;font-size:1.15rem}.adv span{opacity:.9;font-size:.92rem}
.hero{display:grid;grid-template-columns:1.1fr .9fr;gap:0;border-radius:22px;overflow:hidden;background:#fff;box-shadow:0 12px 30px rgba(0,0,0,.12);margin-bottom:26px;cursor:pointer;border:1px solid var(--line)}
.hero-text{padding:26px 28px}.hero-text .badge{background:#fef3c7;color:#92400e;font-weight:800;padding:5px 10px;border-radius:999px;font-size:.8rem;letter-spacing:.06em;text-transform:uppercase}
.hero-text h2{font-family:Georgia,serif;font-size:clamp(1.7rem,3.6vw,2.6rem);line-height:1.15;margin:14px 0 8px}
.hero-text p{color:var(--muted);font-size:1.08rem}
.hero-img{margin:0;display:flex;flex-direction:column}.hero-img img{width:100%;flex:1;min-height:260px;object-fit:cover;display:block}
.hero-img figcaption{font-size:.78rem;color:var(--muted);padding:6px 10px;background:#fff}
.cta{display:inline-block;background:var(--red);color:#fff;font-weight:800;padding:10px 18px;border-radius:999px;margin-top:8px}
h2.sec{font-family:Georgia,serif;font-size:1.7rem;margin:26px 0 12px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(290px,1fr));gap:18px}
.card{border:1px solid var(--line);background:#fff;border-radius:18px;overflow:hidden;cursor:pointer;box-shadow:0 3px 10px rgba(0,0,0,.05);display:flex;flex-direction:column}
.card:hover{transform:translateY(-3px);box-shadow:0 12px 24px rgba(0,0,0,.12)}
.media{aspect-ratio:16/10;overflow:hidden;position:relative;background:#e5e7eb}
.media img{width:100%;height:100%;object-fit:cover;display:block}
.media .credit{position:absolute;left:0;right:0;bottom:0;background:linear-gradient(transparent,rgba(0,0,0,.75));color:#fff;font-size:.72rem;padding:18px 10px 6px}
.media.tile{display:flex;flex-direction:column;align-items:center;justify-content:center;gap:4px;color:#fff}
.tile-emoji{font-size:44px}.tile-init{font-family:Georgia,serif;font-size:64px;line-height:1}.tile-note{font-size:.75rem;opacity:.85;padding:0 18px;text-align:center}
.card-body{padding:16px 16px 18px}
.kicker{font-size:11px;letter-spacing:.12em;text-transform:uppercase;color:var(--red);font-weight:800}
.card h2{font-family:Georgia,serif;font-size:1.22rem;line-height:1.3;margin:8px 0}
.card p{color:var(--muted);margin:0}
.tag{font-size:12px;background:#f1f5f9;padding:3px 8px;border-radius:999px;display:inline-block}
.tagrow{margin-top:12px;display:flex;flex-wrap:wrap;gap:6px;align-items:center}
.flag{font-size:12px;background:var(--red);color:#fff;padding:3px 8px;border-radius:999px;font-weight:800}
.flag.bad{background:#7f1d1d}
.reader{display:none;background:#fff;border:1px solid var(--line);border-radius:20px;padding:26px;max-width:860px;margin:0 auto;box-shadow:0 10px 26px rgba(0,0,0,.08)}
.reader h1{font-family:Georgia,serif;font-size:clamp(1.7rem,4vw,2.5rem);line-height:1.2}
.dek{font-size:1.18rem;color:#334155}
.visual{background:#fffbeb;border:2px solid #fde68a;border-radius:16px;padding:16px;margin:18px 0}
.cluebar{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:10px}.cluebar span{background:#fff;border:1px solid #fde68a;border-radius:999px;padding:4px 10px;font-size:.85rem;font-weight:700}
.tl-track{display:flex;gap:10px;overflow-x:auto;padding:8px 2px 12px}
.tl-step{min-width:180px;background:#fff;border:1px solid var(--line);border-radius:12px;padding:10px;font-size:.9rem}
.tl-step .dot{display:block;width:12px;height:12px;border-radius:50%;background:var(--red);margin-bottom:6px}
.tl-step b{display:block}.tl-step span{color:var(--muted)}
.chart{margin-top:14px}.bar-row{display:grid;grid-template-columns:170px 1fr auto;gap:10px;align-items:center;margin:7px 0;font-size:.92rem}
.bar{background:#f1f5f9;border-radius:999px;height:18px;overflow:hidden}.bar i{display:block;height:100%;background:linear-gradient(90deg,#0ea5e9,#7c3aed)}
.mapbox{background:#ecfeff;border:1px solid #a5f3fc;border-radius:12px;padding:12px;margin-top:14px}
.small{font-size:.82rem;color:var(--muted)}
.both{display:grid;grid-template-columns:1fr auto 1fr;gap:12px;align-items:stretch;margin:20px 0}
@media(max-width:700px){.both{grid-template-columns:1fr}.vs{display:none}}
.claim{border:2px solid var(--red);border-radius:16px;padding:14px;background:#fff1f2}
.push{border:2px solid var(--teal);border-radius:16px;padding:14px;background:#f0fdfa}
.vs{align-self:center;font-weight:900;font-size:1.4rem;color:var(--ink)}
.boxes{display:grid;grid-template-columns:1fr 1fr;gap:14px}
@media(max-width:700px){.boxes{grid-template-columns:1fr}.hero{grid-template-columns:1fr}.bar-row{grid-template-columns:1fr}.bar-row b{grid-column:1}}
.boxes>div{border:1px solid var(--line);border-radius:14px;padding:14px;background:#f8fafc}
.tl li,.sources li,.watch li{margin:7px 0}
.kind{font-size:12px;color:#666}
.back{font:700 16px system-ui,sans-serif;padding:9px 16px;cursor:pointer;margin-bottom:14px;border-radius:999px;border:2px solid var(--ink);background:#fff}
footer{max-width:1180px;margin:34px auto;padding:20px 16px;border-top:3px solid var(--ink)}
footer ul{columns:2;column-gap:28px}
@media(max-width:700px){footer ul{columns:1}}
.note{background:#fff3cd;border:1px solid #d4a017;border-radius:12px;padding:12px 14px;margin:18px 0}
img{max-width:100%}
</style></head><body>
<header class="masthead"><div class="topbar"><span>🔍 The Scout Ledger</span><span>History · Ancient World · Rogan Science</span></div>
<h1>The Scout Ledger</h1><p>History, the ancient world, and the scientists Rogan has on — every story with both sides, sources, and something to watch.</p>
<p class="how"><b>🧭 How to read this paper:</b> each article states the claim at full strength beside the documented pushback. No winner is picked for you. Flags mark contested claims, independent researchers, and financial stakes. Watch links are direct videos only where verified; otherwise they are labelled searches. <b>Look at the pictures and charts first — then dive into the story.</b></p></header>
<nav id="nav">
<button data-f="all" class="on" onclick="filter('all',this)">All</button>
<button data-f="History" onclick="filter('History',this)">History</button>
<button data-f="Deep Past" onclick="filter('Deep Past',this)">Deep Past</button>
<button data-f="Rogan Science" onclick="filter('Rogan Science',this)">Rogan Science</button>
<button data-f="Contested" onclick="filter('Contested',this)">Contested</button>
<input id="q" placeholder="🔎 Search headlines…" oninput="searchArt(this.value)">
</nav>
<main id="home">
<div class="adventure">
<button class="adv" style="background:linear-gradient(135deg,#f59e0b,#ef4444)" onclick="filter('History',null)"><b>🏛️ History adventures</b><span>Big events, mysteries &amp; escapes</span></button>
<button class="adv" style="background:linear-gradient(135deg,#059669,#0ea5e9)" onclick="filter('Deep Past',null)"><b>🦴 Deep Past</b><span>Other humans, lost worlds &amp; ancient tools</span></button>
<button class="adv" style="background:linear-gradient(135deg,#7c3aed,#db2777)" onclick="filter('Rogan Science',null)"><b>🔬 Rogan Science</b><span>What Rogan's scientist guests actually say</span></button>
<button class="adv" style="background:linear-gradient(135deg,#334155,#f59e0b)" onclick="filter('Contested',null)"><b>❓ Contested corner</b><span>Wild claims — both sides, you decide</span></button>
</div>
<div class="note"><b>Today's lead story — and a note on accuracy:</b> dates, sites, and episode numbers are given only where they could be verified. Where a detail could not be verified (for example John Lisle's exact episode day, or the reported retraction of Biondi's earlier method paper), the article says so instead of guessing. Zahi Hawass's Rogan episode (May 2025) falls just before the Nov 2025–Oct 2026 window and is included by request, labelled as such.</div>
<div class="hero" onclick="openArt('sulawesi')"><div class="hero-text"><span class="badge">🔥 Today's big discovery</span>
<div class="kicker" style="margin-top:12px">Lead story · History · Nature, August 2025</div>
<h2>The Million-Year Sea Crossing: Seven Stone Tools Rewrite When Humans First Sailed</h2>
<p>Seven flakes of stone from a cornfield in Sulawesi say early human relatives crossed deep ocean water more than a million years ago — long before modern humans, and long before anyone was supposed to have a boat.</p>
<p><span class="tag">◈ Both sides inside · ▶ Watch / Listen</span> <span class="cta">Read the expedition →</span></p></div>
<figure class="hero-img"><img src="images/sulawesi.png" alt="Topographic map of Sulawesi, Indonesia"><figcaption>📸 Topographic map of Sulawesi — Wikimedia Commons</figcaption></figure></div>
<h2 class="sec">🗺️ Pick a story to explore</h2>
<div class="grid" id="grid">""" + "".join(cards) + """</div>
</main>
<div id="readers" style="max-width:1080px;margin:0 auto;padding:18px">""" + "".join(readers) + """</div>
<footer><h2>Source Index — every source, every story</h2><ul>""" + "".join(index_items) + """</ul>
<p>Direct video links are used only where copied verbatim from a verified result; other watch items are labelled searches. No quotes in this paper are invented; where a source is a guest's own site, it is linked as their own account of their work.</p></footer>
<script>
function goHome(){document.getElementById('home').style.display='block';document.querySelectorAll('.reader').forEach(function(r){r.style.display='none'});window.scrollTo(0,0)}
function openArt(id){document.getElementById('home').style.display='none';document.querySelectorAll('.reader').forEach(function(r){r.style.display='none'});var el=document.getElementById('art-'+id);if(el){el.style.display='block';window.scrollTo(0,0)}}
function filter(cat,btn){document.querySelectorAll('#nav button').forEach(function(b){b.classList.remove('on')});if(btn)btn.classList.add('on');document.querySelectorAll('.card').forEach(function(c){var cs=c.dataset.cats||'';var ok=(cat==='all'||cs===cat||cs.endsWith(' '+cat)||cs.startsWith(cat+' '));c.style.display=ok?'flex':'none'});document.getElementById('q').value=''}
function searchArt(q){q=q.toLowerCase();document.querySelectorAll('.card').forEach(function(c){c.style.display=c.dataset.title.includes(q)?'flex':'none'})}
</script></body></html>
"""
open("index.html", "w").write(html_doc)
print("articles:", len(A))
print("bytes:", len(html_doc))
