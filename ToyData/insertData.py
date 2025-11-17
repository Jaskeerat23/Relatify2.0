from pymongo import MongoClient
from datetime import datetime
from bson.dbref import DBRef

# --- CONNECTION ---
uri = "mongodb+srv://jaskeerat23006:waheguru1313@cluster0.qhch8uk.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri)

try:
    client.admin.command('ping')
    print("Successfully connected to MongoDB Atlas!")
except Exception as e:
    print("Connection failed:", e)
    exit()

db = client['festdb']  # Use dedicated DB name
print(f"Using database: {db.name}")

# --- INSERT FUNCTIONS ---

def insert_accounts(db):
    collection = db['Accounts']
    accounts = []

    # ---------- Users ----------
    user_base = [
        ("john_doe", "U1001", "john@gmail.com", "Mumbai"),
        ("priya_sharma", "U1002", "priya@outlook.com", "Delhi"),
        ("neha_m", "U1003", "neha.m@gmail.com", "Chennai"),
        ("vivek_s", "U1004", "vivek.s@yahoo.com", "Hyderabad"),
        ("sneha_nair", "U1005", "sneha.n@live.com", "Kochi"),
        ("rohit_kapoor", "U1006", "rohit.k@gmail.com", "Jaipur"),
        ("aisha_khan", "U1007", "aisha.k@icloud.com", "Lucknow"),
        ("ananya_r", "U1008", "ananya.r@gmail.com", "Kolkata"),
        ("kabir_singh", "U1009", "kabir.s@gmail.com", "Pune"),
        ("riya_patel", "U1010", "riya.p@gmail.com", "Surat"),
        ("siddharth_m", "U1011", "sid.m@gmail.com", "Indore"),
        ("tanya_g", "U1012", "tanya.g@gmail.com", "Chandigarh"),
        ("arjun_malhotra", "U1013", "arjun.m@gmail.com", "Ludhiana"),
        ("meera_k", "U1014", "meera.k@gmail.com", "Nagpur"),
        ("vikas_jain", "U1015", "vikas.j@gmail.com", "Bhopal"),
        ("isha_shah", "U1016", "isha.s@gmail.com", "Vadodara"),
        ("rohan_b", "U1017", "rohan.b@gmail.com", "Rajkot"),
        ("nisha_r", "U1018", "nisha.r@gmail.com", "Nashik"),
        ("aman_t", "U1019", "aman.t@gmail.com", "Aurangabad"),
        ("kavya_l", "U1020", "kavya.l@gmail.com", "Solapur"),
        ("pranav_s", "U1021", "pranav.s@gmail.com", "Amritsar"),
        ("diya_v", "U1022", "diya.v@gmail.com", "Jodhpur"),
        ("yash_m", "U1023", "yash.m@gmail.com", "Gwalior"),
        ("zara_k", "U1024", "zara.k@gmail.com", "Udaipur"),
        ("aarav_p", "U1025", "aarav.p@gmail.com", "Mysore"),
        ("bhavya_s", "U1026", "bhavya.s@gmail.com", "Coimbatore"),
        ("chetan_g", "U1027", "chetan.g@gmail.com", "Madurai"),
        ("disha_r", "U1028", "disha.r@gmail.com", "Visakhapatnam"),
        ("eshan_m", "U1029", "eshan.m@gmail.com", "Vijayawada"),
        ("falguni_s", "U1030", "falguni.s@gmail.com", "Thiruvananthapuram")
    ]
    for i, (username, uid, email, city) in enumerate(user_base, start=1):
        accounts.append({
            "_id": f"acc{i:03d}",
            "UserName": username,
            "UserId": uid,
            "Password": "hashPass",
            "ContactNo": [f"9{i:02d}12345678"],
            "Email": email,
            "City": city,
            "Role": DBRef("Users", f"user{i:03d}")
        })

    # ---------- Artists ----------
    artist_base = [
        ("dj_arjun", "A2001", "dj.arjun@gmail.com", "Mumbai"),
        ("neha_kakkar", "A2002", "neha.kakkar@music.com", "Delhi"),
        ("rahul_v", "A2003", "rahul.v@indie.com", "Bangalore"),
        ("aisha_beats", "A2004", "aisha@beats.com", "Pune"),
        ("vikram_vibes", "A2005", "vikram@vibes.com", "Hyderabad"),
        ("tara_trance", "A2006", "tara@trance.com", "Goa"),
        ("rohan_rock", "A2007", "rohan@rock.com", "Kolkata"),
        ("sana_soul", "A2008", "sana@soul.com", "Chennai"),
        ("karan_k", "A2009", "karan@k.com", "Jaipur"),
        ("pooja_pulse", "A2010", "pooja@pulse.com", "Lucknow"),
        ("adi_beats", "A2011", "adi@beats.com", "Ahmedabad"),
        ("nia_nova", "A2012", "nia@nova.com", "Surat"),
        ("yash_yonder", "A2013", "yash@yonder.com", "Indore"),
        ("zoya_zenith", "A2014", "zoya@zenith.com", "Chandigarh"),
        ("aryan_aura", "A2015", "aryan@aura.com", "Ludhiana"),
        ("bela_blaze", "A2016", "bela@blaze.com", "Nagpur"),
        ("chetan_chill", "A2017", "chetan@chill.com", "Bhopal"),
        ("diya_dawn", "A2018", "diya@dawn.com", "Vadodara"),
        ("eshan_echo", "A2019", "eshan@echo.com", "Rajkot"),
        ("fiza_flow", "A2020", "fiza@flow.com", "Nashik"),
        ("gaurav_groove", "A2021", "gaurav@groove.com", "Aurangabad"),
        ("hina_harmony", "A2022", "hina@harmony.com", "Solapur"),
        ("ishan_indie", "A2023", "ishan@indie.com", "Amritsar"),
        ("jia_jazz", "A2024", "jia@jazz.com", "Jodhpur"),
        ("karan_kinetic", "A2025", "karan@kinetic.com", "Gwalior"),
        ("lara_lights", "A2026", "lara@lights.com", "Udaipur"),
        ("mira_melody", "A2027", "mira@melody.com", "Mysore"),
        ("nikhil_neon", "A2028", "nikhil@neon.com", "Coimbatore"),
        ("ojas_orbit", "A2029", "ojas@orbit.com", "Madurai"),
        ("priya_prism", "A2030", "priya@prism.com", "Visakhapatnam"),
        ("qasim_quest", "A2031", "qasim@quest.com", "Vijayawada"),
        ("rhea_rhythm", "A2032", "rhea@rhythm.com", "Thiruvananthapuram"),
        ("samar_surge", "A2033", "samar@surge.com", "Kochi"),
        ("tia_twilight", "A2034", "tia@twilight.com", "Jaipur"),
        ("uday_uplift", "A2035", "uday@uplift.com", "Lucknow")
    ]
    start = len(accounts) + 1
    for i, (username, uid, email, city) in enumerate(artist_base, start=start):
        accounts.append({
            "_id": f"acc{i:03d}",
            "UserName": username,
            "UserId": uid,
            "Password": "hashArtist",
            "ContactNo": [f"8{i:02d}87654321"],
            "Email": email,
            "City": city,
            "Role": DBRef("Artists", f"artist{i-start+1:03d}")
        })

    # ---------- Organizers ----------
    org_base = [
        ("eventorg_india", "O2001", "org@eventorg.in", "Pune"),
        ("festify_events", "O2002", "info@festify.in", "Mumbai"),
        ("youthfest_org", "O2003", "youthfest@org.in", "Bangalore"),
        ("globalfest_org", "O2004", "global@fest.in", "Delhi"),
        ("goafest_team", "O2005", "goa@fest.in", "Goa"),
        ("indiefest_bangalore", "O2006", "indie@bangalore.in", "Bangalore"),
        ("mumbai_music_co", "O2007", "mumbai@music.co", "Mumbai"),
        ("delhi_nights", "O2008", "delhi@nights.in", "Delhi"),
        ("pune_beats", "O2009", "pune@beats.in", "Pune"),
        ("chennai_vibes", "O2010", "chennai@vibes.in", "Chennai"),
        ("kolkata_jam", "O2011", "kolkata@jam.in", "Kolkata"),
        ("hyderabad_rave", "O2012", "hyd@rave.in", "Hyderabad"),
        ("jaipur_heritage", "O2013", "jaipur@heritage.in", "Jaipur"),
        ("goa_sunset", "O2014", "goa@sunset.in", "Goa"),
        ("bangalore_nightlife", "O2015", "blr@nightlife.in", "Bangalore"),
        ("mumbai_underground", "O2016", "mum@underground.in", "Mumbai")
    ]
    start = len(accounts) + 1
    for i, (username, uid, email, city) in enumerate(org_base, start=start):
        accounts.append({
            "_id": f"acc{i:03d}",
            "UserName": username,
            "UserId": uid,
            "Password": "hashOrg",
            "ContactNo": [f"7{i:02d}11223344"],
            "Email": email,
            "City": city,
            "Role": DBRef("Organizers", f"org{i-start+1:03d}")
        })

    # ---------- Crew ----------
    crew_base = [
        ("crew_rajesh", "C3001", "rajesh.crew@org.in", "Pune"),
        ("crew_sneha", "C3002", "sneha.crew@org.in", "Delhi"),
        ("crew_vikram", "C3003", "vikram@org.in", "Bangalore"),
        ("crew_ankit", "C3004", "ankit.crew@org.in", "Mumbai"),
        ("crew_manish", "C3005", "manish@org.in", "Hyderabad"),
        ("crew_divya", "C3006", "divya.crew@org.in", "Goa"),
        ("crew_sahil", "C3007", "sahil@org.in", "Kolkata"),
        ("crew_nehal", "C3008", "nehal.crew@org.in", "Chennai"),
        ("crew_karan", "C3009", "karan@org.in", "Jaipur"),
        ("crew_tina", "C3010", "tina.crew@org.in", "Lucknow"),
        ("crew_rajat", "C3011", "rajat@org.in", "Ahmedabad"),
        ("crew_priya_c", "C3012", "priya.c@org.in", "Surat"),
        ("crew_aditya", "C3013", "aditya@org.in", "Indore"),
        ("crew_shruti", "C3014", "shruti.crew@org.in", "Chandigarh"),
        ("crew_nikhil", "C3015", "nikhil@org.in", "Ludhiana")
    ]
    start = len(accounts) + 1
    for i, (username, uid, email, city) in enumerate(crew_base, start=start):
        accounts.append({
            "_id": f"acc{i:03d}",
            "UserName": username,
            "UserId": uid,
            "Password": "hashCrew",
            "ContactNo": [f"6{i:02d}55443322"],
            "Email": email,
            "City": city,
            "Role": DBRef("CrewMember", f"crew{i-start+1:03d}")
        })

    # ---------- Sponsors ----------
    spon_base = [
        ("pepsi_india", "S4001", "pepsi@india.com", "Mumbai"),
        ("redbull_india", "S4002", "redbull@india.com", "Delhi"),
        ("jbl_india", "S4003", "jbl@india.com", "Bangalore"),
        ("paytm_official", "S4004", "paytm@corp.in", "Noida"),
        ("boat_official", "S4005", "boat@corp.in", "Mumbai"),
        ("kingfisher_official", "S4006", "kingfisher@corp.in", "Bangalore"),
        ("zomato_official", "S4007", "zomato@corp.in", "Gurgaon"),
        ("ola_official", "S4008", "ola@corp.in", "Bangalore"),
        ("makemytrip_official", "S4009", "mmt@corp.in", "Gurgaon"),
        ("sonymusic_india", "S4010", "sony@music.in", "Mumbai"),
        ("bira91_official", "S4011", "bira@corp.in", "Delhi"),
        ("nykaa_official", "S4012", "nykaa@corp.in", "Mumbai")
    ]
    start = len(accounts) + 1
    for i, (username, uid, email, city) in enumerate(spon_base, start=start):
        accounts.append({
            "_id": f"acc{i:03d}",
            "UserName": username,
            "UserId": uid,
            "Password": "hashSponsor",
            "ContactNo": [f"5{i:02d}99887766"],
            "Email": email,
            "City": city,
            "Role": DBRef("Sponsors", f"spon{i-start+1:03d}")
        })

    result = collection.insert_many(accounts)
    print(f"Accounts: {len(result.inserted_ids)} inserted (30 Users + 35 Artists + 16 Organizers + 15 Crew + 12 Sponsors = 108)")

