# insertData.py
from pymongo import MongoClient
from datetime import datetime, timedelta
from bson.dbref import DBRef
import random

# --- CONNECTION ---
uri = "mongodb+srv://jaskeerat23006:waheguru1313@cluster0.qhch8uk.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri)
db = client['festdb']

# Drop all collections first for clean insert
print("Dropping existing collections...")
collections = ["Accounts", "Users", "Artists", "Organizers", "CrewMember", "Fests", "EventsInFests",
            "Stage", "Tickets", "Sponsors", "Jobs", "Applications", "ActiveTransactions", "CountCollections"]
for coll in collections:
    db[coll].drop()
print("All collections cleared.\n")

# --- ID COUNTER SYSTEM ---
class ID:
    def __init__(self):
        self.counters = {}
    
    def next(self, prefix):
        if prefix not in self.counters:
            self.counters[prefix] = 0
        self.counters[prefix] += 1
        return f"{prefix}{self.counters[prefix]}"

id_gen = ID()

# --- DATA POOLS ---
indian_cities = ["Mumbai", "Delhi", "Bangalore", "Pune", "Hyderabad", "Chennai", "Kolkata", "Jaipur", "Goa", "Ahmedabad", "Chandigarh", "Lucknow", "Indore", "Kochi", "Surat"]
genres_list = ["Bollywood", "Punjabi", "EDM", "Hip-Hop", "Indie", "Rock", "Classical", "Sufi", "Folk", "Pop"]
real_artists = [
    ("Arijit", "", "Singh"), ("Neha", "", "Kakkar"), ("Badshah", "", ""),
    ("Diljit", "", "Dosanjh"), ("AP", "", "Dhillon"), ("Guru", "", "Randhawa"),
    ("Shreya", "", "Ghoshal"), ("AR", "", "Rahman"), ("Honey", "", "Singh"),
    ("Jubin", "", "Nautiyal"), ("Darshan", "", "Raval"), ("Armaan", "", "Malik"),
    ("Sunidhi", "", "Chauhan"), ("Mika", "", "Singh"), ("Vishal", "", "Dadlani"),
    ("Yo Yo", "", "Honey Singh"), ("King", "", ""), ("Karan", "", "Aujla"),
    ("Prateek", "", "Kuhad"), ("Anuv", "", "Jain"), ("Ritviz", "", ""),
    ("When Chai Met Toast", "", ""), ("The Local Train", "", ""), ("Naezy", "", ""),
    ("DIVINE", "", ""), ("Raftaar", "", ""), ("Jonita", "", "Gandhi")
]

