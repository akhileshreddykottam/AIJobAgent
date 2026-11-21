def job_locations(job):
    """Return a job's locations as a list; "location" may be a string or a list."""
    location = job.get("location", [])
    if isinstance(location, str):
        location = [location]

    return [
        item.strip()
        for item in location
        if isinstance(item, str) and item.strip()
    ]


jobs = [
    {
        "title": "Store Assistant",
        "company": "Kiwi",
        "location": "Oslo",
        "skills": ["communication", "customer service"],
        "interests": ["retail", "helping customers", "fashion"]
    },
    {
        "title": "Store Assistant",
        "company": "Nille",
        "location": "Asker",
        "skills": ["communication", "customer service"],
        "interests": ["retail", "home goods", "customer experience"]
    },
    {
        "title": "Cafe Worker",
        "company": "Espresso House",
        "location": "Oslo",
        "skills": ["communication", "baking", "coffee"],
        "interests": ["coffee culture", "baking", "hospitality"]
    },
    {
        "title": "Restaurant Worker",
        "company": "Lille haveli",
        "location": "Asker",
        "skills": ["communication", "cooking"],
        "interests": ["cuisine", "food service", "hospitality"]
    },
    {
        "title": "Coding",
        "company": "Oslo Software company",
        "location": "Oslo",
        "skills": ["communication", "python"],
        "interests": ["software development", "technology", "problem solving"]
    },
    {
        "title": "Coding",
        "company": "Asker Software company",
        "location": "Asker",
        "skills": ["communication", "python", "technology", "team work"],
        "interests": ["software development", "technology", "team collaboration"]
    },
    {
        "title": "Data Analyst",
        "company": "Example Data Works",
        "location": "Oslo",
        "skills": ["python", "sql", "data analysis"],
        "interests": ["data science", "business insights", "analytics"]
    },
    {
        "title": "Frontend Developer",
        "company": "Sample Pixel Studio",
        "location": "Trondheim",
        "skills": ["javascript", "html", "css"],
        "interests": ["web design", "digital products", "accessibility"]
    },
    {
        "title": "IT Support Technician",
        "company": "Example Tech Support",
        "location": "Bergen",
        "skills": ["troubleshooting", "customer service", "computer hardware"],
        "interests": ["technology", "computer systems", "helping people"]
    },
    {
        "title": "Cybersecurity Analyst",
        "company": "Sample Secure Systems",
        "location": "Stavanger",
        "skills": ["network security", "risk assessment", "linux"],
        "interests": ["cyber defense", "privacy", "threat research"]
    },
    {
        "title": "UX Designer",
        "company": "Example User Experience Lab",
        "location": "Oslo",
        "skills": ["figma", "user research", "prototyping"],
        "interests": ["user-centered design", "accessibility", "digital products"]
    },
    {
        "title": "DevOps Engineer",
        "company": "Sample Cloud Operations",
        "location": "Trondheim",
        "skills": ["linux", "docker", "cloud computing"],
        "interests": ["cloud infrastructure", "automation", "service reliability"]
    },
    {
        "title": "Nurse",
        "company": "Example Community Health",
        "location": "Bergen",
        "skills": ["patient care", "communication", "teamwork"],
        "interests": ["community health", "patient advocacy", "wellness"]
    },
    {
        "title": "Medical Secretary",
        "company": "Sample Medical Office",
        "location": "Tromsø",
        "skills": ["scheduling", "medical records", "customer service"],
        "interests": ["healthcare", "medical administration", "patient support"]
    },
    {
        "title": "Physiotherapist",
        "company": "Example Movement Clinic",
        "location": "Kristiansand",
        "skills": ["rehabilitation", "anatomy", "patient care"],
        "interests": ["movement", "rehabilitation", "wellness"]
    },
    {
        "title": "Care Assistant",
        "company": "Sample Caring Hands",
        "location": "Drammen",
        "skills": ["personal care", "empathy", "communication"],
        "interests": ["elder care", "community health", "supporting people"]
    },
    {
        "title": "Dentist",
        "company": "Example Dental Studio",
        "location": "Bodø",
        "skills": ["dentistry", "patient care", "attention to detail"],
        "interests": ["oral health", "patient wellness", "preventive care"]
    },
    {
        "title": "Pharmacist",
        "company": "Sample Pharmacy Services",
        "location": "Ålesund",
        "skills": ["pharmacology", "medication safety", "customer service"],
        "interests": ["medicine", "public health", "patient education"]
    },
    {
        "title": "Primary School Teacher",
        "company": "Example Learning School",
        "location": "Lillehammer",
        "skills": ["lesson planning", "classroom management", "communication"],
        "interests": ["education", "child development", "literacy"]
    },
    {
        "title": "Preschool Assistant",
        "company": "Sample Early Learning",
        "location": "Asker",
        "skills": ["child care", "creativity", "teamwork"],
        "interests": ["early childhood", "play-based learning", "child development"]
    },
    {
        "title": "Teaching Assistant",
        "company": "Example Classroom Support",
        "location": "Fredrikstad",
        "skills": ["student support", "patience", "communication"],
        "interests": ["education", "student success", "inclusive learning"]
    },
    {
        "title": "English Tutor",
        "company": "Sample Language Learning",
        "location": "Oslo",
        "skills": ["english", "tutoring", "writing"],
        "interests": ["languages", "education", "literacy"]
    },
    {
        "title": "Electrician",
        "company": "Example Electrical Services",
        "location": "Stavanger",
        "skills": ["electrical systems", "safety procedures", "troubleshooting"],
        "interests": ["renewable energy", "building systems", "hands-on work"]
    },
    {
        "title": "Carpenter",
        "company": "Sample Woodcraft Builders",
        "location": "Bodø",
        "skills": ["carpentry", "blueprint reading", "woodworking"],
        "interests": ["woodworking", "construction", "sustainable building"]
    },
    {
        "title": "Plumber",
        "company": "Example Pipe and Heat",
        "location": "Drammen",
        "skills": ["plumbing", "pipe fitting", "problem solving"],
        "interests": ["home improvement", "building systems", "hands-on work"]
    },
    {
        "title": "Auto Mechanic",
        "company": "Sample Motor Workshop",
        "location": "Trondheim",
        "skills": ["vehicle repair", "diagnostics", "mechanics"],
        "interests": ["automotive technology", "vehicle restoration", "hands-on work"]
    },
    {
        "title": "HVAC Technician",
        "company": "Example Climate Solutions",
        "location": "Bergen",
        "skills": ["hvac", "maintenance", "troubleshooting"],
        "interests": ["climate control", "energy efficiency", "building systems"]
    },
    {
        "title": "Painter",
        "company": "Sample Fresh Finish",
        "location": "Ålesund",
        "skills": ["painting", "surface preparation", "attention to detail"],
        "interests": ["color and design", "home improvement", "craftsmanship"]
    },
    {
        "title": "Accountant",
        "company": "Example Ledger Partners",
        "location": "Oslo",
        "skills": ["accounting", "excel", "attention to detail"],
        "interests": ["finance", "business strategy", "financial planning"]
    },
    {
        "title": "HR Coordinator",
        "company": "Sample People Operations",
        "location": "Bergen",
        "skills": ["recruitment", "organization", "communication"],
        "interests": ["people development", "workplace culture", "talent development"]
    },
    {
        "title": "Project Coordinator",
        "company": "Example Project Office",
        "location": "Tromsø",
        "skills": ["project management", "scheduling", "teamwork"],
        "interests": ["project delivery", "collaboration", "planning"]
    },
    {
        "title": "Office Administrator",
        "company": "Sample Office Support",
        "location": "Kristiansand",
        "skills": ["organization", "data entry", "communication"],
        "interests": ["workplace organization", "administration", "supporting teams"]
    },
    {
        "title": "Sales Representative",
        "company": "Example Sales Collective",
        "location": "Trondheim",
        "skills": ["sales", "negotiation", "customer service"],
        "interests": ["relationship building", "business development", "market trends"]
    },
    {
        "title": "Warehouse Operator",
        "company": "Sample Store and Ship",
        "location": "Drammen",
        "skills": ["inventory management", "forklift operation", "teamwork"],
        "interests": ["logistics", "supply chain", "warehouse operations"]
    },
    {
        "title": "Delivery Driver",
        "company": "Example Local Delivery",
        "location": "Fredrikstad",
        "skills": ["driving", "navigation", "time management"],
        "interests": ["local travel", "transportation", "community service"]
    },
    {
        "title": "Logistics Coordinator",
        "company": "Sample Freight Planning",
        "location": "Stavanger",
        "skills": ["logistics", "planning", "problem solving"],
        "interests": ["transport networks", "supply chain", "operations planning"]
    },
    {
        "title": "Retail Team Lead",
        "company": "Example Market Team",
        "location": "Bergen",
        "skills": ["leadership", "retail", "customer service"],
        "interests": ["retail", "customer experience", "team leadership"]
    },
    {
        "title": "Hotel Receptionist",
        "company": "Sample Northside Hotel",
        "location": "Tromsø",
        "skills": ["hospitality", "communication", "reservation systems"],
        "interests": ["travel", "guest experience", "hospitality"]
    },
    {
        "title": "Chef",
        "company": "Example Table Kitchen",
        "location": "Bergen",
        "skills": ["cooking", "food safety", "menu planning"],
        "interests": ["cuisine", "food creativity", "hospitality"]
    },
    {
        "title": "Barista",
        "company": "Sample Coffee Corner",
        "location": "Drammen",
        "skills": ["coffee", "customer service", "cash handling"],
        "interests": ["coffee culture", "customer experience", "hospitality"]
    },
    {
        "title": "Event Coordinator",
        "company": "Example Gatherings",
        "location": "Oslo",
        "skills": ["event planning", "organization", "communication"],
        "interests": ["live events", "community gatherings", "event design"]
    },
    {
        "title": "Graphic Designer",
        "company": "Sample Visual Workshop",
        "location": "Kristiansand",
        "skills": ["graphic design", "adobe illustrator", "creativity"],
        "interests": ["visual communication", "branding", "illustration"]
    },
    {
        "title": "Digital Marketing Specialist",
        "company": "Example Online Reach",
        "location": "Oslo",
        "skills": ["digital marketing", "seo", "analytics"],
        "interests": ["online campaigns", "brand strategy", "audience insights"]
    },
    {
        "title": "Content Writer",
        "company": "Sample Story Studio",
        "location": "Ålesund",
        "skills": ["writing", "editing", "content strategy"],
        "interests": ["storytelling", "journalism", "publishing"]
    },
    {
        "title": "Photographer",
        "company": "Example Light and Lens",
        "location": "Trondheim",
        "skills": ["photography", "photo editing", "creativity"],
        "interests": ["visual storytelling", "portraiture", "travel"]
    },
    {
        "title": "Civil Engineer",
        "company": "Sample Infrastructure Design",
        "location": "Stavanger",
        "skills": ["civil engineering", "autocad", "project management"],
        "interests": ["infrastructure", "sustainable cities", "construction"]
    },
    {
        "title": "Mechanical Engineer",
        "company": "Example Mechanical Design",
        "location": "Bodø",
        "skills": ["mechanical engineering", "cad", "problem solving"],
        "interests": ["product design", "robotics", "manufacturing"]
    },
    {
        "title": "Lab Technician",
        "company": "Sample Science Services",
        "location": "Bergen",
        "skills": ["laboratory techniques", "data recording", "safety procedures"],
        "interests": ["scientific research", "experimentation", "public health"]
    },
    {
        "title": "Environmental Consultant",
        "company": "Example Green Advisory",
        "location": "Tromsø",
        "skills": ["environmental science", "research", "report writing"],
        "interests": ["conservation", "climate action", "sustainable development"]
    },
    {
        "title": "Gardener",
        "company": "Sample Urban Gardens",
        "location": "Fredrikstad",
        "skills": ["horticulture", "plant care", "physical fitness"],
        "interests": ["plants", "urban green spaces", "nature"]
    },
    {
        "title": "Security Guard",
        "company": "Example Safe Spaces",
        "location": "Oslo",
        "skills": ["observation", "conflict resolution", "communication"],
        "interests": ["public safety", "community protection", "emergency response"]
    },
    {
        "title": "Cleaner",
        "company": "Sample Clean Environment",
        "location": "Asker",
        "skills": ["cleaning", "time management", "attention to detail"],
        "interests": ["healthy spaces", "sustainability", "practical work"]
    },
    {
        "title": "Customer Support Agent",
        "company": "Example Helpful Answers",
        "location": "Drammen",
        "skills": ["customer service", "communication", "problem solving"],
        "interests": ["helping people", "customer experience", "service improvement"]
    },
    {
        "title": "Fitness Instructor",
        "company": "Sample Active Living",
        "location": "Kristiansand",
        "skills": ["fitness coaching", "motivation", "anatomy"],
        "interests": ["exercise", "wellness", "coaching"]
    },
    {
        "title": "Library Assistant",
        "company": "Example Community Library",
        "location": "Lillehammer",
        "skills": ["cataloging", "organization", "customer service"],
        "interests": ["reading", "community learning", "information access"]
    },
    {
        "title": "Marine Biologist",
        "company": "Sample Ocean Research",
        "location": "Ålesund",
        "skills": ["marine biology", "field research", "data analysis"],
        "interests": ["ocean conservation", "marine ecosystems", "field science"]
    },
    {
        "title": "Renewable Energy Technician",
        "company": "Example Renewable Systems",
        "location": "Stavanger",
        "skills": ["renewable energy", "electrical systems", "maintenance"],
        "interests": ["clean energy", "sustainability", "electrical engineering"]
    },
    {
        "title": "Junior Software Developer",
        "company": "Example Fjord Software",
        "location": "Bergen",
        "skills": ["typescript", "git", "debugging"],
        "interests": ["software development", "open source", "problem solving"]
    },
    {
        "title": "Backend Developer",
        "company": "Sample Northern Code",
        "location": "Trondheim",
        "skills": ["java", "sql", "rest apis"],
        "interests": ["software architecture", "databases", "technology"]
    },
    {
        "title": "Full Stack Developer",
        "company": "Example Stack Studio",
        "location": "Oslo",
        "skills": ["javascript", "react", "node.js"],
        "interests": ["web development", "digital products", "software development"]
    },
    {
        "title": "Mobile App Developer",
        "company": "Sample App Harbour",
        "location": "Stavanger",
        "skills": ["kotlin", "swift", "mobile development"],
        "interests": ["mobile apps", "user experience", "technology"]
    },
    {
        "title": "Software Tester",
        "company": "Example Quality Code Lab",
        "location": ["Kristiansand", "Bergen", "Oslo"],
        "skills": ["test automation", "debugging", "attention to detail"],
        "interests": ["software quality", "automation", "problem solving"]
    },
    {
        "title": "Machine Learning Engineer",
        "company": "Sample Neural Works",
        "location": "Trondheim",
        "skills": ["python", "machine learning", "statistics"],
        "interests": ["artificial intelligence", "data science", "research"]
    },
    {
        "title": "Game Developer",
        "company": "Example Midnight Sun Games",
        "location": "Tromsø",
        "skills": ["c#", "unity", "game design"],
        "interests": ["game development", "interactive media", "creativity"]
    },
    {
        "title": "Embedded Systems Developer",
        "company": "Sample Circuit Coast",
        "location": "Drammen",
        "skills": ["c++", "microcontrollers", "electronics"],
        "interests": ["embedded systems", "robotics", "technology"]
    },
    {
        "title": "Registered Nurse",
        "company": "Example City Hospital",
        "location": "Oslo",
        "skills": ["patient care", "clinical assessment", "medication administration"],
        "interests": ["hospital care", "patient advocacy", "healthcare"]
    },
    {
        "title": "Registered Nurse",
        "company": "Sample Fjord Health Centre",
        "location": "Stavanger",
        "skills": ["patient care", "wound care", "teamwork"],
        "interests": ["community health", "healthcare", "wellness"]
    },
    {
        "title": "Emergency Nurse",
        "company": "Example Rapid Response Hospital",
        "location": "Trondheim",
        "skills": ["triage", "patient care", "stress management"],
        "interests": ["emergency response", "hospital care", "healthcare"]
    },
    {
        "title": "Pediatric Nurse",
        "company": "Sample Little Steps Clinic",
        "location": "Bergen",
        "skills": ["patient care", "child care", "empathy"],
        "interests": ["child development", "healthcare", "family support"]
    },
    {
        "title": "Home Care Nurse",
        "company": "Example Home Visit Care",
        "location": "Kristiansand",
        "skills": ["patient care", "elder care", "time management"],
        "interests": ["elder care", "community health", "supporting people"]
    },
    {
        "title": "Mental Health Nurse",
        "company": "Sample Calm Minds Centre",
        "location": "Tromsø",
        "skills": ["mental health support", "empathy", "patient care"],
        "interests": ["mental wellbeing", "patient advocacy", "wellness"]
    },
    {
        "title": "Nursing Assistant",
        "company": "Example Care Ward Services",
        "location": ["Fredrikstad", "Asker", "Drammen"],
        "skills": ["personal care", "patient care", "teamwork"],
        "interests": ["elder care", "healthcare", "supporting people"]
    },
    {
        "title": "Construction Site Manager",
        "company": "Example Nordic Builders",
        "location": "Oslo",
        "skills": ["site management", "blueprint reading", "safety procedures"],
        "interests": ["construction", "project delivery", "building systems"]
    },
    {
        "title": "Bricklayer",
        "company": "Sample Stone and Mortar",
        "location": "Bergen",
        "skills": ["bricklaying", "blueprint reading", "physical fitness"],
        "interests": ["construction", "craftsmanship", "hands-on work"]
    },
    {
        "title": "Construction Worker",
        "company": "Example Ground Up Construction",
        "location": ["Trondheim", "Oslo", "Drammen"],
        "skills": ["construction", "safety procedures", "teamwork"],
        "interests": ["construction", "hands-on work", "infrastructure"]
    },
    {
        "title": "Structural Engineer",
        "company": "Sample Steel and Beam Consulting",
        "location": "Oslo",
        "skills": ["structural analysis", "autocad", "civil engineering"],
        "interests": ["infrastructure", "sustainable cities", "construction"]
    },
    {
        "title": "Quantity Surveyor",
        "company": "Example Build Cost Advisors",
        "location": "Stavanger",
        "skills": ["cost estimation", "construction", "excel"],
        "interests": ["construction", "project delivery", "finance"]
    },
    {
        "title": "Crane Operator",
        "company": "Sample Skyline Lifting",
        "location": "Drammen",
        "skills": ["crane operation", "safety procedures", "attention to detail"],
        "interests": ["heavy machinery", "construction", "hands-on work"]
    },
    {
        "title": "Roofer",
        "company": "Example Top Cover Roofing",
        "location": "Kristiansand",
        "skills": ["roofing", "safety procedures", "physical fitness"],
        "interests": ["construction", "home improvement", "craftsmanship"]
    },
    {
        "title": "Building Inspector",
        "company": "Sample Safe Structures Authority",
        "location": "Tromsø",
        "skills": ["building codes", "inspection", "report writing"],
        "interests": ["public safety", "construction", "sustainable building"]
    },
    {
        "title": "Architectural Technologist",
        "company": "Example Blueprint Studio",
        "location": "Bergen",
        "skills": ["autocad", "building information modeling", "blueprint reading"],
        "interests": ["architecture", "sustainable building", "building systems"]
    },
    {
        "title": "Heavy Equipment Operator",
        "company": "Sample Earthworks Norway",
        "location": "Bodø",
        "skills": ["excavator operation", "safety procedures", "maintenance"],
        "interests": ["heavy machinery", "infrastructure", "construction"]
    },
    {
        "title": "Welder",
        "company": "Example Steel Fabrication",
        "location": "Ålesund",
        "skills": ["welding", "blueprint reading", "safety procedures"],
        "interests": ["metalwork", "construction", "craftsmanship"]
    },
    {
        "title": "Scaffolder",
        "company": "Sample High Reach Scaffolding",
        "location": "Fredrikstad",
        "skills": ["scaffolding", "safety procedures", "teamwork"],
        "interests": ["construction", "hands-on work", "building systems"]
    }
]