# def insert_accounts(db):
#     collection = db['Accounts']
#     accounts = [
#         { "_id": "acc001", "UserName": "john_doe", "UserId": "U1001", "Password": "hash123", "ContactNo": ["9876543210"], "Email": "john@gmail.com", "City": "Mumbai", "Role": DBRef("Users", "user001") },
#         { "_id": "acc002", "UserName": "priya_sharma", "UserId": "U1002", "Password": "hash456", "ContactNo": ["9988776655"], "Email": "priya@outlook.com", "City": "Delhi", "Role": DBRef("Users", "user002") },
#         { "_id": "acc003", "UserName": "arjun_k", "UserId": "U1003", "Password": "hash789", "ContactNo": ["7766554433"], "Email": "arjun.k@gmail.com", "City": "Bangalore", "Role": DBRef("Artists", "artist001") },
#         { "_id": "acc004", "UserName": "eventorg_india", "UserId": "O2001", "Password": "org2025", "ContactNo": ["1122334455"], "Email": "org@eventorg.in", "City": "Pune", "Role": DBRef("Organizers", "org001") },
#         { "_id": "acc005", "UserName": "crew_rajesh", "UserId": "C3001", "Password": "crewSafe", "ContactNo": ["9900112233"], "Email": "rajesh.crew@org.in", "City": "Pune", "Role": DBRef("CrewMember", "crew001") },
#         { "_id": "acc006", "UserName": "neha_m", "UserId": "U1004", "Password": "hashNeha", "ContactNo": ["8877665544", "7766554433"], "Email": "neha.m@gmail.com", "City": "Chennai", "Role": DBRef("Users", "user003") },
#         { "_id": "acc007", "UserName": "vivek_s", "UserId": "U1005", "Password": "vivekPass", "ContactNo": ["9012345678"], "Email": "vivek.s@yahoo.com", "City": "Hyderabad", "Role": DBRef("Users", "user004") },
#         { "_id": "acc008", "UserName": "sneha_nair", "UserId": "U1006", "Password": "sneha2025", "ContactNo": ["8098765432"], "Email": "sneha.n@live.com", "City": "Kochi", "Role": DBRef("Users", "user005") },
#         { "_id": "acc009", "UserName": "rohit_kapoor", "UserId": "U1007", "Password": "rohitPass", "ContactNo": ["7012345678"], "Email": "rohit.k@gmail.com", "City": "Jaipur", "Role": DBRef("Users", "user006") },
#         { "_id": "acc010", "UserName": "aisha_khan", "UserId": "U1008", "Password": "aisha123", "ContactNo": ["6012345678"], "Email": "aisha.k@icloud.com", "City": "Lucknow", "Role": DBRef("Users", "user007") },
#         { "_id": "acc011", "UserName": "rahul_v", "UserId": "U1009", "Password": "rahulV123", "ContactNo": ["5012345678"], "Email": "rahul.v@gmail.com", "City": "Ahmedabad", "Role": DBRef("Artists", "artist003") },
#         { "_id": "acc012", "UserName": "festify_events", "UserId": "O2002", "Password": "festify2025", "ContactNo": ["4112233445"], "Email": "info@festify.in", "City": "Mumbai", "Role": DBRef("Organizers", "org002") },
#         { "_id": "acc013", "UserName": "crew_vikram", "UserId": "C3002", "Password": "vikramCrew", "ContactNo": ["3112233445"], "Email": "vikram@org.in", "City": "Delhi", "Role": DBRef("CrewMember", "crew002") },
#         { "_id": "acc014", "UserName": "ananya_r", "UserId": "U1010", "Password": "ananyaPass", "ContactNo": ["2112233445"], "Email": "ananya.r@gmail.com", "City": "Kolkata", "Role": DBRef("Users", "user008") },
#         { "_id": "acc015", "UserName": "kabir_singh", "UserId": "U1011", "Password": "kabir2025", "ContactNo": ["1112233445"], "Email": "kabir.s@gmail.com", "City": "Pune", "Role": DBRef("Users", "user009") },
#         { "_id": "acc016", "UserName": "dj_armaan", "UserId": "U1012", "Password": "armaanDJ", "ContactNo": ["9911223344"], "Email": "dj.armaan@gmail.com", "City": "Goa", "Role": DBRef("Artists", "artist004") },
#         { "_id": "acc017", "UserName": "youthfest_org", "UserId": "O2003", "Password": "youth2025", "ContactNo": ["8811223344"], "Email": "youthfest@org.in", "City": "Bangalore", "Role": DBRef("Organizers", "org003") },
#         { "_id": "acc018", "UserName": "crew_pooja", "UserId": "C3003", "Password": "poojaCrew", "ContactNo": ["7711223344"], "Email": "pooja.crew@org.in", "City": "Mumbai", "Role": DBRef("CrewMember", "crew003") },
#         { "_id": "acc019", "UserName": "riya_patel", "UserId": "U1013", "Password": "riyaPass", "ContactNo": ["6611223344"], "Email": "riya.p@gmail.com", "City": "Surat", "Role": DBRef("Users", "user010") },
#         { "_id": "acc020", "UserName": "siddharth_m", "UserId": "U1014", "Password": "sidPass", "ContactNo": ["5511223344"], "Email": "sid.m@gmail.com", "City": "Indore", "Role": DBRef("Users", "user011") },
#         { "_id": "acc021", "UserName": "tanya_g", "UserId": "U1015", "Password": "tanya2025", "ContactNo": ["4411223344"], "Email": "tanya.g@gmail.com", "City": "Chandigarh", "Role": DBRef("Users", "user012") },
#         { "_id": "acc022", "UserName": "arjun_malhotra", "UserId": "U1016", "Password": "arjunM", "ContactNo": ["3311223344"], "Email": "arjun.m@gmail.com", "City": "Ludhiana", "Role": DBRef("Users", "user013") },
#         { "_id": "acc023", "UserName": "meera_k", "UserId": "U1017", "Password": "meeraPass", "ContactNo": ["2211223344"], "Email": "meera.k@gmail.com", "City": "Nagpur", "Role": DBRef("Users", "user014") },
#         { "_id": "acc024", "UserName": "vikas_jain", "UserId": "U1018", "Password": "vikasJ", "ContactNo": ["1211223344"], "Email": "vikas.j@gmail.com", "City": "Bhopal", "Role": DBRef("Users", "user015") },
#         { "_id": "acc025", "UserName": "isha_shah", "UserId": "U1019", "Password": "isha2025", "ContactNo": ["0111223344"], "Email": "isha.s@gmail.com", "City": "Vadodara", "Role": DBRef("Users", "user016") },
#         { "_id": "acc026", "UserName": "rohan_b", "UserId": "U1020", "Password": "rohanB", "ContactNo": ["9011223344"], "Email": "rohan.b@gmail.com", "City": "Rajkot", "Role": DBRef("Users", "user017") },
#         { "_id": "acc027", "UserName": "nisha_r", "UserId": "U1021", "Password": "nishaR", "ContactNo": ["8011223344"], "Email": "nisha.r@gmail.com", "City": "Nashik", "Role": DBRef("Users", "user018") },
#         { "_id": "acc028", "UserName": "aman_t", "UserId": "U1022", "Password": "amanT", "ContactNo": ["7011223344"], "Email": "aman.t@gmail.com", "City": "Aurangabad", "Role": DBRef("Users", "user019") },
#         { "_id": "acc029", "UserName": "kavya_l", "UserId": "U1023", "Password": "kavyaL", "ContactNo": ["6011223344"], "Email": "kavya.l@gmail.com", "City": "Solapur", "Role": DBRef("Users", "user020") },
#         { "_id": "acc030", "UserName": "pranav_s", "UserId": "U1024", "Password": "pranavS", "ContactNo": ["5011223344"], "Email": "pranav.s@gmail.com", "City": "Amritsar", "Role": DBRef("Users", "user021") },
#         { "_id": "acc031", "UserName": "crew_ankit", "UserId": "C3004", "Password": "ankitCrew", "ContactNo": ["4011223344"], "Email": "ankit.crew@org.in", "City": "Mumbai", "Role": DBRef("CrewMember", "crew004") },
#         { "_id": "acc032", "UserName": "crew_manish", "UserId": "C3005", "Password": "manishC", "ContactNo": ["3011223344"], "Email": "manish@org.in", "City": "Delhi", "Role": DBRef("CrewMember", "crew005") },
#         { "_id": "acc033", "UserName": "crew_divya", "UserId": "C3006", "Password": "divyaC", "ContactNo": ["2011223344"], "Email": "divya.crew@org.in", "City": "Pune", "Role": DBRef("CrewMember", "crew006") },
#         { "_id": "acc034", "UserName": "crew_sahil", "UserId": "C3007", "Password": "sahilC", "ContactNo": ["1011223344"], "Email": "sahil@org.in", "City": "Bangalore", "Role": DBRef("CrewMember", "crew007") },
#         { "_id": "acc035", "UserName": "crew_nehal", "UserId": "C3008", "Password": "nehalC", "ContactNo": ["9011223345"], "Email": "nehal.crew@org.in", "City": "Chennai", "Role": DBRef("CrewMember", "crew008") },
#         { "_id": "acc036", "UserName": "crew_karan", "UserId": "C3009", "Password": "karanC", "ContactNo": ["8011223345"], "Email": "karan@org.in", "City": "Hyderabad", "Role": DBRef("CrewMember", "crew009") },
#         { "_id": "acc037", "UserName": "crew_tina", "UserId": "C3010", "Password": "tinaC", "ContactNo": ["7011223345"], "Email": "tina.crew@org.in", "City": "Kochi", "Role": DBRef("CrewMember", "crew010") },
#         { "_id": "acc038", "UserName": "crew_rajat", "UserId": "C3011", "Password": "rajatC", "ContactNo": ["6011223345"], "Email": "rajat@org.in", "City": "Jaipur", "Role": DBRef("CrewMember", "crew011") },
#         { "_id": "acc039", "UserName": "crew_priya_c", "UserId": "C3012", "Password": "priyaC", "ContactNo": ["5011223345"], "Email": "priya.c@org.in", "City": "Lucknow", "Role": DBRef("CrewMember", "crew012") },
#         { "_id": "acc040", "UserName": "crew_aditya", "UserId": "C3013", "Password": "adityaC", "ContactNo": ["4011223345"], "Email": "aditya@org.in", "City": "Ahmedabad", "Role": DBRef("CrewMember", "crew013") },
#         { "_id": "acc041", "UserName": "crew_shruti", "UserId": "C3014", "Password": "shrutiC", "ContactNo": ["3011223345"], "Email": "shruti.crew@org.in", "City": "Kolkata", "Role": DBRef("CrewMember", "crew014") },
#         { "_id": "acc042", "UserName": "crew_nikhil", "UserId": "C3015", "Password": "nikhilC", "ContactNo": ["2011223345"], "Email": "nikhil@org.in", "City": "Pune", "Role": DBRef("CrewMember", "crew015") },
#         { "_id": "acc043", "UserName": "globalfest_org", "UserId": "O2004", "Password": "global2025", "ContactNo": ["1011223345"], "Email": "global@fest.in", "City": "Delhi", "Role": DBRef("Organizers", "org004") },
#         { "_id": "acc044", "UserName": "goafest_team", "UserId": "O2005", "Password": "goa2025", "ContactNo": ["9011223346"], "Email": "goa@fest.in", "City": "Goa", "Role": DBRef("Organizers", "org005") },
#         { "_id": "acc045", "UserName": "indiefest_bangalore", "UserId": "O2006", "Password": "indie2025", "ContactNo": ["8011223346"], "Email": "indie@bangalore.in", "City": "Bangalore", "Role": DBRef("Organizers", "org006") },
#         { "_id": "acc046", "UserName": "mumbai_music_co", "UserId": "O2007", "Password": "mumbai2025", "ContactNo": ["7011223346"], "Email": "mumbai@music.co", "City": "Mumbai", "Role": DBRef("Organizers", "org007") },
#         { "_id": "acc047", "UserName": "delhi_nights", "UserId": "O2008", "Password": "delhi2025", "ContactNo": ["6011223346"], "Email": "delhi@nights.in", "City": "Delhi", "Role": DBRef("Organizers", "org008") },
#         { "_id": "acc048", "UserName": "pune_beats", "UserId": "O2009", "Password": "pune2025", "ContactNo": ["5011223346"], "Email": "pune@beats.in", "City": "Pune", "Role": DBRef("Organizers", "org009") },
#         { "_id": "acc049", "UserName": "chennai_vibes", "UserId": "O2010", "Password": "chennai2025", "ContactNo": ["4011223346"], "Email": "chennai@vibes.in", "City": "Chennai", "Role": DBRef("Organizers", "org010") },
#         { "_id": "acc050", "UserName": "kolkata_jam", "UserId": "O2011", "Password": "kolkata2025", "ContactNo": ["3011223346"], "Email": "kolkata@jam.in", "City": "Kolkata", "Role": DBRef("Organizers", "org011") },
#         { "_id": "acc051", "UserName": "hyderabad_rave", "UserId": "O2012", "Password": "hyd2025", "ContactNo": ["2011223346"], "Email": "hyd@rave.in", "City": "Hyderabad", "Role": DBRef("Organizers", "org012") },
#         { "_id": "acc052", "UserName": "jaipur_heritage", "UserId": "O2013", "Password": "jaipur2025", "ContactNo": ["1011223346"], "Email": "jaipur@heritage.in", "City": "Jaipur", "Role": DBRef("Organizers", "org013") },
#         { "_id": "acc053", "UserName": "goa_sunset", "UserId": "O2014", "Password": "goaSunset", "ContactNo": ["9011223347"], "Email": "goa@sunset.in", "City": "Goa", "Role": DBRef("Organizers", "org014") },
#         { "_id": "acc054", "UserName": "bangalore_nightlife", "UserId": "O2015", "Password": "blrNight", "ContactNo": ["8011223347"], "Email": "blr@nightlife.in", "City": "Bangalore", "Role": DBRef("Organizers", "org015") },
#         { "_id": "acc055", "UserName": "mumbai_underground", "UserId": "O2016", "Password": "mumUnderground", "ContactNo": ["7011223347"], "Email": "mum@underground.in", "City": "Mumbai", "Role": DBRef("Organizers", "org016") }
#     ]
#     result = collection.insert_many(accounts)
#     print(f"Accounts: {len(result.inserted_ids)} inserted")

