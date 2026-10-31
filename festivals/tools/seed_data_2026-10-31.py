import json
CK="2026-10-31"
UKFG=("https://www.ukfestivalguides.com/news/14092026/uk-festivals-2027-which-one-fits-you-and-what-to-book-right-now/","UK Festival Guides 2027 planning guide (14 Sep 2026)","other")
SKL=("https://www.skiddle.com/festivals/","Skiddle festivals listing","agent")
def S(url,title,typ="official"): return {"source_url":url,"source_title":title,"source_type":typ,"checked":CK}
def P(value,label,src,fees=None,note="",days=None):
    d={"value":value,"label":label,"fees":fees,"note":note}; d.update(src)
    if days: d["days"]=days  # days the ticket covers, as stated in its label (used for per-day when fewer than the festival's dates)
    return d
def NA(): return None
F=[]
def add(**k): F.append(k)

g=S("https://www.glastonburyfestivals.co.uk/news/glastonbury-2027-ticket-information-confirmed/","Glastonbury: 2027 ticket information confirmed (8 Sep 2026)")
add(id="glastonbury",name="Glastonbury Festival",start="2027-06-23",end="2027-06-27",dates_src=g,
    venue="Worthy Farm, Pilton",county="Somerset",region="South West England",loc_src=S(*UKFG),
    camping="included",status="sale_held",status_note="General sale held in October 2026. The balance is due 1 to 7 April 2027; check the official site for the April resale.",
    seller="See Tickets",
    adult=P(408,"General admission, 5 days with camping",g,fees="included",note="Includes £5 booking fee. Plus £11.25 postage per order."),
    deposit="£100 per person, balance £308 due 1 to 7 April 2027",
    kids="", parking=None, campervan=None, day=None, noncamp=None, extras=[])

iow=S("https://isleofwightfestival.com/tickets/","Isle of Wight Festival: Tickets")
add(id="isle-of-wight",name="Isle of Wight Festival",start="2027-06-17",end="2027-06-20",dates_src=S("https://isleofwightfestival.com/","Isle of Wight Festival homepage"),
    venue="Seaclose Park, Newport",county="Isle of Wight",region="South East England",loc_src=S(*UKFG),
    camping="optional",status="on_sale",status_note="Page says prices correct as of 23/10/2026.",seller="Ticketmaster",
    adult=P(330,"Weekend, with or without camping",iow,fees="unknown"),
    noncamp=P(330,"Weekend, with or without camping (same price)",iow,fees="unknown"),
    kids="Older child (9-12) £45; younger child (3-8) £35; infants (2 and under) free.",
    parking=P(50,"Weekend parking bought in advance",iow,note="Includes £2 green levy."),
    campervan=P(350,"Campervan",iow,note="Sold out when checked."),
    day=None,deposit="Payment plans and Ticketmaster instalments available",extras=["Islander weekend ticket £299 for island residents."])

dl=S("https://downloadfestival.co.uk/","Download Festival homepage")
dlp=S("https://www.timeout.com/uk/news/download-festival-2027-early-bird-tickets-prices-dates-headliner-rumours-061526","Time Out: Download 2027 early bird prices","press")
add(id="download",name="Download Festival",start="2027-06-09",end="2027-06-13",dates_src=dl,
    venue="Donington Park",county="",region="East Midlands",loc_src=dl,
    camping="optional",status="on_sale",status_note="Official ticket page lists camping, non-camping and day options; prices are shown only at Ticketmaster.",seller="Ticketmaster, Big Green Coach",
    adult=P(320,"Early bird adult camping, 3 nights",dlp,fees="unknown",note="Early bird price reported by Time Out in June 2026. The tier on sale now may cost more."),
    kids="",parking=None,campervan=None,day=None,noncamp=None,deposit="PayPal Pay in 3 via Ticketmaster",
    extras=["Early bird 5-night adult camping was £330 (Time Out)."])

rd=S("https://www.readingfestival.com/tickets","Reading Festival: Tickets")
add(id="reading",name="Reading Festival",start="2027-08-26",end="2027-08-29",dates_src=S("https://www.readingfestival.com/","Reading Festival homepage"),
    venue="Richfield Avenue",county="Berkshire",region="South East England",loc_src=S("https://www.readingfestival.com/","Reading Festival homepage"),
    camping="optional",status="on_sale",status_note="1st release.",seller="Ticketmaster",
    adult=P(326,"Weekend camping (from Thursday), 1st release",rd,fees="unknown"),
    deposit="£20 deposit plus 8 monthly instalments",kids="",parking=None,campervan=None,day=None,noncamp=None,
    extras=["Weekend camping plus early entry (from Wednesday) £362."])

ld=S("https://www.leedsfestival.com/tickets","Leeds Festival: Tickets")
add(id="leeds",name="Leeds Festival",start="2027-08-26",end="2027-08-29",dates_src=ld,
    venue="Bramham Park",county="West Yorkshire",region="Yorkshire and the Humber",loc_src=ld,
    camping="optional",status="on_sale",status_note="1st release.",seller="Ticketmaster",
    adult=P(326,"Weekend camping (from Thursday)",ld,fees="unknown"),
    noncamp=P(296,"Weekend non-camping (arena Fri to Sun)",ld,fees="unknown"),
    deposit="£20 deposit plus monthly instalments",kids="",parking=None,campervan=None,day=None,
    extras=["Weekend camping plus early entry (from Wednesday) £362."])

cf=S("https://www.creamfields.com/tickets","Creamfields: Tickets")
add(id="creamfields",name="Creamfields",start="2027-08-26",end="2027-08-29",dates_src=S("https://www.creamfields.com/","Creamfields homepage"),
    venue="Daresbury",county="Cheshire",region="North West England",loc_src=S(*UKFG),
    camping="optional",status="on_sale",status_note="The 2-day Saturday and Sunday camping ticket (£250 + £25) was sold out.",seller="Creamfields / Ticketmaster",
    adult=P(325,"Standard 4-day camping",cf,fees="included",note="£300 plus £25 booking fee."),
    noncamp=P(300,"Standard 3-day non-camping (Fri to Sun)",cf,fees="included",note="£275 plus £25 booking fee."),
    day=P(85.5,"Standard Friday day ticket",cf,fees="included",note="£75 plus £10.50 booking fee. Saturday or Sunday: £125 plus £15."),
    deposit="£20 deposit plus 9 payments",kids="",parking=None,campervan=None,
    extras=["Standard 3-day camping £280 + £25 booking fee."])

