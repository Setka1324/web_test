import sqlite3


def remove_and_prefix_from_technology_sold(db_path):

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("""
        UPDATE operations
        SET technology_sold = REPLACE(technology_sold, 'and ', '')
        WHERE technology_sold LIKE 'and %'
    """)
    
    conn.commit()
    conn.close()

remove_and_prefix_from_technology_sold("./DB/companies.db")

standard_technologies = {
    "phone monitoring": "Phone Monitoring",
    "internet monitoring": "Internet Monitoring",
    "intrusion": "Intrusion",
    "analysis": "Analysis",
    "monitoring centre": "Monitoring Centre",
    "monitoring centres": "Monitoring Centre",
    "location monitoring": "Location Monitoring",
    "video surveillance": "Video Surveillance",
    "video": "Video Surveillance",
    "biometrics": "Biometrics",
    "equipment": "Equipment",
    "audio surveillance": "Audio Surveillance",
    "counter-surveillance": "Counter-Surveillance",
    "forensics": "Forensics",
    "network": "Network",
    "tactical": "Tactical",
    "communications monitoring": "Communications Monitoring",
    "technical surveillance": "Technical Surveillance",
    "surveillance": "Video Surveillance"
}

def standardize_technology(tech):
    return standard_technologies.get(tech.lower(), tech)

def update_technologies(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Fetch all entries from the operations table
    cursor.execute("SELECT rowid, technology_sold FROM operations")
    rows = cursor.fetchall()
    
    # Standardize the technologies
    updates = []
    for rowid, tech in rows:
        standardized_tech = standardize_technology(tech)
        if standardized_tech != tech:
            updates.append((standardized_tech, rowid))
    
    # Update the database
    cursor.executemany("UPDATE operations SET technology_sold = ? WHERE rowid = ?", updates)
    
    conn.commit()
    conn.close()
    print(f"Updated {len(updates)} rows with standardized technologies.")

update_technologies("./DB/companies.db")