# --- 1. INSERT USERS ---
def insert_users():
    users = []
    
    # Safely fetch existing data (even if collections are empty)
    all_artist_ids = [doc["_id"] for doc in db.Artists.find({}, {"_id": 1})]
    all_fest_ids   = [doc["_id"] for doc in db.Fests.find({}, {"_id": 1})]
    all_ticket_docs = list(db.Tickets.find({}, {"_id": 1, "FestId.$id": 1}))  # Get ticket _id + fest reference
    
    # Build map: ticket_id → fest_id
    ticket_to_fest = {}
    for t in all_ticket_docs:
        if "FestId" in t and "$id" in t["FestId"]:
            ticket_to_fest[t["_id"]] = t["FestId"]["$id"]

    name_pool = [
        ("Priya", "Kumari", "Sharma"), ("Rohan", "", "Verma"), ("Neha", "", "Mehta"),
        ("Arjun", "", "Singh"), ("Ananya", "", "Patel"), ("Vikram", "Raj", "Yadav"),
        ("Sia", "", "Gupta"), ("Kabir", "", "Khan"), ("Aisha", "", "Malhotra"),
        ("Riya", "", "Joshi"), ("Siddhant", "", "Reddy"), ("Tanya", "", "Nair"),
        ("Aarav", "", "Singh"), ("Diya", "", "Patel"), ("Reyansh", "", "Kumar"),
        ("Saanvi", "", "Gupta"), ("Ishaan", "", "Mehta"), ("Myra", "", "Joshi"),
        ("Aditya", "", "Verma"), ("Kavya", "", "Reddy"), ("Vihaan", "", "Gupta"),
        ("Zara", "", "Khan"), ("Arnav", "", "Malhotra"), ("Rhea", "", "Joshi")
    ]

    for i in range(1, 31):
        fname, mname, lname = random.choice(name_pool)
        lname = lname or fname

        # ----- Artist behavior -----
        viewed_artists = random.sample(all_artist_ids, min(12, len(all_artist_ids))) if all_artist_ids else []
        fav_artists    = random.sample(viewed_artists, min(4, len(viewed_artists))) if viewed_artists else []

        # ----- Fest behavior (safe sampling) -----
        viewed_fests   = random.sample(all_fest_ids, min(10, len(all_fest_ids))) if all_fest_ids else []
        flagged_fests  = random.sample(viewed_fests, min(3, len(viewed_fests))) if viewed_fests else []

        # ----- Ticket purchases -----
        user_tickets   = random.sample(all_ticket_docs, min(6, len(all_ticket_docs))) if all_ticket_docs else []
        bought_ticket_ids = [t["_id"] for t in user_tickets]
        # Optional: also store which fests they attended
        attended_fest_ids = [ticket_to_fest[tid] for tid in bought_ticket_ids if tid in ticket_to_fest]

        users.append({
            "_id": id_gen.next("user"),
            "Name": {
                "Fname": fname,
                "Mname": mname,
                "Lname": lname
            },
            "ArtistViewed": viewed_artists,
            "FestsViewed": viewed_fests,
            "FavGenre": random.sample(genres_list, random.randint(1, 5)),
            "favArtist": fav_artists,
            "FlagFests": flagged_fests,
            "FestsTickets": bought_ticket_ids,        # Real ticket _ids
            "DOB": datetime(1992 + random.randint(0, 28), random.randint(1, 12), random.randint(1, 28)),
            "Gender": random.choice(["Male", "Female", "Other"])
        })

    db.Users.insert_many(users)
    print(f"Inserted {len(users)} Users with complete realistic data (no errors even if few fests/tickets exist)")


# --- 2. INSERT ARTISTS ---
def insert_artists():
    artists = []
    for fname, mname, lname in real_artists[:27]:
        full_name = f"{fname} {mname} {lname}".strip()
        stage_name = full_name if lname else fname
        artists.append({
            "_id": id_gen.next("artist"),
            "Name": {"Fname": fname, "Mname": mname, "Lname": lname or fname},
            "StageName": stage_name,
            "ContractFee": random.randint(500000, 8000000),
            "Genre": random.sample(genres_list, random.randint(1, 3))
        })
    db.Artists.insert_many(artists)
    print(f"Inserted {len(artists)} Artists (Real Indian Names)")

# --- 3. INSERT ORGANIZERS ---
def insert_organizers():
    orgs = []
    org_names = ["BookMyShow Live", "Zomato Live", "Paytm Insider", "Skillboxes", "SteppinOut", "Social Offline", "NH7 Events", "Mood Indigo IITB", "Rendezvous IITD", "Sunburn Festival", "VH1 Supersonic", "Enchanted Valley Carnival"]
    for name in org_names[:12]:
        orgs.append({
            "_id": id_gen.next("org"),
            "OrgName": name,
            "FestsHosted": []
        })
    db.Organizers.insert_many(orgs)
    print(f"Inserted {len(orgs)} Organizers")