bt=S("https://www.boomtownfair.co.uk/tickets/","Boomtown: Tickets")
add(id="boomtown",name="Boomtown Fair",start="2027-08-11",end="2027-08-15",dates_src=bt,
    venue="Matterley Estate, near Winchester",county="Hampshire",region="South East England",loc_src=S(*UKFG),
    camping="available",status="on_sale",status_note="18+ festival (UK Festival Guides).",seller="Kaboodle",
    adult=P(325,"Thursday entry, travelling by public transport",bt,fees="unknown",note="Thursday entry for other travel is from £370. The page also says 'starting at £315' without saying which ticket that is."),
    deposit="£38 deposit plus 7 instalments",kids="18+ only",parking=None,campervan=None,day=None,noncamp=None,
    extras=["Wednesday entry from £395 (public transport) or £450 (other).","£20 refundable eco bond added to every entry ticket."])

gm=S("https://www.greenman.net/tickets/","Green Man: 2027 tickets")
add(id="green-man",name="Green Man",start="2027-08-19",end="2027-08-22",dates_src=gm,
    venue="Glanusk Estate, Crickhowell",county="Powys",region="Wales",loc_src=gm,
    camping="included",status="sold_out",status_note="All 2027 tickets sold out. Official resale is via Tixel.",seller="Green Man (resale: Tixel)",
    adult=P(318,"Adult weekend ticket with camping (Thu to Sun)",gm,fees="extra",note="Booking fees are extra. Student/under-25 £286."),
    kids="Teen (13-17) £227; Little Folk 6-12 £66; 3-5 £44; infants free.",
    parking=P(34,"Orange car park pass",gm,fees="extra",note="Park and ride £15."),
    campervan=P(197,"Small live-in vehicle",gm,fees="extra",note="Large live-in vehicle £265. People tickets are extra."),
    day=None,noncamp=None,deposit="",extras=["Settlement ticket (from Monday) adult £404."])

trk=S("https://truckfestival.com/tickets/","Truck Festival: Tickets")
add(id="truck",name="Truck Festival",start="2027-07-22",end="2027-07-25",dates_src=S("https://www.efestivals.co.uk/festivals/truck/2027","eFestivals: Truck 2027","other"),
    venue="Hill Farm, Steventon",county="Oxfordshire",region="South East England",loc_src=S("https://www.efestivals.co.uk/festivals/truck/2027","eFestivals: Truck 2027","other"),
    camping="included",status="on_sale",status_note="Tier 3 on sale.",seller="Truck Festival",
    adult=P(182,"General camping, Friday entry (tier 3)",trk,fees="included",note="Price includes all fees. Thursday entry £234."),
    kids="Kids 6-12 £23; 5 and under £12.50.",
    parking=P(39,"Car park, booked in advance",trk,fees="included"),
    campervan=P(212,"Campervan without electric hook-up",trk,fees="included",note="With hook-up £312."),
    day=None,noncamp=None,deposit="Payment plan from £18.88 a month",extras=[])

eo=S("https://endoftheroad.citizenticket.co.uk/events/end-of-the-road/end-of-the-road-festival-2027/","End of the Road 2027 on Citizen Ticket (official)")
add(id="end-of-the-road",name="End of the Road",start="2027-09-02",end="2027-09-05",dates_src=eo,
    venue="Larmer Tree Gardens, Tollard Royal",county="Dorset",region="South West England",loc_src=eo,
    camping="included",status="on_sale",status_note="Tier 4. No day tickets.",seller="Citizen Ticket",
    adult=P(359.12,"Tier 4 adult weekend with camping",eo,fees="included",note="£335 plus £24.12 booking fee."),
    kids="Youth 13-17 £220; child 6-12 £95; child 3-5 £75 (all plus booking fee); infants free but need a ticket.",
    parking=P(30,"Car parking",S("https://www.endoftheroadfestival.com/tickets/","End of the Road: Tickets"),fees="extra"),
    campervan=None,day=None,noncamp=None,deposit="£60 initial payment plus monthly payments to 30 June 2027",extras=[])

pl=S("https://www.parklife.uk.com/tickets","Parklife 2027 tickets")
add(id="parklife",name="Parklife",start="2027-07-10",end="2027-07-11",dates_src=pl,
    venue="Heaton Park",county="Greater Manchester",region="North West England",loc_src=pl,
    camping="unknown",status="on_sale",status_note="Early bird weekend.",seller="Parklife",
    adult=P(162.90,"Weekend general admission",pl,fees="included",note="Including all fees."),
    noncamp=P(162.90,"Weekend general admission",pl,fees="included"),
    deposit="£20 deposit plus 6 monthly payments",kids="",parking=None,campervan=None,day=None,extras=["Weekend VIP £223.10."])

tl=S("https://www.tramlines.org.uk/tickets/","Tramlines: Tickets")
add(id="tramlines",name="Tramlines",start="2027-07-23",end="2027-07-25",dates_src=S("https://tramlines.org.uk/tramlines-2027-super-early-bird-pre-sale-sign-up/","Tramlines 2027 presale page"),
    venue="Hillsborough Park",county="South Yorkshire",region="Yorkshire and the Humber",loc_src=S("https://tramlines.org.uk/","Tramlines homepage"),
    camping="unknown",status="on_sale",status_note="Tier 2. Super early bird, early bird and tier 1 have sold out.",seller="Tramlines",
    adult=P(165,"Weekend general admission (tier 2)",tl,fees="unknown"),
    noncamp=P(165,"Weekend general admission (tier 2)",tl,fees="unknown"),
    kids="Kids weekend from £12.50.",parking=None,campervan=None,day=None,deposit="Monthly plan from £16.66",extras=["Weekend VIP £235."])

bm=S("https://boardmasters.com/book-tickets-2027/","Boardmasters: Book tickets (2027)")
add(id="boardmasters",name="Boardmasters",start="2027-08-04",end="2027-08-08",dates_src=S(*UKFG),
    venue="Watergate Bay and Fistral Beach, Newquay",county="Cornwall",region="South West England",loc_src=S(*UKFG),
    camping="optional",status="on_sale",status_note="",seller="Boardmasters",
    adult=P(259,"General camping (from)",bm,fees="unknown",note="Includes a £20 litter bond, refunded when you return a full bag of rubbish."),
    noncamp=P(233,"3-day non-camping",bm,fees="unknown"),
    kids="Child tickets from £45 (general camping).",parking=None,campervan=None,day=None,deposit="",extras=["Chilled camping £294; VIP camping £379.","Big Green Coach camping returns from £51."])

cb=S("https://dorset.campbestival.net/weekend-tickets/","Camp Bestival Dorset: Weekend tickets")
add(id="camp-bestival-dorset",name="Camp Bestival Dorset",start="2027-07-29",end="2027-08-01",dates_src=cb,
    venue="Lulworth Castle",county="Dorset",region="South West England",loc_src=S(*UKFG),
    camping="included",status="on_sale",status_note="The page also lists a 'Tier 7, coming soon'.",seller="Ticketmaster",
    adult=P(225,"Adult general weekend camping",cb,fees="unknown"),
    kids="Teen 13-17 £157.50; child 10-12 £130.50; child 5-9 £110.50.",
    parking=None,campervan=P(160,"General campervan pass",cb,note="General caravan £180. People tickets are extra."),
    day=None,noncamp=None,deposit="Ticketmaster instalments",extras=[])