def insert_users(db):
    collection = db['Users']
    users = [
        { "_id": "user001", "Name": { "Fname": "John", "Mname": "", "Lname": "Doe" }, "favArtist": ["artist001", "artist003"], "FlagFests": ["fest001", "fest002"], "FestsTickets": ["tkt001", "tkt002"], "DOB": datetime(1998, 5, 14), "Gender": "Male" },
        { "_id": "user002", "Name": { "Fname": "Priya", "Mname": "Rani", "Lname": "Sharma" }, "favArtist": ["artist002"], "FlagFests": ["fest001"], "FestsTickets": ["tkt003"], "DOB": datetime(2000, 11, 22), "Gender": "Female" },
        { "_id": "user003", "Name": { "Fname": "Neha", "Mname": "", "Lname": "Mehta" }, "favArtist": ["artist004", "artist005"], "FlagFests": ["fest003"], "FestsTickets": ["tkt004"], "DOB": datetime(1997, 3, 10), "Gender": "Female" },
        { "_id": "user004", "Name": { "Fname": "Vivek", "Mname": "", "Lname": "Singh" }, "favArtist": ["artist001"], "FlagFests": ["fest002"], "FestsTickets": ["tkt005"], "DOB": datetime(1995, 7, 19), "Gender": "Male" },
        { "_id": "user005", "Name": { "Fname": "Sneha", "Mname": "K", "Lname": "Nair" }, "favArtist": ["artist006"], "FlagFests": ["fest004"], "FestsTickets": ["tkt006"], "DOB": datetime(1999, 12, 1), "Gender": "Female" },
        { "_id": "user006", "Name": { "Fname": "Rohit", "Mname": "", "Lname": "Kapoor" }, "favArtist": ["artist007"], "FlagFests": ["fest005"], "FestsTickets": ["tkt007"], "DOB": datetime(1996, 9, 25), "Gender": "Male" },
        { "_id": "user007", "Name": { "Fname": "Aisha", "Mname": "", "Lname": "Khan" }, "favArtist": ["artist008"], "FlagFests": ["fest006"], "FestsTickets": ["tkt008"], "DOB": datetime(2001, 2, 14), "Gender": "Female" },
        { "_id": "user008", "Name": { "Fname": "Ananya", "Mname": "", "Lname": "Rao" }, "favArtist": ["artist009"], "FlagFests": ["fest007"], "FestsTickets": ["tkt009"], "DOB": datetime(1998, 8, 30), "Gender": "Female" },
        { "_id": "user009", "Name": { "Fname": "Kabir", "Mname": "", "Lname": "Singh" }, "favArtist": ["artist010"], "FlagFests": ["fest008"], "FestsTickets": ["tkt010"], "DOB": datetime(1994, 4, 5), "Gender": "Male" },
        { "_id": "user010", "Name": { "Fname": "Riya", "Mname": "", "Lname": "Patel" }, "favArtist": ["artist011"], "FlagFests": ["fest009"], "FestsTickets": ["tkt011"], "DOB": datetime(2000, 6, 17), "Gender": "Female" },
        { "_id": "user011", "Name": { "Fname": "Siddharth", "Mname": "", "Lname": "Malhotra" }, "favArtist": ["artist012"], "FlagFests": ["fest010"], "FestsTickets": ["tkt012"], "DOB": datetime(1997, 11, 11), "Gender": "Male" },
        { "_id": "user012", "Name": { "Fname": "Tanya", "Mname": "", "Lname": "Gupta" }, "favArtist": ["artist013"], "FlagFests": ["fest011"], "FestsTickets": ["tkt013"], "DOB": datetime(1999, 1, 20), "Gender": "Female" },
        { "_id": "user013", "Name": { "Fname": "Arjun", "Mname": "", "Lname": "Malhotra" }, "favArtist": ["artist014"], "FlagFests": ["fest012"], "FestsTickets": ["tkt014"], "DOB": datetime(1995, 10, 3), "Gender": "Male" },
        { "_id": "user014", "Name": { "Fname": "Meera", "Mname": "", "Lname": "Kumari" }, "favArtist": ["artist015"], "FlagFests": ["fest013"], "FestsTickets": ["tkt015"], "DOB": datetime(2002, 7, 28), "Gender": "Female" },
        { "_id": "user015", "Name": { "Fname": "Vikas", "Mname": "", "Lname": "Jain" }, "favArtist": ["artist016"], "FlagFests": ["fest014"], "FestsTickets": ["tkt016"], "DOB": datetime(1993, 12, 15), "Gender": "Male" },
        { "_id": "user016", "Name": { "Fname": "Isha", "Mname": "", "Lname": "Shah" }, "favArtist": ["artist017"], "FlagFests": ["fest015"], "FestsTickets": ["tkt017"], "DOB": datetime(2000, 5, 9), "Gender": "Female" },
        { "_id": "user017", "Name": { "Fname": "Rohan", "Mname": "", "Lname": "Bose" }, "favArtist": ["artist018"], "FlagFests": ["fest016"], "FestsTickets": ["tkt018"], "DOB": datetime(1998, 3, 22), "Gender": "Male" },
        { "_id": "user018", "Name": { "Fname": "Nisha", "Mname": "", "Lname": "Reddy" }, "favArtist": ["artist019"], "FlagFests": ["fest017"], "FestsTickets": ["tkt019"], "DOB": datetime(1997, 9, 14), "Gender": "Female" },
        { "_id": "user019", "Name": { "Fname": "Aman", "Mname": "", "Lname": "Thakur" }, "favArtist": ["artist020"], "FlagFests": ["fest018"], "FestsTickets": ["tkt020"], "DOB": datetime(1996, 11, 30), "Gender": "Male" },
        { "_id": "user020", "Name": { "Fname": "Kavya", "Mname": "", "Lname": "Luthra" }, "favArtist": ["artist021"], "FlagFests": ["fest019"], "FestsTickets": ["tkt021"], "DOB": datetime(2001, 8, 18), "Gender": "Female" },
        { "_id": "user021", "Name": { "Fname": "Pranav", "Mname": "", "Lname": "Sharma" }, "favArtist": ["artist022"], "FlagFests": ["fest020"], "FestsTickets": ["tkt022"], "DOB": datetime(1994, 2, 25), "Gender": "Male" },
        { "_id": "user022", "Name": { "Fname": "Diya", "Mname": "", "Lname": "Verma" }, "favArtist": ["artist023"], "FlagFests": ["fest021"], "FestsTickets": ["tkt023"], "DOB": datetime(2000, 10, 12), "Gender": "Female" },
        { "_id": "user023", "Name": { "Fname": "Yash", "Mname": "", "Lname": "Mehta" }, "favArtist": ["artist024"], "FlagFests": ["fest022"], "FestsTickets": ["tkt024"], "DOB": datetime(1995, 6, 7), "Gender": "Male" },
        { "_id": "user024", "Name": { "Fname": "Zara", "Mname": "", "Lname": "Khan" }, "favArtist": ["artist025"], "FlagFests": ["fest023"], "FestsTickets": ["tkt025"], "DOB": datetime(1999, 4, 19), "Gender": "Female" },
        { "_id": "user025", "Name": { "Fname": "Aarav", "Mname": "", "Lname": "Patel" }, "favArtist": ["artist026"], "FlagFests": ["fest024"], "FestsTickets": ["tkt026"], "DOB": datetime(1997, 1, 30), "Gender": "Male" },
        { "_id": "user026", "Name": { "Fname": "Bhavya", "Mname": "", "Lname": "Singh" }, "favArtist": ["artist027"], "FlagFests": ["fest025"], "FestsTickets": ["tkt027"], "DOB": datetime(2002, 9, 5), "Gender": "Female" },
        { "_id": "user027", "Name": { "Fname": "Chetan", "Mname": "", "Lname": "Gupta" }, "favArtist": ["artist028"], "FlagFests": ["fest026"], "FestsTickets": ["tkt028"], "DOB": datetime(1996, 7, 21), "Gender": "Male" },
        { "_id": "user028", "Name": { "Fname": "Disha", "Mname": "", "Lname": "Rao" }, "favArtist": ["artist029"], "FlagFests": ["fest027"], "FestsTickets": ["tkt029"], "DOB": datetime(1998, 12, 3), "Gender": "Female" },
        { "_id": "user029", "Name": { "Fname": "Eshan", "Mname": "", "Lname": "Malhotra" }, "favArtist": ["artist030"], "FlagFests": ["fest028"], "FestsTickets": ["tkt030"], "DOB": datetime(1995, 5, 16), "Gender": "Male" },
        { "_id": "user030", "Name": { "Fname": "Falguni", "Mname": "", "Lname": "Shah" }, "favArtist": ["artist031"], "FlagFests": ["fest029"], "FestsTickets": ["tkt031"], "DOB": datetime(2000, 3, 28), "Gender": "Female" }
    ]
    result = collection.insert_many(users)
    print(f"Users: {len(result.inserted_ids)} inserted")
    