# --- 4. INSERT CREW MEMBERS ---
def insert_crew():
    crew = []
    roles = ["Sound Engineer", "Lighting Tech", "Stage Manager", "Video Director", "Pyro Tech", "Security Lead", "Runner"]
    
    # Real Indian event/festival/venue names for experience
    past_organizations = [
        "Sunburn Festival", "NH7 Weekender", "VH1 Supersonic", "Mood Indigo IIT Bombay",
        "Rendezvous IIT Delhi", "Enchanted Valley Carnival", "Zomato Live", "BookMyShow Live",
        "Goa Sunsplash", "Magnetic Fields Rajasthan", "Echoes of Earth", "Bacardi House Party",
        "Tomorrowland (India Tour)", "Ed Sheeran India Tour 2025", "Coldplay India 2025",
        "Arijit Singh Live", "AP Dhillon Tour", "Diljit Dosanjh Concert", "Lollapalooza India",
        "Hornbill Festival", "Ragafest Mumbai", "SteppinOut Nights", "Social Offline Events"
    ]

    for i in range(20):
        first_name = random.choice(["Rajesh", "Ankit", "Priya", "Vikram", "Sneha", "Manoj", "Divya", "Karan", "Neha", "Sahil", "Rohit", "Pooja", "Arjun", "Kavya", "Aditya", "Shruti", "Nikhil", "Tanya", "Ravi", "Meera"])
        last_name = random.choice(["Kumar", "Sharma", "Verma", "Singh", "Patel", "Reddy", "Mehta", "Joshi", "Nair", "Gupta", "Yadav", "Rao", "Malhotra", "Chauhan", "Jain"])
        
        # Generate 1 to 5 past experiences
        num_exp = random.randint(1, 5)
        experiences = []
        
        for _ in range(num_exp):
            start_year = random.randint(2018, 2024)
            start_month = random.randint(1, 12)
            start_day = random.randint(1, 28)
            start_date = datetime(start_year, start_month, start_day)
            
            # Duration: 1 day to 2 years
            duration_days = random.randint(1, 730)
            end_date = start_date + timedelta(days=duration_days)
            
            # 30% chance it's current job → EndDate = "present"
            if random.random() < 0.3 and end_date > datetime(2025, 1, 1):
                end_str = "present"
            else:
                end_str = end_date.strftime("%Y-%m-%d")
            
            org = random.choice(past_organizations)
            role_in_exp = random.choice(roles + ["Stage Hand", "AV Technician", "Event Coordinator", "Production Assistant"])
            
            experiences.append({
                "StartDate": start_date.strftime("%Y-%m-%d"),
                "EndDate": end_str,
                "Organization": org,
                "Role": role_in_exp,
                "Description": random.choice([
                    "Handled live sound mixing for 10,000+ audience",
                    "Managed LED walls and projection mapping",
                    "Coordinated artist entry and stage transitions",
                    "Executed pyro and SFX cues flawlessly",
                    "Led team of 15 security personnel",
                    "Set up and operated Martin Audio & L-Acoustics systems",
                    "Rigged moving lights and lasers for EDM acts"
                ]),
                "Feedback": random.choice([
                    "Excellent work, highly recommended",
                    "Very professional and punctual",
                    "Outstanding technical skills",
                    "Great team player, will hire again",
                    "Delivered beyond expectations",
                    "Best in class execution"
                ]) if end_str != "present" else None
            })

        crew.append({
            "_id": id_gen.next("crew"),
            "Name": {
                "Fname": first_name,
                "Mname": random.choice(["", "Kumar", "Devi", "Singh", "Raj", "Lal"]) if random.random() > 0.4 else "",
                "Lname": last_name
            },
            "JobTypePreference": random.choice(["Freelance", "Full-Time"]),
            "Gender": random.choice(["Male", "Female", "Other"]),
            "Role": random.choice(roles),
            "Experience": experiences  # Now rich and populated!
        })
    
    db.CrewMember.insert_many(crew)
    print(f"Inserted {len(crew)} Crew Members with realistic work experience")

