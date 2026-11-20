"""Stories of Friday 20 November 2026, each checked against the dated briefs.

Date rule: every entry is an event that happened, or was first reported, on
20 November 2026 in some time zone.  Where a source item belongs to 19 November
it is either left out or, for one line only, marked with its own date ("19 NOV").
The Nvidia subpoena (19 Nov) and the ICJ Myanmar ruling (19 Nov) are therefore
not presented as this day's news; Nvidia appears only inside the chip story that
*is* about 20 November's Asian market reaction.

Record shapes:
    heroes/panels: (region, field, headline, deck, body, colour, illo, source)
    index:         (region, field, one-line headline[, date override])
"""

STRAP = ("Each story below happened, or was first reported, on 20 November 2026 in some "
         "time zone; the three lines marked 19 NOV are the previous day. Contested claims "
         "are attributed to whoever made them, and figures are as reported, not verified.")

# ------------------------------------------------------------------ leads
HEROES = [
    ("EUROPE", "CONFLICT",
     "Russia strikes Kyiv; three Dnipro bridges reported hit",
     "At least three killed, about 15 hurt, mayor says",
     "Kyiv's mayor, Vitali Klitschko, said an overnight missile attack hit strategic "
     "infrastructure and three bridges across the Dnipro, cutting east from west. "
     "Ukrainian drones reportedly struck the Dorogobuzh chemical plant in Smolensk; "
     "the damage there is unverified.",
     "TEAL", "bridge",
     "Open Chronicle brief 20 Nov; BBC/AP, Kyiv 20 Nov; Kyiv Independent on Dorogobuzh 20 Nov"),

    ("EUROPE", "DIPLOMACY",
     "Germany rejects a new Yalta over Europe",
     "Merz: no settlement negotiated over Europe's head",
     "Chancellor Friedrich Merz said European states would not accept a deal struck by "
     "outside powers without them, invoking 1945. President Emmanuel Macron made the same "
     "point, after Trump, Xi and Putin met in Shenzhen.",
     "NAVY", "berlin",
     "Open Chronicle brief 20 Nov; European Council 20 Nov; Reuters; AFP"),

    ("ASIA", "SUMMIT",
     "Three powers sign a declaration, but no arms deal",
     "Nuclear war 'must never be fought'; no timetable",
     "After their Shenzhen summit, the US, China and Russia issued a joint declaration that "
     "nuclear war must never be fought and backing for international peace. Reported as "
     "mainly symbolic: no binding arms cuts, no timetable, no settlement in Ukraine or Iran.",
     "RED", "summit",
     "Open Chronicle brief 20 Nov; Reuters 20 Nov; Guardian"),
]

# ------------------------------------------------------------------ panels
PANELS = [
    ("EUROPE", "DIPLOMACY",
     "EU and UK hold their second summit in Brussels",
     "Costa, von der Leyen and PM Andy Burnham meet on trade, energy, "
     "security and migration; youth mobility is live.",
     "NAVY", "handshake",
     "Open Chronicle brief 20 Nov; Council of the EU programme 20 Nov"),

    ("EUROPE", "ARCTIC",
     "Denmark approves an Arctic security pact",
     "Parliament backs a deal with Greenland and the US allowing a wider "
     "American presence at Pituffik; Danish sovereignty is kept.",
     "SLATE", "arctic",
     "Open Chronicle brief 20 Nov; AP 20 Nov; Danish Folketing"),

    ("MIDEAST", "CONFLICT",
     "Iraq and Kataib Hezbollah reach a compromise",
     "Forces are expected to enter Jurf al-Sakhar as the Iran-backed "
     "militia relocates, Reuters reported, easing a standoff.",
     "OCHRE", "parliament",
     "Reuters via Open Chronicle 20 Nov; Iraqi government statement"),

    ("AFRICA", "DIPLOMACY",
     "Somalia orders the UAE ambassador out",
     "Mogadishu gave the envoy 72 hours to leave in a sovereignty dispute; "
     "the UAE rejected the charge, reports said.",
     "GREEN", "embassy",
     "Open Chronicle brief 20 Nov; AP; Al Jazeera"),

    ("ASIA", "DISASTER",
     "Cyclone Akvan comes ashore in India",
     "It came ashore on the north Andhra-south Odisha coast early on "
     "Friday, the IMD said, after evacuations. Damage is unassessed.",
     "RED", "cyclone",
     "India Meteorological Department 20 Nov; The Hindu 20 Nov 07:00 IST"),

    ("OCEANIA", "WEATHER",
     "Category 4 Cyclone Xavier watched in the South Pacific",
     "Fiji's Nadi centre reported Severe Tropical Cyclone Xavier at Category "
     "4 and forecast a change in strength and track on 20 November.",
     "TEAL", "cyclone",
     "Fiji Meteorological Service outlook; RSMC Nadi 20 Nov"),

    ("MIDEAST", "HUMANITARIAN",
     "Gaza: health authorities report 22,000 children killed",
     "Palestinian health authorities put the number of children killed "
     "above 22,000. The figure is theirs and unverified; hospitals are damaged.",
     "OCHRE", "memorial",
     "Palestinian health authorities via Open Chronicle 20 Nov; UN agencies"),

    ("AMERICAS", "POLICE",
     "Haiti police say 34 suspects killed in Martissant",
     "Police said an operation in Port-au-Prince's Martissant district killed "
     "at least 34 suspects, with no losses to civilians or police. Unconfirmed.",
     "PLUM", "shield",
     "Haitian National Police via Open Chronicle 19-20 Nov; AP"),

    ("AMERICAS", "RIGHTS",
     "Brazil advances Indigenous land rights at Chief Raoni's side",
     "Lula pressed legal recognition of Indigenous territory during a visit "
     "to the Amazon leader Chief Raoni, reports said.",
     "PLUM", "forest",
     "Open Chronicle brief 20 Nov; Agencia Brasil; Al Jazeera"),

    ("WORLD", "SCIENCE",
     "Voyager 1 passes one light-day from Earth",
     "NASA's 1977 probe is now so far out that its radio signal takes about "
     "24 hours to reach us.",
     "NAVY", "probe",
     "NASA/JPL; PBS 20 Nov; Space.com 20 Nov"),

    ("AMERICAS", "MARKETS",
     "AI doubts drag Asia lower after Anthropic's debut",
     "Seoul opened sharply lower and Asian markets weakened on doubts about "
     "AI valuations, even as Anthropic's debut rose 17pc.",
     "PLUM", "chart",
     "Korea Herald 20 Nov; Open Chronicle brief 20 Nov; The Hindu 20 Nov"),

    ("WORLD", "CULTURE",
     "GTA VI estimates pass 2 billion dollars in sales",
     "Early industry estimates put revenue above $2 billion; the publisher "
     "has not confirmed it.",
     "SLATE", "gamepad",
     "Industry estimates via Open Chronicle 20 Nov; trade press"),
]