def insert_artists(db):
    collection = db['Artists']
    artists = [
        { "_id": "artist001", "Name": { "Fname": "Arjun", "Mname": "", "Lname": "Kumar" }, "StageName": "DJ Arjun", "ContractFee": 750000, "Genre": "EDM" },
        { "_id": "artist002", "Name": { "Fname": "Neha", "Mname": "Devi", "Lname": "Singh" }, "StageName": "Neha Kakkar", "ContractFee": 1200000, "Genre": "Bollywood Pop" },
        { "_id": "artist003", "Name": { "Fname": "Rahul", "Mname": "", "Lname": "Verma" }, "StageName": "Rahul V", "ContractFee": 500000, "Genre": "Indie Rock" },
        { "_id": "artist004", "Name": { "Fname": "Aisha", "Mname": "", "Lname": "Malhotra" }, "StageName": "Aisha Beats", "ContractFee": 600000, "Genre": "Hip-Hop" },
        { "_id": "artist005", "Name": { "Fname": "Vikram", "Mname": "", "Lname": "Rao" }, "StageName": "Vikram Vibes", "ContractFee": 800000, "Genre": "Techno" },
        { "_id": "artist006", "Name": { "Fname": "Tara", "Mname": "", "Lname": "Nair" }, "StageName": "Tara Trance", "ContractFee": 550000, "Genre": "Trance" },
        { "_id": "artist007", "Name": { "Fname": "Rohan", "Mname": "", "Lname": "Patel" }, "StageName": "Rohan Rock", "ContractFee": 450000, "Genre": "Rock" },
        { "_id": "artist008", "Name": { "Fname": "Sana", "Mname": "", "Lname": "Khan" }, "StageName": "Sana Soul", "ContractFee": 700000, "Genre": "Soul" },
        { "_id": "artist009", "Name": { "Fname": "Karan", "Mname": "", "Lname": "Mehta" }, "StageName": "Karan K", "ContractFee": 900000, "Genre": "Pop" },
        { "_id": "artist010", "Name": { "Fname": "Pooja", "Mname": "", "Lname": "Sharma" }, "StageName": "Pooja Pulse", "ContractFee": 480000, "Genre": "Electronic" },
        { "_id": "artist011", "Name": { "Fname": "Aditya", "Mname": "", "Lname": "Singh" }, "StageName": "Adi Beats", "ContractFee": 620000, "Genre": "Hip-Hop" },
        { "_id": "artist012", "Name": { "Fname": "Nia", "Mname": "", "Lname": "Gupta" }, "StageName": "Nia Nova", "ContractFee": 580000, "Genre": "Indie Pop" },
        { "_id": "artist013", "Name": { "Fname": "Yash", "Mname": "", "Lname": "Joshi" }, "StageName": "Yash Yonder", "ContractFee": 510000, "Genre": "Folk" },
        { "_id": "artist014", "Name": { "Fname": "Zoya", "Mname": "", "Lname": "Ali" }, "StageName": "Zoya Zenith", "ContractFee": 670000, "Genre": "Jazz" },
        { "_id": "artist015", "Name": { "Fname": "Aryan", "Mname": "", "Lname": "Verma" }, "StageName": "Aryan Aura", "ContractFee": 730000, "Genre": "EDM" },
        { "_id": "artist016", "Name": { "Fname": "Bela", "Mname": "", "Lname": "Reddy" }, "StageName": "Bela Blaze", "ContractFee": 490000, "Genre": "Rock" },
        { "_id": "artist017", "Name": { "Fname": "Chetan", "Mname": "", "Lname": "Thakur" }, "StageName": "Chetan Chill", "ContractFee": 540000, "Genre": "Lo-Fi" },
        { "_id": "artist018", "Name": { "Fname": "Diya", "Mname": "", "Lname": "Luthra" }, "StageName": "Diya Dawn", "ContractFee": 610000, "Genre": "Pop" },
        { "_id": "artist019", "Name": { "Fname": "Eshan", "Mname": "", "Lname": "Shah" }, "StageName": "Eshan Echo", "ContractFee": 560000, "Genre": "Electronic" },
        { "_id": "artist020", "Name": { "Fname": "Fiza", "Mname": "", "Lname": "Khan" }, "StageName": "Fiza Flow", "ContractFee": 680000, "Genre": "R&B" },
        { "_id": "artist021", "Name": { "Fname": "Gaurav", "Mname": "", "Lname": "Mehta" }, "StageName": "Gaurav Groove", "ContractFee": 590000, "Genre": "Funk" },
        { "_id": "artist022", "Name": { "Fname": "Hina", "Mname": "", "Lname": "Singh" }, "StageName": "Hina Harmony", "ContractFee": 710000, "Genre": "Classical Fusion" },
        { "_id": "artist023", "Name": { "Fname": "Ishan", "Mname": "", "Lname": "Patel" }, "StageName": "Ishan Indie", "ContractFee": 470000, "Genre": "Indie" },
        { "_id": "artist024", "Name": { "Fname": "Jia", "Mname": "", "Lname": "Gupta" }, "StageName": "Jia Jazz", "ContractFee": 640000, "Genre": "Jazz" },
        { "_id": "artist025", "Name": { "Fname": "Karan", "Mname": "", "Lname": "Joshi" }, "StageName": "Karan Kinetic", "ContractFee": 780000, "Genre": "Techno" },
        { "_id": "artist026", "Name": { "Fname": "Lara", "Mname": "", "Lname": "Ali" }, "StageName": "Lara Lights", "ContractFee": 520000, "Genre": "EDM" },
        { "_id": "artist027", "Name": { "Fname": "Mira", "Mname": "", "Lname": "Verma" }, "StageName": "Mira Melody", "ContractFee": 690000, "Genre": "Pop" },
        { "_id": "artist028", "Name": { "Fname": "Nikhil", "Mname": "", "Lname": "Reddy" }, "StageName": "Nikhil Neon", "ContractFee": 530000, "Genre": "Electronic" },
        { "_id": "artist029", "Name": { "Fname": "Ojas", "Mname": "", "Lname": "Thakur" }, "StageName": "Ojas Orbit", "ContractFee": 600000, "Genre": "Trance" },
        { "_id": "artist030", "Name": { "Fname": "Priya", "Mname": "", "Lname": "Luthra" }, "StageName": "Priya Prism", "ContractFee": 720000, "Genre": "Indie Pop" },
        { "_id": "artist031", "Name": { "Fname": "Qasim", "Mname": "", "Lname": "Khan" }, "StageName": "Qasim Quest", "ContractFee": 550000, "Genre": "Hip-Hop" },
        { "_id": "artist032", "Name": { "Fname": "Rhea", "Mname": "", "Lname": "Shah" }, "StageName": "Rhea Rhythm", "ContractFee": 660000, "Genre": "R&B" },
        { "_id": "artist033", "Name": { "Fname": "Samar", "Mname": "", "Lname": "Mehta" }, "StageName": "Samar Surge", "ContractFee": 740000, "Genre": "EDM" },
        { "_id": "artist034", "Name": { "Fname": "Tia", "Mname": "", "Lname": "Singh" }, "StageName": "Tia Twilight", "ContractFee": 500000, "Genre": "Lo-Fi" },
        { "_id": "artist035", "Name": { "Fname": "Uday", "Mname": "", "Lname": "Patel" }, "StageName": "Uday Uplift", "ContractFee": 680000, "Genre": "Rock" }
    ]
    result = collection.insert_many(artists)
    print(f"Artists: {len(result.inserted_ids)} inserted")

def insert_organizers(db):
    collection = db['Organizers']
    organizers = [
        { "_id": "org001", "OrgName": "EventOrg India Pvt Ltd", "FestsHosted": ["fest001", "fest002", "fest005"] },
        { "_id": "org002", "OrgName": "Festify Events", "FestsHosted": ["fest003", "fest006"] },
        { "_id": "org003", "OrgName": "YouthFest Collective", "FestsHosted": ["fest004", "fest007"] },
        { "_id": "org004", "OrgName": "Global Music Co", "FestsHosted": ["fest008", "fest009"] },
        { "_id": "org005", "OrgName": "Goa Sunset Events", "FestsHosted": ["fest010", "fest011"] },
        { "_id": "org006", "OrgName": "IndieFest Bangalore", "FestsHosted": ["fest012"] },
        { "_id": "org007", "OrgName": "Mumbai Music Co", "FestsHosted": ["fest013", "fest014"] },
        { "_id": "org008", "OrgName": "Delhi Nights Productions", "FestsHosted": ["fest015"] },
        { "_id": "org009", "OrgName": "Pune Beats Collective", "FestsHosted": ["fest016", "fest017"] },
        { "_id": "org010", "OrgName": "Chennai Vibes", "FestsHosted": ["fest018"] },
        { "_id": "org011", "OrgName": "Kolkata Jam Sessions", "FestsHosted": ["fest019"] },
        { "_id": "org012", "OrgName": "Hyderabad Rave Crew", "FestsHosted": ["fest020"] },
        { "_id": "org013", "OrgName": "Jaipur Heritage Music", "FestsHosted": ["fest021"] },
        { "_id": "org014", "OrgName": "Goa Sunset Festival", "FestsHosted": ["fest022", "fest023"] },
        { "_id": "org015", "OrgName": "Bangalore Nightlife", "FestsHosted": ["fest024"] },
        { "_id": "org016", "OrgName": "Mumbai Underground", "FestsHosted": ["fest025", "fest026"] }
    ]
    result = collection.insert_many(organizers)
    print(f"Organizers: {len(result.inserted_ids)} inserted")