# --- 5. INSERT ACCOUNTS (with proper DBRef Role) ---
def insert_accounts():
    accounts = []
    # Users
    for i in range(1, 31):
        accounts.append({
            "_id": id_gen.next("acc"),
            "UserName": f"user_{i}",
            "Password": "pass123",
            "ContactNo": [f"9{random.randint(100000000,999999999)}"],
            "Email": f"user{i}@gmail.com",
            "City": random.choice(indian_cities),
            "About": "Music lover from India",
            "Role": DBRef("Users", f"user{i}")
        })
    # Artists
    for i in range(1, 28):
        accounts.append({
            "_id": id_gen.next("acc"),
            "UserName": f"artist_{i}",
            "Password": "artist123",
            "ContactNo": [f"8{random.randint(100000000,999999999)}"],
            "Email": f"artist{i}@music.com",
            "City": random.choice(indian_cities),
            "About": "Official artist account",
            "Role": DBRef("Artists", f"artist{i}")
        })
    # Organizers
    for i in range(1, 13):
        accounts.append({
            "_id": id_gen.next("acc"),
            "UserName": f"org_{i}",
            "Password": "org123",
            "ContactNo": [f"7{random.randint(100000000,999999999)}"],
            "Email": f"org{i}@events.in",
            "City": random.choice(indian_cities),
            "About": "Event management company",
            "Role": DBRef("Organizers", f"org{i}")
        })
    # Crew
    for i in range(1, 21):
        accounts.append({
            "_id": id_gen.next("acc"),
            "UserName": f"crew_{i}",
            "Password": "crew123",
            "ContactNo": [f"6{random.randint(100000000,999999999)}"],
            "Email": f"crew{i}@gig.in",
            "City": random.choice(indian_cities),
            "About": "Professional crew member",
            "Role": DBRef("CrewMember", f"crew{i}")
        })
    db.Accounts.insert_many(accounts)
    print(f"Inserted {len(accounts)} Accounts (Users + Artists + Organizers + Crew)")


# =====================================================
#               PART 2 – REMAINING COLLECTIONS         
# ===================================================== 

# --- 6. INSERT SPONSORS ---
def insert_sponsors():
    sponsors = [
        {"_id": id_gen.next("spon"), "SponsorName": "Pepsi India", "AmountContributed": 0, "Sponsored": []},
        {"_id": id_gen.next("spon"), "SponsorName": "Red Bull India", "AmountContributed": 0, "Sponsored": []},
        {"_id": id_gen.next("spon"), "SponsorName": "JBL by Harman", "AmountContributed": 0, "Sponsored": []},
        {"_id": id_gen.next("spon"), "SponsorName": "Paytm", "AmountContributed": 0, "Sponsored": []},
        {"_id": id_gen.next("spon"), "SponsorName": "boAt", "AmountContributed": 0, "Sponsored": []},
        {"_id": id_gen.next("spon"), "SponsorName": "Kingfisher", "AmountContributed": 0, "Sponsored": []},
        {"_id": id_gen.next("spon"), "SponsorName": "Zomato", "AmountContributed": 0, "Sponsored": []},
        {"_id": id_gen.next("spon"), "SponsorName": "Ola Cabs", "AmountContributed": 0, "Sponsored": []},
        {"_id": id_gen.next("spon"), "SponsorName": "MakeMyTrip", "AmountContributed": 0, "Sponsored": []},
        {"_id": id_gen.next("spon"), "SponsorName": "Bira 91", "AmountContributed": 0, "Sponsored": []},
        {"_id": id_gen.next("spon"), "SponsorName": "Nykaa", "AmountContributed": 0, "Sponsored": []},
        {"_id": id_gen.next("spon"), "SponsorName": "Tinder India", "AmountContributed": 0, "Sponsored": []},
    ]
    db.Sponsors.insert_many(sponsors)
    print(f"Inserted {len(sponsors)} Sponsors")