ly=S("https://www.lythamfestival.com/lytham-festival-tickets-prices-2027","Lytham Festival: 2027 ticket prices")
add(id="lytham",name="Lytham Festival",start="2027-06-30",end="2027-07-04",dates_src=S(*UKFG),
    venue="Lytham Green",county="Lancashire",region="North West England",loc_src=S(*UKFG),
    camping="none",status="on_sale",status_note="",seller="Ticketmaster",
    adult=P(325,"5-day pass, general admission wave 1 (from)",ly,fees="unknown"),
    noncamp=P(325,"5-day pass, general admission wave 1 (from)",ly,fees="unknown"),
    day=P(63.25,"Day ticket, general admission release 1 (cheapest night listed)",ly,fees="unknown"),
    kids="",parking=None,campervan=None,deposit="",extras=["Day prices differ by night; the dearest release 1 day is £74.75."])

lat=S("https://www.latitudefestival.com/news/latitude-2027-early-bird-tickets-key-info/","Latitude: 2027 Early Bird tickets key info (10 Aug 2026)")
add(id="latitude",name="Latitude",start="2027-07-22",end="2027-07-25",dates_src=lat,
    venue="Henham Park",county="Suffolk",region="East of England",loc_src=lat,
    camping="included",status="on_sale",status_note="Early bird on sale; day tickets coming soon.",seller="Ticketmaster",
    adult=P(320,"Early bird adult weekend, general camping",lat,fees="extra",note="Ticket page says all tickets are subject to booking and delivery fees."),
    kids="Accompanied teen £195; child £28.",
    parking=P(0,"Car parking",S("https://www.latitudefestival.com/tickets","Latitude: Tickets"),note="The tickets page says car parking is free."),
    campervan=None,day=None,noncamp=None,deposit="",extras=[])

bs=S("https://www.woldtopbrewery.co.uk/product/big-sky-festival-ticket","Wold Top Brewery: Big Sky Festival ticket")
add(id="big-sky",name="Big Sky Beer Festival",start="2027-07-09",end="2027-07-10",dates_src=bs,
    venue="Wold Top Brewery, Hunmanby Grange",county="East Yorkshire",region="Yorkshire and the Humber",loc_src=bs,
    camping="optional",status="on_sale",status_note="Early bird pricing until 31 October 2026.",seller="Wold Top Brewery",
    adult=P(32,"Weekend pass (early bird)",bs,fees="unknown",note="Includes 2 free pints. Weekend camping (2 nights) is £24 more."),
    noncamp=P(32,"Weekend pass (early bird)",bs,fees="unknown"),
    day=P(17,"Friday ticket (early bird)",bs,fees="unknown",note="Saturday £20."),
    kids="",parking=None,campervan=None,deposit="",extras=["A beer festival with live music."])

ol=S("https://www.onelovefestival.co.uk/tickets/","One Love Festival 2027 tickets")
add(id="one-love",name="One Love Festival",start="2027-08-20",end="2027-08-22",dates_src=ol,
    venue="Bentley Estate, near Lewes",county="East Sussex",region="South East England",loc_src=ol,
    camping="optional",status="on_sale",status_note="",seller="One Love Festival",
    adult=P(115,"Weekend ticket (from)",ol,fees="unknown"),
    day=P(40,"Day ticket (from)",ol,fees="unknown",note="Friday or Saturday £50. Day plus camping from £65."),
    kids="Under-12s free. Child 12-14 weekend £55.",parking=None,campervan=None,noncamp=None,deposit="Payment plans from £20 a month",extras=[])

pr=S("https://plumptonrevival.co.uk/tickets","Plumpton Revival: Tickets")
add(id="plumpton-revival",name="Plumpton Revival",start="2027-08-07",end="2027-08-08",dates_src=pr,
    venue="Plumpton Racecourse",county="East Sussex",region="South East England",loc_src=pr,
    camping="optional",status="on_sale",status_note="",seller="Plumpton Revival",
    adult=P(150,"Adult weekend ticket and camping",pr,fees="unknown"),
    noncamp=P(120,"Adult weekend ticket (no camping)",pr,fees="unknown"),
    day=P(70,"Adult day ticket",pr,fees="unknown"),
    parking=P(15,"Car parking pass",pr,fees="unknown"),
    campervan=P(50,"Campervan ticket",pr,fees="unknown"),
    kids="",deposit="",extras=["65+ tickets are 10% off."])

bf=S("https://buddhafield.citizenticket.com/events/buddhafield/buddhafield-festival-2027/","Buddhafield Festival 2027 on Citizen Ticket (official)")
add(id="buddhafield",name="Buddhafield Festival",start="2027-07-14",end="2027-07-18",dates_src=bf,
    venue="",county="Somerset",region="South West England",loc_src=bf,
    camping="included",status="on_sale",status_note="",seller="Citizen Ticket",
    adult=P(194.99,"Adult early bird, full event with camping",bf,fees="included",note="£185 plus £9.99 booking fee. Standard adult £225 plus £12.15."),
    kids="Young person 13-17 £80 + fee; child 3-5 £35 + fee.",
    parking=P(39.52,"Car pass, full event",bf,fees="included",note="£37.50 plus £2.03 booking fee."),
    campervan=P(84.32,"Live-in pass (6m and under)",bf,fees="included",note="£80 plus £4.32 booking fee."),
    day=None,noncamp=None,deposit="",extras=["Concession adult £165 + fee."])

sw=S("https://www.stowawayfestival.co.uk/tickets","Stowaway Festival: Tickets")
add(id="stowaway",name="Stowaway Festival",start="2027-07-30",end="2027-08-02",dates_src=sw,dates_basis="camping",
    venue="",county="",region="",loc_src=None,
    camping="included",status="on_sale",status_note="Dates shown are the camping dates (Friday 10am to Monday midday).",seller="Stowaway",
    adult=P(225.72,"Adult weekend with camping",sw,fees="included",note="Including booking fee."),
    kids="Teen 13-17 £122.04; child 2-12 £64.80.",
    parking=P(21,"Car pass",sw),campervan=P(114.45,"Camper",sw),day=None,noncamp=None,deposit="9-month payment plan or Klarna Pay in 3",extras=["Buy 5, get one free group discount."])

ef=S("https://elyfolkfestival.co.uk/tickets/","Ely Folk Festival: Tickets")
add(id="ely-folk",name="Ely Folk Festival",start="2027-07-09",end="2027-07-11",dates_src=ef,
    venue="",county="Cambridgeshire",region="East of England",loc_src=ef,
    camping="optional",status="on_sale",status_note="Early bird (tier 1).",seller="Ely Folk Festival",
    adult=P(130,"Adult weekend ticket, early bird",ef,fees="unknown",note="Tent pitch is £30 extra."),
    noncamp=P(130,"Adult weekend ticket, early bird",ef,fees="unknown"),
    day=P(36,"Friday adult day ticket, early bird",ef,fees="unknown"),
    campervan=P(52,"Caravan or campervan pitch",ef),
    kids="Youth 12-17 £43; children under 12 free.",parking=None,deposit="Klarna",extras=["Concession (over 66 and registered disabled) £120."])