def insert_crew(db):
    collection = db['CrewMember']
    crew = [
        { "_id": "crew001", "Name": { "Fname": "Rajesh", "Mname": "Kumar", "Lname": "Patel" }, "DOJ": datetime(2023, 6, 15), "Organization": "EventOrg India Pvt Ltd", "Gender": "Male", "Role": "Sound Engineer" },
        { "_id": "crew002", "Name": { "Fname": "Sneha", "Mname": "", "Lname": "Nair" }, "DOJ": datetime(2024, 1, 10), "Organization": "EventOrg India Pvt Ltd", "Gender": "Female", "Role": "Stage Manager" },
        { "_id": "crew003", "Name": { "Fname": "Vikram", "Mname": "", "Lname": "Singh" }, "DOJ": datetime(2023, 9, 20), "Organization": "YouthFest Collective", "Gender": "Male", "Role": "Lighting Technician" },
        { "_id": "crew004", "Name": { "Fname": "Ankit", "Mname": "", "Lname": "Sharma" }, "DOJ": datetime(2022, 11, 5), "Organization": "Festify Events", "Gender": "Male", "Role": "AV Technician" },
        { "_id": "crew005", "Name": { "Fname": "Manish", "Mname": "", "Lname": "Verma" }, "DOJ": datetime(2023, 3, 18), "Organization": "Global Music Co", "Gender": "Male", "Role": "Production Head" },
        { "_id": "crew006", "Name": { "Fname": "Divya", "Mname": "", "Lname": "Joshi" }, "DOJ": datetime(2024, 5, 22), "Organization": "Goa Sunset Events", "Gender": "Female", "Role": "Event Coordinator" },
        { "_id": "crew007", "Name": { "Fname": "Sahil", "Mname": "", "Lname": "Khan" }, "DOJ": datetime(2023, 7, 30), "Organization": "IndieFest Bangalore", "Gender": "Male", "Role": "Security Lead" },
        { "_id": "crew008", "Name": { "Fname": "Nehal", "Mname": "", "Lname": "Reddy" }, "DOJ": datetime(2022, 12, 1), "Organization": "Mumbai Music Co", "Gender": "Female", "Role": "Artist Liaison" },
        { "_id": "crew009", "Name": { "Fname": "Karan", "Mname": "", "Lname": "Mehta" }, "DOJ": datetime(2024, 2, 14), "Organization": "Delhi Nights Productions", "Gender": "Male", "Role": "Logistics Manager" },
        { "_id": "crew010", "Name": { "Fname": "Tina", "Mname": "", "Lname": "Gupta" }, "DOJ": datetime(2023, 10, 25), "Organization": "Pune Beats Collective", "Gender": "Female", "Role": "Ticketing Head" },
        { "_id": "crew011", "Name": { "Fname": "Rajat", "Mname": "", "Lname": "Singh" }, "DOJ": datetime(2024, 4, 8), "Organization": "Chennai Vibes", "Gender": "Male", "Role": "Stage Builder" },
        { "_id": "crew012", "Name": { "Fname": "Priya", "Mname": "C", "Lname": "Luthra" }, "DOJ": datetime(2023, 8, 17), "Organization": "Kolkata Jam Sessions", "Gender": "Female", "Role": "Marketing Lead" },
        { "_id": "crew013", "Name": { "Fname": "Aditya", "Mname": "", "Lname": "Rao" }, "DOJ": datetime(2022, 9, 12), "Organization": "Hyderabad Rave Crew", "Gender": "Male", "Role": "DJ Console Tech" },
        { "_id": "crew014", "Name": { "Fname": "Shruti", "Mname": "", "Lname": "Patel" }, "DOJ": datetime(2024, 6, 20), "Organization": "Jaipur Heritage Music", "Gender": "Female", "Role": "Hospitality Manager" },
        { "_id": "crew015", "Name": { "Fname": "Nikhil", "Mname": "", "Lname": "Shah" }, "DOJ": datetime(2023, 11, 3), "Organization": "Mumbai Underground", "Gender": "Male", "Role": "Visual Effects Lead" }
    ]
    result = collection.insert_many(crew)
    print(f"Crew: {len(result.inserted_ids)} inserted")
    
def insert_fests(db):
    collection = db['Fests']
    fests = [
        { "_id": "fest001", "FestId": "F1001", "FestName": "Mumbai Music Carnival 2025", "Events": ["evt001","evt002","evt003"], "TicketsAva": 4800, "Description": "3-day EDM & Pop fest", "StartDate": datetime(2025, 12, 20), "EndDate": datetime(2025, 12, 22), "Tier": { "VIP": { "cost": 5000, "available": 200 }, "Premium": { "cost": 2500, "available": 800 }, "General": { "cost": 1200, "available": 3800 } } },
        { "_id": "fest002", "FestId": "F1002", "FestName": "Delhi Winter Beats", "Events": ["evt004","evt005"], "TicketsAva": 3200, "Description": "EDM & Hip-Hop", "StartDate": datetime(2025, 12, 28), "EndDate": datetime(2025, 12, 29), "Tier": { "Platinum": { "cost": 8000, "available": 100 }, "Gold": { "cost": 4000, "available": 600 }, "Silver": { "cost": 2000, "available": 2500 } } },
        { "_id": "fest003", "FestId": "F1003", "FestName": "Bangalore Indie Fest", "Events": ["evt006"], "TicketsAva": 1500, "Description": "Indie showcase", "StartDate": datetime(2025, 11, 15), "EndDate": datetime(2025, 11, 15), "Tier": { "EarlyBird": { "cost": 800, "available": 500 }, "Standard": { "cost": 1200, "available": 1000 } } },
        { "_id": "fest004", "FestId": "F1004", "FestName": "Goa Sunset Festival", "Events": ["evt007","evt008"], "TicketsAva": 4000, "Description": "Beach EDM fest", "StartDate": datetime(2025, 12, 26), "EndDate": datetime(2025, 12, 27), "Tier": { "Beachfront": { "cost": 6000, "available": 300 }, "Standard": { "cost": 3000, "available": 3700 } } },
        { "_id": "fest005", "FestId": "F1005", "FestName": "Pune Rockstorm", "Events": ["evt009"], "TicketsAva": 2000, "Description": "Rock music revival", "StartDate": datetime(2025, 11, 22), "EndDate": datetime(2025, 11, 22), "Tier": { "MoshPit": { "cost": 1800, "available": 800 }, "Seated": { "cost": 1000, "available": 1200 } } },
        { "_id": "fest006", "FestId": "F1006", "FestName": "Chennai Pop Fiesta", "Events": ["evt010","evt011"], "TicketsAva": 2800, "Description": "Bollywood pop", "StartDate": datetime(2025, 12, 14), "EndDate": datetime(2025, 12, 15), "Tier": { "FrontRow": { "cost": 4000, "available": 400 }, "General": { "cost": 1800, "available": 2400 } } },
        { "_id": "fest007", "FestId": "F1007", "FestName": "Kolkata Jazz Nights", "Events": ["evt012"], "TicketsAva": 1200, "Description": "Jazz & fusion", "StartDate": datetime(2025, 11, 30), "EndDate": datetime(2025, 11, 30), "Tier": { "VIP": { "cost": 3500, "available": 200 }, "Standard": { "cost": 1500, "available": 1000 } } },
        { "_id": "fest008", "FestId": "F1008", "FestName": "Hyderabad Techno Rave", "Events": ["evt013","evt014"], "TicketsAva": 3500, "Description": "Techno & trance", "StartDate": datetime(2025, 12, 21), "EndDate": datetime(2025, 12, 22), "Tier": { "RaveZone": { "cost": 4500, "available": 500 }, "General": { "cost": 2200, "available": 3000 } } },
        { "_id": "fest009", "FestId": "F1009", "FestName": "Jaipur Folk Fusion", "Events": ["evt015"], "TicketsAva": 1800, "Description": "Folk & classical", "StartDate": datetime(2025, 11, 8), "EndDate": datetime(2025, 11, 8), "Tier": { "Royal": { "cost": 3000, "available": 300 }, "Standard": { "cost": 1200, "available": 1500 } } },
        { "_id": "fest010", "FestId": "F1010", "FestName": "Goa New Year Blast", "Events": ["evt016","evt017"], "TicketsAva": 5000, "Description": "NYE EDM party", "StartDate": datetime(2025, 12, 31), "EndDate": datetime(2026, 1, 1), "Tier": { "NYEVIP": { "cost": 10000, "available": 200 }, "Premium": { "cost": 6000, "available": 800 }, "General": { "cost": 3500, "available": 4000 } } },
        { "_id": "fest011", "FestId": "F1011", "FestName": "Bangalore Hip-Hop Fest", "Events": ["evt018"], "TicketsAva": 2200, "Description": "Rap & hip-hop", "StartDate": datetime(2025, 12, 7), "EndDate": datetime(2025, 12, 7), "Tier": { "Cypher": { "cost": 2500, "available": 500 }, "General": { "cost": 1300, "available": 1700 } } },
        { "_id": "fest012", "FestId": "F1012", "FestName": "Mumbai Indie Unplugged", "Events": ["evt019"], "TicketsAva": 1000, "Description": "Acoustic indie", "StartDate": datetime(2025, 11, 23), "EndDate": datetime(2025, 11, 23), "Tier": { "Unplugged": { "cost": 2000, "available": 1000 } } },
        { "_id": "fest013", "FestId": "F1013", "FestName": "Delhi EDM Drop", "Events": ["evt020","evt021"], "TicketsAva": 4200, "Description": "Massive EDM", "StartDate": datetime(2025, 12, 13), "EndDate": datetime(2025, 12, 14), "Tier": { "DropZone": { "cost": 5500, "available": 600 }, "General": { "cost": 2800, "available": 3600 } } },
        { "_id": "fest014", "FestId": "F1014", "FestName": "Pune Metal Mayhem", "Events": ["evt022"], "TicketsAva": 1600, "Description": "Heavy metal", "StartDate": datetime(2025, 11, 29), "EndDate": datetime(2025, 11, 29), "Tier": { "Mosh": { "cost": 2200, "available": 800 }, "Seated": { "cost": 1400, "available": 800 } } },
        { "_id": "fest015", "FestId": "F1015", "FestName": "Chennai Trance Temple", "Events": ["evt023"], "TicketsAva": 1900, "Description": "Psytrance", "StartDate": datetime(2025, 12, 6), "EndDate": datetime(2025, 12, 6), "Tier": { "Temple": { "cost": 3200, "available": 400 }, "General": { "cost": 1600, "available": 1500 } } },
        { "_id": "fest016", "FestId": "F1016", "FestName": "Kolkata Sufi Nights", "Events": ["evt024"], "TicketsAva": 1100, "Description": "Sufi music", "StartDate": datetime(2025, 11, 16), "EndDate": datetime(2025, 11, 16), "Tier": { "Sufi": { "cost": 2800, "available": 1100 } } },
        { "_id": "fest017", "FestId": "F1017", "FestName": "Hyderabad House Party", "Events": ["evt025"], "TicketsAva": 3000, "Description": "House music", "StartDate": datetime(2025, 12, 20), "EndDate": datetime(2025, 12, 20), "Tier": { "HouseVIP": { "cost": 4800, "available": 500 }, "General": { "cost": 2500, "available": 2500 } } },
        { "_id": "fest018", "FestId": "F1018", "FestName": "Jaipur Royal Beats", "Events": ["evt026"], "TicketsAva": 1400, "Description": "Royal fusion", "StartDate": datetime(2025, 11, 9), "EndDate": datetime(2025, 11, 9), "Tier": { "Royal": { "cost": 4000, "available": 400 }, "Standard": { "cost": 1800, "available": 1000 } } },
        { "_id": "fest019", "FestId": "F1019", "FestName": "Goa Psychedelic Fest", "Events": ["evt027"], "TicketsAva": 2500, "Description": "Psytrance & visuals", "StartDate": datetime(2025, 12, 27), "EndDate": datetime(2025, 12, 27), "Tier": { "Psy": { "cost": 5000, "available": 600 }, "General": { "cost": 2800, "available": 1900 } } },
        { "_id": "fest020", "FestId": "F1020", "FestName": "Bangalore Lo-Fi Lounge", "Events": ["evt028"], "TicketsAva": 900, "Description": "Chill beats", "StartDate": datetime(2025, 11, 30), "EndDate": datetime(2025, 11, 30), "Tier": { "Lounge": { "cost": 2200, "available": 900 } } },
        { "_id": "fest021", "FestId": "F1021", "FestName": "Mumbai Bollywood Nights", "Events": ["evt029"], "TicketsAva": 3800, "Description": "Bollywood live", "StartDate": datetime(2025, 12, 15), "EndDate": datetime(2025, 12, 15), "Tier": { "Star": { "cost": 6000, "available": 500 }, "General": { "cost": 3000, "available": 3300 } } },
        { "_id": "fest022", "FestId": "F1022", "FestName": "Delhi Classical Fusion", "Events": ["evt030"], "TicketsAva": 1300, "Description": "Classical meets modern", "StartDate": datetime(2025, 11, 10), "EndDate": datetime(2025, 11, 10), "Tier": { "Fusion": { "cost": 3500, "available": 1300 } } },
        { "_id": "fest023", "FestId": "F1023", "FestName": "Pune EDM Arena", "Events": ["evt031"], "TicketsAva": 4500, "Description": "Arena EDM", "StartDate": datetime(2025, 12, 21), "EndDate": datetime(2025, 12, 21), "Tier": { "Arena": { "cost": 7000, "available": 700 }, "General": { "cost": 3500, "available": 3800 } } },
        { "_id": "fest024", "FestId": "F1024", "FestName": "Chennai Reggae Fest", "Events": ["evt032"], "TicketsAva": 1700, "Description": "Reggae & dub", "StartDate": datetime(2025, 11, 24), "EndDate": datetime(2025, 11, 24), "Tier": { "Reggae": { "cost": 2400, "available": 1700 } } },
        { "_id": "fest025", "FestId": "F1025", "FestName": "Kolkata Indie Rock", "Events": ["evt033"], "TicketsAva": 1600, "Description": "Indie rock", "StartDate": datetime(2025, 12, 8), "EndDate": datetime(2025, 12, 8), "Tier": { "Rock": { "cost": 2000, "available": 1600 } } },
        { "_id": "fest026", "FestId": "F1026", "FestName": "Hyderabad Drum & Bass", "Events": ["evt034"], "TicketsAva": 2100, "Description": "D&B night", "StartDate": datetime(2025, 12, 19), "EndDate": datetime(2025, 12, 19), "Tier": { "DNB": { "cost": 3800, "available": 400 }, "General": { "cost": 1900, "available": 1700 } } }
    ]
    result = collection.insert_many(fests)
    print(f"Fests: {len(result.inserted_ids)} inserted")

