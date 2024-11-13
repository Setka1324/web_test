import sqlite3

def create_database_schema(db_path):
    """
    Create the relational database schema for storing company data.
    
    Args:
    db_path (str): Path to the SQLite database file.
    """
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    

    
    # Create table for company general information
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS companies (
            bibtex_key TEXT PRIMARY KEY,
            bibtex_type TEXT,
            company_name TEXT,
            description TEXT,
            website TEXT,
            public_private TEXT,
            highlighted_company TEXT,
            founder TEXT,
            ceo TEXT,
            company_number TEXT,
            parent_company TEXT,
            other_known_trading_names TEXT,
            date_added TEXT,
            date_modified TEXT,
            incorporation_date TEXT
        );
    """)
    
    # Create table for headquarters information
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS headquarters (
            company_key TEXT,
            hq_city TEXT,
            hq_country TEXT,
            FOREIGN KEY(company_key) REFERENCES companies(bibtex_key)
        );
    """)
    
    # Create table for addresses
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS addresses (
            company_key TEXT,
            address TEXT,
            previous_address TEXT,
            FOREIGN KEY(company_key) REFERENCES companies(bibtex_key)
        );
    """)
    
    # Create table for operational information
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS operations (
            company_key TEXT,
            offices_in TEXT,
            technology_sold TEXT,
            trade_show TEXT,
            FOREIGN KEY(company_key) REFERENCES companies(bibtex_key)
        );
    """)
    
    # Create table for compliance
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS compliance (
            company_key TEXT,
            eu TEXT,
            nato TEXT,
            wassenaar TEXT,
            oecd TEXT,
            csr TEXT,
            FOREIGN KEY(company_key) REFERENCES companies(bibtex_key)
        );
    """)
    
    # Create table for communications 
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS communications (
            company_key TEXT,
            twitter_handle TEXT,
            telephone TEXT,
            email TEXT,
            FOREIGN KEY(company_key) REFERENCES companies(bibtex_key)
        );
    """)

    # Create table for blogs 
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS blogs (
            company_key TEXT,
            blog TEXT,
            FOREIGN KEY(company_key) REFERENCES companies(bibtex_key)
        );
    """)

    # Create table for news
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS news (
            company_key TEXT,
            news TEXT,
            FOREIGN KEY(company_key) REFERENCES companies(bibtex_key)
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS country_data (
            Country TEXT,
            Incident TEXT
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_tracking (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT,
            page_name TEXT,
            action TEXT,
            detail TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        );
    """)
    
    
    # Commit the changes and close the database connection
    conn.commit()
    conn.close()
create_database_schema("companies.db")