cam=S("https://www.cambridgefolkfestival.co.uk/","Cambridge Folk Festival homepage")
add(id="cambridge-folk",name="Cambridge Folk Festival",start="2027-07-30",end="2027-08-01",dates_src=cam,
    venue="Cherry Hinton Hall",county="Cambridgeshire",region="East of England",loc_src=cam,
    camping="available",status="on_sale",status_note="Tier 1 went on sale on 2 October 2026.",seller="Cambridge Live",
    adult=P(170,"Full festival ticket (from)",cam,fees="unknown"),
    noncamp=P(170,"Full festival ticket (from)",cam,fees="unknown"),
    parking=P(21,"Weekend parking (Netherhall School), from",cam),
    campervan=P(85,"Cherry Hinton caravan, from",cam,note="Sold out when checked."),
    kids="",day=None,deposit="",extras=[])

cr=S("https://www.fairportconvention.com/festival-faqs/","Fairport Convention: Festival FAQs")
add(id="cropredy",name="Fairport's Cropredy Convention",start="2027-08-12",end="2027-08-14",dates_src=cr,
    venue="Cropredy, near Banbury",county="Oxfordshire",region="South East England",loc_src=cr,
    camping="optional",status="coming_soon",status_note="Tickets go on sale at 10am on Monday 7 December 2026.",seller="AXS",
    adult=P(250,"Three-day festival ticket",cr,fees="extra",note="£2 handling charge per order."),
    noncamp=P(250,"Three-day festival ticket",cr,fees="extra"),
    kids="Teen 12-17 £90.",parking=P(15,"Parking for non-campers",cr),
    campervan=P(65,"Three-day camping, per vehicle",cr),day=None,deposit="PayPal Pay in 3",extras=[])

def basic(id,name,start,end,dsrc,venue,county,region,lsrc,camping,status,note,extras=None,parking=None,kids=""):
    add(id=id,name=name,start=start,end=end,dates_src=dsrc,venue=venue,county=county,region=region,loc_src=lsrc,camping=camping,
        status=status,status_note=note,seller="",adult=None,noncamp=None,day=None,parking=parking,campervan=None,kids=kids,deposit="",extras=extras or [])

v=S("https://www.victoriousfestival.co.uk/information/tickets/","Victorious Festival: Tickets")
basic("victorious","Victorious Festival","2027-08-27","2027-08-29",v,"Southsea Common, Portsmouth","Hampshire","South East England",v,"unknown","unknown","2027 dates confirmed; prices not shown on the official page when checked.")
t2=S("https://2000trees.co.uk/tickets/","2000trees: Tickets")
basic("2000trees","2000trees","2027-07-07","2027-07-10",t2,"","","",None,"unknown","sold_out","The 4-day ticket is sold out; the 3-day ticket is 'coming soon' with a wait list.")
at=S("https://arctangent.co.uk/tickets/","ArcTanGent: Tickets")
basic("arctangent","ArcTanGent","2027-08-18","2027-08-21",at,"Cotswolds","","",at,"unknown","on_sale","Payment plan 3-day from £24 x 10 payments; full price not shown on the page.")
bl=S("https://bloodstock.uk.com/","Bloodstock homepage")
basic("bloodstock","Bloodstock Open Air","2027-08-05","2027-08-08",bl,"Catton Park","Derbyshire","East Midlands",bl,"unknown","unknown","Tickets sold via See Tickets; price not readable when checked.")
bd=S("https://www.beautifuldays.org/tickets/","Beautiful Days: Tickets")
basic("beautiful-days","Beautiful Days","2027-08-20","2027-08-22",bd,"Escot Park","Devon","South West England",bd,"unknown","coming_soon","Tickets for 2027 go on sale on Thursday 5 November 2026.")
sh=S("https://www.shambalafestival.org/","Shambala homepage")
basic("shambala","Shambala","2027-08-26","2027-08-29",sh,"","","",None,"unknown","on_sale","On sale; prices are only shown in the booking portal. A refundable £25 recycling bond is added to each order.")
bth=S("https://beardedtheory.co.uk/tickets/","Bearded Theory: Tickets")
basic("bearded-theory","Bearded Theory","2027-05-26","2027-05-30",bth,"Catton Park","Derbyshire","East Midlands",bth,"unknown","unknown","Prices not shown on the official page when checked.")
vf=S("https://www.skiddle.com/festivals/valley-fest/","Skiddle: Valley Fest 2027","agent")
basic("valley-fest","Valley Fest","2027-07-29","2027-08-01",vf,"Near Bristol (BS40 8SZ)","","South West England",vf,"available","on_sale","Sold on Skiddle; price not readable when checked.",
      parking=P(20,"Car parking in advance",vf,fees="extra",note="More on the gate."))
lf=S("https://www.skiddle.com/festivals/lindisfarne-festival/","Skiddle: Lindisfarne Festival 2027","agent")
basic("lindisfarne","Lindisfarne Festival","2027-09-02","2027-09-04",lf,"Beal Farm","Northumberland","North East England",lf,"available","on_sale","Over-18s only (official site). Sold on Skiddle; price not readable when checked.",
      parking=P(20,"Parking pass per vehicle",lf),kids="18+ only")
gf=S("https://www.skiddle.com/festivals/gemfest/","Skiddle: GemFest 2027","agent")
basic("gemfest","GemFest","2027-06-17","2027-06-20",gf,"Charlton Park Estate","Wiltshire","South West England",gf,"unknown","on_sale","Sold on Skiddle; price not readable when checked.")
wo=S("https://weoutherefestival.com/tickets/","We Out Here: Tickets")
basic("we-out-here","We Out Here","2027-08-19","2027-08-22",wo,"","","",None,"unknown","unknown","Day tickets are not on sale yet; weekend price not shown on the FAQ page.")
js=S("https://justsofestival.org.uk/tickets/","Just So Festival: Tickets")
basic("just-so","Just So Festival","2027-08-20","2027-08-22",js,"Rode Hall Estate","Cheshire","North West England",js,"unknown","on_sale","Family festival. Payment plans over 3, 6, 9 or 12 months.")
td=S("https://tunesinthedunes.co.uk/","Tunes in the Dunes homepage")
basic("tunes-in-the-dunes","Tunes in the Dunes","2027-06-11","2027-06-13",td,"Perranporth Beach","Cornwall","South West England",td,"unknown","on_sale","2027 tickets on sale; prices not readable when checked.")
basic("wychwood","Wychwood Festival","2027-06-04","2027-06-06",S(*SKL),"","","",None,"unknown","unknown","Dates from the Skiddle listing.")
basic("glastonbudget","Glastonbudget","2027-05-27","2027-05-30",S(*SKL),"","","",None,"unknown","unknown","Dates from the Skiddle listing.")
basic("neighbourhood-weekender","Neighbourhood Weekender","2027-05-29","2027-05-30",S(*SKL),"","","",None,"unknown","unknown","Dates from the Skiddle listing. Minimum age 5.")