def insert_events(db):
    collection = db['EventsInFests']
    events = [
        { "_id": "evt001", "EventId": "E2001", "EventName": "Sunset EDM Night", "FestId": DBRef("Fests", "fest001"), "ArtistsPerforming": [DBRef("Artists", "artist001"), DBRef("Artists", "artist004")], "Description": "EDM finale", "EventDate": datetime(2025, 12, 22), "StageId": DBRef("Stage", "stage001"), "Crewmembers": [DBRef("CrewMember", "crew001")], "StartTime": datetime(2025, 12, 22, 18, 0), "EndTime": datetime(2025, 12, 22, 23, 0) },
        { "_id": "evt002", "EventId": "E2002", "EventName": "Bollywood Live", "FestId": DBRef("Fests", "fest001"), "ArtistsPerforming": [DBRef("Artists", "artist002")], "Description": "Bollywood hits", "EventDate": datetime(2025, 12, 21), "StageId": DBRef("Stage", "stage002"), "Crewmembers": [DBRef("CrewMember", "crew002")], "StartTime": datetime(2025, 12, 21, 19, 30), "EndTime": datetime(2025, 12, 21, 22, 0) },
        { "_id": "evt003", "EventId": "E2003", "EventName": "Indie Showcase", "FestId": DBRef("Fests", "fest001"), "ArtistsPerforming": [DBRef("Artists", "artist003")], "Description": "Indie bands", "EventDate": datetime(2025, 12, 20), "StageId": DBRef("Stage", "stage003"), "Crewmembers": [DBRef("CrewMember", "crew003")], "StartTime": datetime(2025, 12, 20, 17, 0), "EndTime": datetime(2025, 12, 20, 20, 0) },
        { "_id": "evt004", "EventId": "E2004", "EventName": "Winter EDM Drop", "FestId": DBRef("Fests", "fest002"), "ArtistsPerforming": [DBRef("Artists", "artist001")], "Description": "EDM finale", "EventDate": datetime(2025, 12, 29), "StageId": DBRef("Stage", "stage004"), "Crewmembers": [DBRef("CrewMember", "crew001")], "StartTime": datetime(2025, 12, 29, 20, 0), "EndTime": datetime(2025, 12, 29, 23, 59) },
        { "_id": "evt005", "EventId": "E2005", "EventName": "Hip-Hop Cypher", "FestId": DBRef("Fests", "fest002"), "ArtistsPerforming": [DBRef("Artists", "artist004")], "Description": "Rap battle", "EventDate": datetime(2025, 12, 28), "StageId": DBRef("Stage", "stage005"), "Crewmembers": [DBRef("CrewMember", "crew003")], "StartTime": datetime(2025, 12, 28, 18, 0), "EndTime": datetime(2025, 12, 28, 21, 0) },
        { "_id": "evt006", "EventId": "E2006", "EventName": "Indie Unplugged", "FestId": DBRef("Fests", "fest003"), "ArtistsPerforming": [DBRef("Artists", "artist003")], "Description": "Acoustic", "EventDate": datetime(2025, 11, 15), "StageId": DBRef("Stage", "stage006"), "Crewmembers": [DBRef("CrewMember", "crew002")], "StartTime": datetime(2025, 11, 15, 16, 0), "EndTime": datetime(2025, 11, 15, 19, 0) },
        { "_id": "evt007", "EventId": "E2007", "EventName": "Sunset Beach Party", "FestId": DBRef("Fests", "fest004"), "ArtistsPerforming": [DBRef("Artists", "artist005")], "Description": "EDM on beach", "EventDate": datetime(2025, 12, 26), "StageId": DBRef("Stage", "stage007"), "Crewmembers": [DBRef("CrewMember", "crew006")], "StartTime": datetime(2025, 12, 26, 17, 0), "EndTime": datetime(2025, 12, 26, 22, 0) },
        { "_id": "evt008", "EventId": "E2008", "EventName": "Goa Trance Night", "FestId": DBRef("Fests", "fest004"), "ArtistsPerforming": [DBRef("Artists", "artist006")], "Description": "Psytrance", "EventDate": datetime(2025, 12, 27), "StageId": DBRef("Stage", "stage008"), "Crewmembers": [DBRef("CrewMember", "crew006")], "StartTime": datetime(2025, 12, 27, 20, 0), "EndTime": datetime(2025, 12, 28, 2, 0) },
        { "_id": "evt009", "EventId": "E2009", "EventName": "Rockstorm Main Event", "FestId": DBRef("Fests", "fest005"), "ArtistsPerforming": [DBRef("Artists", "artist007")], "Description": "Rock concert", "EventDate": datetime(2025, 11, 22), "StageId": DBRef("Stage", "stage009"), "Crewmembers": [DBRef("CrewMember", "crew004")], "StartTime": datetime(2025, 11, 22, 18, 0), "EndTime": datetime(2025, 11, 22, 23, 0) },
        { "_id": "evt010", "EventId": "E2010", "EventName": "Pop Fiesta Day 1", "FestId": DBRef("Fests", "fest006"), "ArtistsPerforming": [DBRef("Artists", "artist009")], "Description": "Pop hits", "EventDate": datetime(2025, 12, 14), "StageId": DBRef("Stage", "stage010"), "Crewmembers": [DBRef("CrewMember", "crew008")], "StartTime": datetime(2025, 12, 14, 17, 0), "EndTime": datetime(2025, 12, 14, 21, 0) },
        { "_id": "evt011", "EventId": "E2011", "EventName": "Pop Fiesta Day 2", "FestId": DBRef("Fests", "fest006"), "ArtistsPerforming": [DBRef("Artists", "artist018")], "Description": "Pop finale", "EventDate": datetime(2025, 12, 15), "StageId": DBRef("Stage", "stage010"), "Crewmembers": [DBRef("CrewMember", "crew008")], "StartTime": datetime(2025, 12, 15, 18, 0), "EndTime": datetime(2025, 12, 15, 22, 0) },
        { "_id": "evt012", "EventId": "E2012", "EventName": "Jazz Nights", "FestId": DBRef("Fests", "fest007"), "ArtistsPerforming": [DBRef("Artists", "artist014")], "Description": "Jazz fusion", "EventDate": datetime(2025, 11, 30), "StageId": DBRef("Stage", "stage011"), "Crewmembers": [DBRef("CrewMember", "crew012")], "StartTime": datetime(2025, 11, 30, 19, 0), "EndTime": datetime(2025, 11, 30, 23, 0) },
        { "_id": "evt013", "EventId": "E2013", "EventName": "Techno Rave Night 1", "FestId": DBRef("Fests", "fest008"), "ArtistsPerforming": [DBRef("Artists", "artist005")], "Description": "Techno", "EventDate": datetime(2025, 12, 21), "StageId": DBRef("Stage", "stage012"), "Crewmembers": [DBRef("CrewMember", "crew013")], "StartTime": datetime(2025, 12, 21, 21, 0), "EndTime": datetime(2025, 12, 22, 3, 0) },
        { "_id": "evt014", "EventId": "E2014", "EventName": "Trance Temple", "FestId": DBRef("Fests", "fest008"), "ArtistsPerforming": [DBRef("Artists", "artist006")], "Description": "Trance", "EventDate": datetime(2025, 12, 22), "StageId": DBRef("Stage", "stage012"), "Crewmembers": [DBRef("CrewMember", "crew013")], "StartTime": datetime(2025, 12, 22, 20, 0), "EndTime": datetime(2025, 12, 23, 2, 0) },
        { "_id": "evt015", "EventId": "E2015", "EventName": "Folk Fusion", "FestId": DBRef("Fests", "fest009"), "ArtistsPerforming": [DBRef("Artists", "artist013")], "Description": "Folk & classical", "EventDate": datetime(2025, 11, 8), "StageId": DBRef("Stage", "stage013"), "Crewmembers": [DBRef("CrewMember", "crew014")], "StartTime": datetime(2025, 11, 8, 18, 0), "EndTime": datetime(2025, 11, 8, 22, 0) },
        { "_id": "evt016", "EventId": "E2016", "EventName": "NYE Countdown", "FestId": DBRef("Fests", "fest010"), "ArtistsPerforming": [DBRef("Artists", "artist001"), DBRef("Artists", "artist005")], "Description": "EDM countdown", "EventDate": datetime(2025, 12, 31), "StageId": DBRef("Stage", "stage014"), "Crewmembers": [DBRef("CrewMember", "crew006")], "StartTime": datetime(2025, 12, 31, 20, 0), "EndTime": datetime(2026, 1, 1, 2, 0) },
        { "_id": "evt017", "EventId": "E2017", "EventName": "New Year Sunrise", "FestId": DBRef("Fests", "fest010"), "ArtistsPerforming": [DBRef("Artists", "artist015")], "Description": "Chill EDM", "EventDate": datetime(2026, 1, 1), "StageId": DBRef("Stage", "stage015"), "Crewmembers": [DBRef("CrewMember", "crew006")], "StartTime": datetime(2026, 1, 1, 5, 0), "EndTime": datetime(2026, 1, 1, 8, 0) },
        { "_id": "evt018", "EventId": "E2018", "EventName": "Hip-Hop Cypher", "FestId": DBRef("Fests", "fest011"), "ArtistsPerforming": [DBRef("Artists", "artist004"), DBRef("Artists", "artist011")], "Description": "Rap battle", "EventDate": datetime(2025, 12, 7), "StageId": DBRef("Stage", "stage016"), "Crewmembers": [DBRef("CrewMember", "crew007")], "StartTime": datetime(2025, 12, 7, 17, 0), "EndTime": datetime(2025, 12, 7, 21, 0) },
        { "_id": "evt019", "EventId": "E2019", "EventName": "Indie Unplugged", "FestId": DBRef("Fests", "fest012"), "ArtistsPerforming": [DBRef("Artists", "artist003")], "Description": "Acoustic set", "EventDate": datetime(2025, 11, 23), "StageId": DBRef("Stage", "stage017"), "Crewmembers": [DBRef("CrewMember", "crew008")], "StartTime": datetime(2025, 11, 23, 18, 0), "EndTime": datetime(2025, 11, 23, 21, 0) },
        { "_id": "evt020", "EventId": "E2020", "EventName": "EDM Drop Night 1", "FestId": DBRef("Fests", "fest013"), "ArtistsPerforming": [DBRef("Artists", "artist001")], "Description": "Massive drop", "EventDate": datetime(2025, 12, 13), "StageId": DBRef("Stage", "stage018"), "Crewmembers": [DBRef("CrewMember", "crew009")], "StartTime": datetime(2025, 12, 13, 19, 0), "EndTime": datetime(2025, 12, 13, 23, 59) },
        { "_id": "evt021", "EventId": "E2021", "EventName": "EDM Drop Night 2", "FestId": DBRef("Fests", "fest013"), "ArtistsPerforming": [DBRef("Artists", "artist015")], "Description": "Finale", "EventDate": datetime(2025, 12, 14), "StageId": DBRef("Stage", "stage018"), "Crewmembers": [DBRef("CrewMember", "crew009")], "StartTime": datetime(2025, 12, 14, 20, 0), "EndTime": datetime(2025, 12, 15, 2, 0) },
        { "_id": "evt022", "EventId": "E2022", "EventName": "Metal Mayhem", "FestId": DBRef("Fests", "fest014"), "ArtistsPerforming": [DBRef("Artists", "artist007")], "Description": "Heavy metal", "EventDate": datetime(2025, 11, 29), "StageId": DBRef("Stage", "stage019"), "Crewmembers": [DBRef("CrewMember", "crew010")], "StartTime": datetime(2025, 11, 29, 18, 0), "EndTime": datetime(2025, 11, 29, 23, 0) },
        { "_id": "evt023", "EventId": "E2023", "EventName": "Trance Temple", "FestId": DBRef("Fests", "fest015"), "ArtistsPerforming": [DBRef("Artists", "artist006")], "Description": "Psytrance", "EventDate": datetime(2025, 12, 6), "StageId": DBRef("Stage", "stage020"), "Crewmembers": [DBRef("CrewMember", "crew011")], "StartTime": datetime(2025, 12, 6, 21, 0), "EndTime": datetime(2025, 12, 7, 3, 0) },
        { "_id": "evt024", "EventId": "E2024", "EventName": "Sufi Nights", "FestId": DBRef("Fests", "fest016"), "ArtistsPerforming": [DBRef("Artists", "artist022")], "Description": "Sufi fusion", "EventDate": datetime(2025, 11, 16), "StageId": DBRef("Stage", "stage021"), "Crewmembers": [DBRef("CrewMember", "crew012")], "StartTime": datetime(2025, 11, 16, 19, 0), "EndTime": datetime(2025, 11, 16, 22, 0) },
        { "_id": "evt025", "EventId": "E2025", "EventName": "House Party", "FestId": DBRef("Fests", "fest017"), "ArtistsPerforming": [DBRef("Artists", "artist021")], "Description": "House music", "EventDate": datetime(2025, 12, 20), "StageId": DBRef("Stage", "stage022"), "Crewmembers": [DBRef("CrewMember", "crew013")], "StartTime": datetime(2025, 12, 20, 20, 0), "EndTime": datetime(2025, 12, 21, 2, 0) },
        { "_id": "evt026", "EventId": "E2026", "EventName": "Royal Beats", "FestId": DBRef("Fests", "fest018"), "ArtistsPerforming": [DBRef("Artists", "artist013")], "Description": "Royal fusion", "EventDate": datetime(2025, 11, 9), "StageId": DBRef("Stage", "stage023"), "Crewmembers": [DBRef("CrewMember", "crew014")], "StartTime": datetime(2025, 11, 9, 18, 0), "EndTime": datetime(2025, 11, 9, 22, 0) },
        { "_id": "evt027", "EventId": "E2027", "EventName": "Psychedelic Fest", "FestId": DBRef("Fests", "fest019"), "ArtistsPerforming": [DBRef("Artists", "artist006")], "Description": "Psytrance & visuals", "EventDate": datetime(2025, 12, 27), "StageId": DBRef("Stage", "stage024"), "Crewmembers": [DBRef("CrewMember", "crew006")], "StartTime": datetime(2025, 12, 27, 20, 0), "EndTime": datetime(2025, 12, 28, 4, 0) },
        { "_id": "evt028", "EventId": "E2028", "EventName": "Lo-Fi Lounge", "FestId": DBRef("Fests", "fest020"), "ArtistsPerforming": [DBRef("Artists", "artist017")], "Description": "Chill beats", "EventDate": datetime(2025, 11, 30), "StageId": DBRef("Stage", "stage025"), "Crewmembers": [DBRef("CrewMember", "crew008")], "StartTime": datetime(2025, 11, 30, 17, 0), "EndTime": datetime(2025, 11, 30, 21, 0) },
        { "_id": "evt029", "EventId": "E2029", "EventName": "Bollywood Nights", "FestId": DBRef("Fests", "fest021"), "ArtistsPerforming": [DBRef("Artists", "artist002")], "Description": "Bollywood live", "EventDate": datetime(2025, 12, 15), "StageId": DBRef("Stage", "stage026"), "Crewmembers": [DBRef("CrewMember", "crew009")], "StartTime": datetime(2025, 12, 15, 19, 0), "EndTime": datetime(2025, 12, 15, 23, 0) },
        { "_id": "evt030", "EventId": "E2030", "EventName": "Classical Fusion", "FestId": DBRef("Fests", "fest022"), "ArtistsPerforming": [DBRef("Artists", "artist022")], "Description": "Classical meets modern", "EventDate": datetime(2025, 11, 10), "StageId": DBRef("Stage", "stage027"), "Crewmembers": [DBRef("CrewMember", "crew012")], "StartTime": datetime(2025, 11, 10, 18, 0), "EndTime": datetime(2025, 11, 10, 21, 0) },
        { "_id": "evt031", "EventId": "E2031", "EventName": "EDM Arena", "FestId": DBRef("Fests", "fest023"), "ArtistsPerforming": [DBRef("Artists", "artist001"), DBRef("Artists", "artist015")], "Description": "Arena EDM", "EventDate": datetime(2025, 12, 21), "StageId": DBRef("Stage", "stage028"), "Crewmembers": [DBRef("CrewMember", "crew010")], "StartTime": datetime(2025, 12, 21, 19, 0), "EndTime": datetime(2025, 12, 22, 1, 0) },
        { "_id": "evt032", "EventId": "E2032", "EventName": "Reggae Fest", "FestId": DBRef("Fests", "fest024"), "ArtistsPerforming": [DBRef("Artists", "artist020")], "Description": "Reggae & dub", "EventDate": datetime(2025, 11, 24), "StageId": DBRef("Stage", "stage029"), "Crewmembers": [DBRef("CrewMember", "crew011")], "StartTime": datetime(2025, 11, 24, 17, 0), "EndTime": datetime(2025, 11, 24, 21, 0) },
        { "_id": "evt033", "EventId": "E2033", "EventName": "Indie Rock", "FestId": DBRef("Fests", "fest025"), "ArtistsPerforming": [DBRef("Artists", "artist007")], "Description": "Indie rock", "EventDate": datetime(2025, 12, 8), "StageId": DBRef("Stage", "stage029"), "Crewmembers": [DBRef("CrewMember", "crew015")], "StartTime": datetime(2025, 12, 8, 18, 0), "EndTime": datetime(2025, 12, 8, 22, 0) },
        { "_id": "evt034", "EventId": "E2034", "EventName": "Drum & Bass", "FestId": DBRef("Fests", "fest026"), "ArtistsPerforming": [DBRef("Artists", "artist028")], "Description": "D&B night", "EventDate": datetime(2025, 12, 19), "StageId": DBRef("Stage", "stage030"), "Crewmembers": [DBRef("CrewMember", "crew013")], "StartTime": datetime(2025, 12, 19, 21, 0), "EndTime": datetime(2025, 12, 20, 3, 0) }
    ]

    result = collection.insert_many(events)
    print(f"Inserted {len(result.inserted_ids)} stages")