# --- 7. INSERT FESTS + STAGES + EVENTS + TICKETS + SPONSORSHIPS ---
def insert_fests_and_related():
    fests = []
    stages = []
    events = []
    tickets = []
    sponsor_updates = {spon["_id"]: [] for spon in db.Sponsors.find()}

    fest_data = [
        ("Sunburn Goa 2025", "Goa", "2025-12-28", "2025-12-31", ["EDM", "Techno", "Trance"], ["Beach Access", "VIP Lounge", "Food Court", "Medical", "Shuttle"]),
        ("NH7 Weekender Pune", "Pune", "2025-12-12", "2025-12-14", ["Indie", "Rock", "Hip-Hop", "Pop"], ["Camping", "Food Stalls", "Merch", "WiFi"]),
        ("Enchanted Valley Carnival", "Mumbai", "2025-12-19", "2025-12-21", ["EDM", "Bollywood", "Punjabi"], ["Camping", "Water Park", "Adventure Zone"]),
        ("VH1 Supersonic 2026", "Goa", "2026-02-14", "2026-02-16", ["EDM", "Hip-Hop", "Pop"], ["Beachfront", "After Parties"]),
        ("Mood Indigo IIT Bombay", "Mumbai", "2025-12-24", "2025-12-27", ["Rock", "Indie", "Classical", "EDM"], ["Free Entry", "Workshops", "Food Court"]),
        ("Rendezvous IIT Delhi", "Delhi", "2025-10-17", "2025-10-20", ["Rock", "Bollywood", "EDM"], ["Celebrity Nights", "Food Stalls"]),
        ("Hornbill Festival", "Nagaland", "2025-12-01", "2025-12-10", ["Folk", "Rock", "Cultural"], ["Cultural Shows", "Handicrafts"]),
        ("Magnetic Fields", "Rajasthan", "2025-12-13", "2025-12-15", ["Electronic", "Indie"], ["Desert Camping", "Art Installations"]),
        ("Echoes of Earth Bangalore", "Bangalore", "2025-12-06", "2025-12-07", ["Indie", "Electronic", "Folk"], ["Sustainable Fest", "Art", "Food"]),
        ("Bacardi NH7 Weekender Hyderabad", "Hyderabad", "2025-11-29", "2025-11-30", ["Indie", "Rock", "Hip-Hop"], ["Food Court", "Merch"]),
    ]

    # Pre-fetch data
    all_artists = list(db.Artists.find().sort("_id", 1))
    artist_ids = [a["_id"] for a in all_artists]
    artist_names = [f"{a['Name']['Fname']} {a['Name']['Lname']}".strip() for a in all_artists]

    org_ids = [doc["_id"] for doc in db.Organizers.find()]
    crew_ids = [doc["_id"] for doc in db.CrewMember.find()]
    user_usernames = [f"user_{i}" for i in range(1, 31)]

    event_name_templates = [
        "Sunset Sessions", "Midnight Madness", "Headliner Night", "Closing Ceremony",
        "Bollywood Night", "EDM Drop", "Indie Unplugged", "Punjabi Power Hour", "Rock Revolution"
    ]

    for idx, (name, city, start, end, genres, facilities) in enumerate(fest_data, 1):
        fest_id = id_gen.next("fest")
        org_id = random.choice(org_ids)
        db.Organizers.update_one({"_id": org_id}, {"$push": {"FestsHosted": fest_id}})

        start_date = datetime.strptime(start, "%Y-%m-%d")
        end_date = datetime.strptime(end, "%Y-%m-%d")

        tiers = {
            "General": {"cost": random.choice([1200, 1500, 1800]), "available": random.randint(500, 3000)},
            "VIP": {"cost": random.choice([5000, 8000, 10000]), "available": random.randint(100, 500)},
            "Platinum": {"cost": random.choice([15000, 25000]), "available": random.randint(20, 100)},
        }

        # Temporary list to collect event IDs for this fest
        fest_event_ids = []

        # Stages for this fest
        stage_names = ["Main Stage", "EDM Arena", "Indie Corner", "Bollywood Beats", "After Hours"]
        fest_stages = []
        for sname in random.sample(stage_names, random.randint(2, 4)):
            stage_id = id_gen.next("stage")
            stages.append({
                "_id": stage_id,
                "StageName": sname,
                "FestId": DBRef("Fests", fest_id),
                "Capacity": random.randint(800, 15000),
                "Location": f"{city} Festival Grounds"
            })
            fest_stages.append(stage_id)

        # Events for this fest
        num_events = random.randint(4, 8)
        for _ in range(num_events):
            evt_date = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))
            stage_id = random.choice(fest_stages)
            performing_artists = random.sample(artist_ids, random.randint(1, 3))
            assigned_crew = random.sample(crew_ids, random.randint(2, 5))

            headliner = random.choice(performing_artists)
            headliner_name = artist_names[artist_ids.index(headliner)]
            event_name = random.choice([
                f"{headliner_name} Live",
                f"{headliner_name} & Friends",
                random.choice(event_name_templates)
            ])

            evt_id = id_gen.next("evt")
            fest_event_ids.append(evt_id)  # Collect event ID

            events.append({
                "_id": evt_id,
                "EventName": event_name,
                "FestId": DBRef("Fests", fest_id),
                "ArtistsPerforming": [DBRef("Artists", a) for a in performing_artists],
                "Description": f"Live performance featuring {headliner_name}",
                "EventDate": evt_date,
                "StageId": DBRef("Stage", stage_id),
                "Crewmembers": [DBRef("CrewMember", c) for c in assigned_crew],
                "StartTime": evt_date.replace(hour=random.choice([17,18,19,20,21]), minute=random.choice([0,30])),
                "EndTime": evt_date.replace(hour=random.choice([22,23,0,1,2]), minute=random.choice([0,30]))
            })

            # Sponsorship
            if random.random() > 0.6:
                spon = random.choice(list(sponsor_updates.keys()))
                sponsor_updates[spon].append({
                    "FestId": DBRef("Fests", fest_id),
                    "events": [DBRef("EventsInFests", evt_id)],
                    "amount": random.randint(500000, 3000000)
                })

        # Tickets
        for _ in range(random.randint(10, 30)):
            tier_name = random.choices(list(tiers.keys()), weights=[70, 20, 10])[0]
            if tiers[tier_name]["available"] > 0:
                tickets.append({
                    "_id": id_gen.next("tkt"),
                    "FestId": DBRef("Fests", fest_id),
                    "Tier": tier_name,
                    "Cost": tiers[tier_name]["cost"],
                    "UserName": random.choice(user_usernames),
                    "PurchaseDate": datetime(2025, random.randint(8, 11), random.randint(1, 28))
                })
                tiers[tier_name]["available"] -= 1

        # Finally insert the Fest with embedded Events array
        fests.append({
            "_id": fest_id,
            "FestName": name,
            "Events": fest_event_ids,                    # New embedded field!
            "TicketsAva": sum(t["available"] for t in tiers.values()),
            "Description": f"India's premier {', '.join(genres)} music festival",
            "StartDate": start_date,
            "EndDate": end_date,
            "City": city,
            "Genres": genres,
            "Facilities": facilities,
            "Tier": tiers
        })

    # Bulk insert everything
    db.Fests.insert_many(fests)
    db.Stage.insert_many(stages)
    db.EventsInFests.insert_many(events)
    db.Tickets.insert_many(tickets)

    # Update sponsors
    for spon_id, contributions in sponsor_updates.items():
        if contributions:
            total = sum(c["amount"] for c in contributions)
            db.Sponsors.update_one(
                {"_id": spon_id},
                {"$set": {"AmountContributed": total, "Sponsored": contributions}}
            )

    print(f"Inserted {len(fests)} Fests (with embedded 'Events' array), {len(stages)} Stages, {len(events)} Events, {len(tickets)} Tickets")
    