# ======================= v2 second pass (checked 31 Oct 2026) =======================
BY={f["id"]:f for f in F}
def upd(id,**k): BY[id].update(k)
def SKF(slug,name): return S(f"https://www.skiddle.com/festivals/{slug}/",f"Skiddle: {name} 2027","agent")
def SKB(ilid,name): return S(f"https://www.skiddle.com/infofeed/ticketbox.php?ilid={ilid}&pid=0&aid=0&eid=0&bid=0&test=false",f"Skiddle ticket box: {name} 2027 (official agent)","agent")

# --- Download: no official price published ---
upd("download",status_note="Official ticket page lists camping, non-camping and day options, but neither downloadfestival.co.uk nor Ticketmaster showed a 2027 price when checked, so the price below is a press figure.")
# --- Truck: official ticket shop ---
tt=S("https://tickets.truckfestival.com/event/truck-festival-2027/hill-farm/3691891?clearoffer=true","Truck Festival 2027 official ticket shop")
upd("truck",start="2027-07-23",end="2027-07-25",dates_src=tt,loc_src=tt,
    status_note="Tier 3 on sale. The festival runs Friday to Sunday; Thursday entry tickets let you arrive on 22 July.",
    adult=P(190,"General camping, Friday entry (tier 3)",tt,fees="included",note="£180 face value plus booking fee. A £2 transaction fee is added per order. The main tickets page says 'from £182 inc. all fees'; the ticket shop showed £190."),
    kids="Kids 6-12 £23; 5 and under £12.50 (from the main tickets page, truckfestival.com/tickets).",
    extras=["Thursday entry general camping (tier 3) £242 (£230 face value)."])
BY["truck"]["parking"]["note"]="From the main tickets page."
# --- Big Sky: early bird expiring ---
bsa=BY["big-sky"]["adult"]; bsa["label"]="Weekend pass (early bird, ends 31 Oct 2026)"
bsa["note"]="Early bird price, shown as valid until 31 October 2026, the day we checked. The next tier's price was not published yet. Includes 2 free pints. Weekend camping (2 nights) is £24 more."
upd("big-sky",status_note="Early bird pricing ends 31 October 2026. The next tier's price was not yet published when checked.")
BY["big-sky"]["noncamp"]["label"]="Weekend pass (early bird, ends 31 Oct 2026)"
# --- Victorious ---
vb=S("https://www.victoriousfestival.co.uk/buy-tickets-2027/","Victorious Festival: Buy tickets 2027")
upd("victorious",camping="optional",status="on_sale",status_note="",seller="Victorious Festival",
    adult=P(220.32,"Weekend camping ticket (from)",vb,fees="included",note="Including booking fee."),
    noncamp=P(209.52,"Weekend ticket (from)",vb,fees="included",note="Including booking fee."))
# --- 2000trees ---
t2t=S("https://tickets.2000trees.co.uk/events/2000trees/2213997","2000trees 2027 official ticket shop")
upd("2000trees",venue="Upcote Farm (GL54 4BL)",county="Gloucestershire",region="South West England",loc_src=t2t,
    status_note="The 4-day ticket is sold out; the 3-day early bird has a wait list and no price shown. The official site gives 7 to 10 July; the ticket shop shows Wednesday 7 July to Sunday 11 July (3pm), which includes departure day.")
# --- ArcTanGent ---
atb=S("https://buytickets.at/arctangent/2263452/r/webticketpage","ArcTanGent 2027 official ticket shop")
upd("arctangent",venue="Todenham Manor Farm (GL56 9NW)",county="Gloucestershire",region="South West England",loc_src=atb,
    status_note="New site for 2027. Payment plan 3-day from £24 x 10 payments; the full price was not shown. The ticket shop lists Wednesday 18 to Sunday 22 August (departure day).")
# --- Bearded Theory ---
bta=S("https://www.alttickets.com/bearded-theory-tickets/walton-on-trent-catton-park/2027-05-19-09-00-85651","alt.tickets: Bearded Theory 2027 (official agent)","agent")
upd("bearded-theory",venue="Catton Park, Walton-on-Trent",status="on_sale",status_note="Early bird adult weekend on sale. The payment-plan version was sold out.",seller="alt.tickets",
    camping="unknown",
    adult=P(269.95,"Adult weekend, early bird (Thursday to Sunday)",bta,fees="included",note="£260 face value plus booking fee.",days=4),
    campervan=P(155,"Campervan, 4 nights",bta,fees="included",note="£150 face value plus fee. 5 nights £190."),
    kids="Child 12-16 £95; child 8-11 £68.50.")
# --- Valley Fest ---
vfb=SKB(42778158,"Valley Fest")
upd("valley-fest",status_note="Tier 1 early bird on sale.",seller="Skiddle",
    adult=P(137.49,"Tier 1 early bird adult weekend (Friday to Sunday)",vfb,fees="included",note="£124.99 plus booking fee. A Thursday add-on is £29.99 plus booking fee.",days=3),
    campervan=P(131.99,"Live-in vehicle",vfb,fees="included",note="£119.99 plus booking fee."),
    kids="Teen weekend £59.99 plus booking fee; child weekend free.")
BY["valley-fest"]["parking"]["note"]="From the Skiddle festival page. More on the gate."
# --- Lindisfarne ---
lfb=SKB(42719465,"Lindisfarne Festival")
upd("lindisfarne",status_note="Over-18s only (official site). 2nd release weekend on sale.",seller="Skiddle",
    adult=P(189,"Weekend camping, Thursday to Sunday (2nd release)",lfb,fees="included",note="£180 plus booking fee."),
    parking=P(36.75,"Car parking",lfb,fees="included",note="£35 plus booking fee."),
    extras=["Friday to Sunday 1st release £157.50 (£150 plus booking fee).","Saturday to Sunday early bird £120.75 (£115 plus booking fee)."])
# --- GemFest ---
gfb=SKB(42462731,"GemFest")
upd("gemfest",status_note="Second release on sale; the first release (£99 plus booking fee) was not on sale.",seller="Skiddle",
    adult=P(129,"Second release, Friday entry (all in)",gfb,fees="included",note="Shown as '[ALL IN]'.",days=3),
    extras=["Thursday entry, second release £159 all in."])