def insert_stage(db):
    collection = db['Stage']
    stages = [
        { "_id": "stage001", "StageId": "STG3001", "StageName": "Main Arena", "FestId": DBRef("Fests", "fest001"), "Capacity": 5000, "Location": "Juhu Beach, Mumbai" },
        { "_id": "stage002", "StageId": "STG3002", "StageName": "Bollywood Stage", "FestId": DBRef("Fests", "fest001"), "Capacity": 2000, "Location": "Juhu Beach, Mumbai" },
        { "_id": "stage003", "StageId": "STG3003", "StageName": "Indie Corner", "FestId": DBRef("Fests", "fest001"), "Capacity": 800, "Location": "Juhu Beach, Mumbai" },
        { "_id": "stage004", "StageId": "STG3004", "StageName": "Winter Arena", "FestId": DBRef("Fests", "fest002"), "Capacity": 3500, "Location": "India Gate Lawns, Delhi" },
        { "_id": "stage005", "StageId": "STG3005", "StageName": "Hip-Hop Zone", "FestId": DBRef("Fests", "fest002"), "Capacity": 1500, "Location": "India Gate Lawns, Delhi" },
        { "_id": "stage006", "StageId": "STG3006", "StageName": "Indie Unplugged", "FestId": DBRef("Fests", "fest003"), "Capacity": 1500, "Location": "Cubbon Park, Bangalore" },
        { "_id": "stage007", "StageId": "STG3007", "StageName": "Sunset Beach", "FestId": DBRef("Fests", "fest004"), "Capacity": 4000, "Location": "Baga Beach, Goa" },
        { "_id": "stage008", "StageId": "STG3008", "StageName": "Trance Temple", "FestId": DBRef("Fests", "fest004"), "Capacity": 2000, "Location": "Anjuna Beach, Goa" },
        { "_id": "stage009", "StageId": "STG3009", "StageName": "Rockstorm Arena", "FestId": DBRef("Fests", "fest005"), "Capacity": 2000, "Location": "Magarpatta, Pune" },
        { "_id": "stage010", "StageId": "STG3010", "StageName": "Pop Fiesta", "FestId": DBRef("Fests", "fest006"), "Capacity": 2800, "Location": "Marina Beach, Chennai" },
        { "_id": "stage011", "StageId": "STG3011", "StageName": "Jazz Lounge", "FestId": DBRef("Fests", "fest007"), "Capacity": 1200, "Location": "Victoria Memorial, Kolkata" },
        { "_id": "stage012", "StageId": "STG3012", "StageName": "Techno Rave", "FestId": DBRef("Fests", "fest008"), "Capacity": 3500, "Location": "Gachibowli Stadium, Hyderabad" },
        { "_id": "stage013", "StageId": "STG3013", "StageName": "Folk Fusion", "FestId": DBRef("Fests", "fest009"), "Capacity": 1800, "Location": "Amber Fort, Jaipur" },
        { "_id": "stage014", "StageId": "STG3014", "StageName": "NYE Countdown", "FestId": DBRef("Fests", "fest010"), "Capacity": 5000, "Location": "Calangute Beach, Goa" },
        { "_id": "stage015", "StageId": "STG3015", "StageName": "Sunrise Chill", "FestId": DBRef("Fests", "fest010"), "Capacity": 1500, "Location": "Calangute Beach, Goa" },
        { "_id": "stage016", "StageId": "STG3016", "StageName": "Hip-Hop Cypher", "FestId": DBRef("Fests", "fest011"), "Capacity": 2200, "Location": "Electronic City, Bangalore" },
        { "_id": "stage017", "StageId": "STG3017", "StageName": "Indie Unplugged", "FestId": DBRef("Fests", "fest012"), "Capacity": 1000, "Location": "Bandra Fort, Mumbai" },
        { "_id": "stage018", "StageId": "STG3018", "StageName": "EDM Drop", "FestId": DBRef("Fests", "fest013"), "Capacity": 4200, "Location": "Jawaharlal Nehru Stadium, Delhi" },
        { "_id": "stage019", "StageId": "STG3019", "StageName": "Metal Mayhem", "FestId": DBRef("Fests", "fest014"), "Capacity": 1600, "Location": "Koregaon Park, Pune" },
        { "_id": "stage020", "StageId": "STG3020", "StageName": "Trance Temple", "FestId": DBRef("Fests", "fest015"), "Capacity": 1900, "Location": "Elliot's Beach, Chennai" },
        { "_id": "stage021", "StageId": "STG3021", "StageName": "Sufi Nights", "FestId": DBRef("Fests", "fest016"), "Capacity": 1100, "Location": "Prinsep Ghat, Kolkata" },
        { "_id": "stage022", "StageId": "STG3022", "StageName": "House Party", "FestId": DBRef("Fests", "fest017"), "Capacity": 3000, "Location": "Hitech City, Hyderabad" },
        { "_id": "stage023", "StageId": "STG3023", "StageName": "Royal Beats", "FestId": DBRef("Fests", "fest018"), "Capacity": 1400, "Location": "Hawa Mahal, Jaipur" },
        { "_id": "stage024", "StageId": "STG3024", "StageName": "Psychedelic", "FestId": DBRef("Fests", "fest019"), "Capacity": 2500, "Location": "Vagator Beach, Goa" },
        { "_id": "stage025", "StageId": "STG3025", "StageName": "Lo-Fi Lounge", "FestId": DBRef("Fests", "fest020"), "Capacity": 900, "Location": "Indiranagar, Bangalore" },
        { "_id": "stage026", "StageId": "STG3026", "StageName": "Bollywood Nights", "FestId": DBRef("Fests", "fest021"), "Capacity": 3800, "Location": "Gateway of India, Mumbai" },
        { "_id": "stage027", "StageId": "STG3027", "StageName": "Classical Fusion", "FestId": DBRef("Fests", "fest022"), "Capacity": 1300, "Location": "Qutub Minar, Delhi" },
        { "_id": "stage028", "StageId": "STG3028", "StageName": "EDM Arena", "FestId": DBRef("Fests", "fest023"), "Capacity": 4500, "Location": "Balewadi Stadium, Pune" },
        { "_id": "stage029", "StageId": "STG3029", "StageName": "Reggae & Indie", "FestId": DBRef("Fests", "fest024"), "Capacity": 1700, "Location": "Besant Nagar Beach, Chennai" },
        { "_id": "stage030", "StageId": "STG3030", "StageName": "D&B Arena", "FestId": DBRef("Fests", "fest026"), "Capacity": 2100, "Location": "Necklace Road, Hyderabad" }
    ]
    result = collection.insert_many(stages)
    print(f"Stage: {len(result.inserted_ids)} inserted")