# --- 8. INSERT JOBS & APPLICATIONS ---
def insert_jobs_and_applications():
    jobs = []
    applications = []

    for _ in range(35):
        job_id = id_gen.next("job")
        org_id = random.choice([doc["_id"] for doc in db.Organizers.find()])
        job_type = random.choice(["Freelance", "Full-Time"])

        jobs.append({
            "_id": job_id,
            "organizer_id": DBRef("Organizers", org_id),
            "title": random.choice(["Sound Engineer", "Lighting Designer", "Stage Manager", "Video Director", "Event Coordinator", "Security Supervisor"]),
            "job_type": job_type,
            "no_of_days": random.randint(3, 15) if job_type == "Freelance" else None,
            "payment": f"₹{random.randint(25,120)}k" if job_type == "Freelance" else f"₹{random.randint(4,12)} LPA",
            "city": random.choice(indian_cities),
            "description": "Looking for experienced crew for upcoming music festival.",
            "date_posted": datetime(2025, random.randint(9,11), random.randint(1,28)),
            "skills_required": random.sample(["AV Setup", "Rigging", "Pyro", "Crowd Management", "Live Mixing", "LED Walls", "Logistics"], random.randint(2,5))
        })

        # Applications
        for _ in range(random.randint(1, 6)):
            crew_id = random.choice([doc["_id"] for doc in db.CrewMember.find()])
            applications.append({
                "_id": id_gen.next("app"),
                "JobId": DBRef("Jobs", job_id),
                "CrewId": DBRef("CrewMember", crew_id),
                "Date": datetime.now() - timedelta(days=random.randint(0, 20)),
                "Status": random.choice(["pending", "accepted", "rejected"])
            })

    db.Jobs.insert_many(jobs)
    db.Applications.insert_many(applications)
    print(f"Inserted {len(jobs)} Jobs & {len(applications)} Applications")