# --- We Out Here ---
woh=S("https://weoutherefestival.com/","We Out Here homepage")
wob=S("https://go.kaboodle.co.uk/woh-2027-wbsg","We Out Here 2027 official ticket shop (Kaboodle)")
upd("we-out-here",venue="Wimborne St Giles",county="Dorset",region="South West England",loc_src=woh,status="on_sale",status_note="General release weekend on sale. Day tickets not on sale yet.",seller="Kaboodle",
    adult=P(317.13,"General release weekend, 18+",wob,fees="included",note="£295 face value plus £22.13 booking fee."),kids="Child 4-13 £27.50.")
# --- Just So ---
jsb=S("https://www.citizenticket.com/event/just-so-festival-2027/","Just So Festival 2027 on Citizen Ticket (official)")
upd("just-so",camping="included",seller="Citizen Ticket",status_note="Tier 1 on sale. Family festival. Payment plans over 3, 6, 9 or 12 months.",
    adult=P(194.18,"Tier 1 adult weekend with camping",jsb,fees="included",note="£185 plus £9.18 booking fee."),
    day=P(68.42,"Adult Saturday ticket",jsb,fees="included"),
    parking=P(28.07,"Car parking",jsb,fees="included",note="£26.50 plus £1.57 booking fee."),
    campervan=P(101.43,"Live-in vehicle",jsb,fees="included"))
# --- Tunes in the Dunes ---
tdb=S("https://tickets.tunesfestivals.com/events/tunes-in-the-dunes-2027","Tunes in the Dunes 2027 official ticket shop")
upd("tunes-in-the-dunes",camping="optional",seller="Tunes Festivals",status_note="",
    adult=P(95,"Adult weekend with camping",tdb,fees="included",note="£90 plus £5 fee."),
    noncamp=P(80,"Adult weekend, no camping",tdb,fees="unknown"),kids="Child weekend camping £70 plus £5 fee.")
# --- Shambala ---
shb=S("https://tickets.shambalafestival.org/?t=kaboodle-9y4i4&c=235&p=27865&k=14753b3d1662372d1f1d20783bef28610086afa1","Shambala 2027 official ticket shop (Kaboodle)")
upd("shambala",camping="included",seller="Kaboodle",status_note="Tiers 1 and 2 sold out; tier 3 on sale; tier 4 (£309.72) coming soon. The location is not published on the pages we checked. A refundable £25 recycling bond is added to each order.",
    adult=P(299.37,"Adult weekend, tier 3",shb,fees="included",note="£289 plus £10.37 booking fee."),extras=["Green traveller adult ticket £268.32."])
# --- Wychwood, Glastonbudget, Neighbourhood ---
wy=SKF("wychwood","Wychwood Festival")
upd("wychwood",dates_src=wy,venue="Cheltenham Racecourse",county="Gloucestershire",region="South West England",loc_src=wy,status_note="Price not readable when checked (the official site returned an error).")
gbg=S("https://glastonbudget.gigantic.com/glastonbudget-tickets/leicestershire-turnpost-farm/2027-05-20-00-00-55379","Gigantic: Glastonbudget 2027 (official agent)","agent")
gbs=SKF("glastonbudget","Glastonbudget")
upd("glastonbudget",dates_src=gbs,venue="Turnpost Farm, Wymeswold",county="Leicestershire",region="East Midlands",loc_src=gbs,camping="included",status="on_sale",status_note="Price from the payment-plan listing; the same tier is sold for full payment.",seller="Gigantic",
    adult=P(166.95,"Adult (18+) weekend, includes standard camping",gbg,fees="included",note="£157.50 plus £9.45 booking fee."),kids="Youth weekend £115.54.")
nb=SKF("neighbourhood-weekender","Neighbourhood Weekender")
upd("neighbourhood-weekender",dates_src=S("https://nbhdweekender.com/information/","Neighbourhood Weekender: Information"),venue="Victoria Park",county="Warrington",region="North West England",loc_src=nb,
    status_note="Minimum age 5. Tickets via See Tickets, Ticketmaster, AXS and Gigs and Tours; price not readable when checked.")

def new(id,name,start,end,dsrc,venue,county,region,lsrc,camping="unknown",status="unknown",note="",seller="",adult=None,noncamp=None,day=None,parking=None,campervan=None,kids="",deposit="",extras=None,nation="England"):
    add(id=id,name=name,start=start,end=end,dates_src=dsrc,venue=venue,county=county,region=region,loc_src=lsrc,camping=camping,status=status,status_note=note,
        seller=seller,adult=adult,noncamp=noncamp,day=day,parking=parking,campervan=campervan,kids=kids,deposit=deposit,extras=extras or [],nation=nation)

# ---------------- Scotland ----------------
bel=S("https://www.gigantic.com/belladrum-tickets/inverness-belladrum-estate/2027-07-29-08-00","Gigantic: Belladrum 2027 (official agent)","agent")
belf=S("https://tartanheartfestival.com/faqs","Belladrum Tartan Heart Festival: FAQs")
new("belladrum","Belladrum Tartan Heart Festival","2027-07-29","2027-07-31",belf,"Belladrum Estate (IV4 7BA), near Inverness","Highland","Scotland",belf,camping="included",status="on_sale",
    note="Early bird sold out; general on-sale weekend tickets available.",seller="Gigantic",
    adult=P(253,"Weekend adult (18+), general on-sale, camping included",bel,fees="included",note="£230 face value plus £23 booking fee. Early bird (£242) sold out."),
    kids="Youth 13-17 early bird £198 (sold out).",nation="Scotland")
heb=S("https://www.hebceltfest.com/booking","HebCelt: 2027 tickets")
new("hebcelt","HebCelt (Hebridean Celtic Festival)","2027-07-15","2027-07-17",heb,"Stornoway, Isle of Lewis","Na h-Eileanan Siar","Scotland",heb,status="on_sale",
    note="Arena weekend runs Thursday to Saturday. Camping not confirmed on the tickets page.",seller="HebCelt",
    adult=P(180,"Arena weekend (Thursday to Saturday)",heb,fees="included",note="The page says 'Buy online with no booking fees'. Payment plans (via Skiddle) carry booking fees."),
    kids="Concession £150; youth 14-17 £115; child 6-13 £60; infant 0-5 £14.",nation="Scotland")
kgp=S("https://www.citizenticket.com/events/kelburn-arts/kelburn-garden-party-2027/","Kelburn Garden Party 2027 on Citizen Ticket (official)")
new("kelburn-garden-party","Kelburn Garden Party","2027-07-01","2027-07-05",kgp,"Kelburn Estate, Fairlie, near Largs","North Ayrshire","Scotland",S("https://www.kelburngardenparty.com/tickets/","Kelburn Garden Party: Tickets"),
    camping="included",status="on_sale",note="Tier 3 on sale. Dates are the ticket shop's opening and closing times (Thursday 4pm to Monday 1pm).",seller="Citizen Ticket",
    adult=P(318.08,"Adult 4-day weekend, tier 3 (Thursday to Sunday)",kgp,fees="included",note="£290 plus £28.08 booking fee. Includes camping and a £10 returnable bond.",days=4),
    kids="Youth 13-17 3-day £115.32; child 5-12 3-day £44.08.",
    extras=["Adult 3-day weekend (Friday to Sunday), tier 3: £274.24 (£250 plus £24.24 booking fee), includes camping and a £10 returnable bond."],nation="Scotland")