def insert_tickets(db):
    collection = db['Tickets']
    tickets = []
    import random
    users = [f"user{str(i).zfill(3)}" for i in range(1, 31)]
    usernames = ["john_doe", "priya_sharma", "neha_m", "vivek_s", "sneha_nair", "rohit_kapoor", "aisha_khan", "ananya_r", "kabir_singh", "riya_patel"]
    tiers_map = {
        "VIP": 5000, "Premium": 2500, "General": 1200, "Platinum": 8000, "Gold": 4000, "Silver": 2000,
        "EarlyBird": 800, "Standard": 1200, "Beachfront": 6000, "MoshPit": 1800, "FrontRow": 4000,
        "Royal": 3000, "NYEVIP": 10000, "Cypher": 2500, "DropZone": 5500, "Temple": 3200,
        "HouseVIP": 4800, "Psy": 5000, "Lounge": 2200, "Star": 6000, "Fusion": 3500, "Arena": 7000,
        "Reggae": 2400, "Rock": 2000, "DNB": 3800
    }

    for i in range(205):
        fest_id = f"fest{random.randint(1,26):03d}"
        tier = random.choice(list(tiers_map.keys()))
        cost = tiers_map[tier]
        username = random.choice(usernames)
        purchase_date = datetime(2025, random.randint(9,11), random.randint(1,28), random.randint(9,20), random.choice([0,15,30,45]))
        tickets.append({
            "_id": f"tkt{str(i+1).zfill(3)}",
            "TicketId": f"TKT{4001+i}",
            "FestId": DBRef("Fests", fest_id),
            "Tier": tier,
            "Cost": cost,
            "UserName": username,
            "PurchaseDate": purchase_date
        })
    result = collection.insert_many(tickets)
    print(f"Tickets: {len(result.inserted_ids)} inserted")

def insert_sponsors(db):
    collection = db['Sponsors']
    sponsors = [
        { "_id": "spon001", "SponsorId": "SPN5001", "SponsorName": "Pepsi India", "AmountContributed": 2500000, "Sponsored": [
            { "FestId": DBRef("Fests", "fest001"), "events": [DBRef("EventsInFests", "evt001")], "amount": 1500000 },
            { "FestId": DBRef("Fests", "fest002"), "events": [DBRef("EventsInFests", "evt004")], "amount": 1000000 }
        ]},
        { "_id": "spon002", "SponsorId": "SPN5002", "SponsorName": "Red Bull", "AmountContributed": 1800000, "Sponsored": [
            { "FestId": DBRef("Fests", "fest004"), "events": [DBRef("EventsInFests", "evt007")], "amount": 1800000 }
        ]},
        { "_id": "spon003", "SponsorId": "SPN5003", "SponsorName": "JBL India", "AmountContributed": 1200000, "Sponsored": [
            { "FestId": DBRef("Fests", "fest008"), "events": [DBRef("EventsInFests", "evt013")], "amount": 1200000 }
        ]},
        { "_id": "spon004", "SponsorId": "SPN5004", "SponsorName": "Paytm", "AmountContributed": 900000, "Sponsored": [
            { "FestId": DBRef("Fests", "fest010"), "events": [DBRef("EventsInFests", "evt016")], "amount": 900000 }
        ]},
        { "_id": "spon005", "SponsorId": "SPN5005", "SponsorName": "Boat", "AmountContributed": 700000, "Sponsored": [
            { "FestId": DBRef("Fests", "fest011"), "events": [DBRef("EventsInFests", "evt018")], "amount": 700000 }
        ]},
        { "_id": "spon006", "SponsorId": "SPN5006", "SponsorName": "Kingfisher", "AmountContributed": 1100000, "Sponsored": [
            { "FestId": DBRef("Fests", "fest013"), "events": [DBRef("EventsInFests", "evt020")], "amount": 1100000 }
        ]},
        { "_id": "spon007", "SponsorId": "SPN5007", "SponsorName": "Zomato", "AmountContributed": 600000, "Sponsored": [
            { "FestId": DBRef("Fests", "fest015"), "events": [DBRef("EventsInFests", "evt023")], "amount": 600000 }
        ]},
        { "_id": "spon008", "SponsorId": "SPN5008", "SponsorName": "Ola", "AmountContributed": 800000, "Sponsored": [
            { "FestId": DBRef("Fests", "fest017"), "events": [DBRef("EventsInFests", "evt025")], "amount": 800000 }
        ]},
        { "_id": "spon009", "SponsorId": "SPN5009", "SponsorName": "MakeMyTrip", "AmountContributed": 950000, "Sponsored": [
            { "FestId": DBRef("Fests", "fest019"), "events": [DBRef("EventsInFests", "evt027")], "amount": 950000 }
        ]},
        { "_id": "spon010", "SponsorId": "SPN5010", "SponsorName": "Sony Music", "AmountContributed": 1300000, "Sponsored": [
            { "FestId": DBRef("Fests", "fest021"), "events": [DBRef("EventsInFests", "evt029")], "amount": 1300000 }
        ]},
        { "_id": "spon011", "SponsorId": "SPN5011", "SponsorName": "Bira 91", "AmountContributed": 750000, "Sponsored": [
            { "FestId": DBRef("Fests", "fest023"), "events": [DBRef("EventsInFests", "evt031")], "amount": 750000 }
        ]},
        { "_id": "spon012", "SponsorId": "SPN5012", "SponsorName": "Nykaa", "AmountContributed": 500000, "Sponsored": [
            { "FestId": DBRef("Fests", "fest011"), "events": [DBRef("EventsInFests", "evt018")], "amount": 500000 }
        ]}
    ]
    result = collection.insert_many(sponsors)
    print(f"Sponsors: {len(result.inserted_ids)} inserted")

# --- MAIN EXECUTION ---
if __name__ == "__main__":
    # Drop DB to avoid duplicates (optional)
    # client.drop_database('festdb')
    insert_accounts(db)
    insert_users(db)
    insert_artists(db)
    insert_organizers(db)
    insert_crew(db)
    insert_fests(db)
    insert_stage(db)
    insert_events(db)
    insert_tickets(db)
    insert_sponsors(db)
    
    print("\nAll data inserted successfully!")
    print(f"Total collections: {len(db.list_collection_names())}")