# =====================================================
#       DELETE ALL DATA FROM EXISTING COLLECTIONS
# =====================================================

def clear_all_collections():
    collections_to_clear = [
        "Accounts",
        "Users",
        "Artists",
        "Organizers",
        "CrewMember",
        "Fests",
        "EventsInFests",
        "Stage",
        "Tickets",
        "Sponsors",
        "Jobs",
        "Applications",
        "ActiveTransactions",
        "CountCollections"
    ]
    
    print("Clearing all existing data from collections...")
    deleted_count = 0
    
    for coll_name in collections_to_clear:
        try:
            result = db[coll_name].delete_many({})
            count = result.deleted_count
            if count > 0:
                print(f"  → {coll_name}: {count} documents deleted")
            deleted_count += count
        except Exception as e:
            # Collection might not exist yet — that's fine
            print(f"  → {coll_name}: not found or empty (skipped)")
    
    print(f"\nTotal documents deleted: {deleted_count}")
    print("Database is now clean and ready for fresh insertion!\n")

# =====================================================
#                  MAIN EXECUTION
# =====================================================

if __name__ == "__main__":
    clear_all_collections()

    insert_artists()
    insert_organizers()
    insert_crew()
    insert_sponsors()
    insert_fests_and_related()      # Creates Fests, Stages, Events, Tickets
    insert_jobs_and_applications()

    insert_users()                  # ← Now 100% safe and full
    insert_accounts()               # ← Last (depends on Users, Artists, etc.)

    print("\nDATABASE FULLY POPULATED – READY FOR DEMO!")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %I:%M %p IST')}")


# =====================================================
#                   FINAL EXECUTION
# =====================================================

# if __name__ == "__main__":
#     insert_users()
#     insert_artists()
#     insert_organizers()
#     insert_crew()
#     insert_accounts()
    
#     print("\nSample data inserted successfully with clean _id and real Indian artists!")
#     print(f"Total documents in Accounts: {db.Accounts.count_documents({})}")
#     print(f"Total Artists: {db.Artists.count_documents({})}")

# if __name__ == "__main__":
#     # First part already run? If not, uncomment below:
#     # insert_users()
#     # insert_artists()
#     # insert_organizers()
#     # insert_crew()
#     # insert_accounts()

#     insert_sponsors()
#     insert_fests_and_related()
#     insert_jobs_and_applications()

#     print("\nALL DATA INSERTED SUCCESSFULLY!")
#     print("Summary:")
#     for coll in ["Accounts","Users","Artists","Organizers","CrewMember","Fests","EventsInFests","Stage","Tickets","Sponsors","Jobs","Applications"]:
#         print(f"  {coll}: {db[coll].count_documents({})} documents")