BY2=None
ed=S("https://edenfestival.citizenticket.co.uk/event/eden-festival-2027/","Eden Festival 2027 on Citizen Ticket (official)")
new("eden","Eden Festival","2027-06-10","2027-06-13",ed,"Raehills Meadows (DG11 1ET)","Dumfries and Galloway","Scotland",ed,status="on_sale",
    note="Tier 1 not available; tier 2 on sale.",seller="Citizen Ticket",
    adult=P(206.11,"Adult 4-day weekend, tier 2 (Thursday to Sunday)",ed,fees="included",note="£194 plus £12.11 booking fee."),
    kids="Teen 13-17 4-day tier 2 £101.17.",extras=["Adult 3-day weekend (Friday to Sunday), tier 1: £158.41 (£149 plus £9.41 booking fee)."],nation="Scotland")
pap=S("https://partyatthepalace.co.uk/product/buy-tickets/","Party at the Palace: Buy tickets")
new("party-at-the-palace","Party at the Palace","2027-08-07","2027-08-08",pap,"Linlithgow Palace","West Lothian","Scotland",S("https://partyatthepalace.co.uk/","Party at the Palace homepage"),
    status="on_sale",note="",seller="Party at the Palace",
    adult=P(86.9,"Earlybird weekend ticket",pap,fees="included",note="£79 plus £7.90 booking fee. Full-price weekend £99 plus booking fee."),
    day=P(49.5,"Earlybird Saturday ticket",pap,fees="included",note="£45 plus £4.50 booking fee."),nation="Scotland")
dr=S("https://www.backdounetherabbithole.co.uk/tickets/","Back Doune The Rabbit Hole: Tickets")
new("doune-the-rabbit-hole","Back Doune The Rabbit Hole","2027-07-16","2027-07-18",dr,"Cardross Estate","Stirlingshire","Scotland",dr,note="Price not readable on the tickets page when checked.",nation="Scotland")
tv=SKF("terminal-v-festival","Terminal V Festival")
new("terminal-v","Terminal V (Glasgow)","2027-06-04","2027-06-06",tv,"Clydeside Live, Glasgow","Glasgow","Scotland",tv,note="Dates from the Skiddle listing; price not found.",nation="Scotland")

# ---------------- Wales ----------------
fw=S("https://www.gigantic.com/focus-wales-tickets/wrexham-various-wrexham-venues/2027-05-06-10-00","Gigantic: FOCUS Wales 2027 standard pass (official agent)","agent")
new("focus-wales","FOCUS Wales","2027-05-06","2027-05-08",fw,"Various venues, Wrexham","Wrexham","Wales",fw,camping="none",status="on_sale",note="Multi-venue showcase festival.",seller="Gigantic",
    adult=P(88,"Standard festival pass, early bird",fw,fees="included",note="£80 plus £8 booking fee. The official tickets page lists it as £80 + booking fee."),
    extras=["Fast track early bird pass £110 plus booking fee (official tickets page).","Delegate early bird pass £140 plus booking fee."],nation="Wales")
sth=S("https://www.gigantic.com/steelhouse-festival-tickets/ebbw-vale-hafod-y-dafal-farm/2027-07-23-12-00","Gigantic: Steelhouse Festival 2027 (official agent)","agent")
new("steelhouse","Steelhouse Festival","2027-07-23","2027-07-25",sth,"Hafod-Y-Dafal Farm, Ebbw Vale (NP13 2ER)","Blaenau Gwent","Wales",sth,status="on_sale",note="First release.",seller="Gigantic",
    adult=P(178.2,"Weekend arena, aged 15+ (first release)",sth,fees="included",note="£165 face value plus £13.20 booking fee. Camping is sold separately."),
    day=P(70.2,"Friday day ticket, 15+",sth,fees="included",note="£65 plus £5.20 booking fee."),kids="Weekend arena 4-14 £43.20; under 4s free.",
    extras=["VIP upgrade £81 including fee."],nation="Wales")
gw=S("https://www.gottwood.co.uk/","Gottwood homepage")
gws=SKF("gottwood","Gottwood")
new("gottwood","Gottwood","2027-06-10","2027-06-13",gw,"Carreglwyd, Llanfaethlu, Anglesey","Anglesey","Wales",gws,note="Early bird sold out; further releases were not on sale when checked.",nation="Wales")

# ---------------- Northern Ireland ----------------
stb=S("https://go.kaboodle.co.uk/St3ndh@l2027","Stendhal Festival 2027 official ticket shop (Kaboodle)")
sth2=S("https://www.stendhalfestival.com/","Stendhal Festival homepage")
new("stendhal","Stendhal Festival","2027-07-01","2027-07-03",stb,"Ballymully Cottage Farm, Limavady","County Londonderry","Northern Ireland",sth2,camping="optional",status="on_sale",
    note="Super early bird on sale.",seller="Kaboodle",
    adult=P(134.55,"Adult weekend camping, 3 nights (Thursday to Saturday), super early bird",stb,fees="included",note="£130 face value plus £4.55 booking fee. A £1 transaction fee is added per booking."),
    noncamp=P(87.98,"Adult non-camping, 2 days (Friday and Saturday), super early bird",stb,fees="included",note="Covers 2 of the 3 days."),
    extras=["Adult camping 2 nights (Friday to Saturday), super early bird £108.68."],nation="Northern Ireland")
mm=S("https://mastermcgrathfestival.co.uk/","Master McGrath Festival homepage")
new("master-mcgrath","Master McGrath Festival","2027-05-21","2027-05-22",mm,"Brownlow Castle, Lurgan","County Armagh","Northern Ireland",mm,note="Not-for-profit festival. Line-up and prices 'coming soon' when checked.",nation="Northern Ireland")

# ---------------- England ----------------
kc=SKF("kendal-calling","Kendal Calling")
new("kendal-calling","Kendal Calling","2027-07-29","2027-08-01",kc,"Lowther Deer Park, near Penrith","Cumbria","North West England",kc,status="on_sale",
    note="Tickets went on sale on 6 August 2026 (official news page). Prices are shown only at See Tickets, which we could not read.",seller="See Tickets",
    extras=["Official news: https://kendalcalling.co.uk/return-to-the-fields-for-kendal-27"])
