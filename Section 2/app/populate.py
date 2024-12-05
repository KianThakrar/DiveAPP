from app import app, db
from app.models import DiveSite

# Push the application context
app.app_context().push()

# Create dive site entries
site1 = DiveSite(
    name="Coral Reef Point",
    location="Bahamas",
    description="A vibrant coral reef with colorful marine life, perfect for underwater photography."
)
db.session.add(site1)

site2 = DiveSite(
    name="Turtle Bay",
    location="Hawaii, USA",
    description="Calm waters filled with sea turtles, ideal for beginner divers."
)
db.session.add(site2)

site3 = DiveSite(
    name="Manta Ray Cove",
    location="Fiji",
    description="Known for its population of majestic manta rays gliding effortlessly through the waters."
)
db.session.add(site3)

site4 = DiveSite(
    name="Blue Hole",
    location="Belize",
    description="A stunning sinkhole with crystal-clear waters and fascinating limestone formations."
)
db.session.add(site4)

site5 = DiveSite(
    name="Shark Alley",
    location="South Africa",
    description="An adrenaline-pumping dive with great white sharks in their natural habitat."
)
db.session.add(site5)

site6 = DiveSite(
    name="Crystal Lagoon",
    location="Maldives",
    description="A serene spot with vibrant coral gardens and schools of tropical fish."
)
db.session.add(site6)

site7 = DiveSite(
    name="Seahorse Sanctuary",
    location="Indonesia",
    description="A tranquil dive spot teeming with seahorses and other unique critters."
)
db.session.add(site7)

site8 = DiveSite(
    name="Wreck Haven",
    location="Truk Lagoon, Micronesia",
    description="A diver's paradise with numerous World War II shipwrecks to explore."
)
db.session.add(site8)

site9 = DiveSite(
    name="Underwater Pinnacles",
    location="Palau",
    description="Dramatic underwater rock formations with thriving marine ecosystems."
)
db.session.add(site9)

site10 = DiveSite(
    name="Kelp Forest",
    location="California, USA",
    description="A mesmerizing underwater forest with swaying kelp and diverse marine life."
)
db.session.add(site10)

site11 = DiveSite(
    name="Deep Abyss",
    location="Cayman Islands",
    description="A thrilling wall dive with dramatic drop-offs and incredible visibility."
)
db.session.add(site11)

site12 = DiveSite(
    name="Barracuda Point",
    location="Sipadan, Malaysia",
    description="A hotspot for schooling barracuda and other pelagic species."
)
db.session.add(site12)

site13 = DiveSite(
    name="Sunken Gardens",
    location="Philippines",
    description="An underwater paradise with lush coral gardens and vibrant marine biodiversity."
)
db.session.add(site13)

site14 = DiveSite(
    name="Octopus Hideout",
    location="Japan",
    description="A fascinating dive site where octopuses are commonly spotted in their natural environment."
)
db.session.add(site14)

site15 = DiveSite(
    name="Giant Clam Reef",
    location="Australia",
    description="A reef teeming with vibrant giant clams and a kaleidoscope of marine creatures."
)
db.session.add(site15)

site16 = DiveSite(
    name="Hidden Grotto",
    location="Greece",
    description="A serene underwater cave with stunning light beams and unique rock formations."
)
db.session.add(site16)

site17 = DiveSite(
    name="Penguin Cove",
    location="Galápagos Islands",
    description="A unique dive experience with penguins darting through the water alongside marine iguanas."
)
db.session.add(site17)

site18 = DiveSite(
    name="Rainbow Reef",
    location="Fiji",
    description="A stunning reef bursting with colors and an abundance of marine life."
)
db.session.add(site18)

site19 = DiveSite(
    name="Coral Archway",
    location="Caribbean",
    description="A natural coral archway filled with marine life and an incredible underwater landscape."
)
db.session.add(site19)

site20 = DiveSite(
    name="Crystal Caves",
    location="Bahamas",
    description="A breathtaking dive into underwater caves with stunning stalactites and stalagmites."
)
db.session.add(site20)

site21 = DiveSite(
    name="Stingray City",
    location="Grand Cayman",
    description="A shallow sandbar where divers can interact with friendly stingrays."
)
db.session.add(site21)

site22 = DiveSite(
    name="Golden Reef",
    location="Thailand",
    description="A vibrant reef with golden-hued corals and a variety of reef fish."
)
db.session.add(site22)

site23 = DiveSite(
    name="Silent Shipwreck",
    location="Egypt",
    description="A hauntingly beautiful shipwreck teeming with coral growth and marine life."
)
db.session.add(site23)

site24 = DiveSite(
    name="Whale Shark Bay",
    location="Mexico",
    description="A once-in-a-lifetime opportunity to swim with gentle whale sharks."
)
db.session.add(site24)

site25 = DiveSite(
    name="Neptune's Garden",
    location="Indonesia",
    description="An underwater paradise filled with soft corals and vibrant sea fans."
)
db.session.add(site25)

site26 = DiveSite(
    name="Eel Canyon",
    location="Maldives",
    description="A sandy channel known for its resident garden eels and curious marine life."
)
db.session.add(site26)

site27 = DiveSite(
    name="Fire Coral Ridge",
    location="Red Sea",
    description="An adventurous dive site with unique fire corals and stunning underwater vistas."
)
db.session.add(site27)

site28 = DiveSite(
    name="Frozen Fjord",
    location="Norway",
    description="A cold-water dive with breathtaking underwater ice formations and marine life."
)
db.session.add(site28)

site29 = DiveSite(
    name="Emerald Lagoon",
    location="Bora Bora",
    description="A tranquil lagoon with crystal-clear emerald waters and diverse marine species."
)
db.session.add(site29)

site30 = DiveSite(
    name="Cuttlefish Cove",
    location="Australia",
    description="A mesmerizing dive site where cuttlefish can be observed in their natural habitat."
)
db.session.add(site30)

# Commit the changes to the database
db.session.commit()

print("Dive sites added successfully!")