# ------------------------------------------------------------------ index
INDEX = [
    ("ASIA", "DEFENCE", "Japan and India widen defence ties; SDF to train in India"),
    ("ASIA", "ELECTION", "Taiwan flags about 2,700 accounts it links to China"),
    ("ASIA", "ECONOMY", "China holds benchmark lending rates for an 18th month"),
    ("ASIA", "ECONOMY", "Japan core inflation 2.2pc in October, as reported"),
    ("ASIA", "HEALTH", "South Korea reports its first cholera case in about a decade"),
    ("ASIA", "SOCIETY", "Heavy snow alerts disrupt transport and daily life in South Korea"),
    ("ASIA", "ECONOMY", "Beijing to bar young 'red-chip' firms from listing abroad"),
    ("ASIA", "JUSTICE", "India's Supreme Court urges deleted voters to act before 30 Nov"),
    ("ASIA", "DIPLOMACY", "Prabowo and Xi discuss future South China Sea cooperation"),
    ("ASIA", "ECONOMY", "Financial Street Securities chairman detained on the mainland"),
    ("ASIA", "CORRUPTION", "Justice Yashwant Varma says removal case died with his resignation"),

    ("EUROPE", "PROTEST", "Cost-of-living marches expected in several European countries"),
    ("EUROPE", "SECURITY", "Poland checks unidentified objects near the Ukrainian border"),
    ("EUROPE", "POLITICS", "Sanchez is said to admit mistakes in Spain's election debate"),
    ("EUROPE", "DIPLOMACY", "Kushner: Trump open to NATO-style security guarantees for Ukraine"),

    ("MIDEAST", "CONFLICT", "Houthi missiles and drones reported intercepted over Saudi Arabia"),
    ("MIDEAST", "SHIPPING", "Tankers report mines and threats near the Strait of Hormuz"),
    ("MIDEAST", "ECONOMY", "Pentagon official puts the Iran campaign cost at $48.3bn"),
    ("MIDEAST", "CONFLICT", "Reports of further strikes and displacement in Gaza"),

    ("AFRICA", "CONFLICT", "Sudan's war drives displacement as armed loyalties shift"),
    ("AFRICA", "CONFLICT", "Sudan: allegiance changes reported among armed groups"),
    ("AFRICA", "LAW", "Nigeria moves towards ending penalties for attempted suicide"),
    ("AFRICA", "CLIMATE", "African states press COP31 for faster adaptation money"),

    ("AMERICAS", "TECH", "California subpoenas Nvidia over chips reaching China (19 NOV)"),
    ("AMERICAS", "SECURITY", "White House fires national cyber director over outages"),
    ("AMERICAS", "MINING", "US weighs deep-sea mining concessions near American Samoa"),
    ("AMERICAS", "POLITICS", "Bukele seeks a third term after El Salvador's constitution change"),
    ("AMERICAS", "POLITICS", "Colombia sees thousands protest tax plans and the US military role"),
    ("AMERICAS", "DISASTER", "Cincinnati Zoo mourns Fiona the hippo; a visitor's hat is blamed"),

    ("OCEANIA", "CLIMATE", "Pacific island states press COP31 for reliable adaptation finance"),
    ("OCEANIA", "CLIMATE", "Drought and rising seas press on Pacific freshwater supplies"),
    ("OCEANIA", "SECURITY", "Australia and Japan deepen Indo-Pacific security coordination"),

    ("WORLD", "CLIMATE", "COP31 draft drops fossil-fuel phase-out and net-zero dates"),
    ("WORLD", "CLIMATE", "The same COP31 draft drops the $120bn adaptation-finance target"),
    ("WORLD", "MARKETS", "Anthropic shares close 17pc higher on their debut (19 NOV)"),
    ("WORLD", "ECONOMY", "US approves sales of hundreds of thousands of AI chips to China"),
    ("WORLD", "MARKETS", "Global stocks slip as AI spending meets doubts about returns"),
    ("WORLD", "LAW", "Myanmar told to pay Rohingya reparations (19 NOV)"),
]

# Kicker for the masthead and the spine of numbers.
NUMBERS = []

DATE_BIG = "FRIDAY 20 NOVEMBER 2026"
KICKER = "THE DAY IN WORLD NEWS"