yn=S("https://ynotfestival.com/tickets/","Y Not Festival: 2027 tickets")
yns=SKF("Y-Not-Festival","Y Not Festival")
new("y-not","Y Not Festival","2027-07-29","2027-08-01",yns,"Pikehall, near Matlock","Derbyshire","East Midlands",yns,camping="included",status="on_sale",
    note="Tier 6. Weekend tickets cover Friday to Sunday; Thursday entry costs extra. The official FAQ gives the dates as 'Thursday 31th July – Sunday 1st August 2027', which looks like a typo; the Skiddle listing shows 29 July to 1 August.",seller="Y Not Festival",
    adult=P(212,"Tier 6 weekend, Friday to Sunday entry and camping",yn,fees="unknown",days=3),
    campervan=P(180,"Live-in vehicle",yn,fees="unknown"),
    parking=P(30,"Parking pass in advance",S("https://ynotfestival.com/faqs/","Y Not Festival: FAQs"),fees="extra",note="£30 plus booking fee."),
    extras=["Weekend plus Thursday £265.","Thursday entry upgrade £55."])
gl=S("https://www.gigantic.com/gloworm-festival-tickets/nottinghamshire-thoresby-park/2027-08-13-17-00","Gigantic: Gloworm Festival 2027 (official agent)","agent")
new("gloworm","Gloworm Festival","2027-08-13","2027-08-15",gl,"Thoresby Park (NG22 9EP)","Nottinghamshire","East Midlands",gl,camping="optional",status="on_sale",note="Tier 1. Family festival.",seller="Gigantic",
    adult=P(148.5,"Adult weekend ticket with camping (tier 1)",gl,fees="included",note="£135 face value plus £13.50 booking fee. Includes 1 parking space per tent pitch."),
    noncamp=P(88,"Adult weekend entry, Saturday and Sunday, no camping",gl,fees="included",note="£80 plus £8 booking fee. Covers 2 of the 3 days."),
    extras=["Family camping offer (2 adults, 2 children) £506 including fees."])
eff=S("https://www.citizenticket.com/events/elderflower-fields/elderflower-fields-2027/","Elderflower Fields 2027 on Citizen Ticket (official)")
eft=SKF("elderflower-fields","Elderflower Fields")
new("elderflower-fields","Elderflower Fields","2027-05-28","2027-05-31",eff,"Pippingford Park, Nutley","East Sussex","South East England",eft,camping="included",status="on_sale",note="1st release. Family festival.",seller="Citizen Ticket",
    adult=P(175.5,"Adult weekend, 1st release, standard camping included",eff,fees="included",note="£165 plus £10.50 booking fee. Final release £244.40."),
    kids="Child 4-16 weekend £96 (1st release); under 4s free.")
def sk(id,name,slug,start,end,venue,county,region,note="Dates from the Skiddle listing; 2027 price not found.",camping="unknown"):
    s=SKF(slug,name); new(id,name,start,end,OFF.get(id,s),venue,county,region,s,note=note,camping=camping)
OFF={"beardy-folk":S("https://www.beardyfolkfestival.co.uk/","Beardy Folk Festival homepage"),
     "towerfest":S("https://www.towerfest.co.uk/","Towerfest homepage"),
     "field-day":S("https://www.fielddayfestivals.com/","Field Day homepage")}
sk("mighty-hoopla","Mighty Hoopla","mighty-hoopla","2027-06-05","2027-06-06","Brockwell Park","London","London")
sk("love-saves-the-day","Love Saves The Day","love-saves-the-day","2027-05-29","2027-05-30","Ashton Court","Bristol","South West England")
sk("field-day","Field Day","field-day","2027-05-29","2027-05-29","Brockwell Park","London","London")
sk("the-great-escape","The Great Escape","the-great-escape","2027-05-12","2027-05-15","Brighton Dome and various venues","Brighton","South East England",camping="none",note="Multi-venue city festival. Dates from the Skiddle listing; 2027 price not found.")
sk("liverpool-sound-city","Liverpool Sound City","liverpool-sound-city","2027-05-01","2027-05-02","Multiple venues","Liverpool","North West England",camping="none",note="Multi-venue city festival. Dates from the Skiddle listing; 2027 price not found.")
sk("parklands","Parklands Festival","parklands-festival","2027-06-18","2027-06-20","Haughton Hall, Shifnal","Shropshire","West Midlands")
sk("beardy-folk","Beardy Folk Festival","beardy-folk-festival","2027-06-17","2027-06-20","Hopton Court, near Ludlow","Shropshire","West Midlands")
sk("exile","Exile Festival","exile-festival","2027-06-25","2027-06-27","Sabine Hay Farm, Matlock","Derbyshire","East Midlands")
sk("towerfest","Towerfest","towerfest","2027-06-17","2027-06-20","Drax Sports and Social Club, Selby","North Yorkshire","Yorkshire and the Humber")
sk("buckle-and-boots","Buckle & Boots","buckle-and-boots","2027-05-27","2027-05-30","Whitebottom Farm, Etherow Country Park","Stockport","North West England")
sk("dot-to-dot","Dot to Dot Festival","dot-to-dot-festival","2027-05-29","2027-05-30","Multiple venues, Bristol and Nottingham","","South West England",camping="none",note="Multi-venue city festival in Bristol and Nottingham. Dates from the Skiddle listing; 2027 price not found.")
sk("gate-to-southwell","Gate to Southwell Festival","gate-to-southwell","2027-07-01","2027-07-04","Eakring Lane, Kirklington, near Newark","Nottinghamshire","East Midlands")
sk("mint-festival","Mint Festival","mint-festival","2027-05-01","2027-05-02","Newsam Green Farm","Leeds","Yorkshire and the Humber")

NAT={"Scotland":"Scotland","Wales":"Wales","Northern Ireland":"Northern Ireland"}
for f in F:
    f.setdefault("nation",NAT.get(f.get("region",""),"England"))

for f in F:
    f.setdefault("dates_basis","festival")
meta={"site":"Price of Festivals","edition":"2027","currency":"GBP","generated":CK,"schema_version":2,
 "fields_null_means":"Not found from a source we trust. Never estimated.",
 "definitions":{"adult":"Cheapest adult weekend (main full-festival) ticket on sale, or last on sale, for the 2027 edition. For camping festivals this is the ticket that includes camping. Partial-weekend tickets are listed as extras.",
   "noncamp":"Cheapest adult full-festival ticket without camping.","day":"Cheapest adult day ticket.",
   "per_day":"adult price divided by the number of days the ticket covers: the days named in the ticket label where it covers fewer days than the festival, otherwise the calendar days in the published festival dates (computed, not sourced).",
   "fees":"included = price shown includes booking fee; extra = page says fees are added; unknown = page does not say."},
 "source_types":{"official":"Festival's own site or its official ticket page","agent":"An official ticket agent's listing","press":"Reputable press","other":"Festival guide or listings site"}}
json.dump({"meta":meta,"festivals":F},open(__import__("pathlib").Path(__file__).resolve().parent.parent/"data"/"festivals.json","w"),indent=1,ensure_ascii=False)
print(len(F),"festivals;",sum(1 for f in F if f["adult"]),"with adult price")
