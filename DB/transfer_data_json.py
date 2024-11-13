import sqlite3
import json

def flatten_list(nested_list):
    """
    Flattens a nested list into a single-level list.
    
    Args:
    nested_list (list): The nested list to be flattened.
    
    Returns:
    list: A single-level list containing all the elements.
    """
    flat_list = []
    for item in nested_list:
        if isinstance(item, list):
            flat_list.extend(flatten_list(item))  # Recursively flatten the list
        else:
            flat_list.append(item)
    return flat_list

def insert_data_from_json_to_db_complete(json_filepath, db_path):
    """
    Parses a JSON file and inserts data into an SQLite database based on the predefined schema,
    handling list types by converting them to single item or string representations, and handling nested lists.
    This version also fills the other tables with foreign key relationships maintained.
    
    Args:
    json_filepath (str): Path to the JSON file containing the entries.
    db_path (str): Path to the SQLite database file.
    """
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Load JSON data from the file
    with open(json_filepath, 'r') as file:
        data = json.load(file)
    
    # Iterate over each entry in the JSON data
    for entry in data:
        # Correct the 'incorperation_date' typo
        if 'incorperation_date' in entry:
            entry['incorporation_date'] = entry.pop('incorperation_date')

        # Flatten lists and handle nested lists
        for key in entry.keys():
            if isinstance(entry[key], list):
                flat_list = flatten_list(entry[key])
                entry[key] = ', '.join(str(item) for item in flat_list) if flat_list else None

        # Insert data into the companies table
        companies_data = (
            entry.get('bibtex_key', None),
            entry.get('bibtex_type', None),
            entry.get('company_name', None),
            entry.get('description', None),
            entry.get('website', None),
            entry.get('public_private', None),
            entry.get('highlighted_company', None),
            entry.get('founder', None),
            entry.get('ceo', None),
            entry.get('company_number', None),
            entry.get('parent_company', None),
            entry.get('other_known_trading_names', None),
            entry.get('date_added', None),
            entry.get('date_modified', None),
            entry.get('incorporation_date', None)
        )
        cursor.execute("""
            INSERT INTO companies VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, companies_data)

        # Insert data into the headquarters table
        
        headquarters_data = (
        entry.get('bibtex_key', None),
        entry.get('hq_city', None),
        entry.get('hq_country', None)
        )
        cursor.execute("""
            INSERT INTO headquarters (company_key, hq_city, hq_country) VALUES (?, ?, ?)
        """, headquarters_data)

        if ('hq_2_city' in entry and entry['hq_2_city']) and ('hq_2_country' in entry and entry['hq_2_country']):

            cursor.execute("""
                INSERT INTO headquarters (company_key, hq_city, hq_country) VALUES (?, ?, ?)
            """, (entry.get('bibtex_key', None),
            entry.get('hq_2_city', None),
            entry.get('hq_2_country', None)))
                
        elif 'hq_2_city' in entry and entry['hq_2_city']:
                
            cursor.execute("""
                INSERT INTO headquarters (company_key, hq_city, hq_country) VALUES (?, ?, ?)
            """, (entry.get('bibtex_key', None),
            entry.get('hq_2_city', None),
            None))
            
        elif 'hq_2_country' in entry and entry['hq_2_country']:

            cursor.execute("""
                INSERT INTO headquarters (company_key, hq_city, hq_country) VALUES (?, ?, ?)
            """, (entry.get('bibtex_key', None),
            None,
            entry.get('hq_2_country', None)))

        

        # Insert data into the addresses table
        address = entry.get('address', None)
        if address is not None:
            # Replace <br /> with ; and split by ; then reverse the list
            address_parts = address.replace("<br />", ";").split(';')
            address_parts.reverse()  # Reverse the list in place
            # Join the parts back with "; " and ensure each part is treated as a string
            formatted_address = "; ".join(map(str, address_parts))[2:]
        else:
            formatted_address = None

        addresses_data = (
            entry.get('bibtex_key', None),
            formatted_address,
            entry.get('previous_address', None)
        )

        cursor.execute("""
            INSERT INTO addresses (company_key, address, 'previous_address') VALUES (?, ?, ?)
        """, addresses_data)

        # Insert data into the operations table
        if 'technology_sold' in entry and entry['technology_sold']:

            # technology_sold is a string with technologies separated by commas
            technologies = entry['technology_sold'].split(', ')
            for technology in technologies:
                operations_data = (
                    entry.get('bibtex_key', None),
                    entry.get('offices_in', None),
                    technology,
                    entry.get('trade_show', None)
                )
                cursor.execute("""
                    INSERT INTO operations (company_key, offices_in, technology_sold, trade_show) VALUES (?, ?, ?, ?)
                """, operations_data)

        # Insert data into the commpliance table
        compliance_data = (
            entry.get('bibtex_key', None),
            entry.get('eu', None),
            entry.get('nato', None),
            entry.get('wassenaar', None),
            entry.get('oecd', None),
            entry.get('csr', None)
        )
        cursor.execute("""
            INSERT INTO compliance (company_key, eu, nato, wassenaar, oecd, csr) VALUES (?, ?, ?, ?, ?, ?)
        """, compliance_data)

        # Insert data into the communications table
        communications_data = (
            entry.get('bibtex_key', None),
            entry.get('twitter_handle', None),
            entry.get('telephone', None),
            entry.get('email', None)
        )

        cursor.execute("""
            INSERT INTO communications (company_key, twitter_handle, telephone, email) VALUES (?, ?, ?, ?)
        """, communications_data)

        # Insert data into the blogs table
        for blog in range(1,7):

            bloq_key = 'blog_'+str(blog)
            if bloq_key in entry and entry[bloq_key].strip():


                blogs_data = (
                    entry.get('bibtex_key', None),
                    entry.get(bloq_key, None),
                )

                cursor.execute("""
                    INSERT INTO blogs (company_key, blog) VALUES (?, ?)
                """, blogs_data)

        # Insert data into the news table
        for news in range(1, 7):

            news_key = 'news_' + str(news)
            if news_key in entry and entry[news_key].strip():  
                news_data = (
                    entry.get('bibtex_key', None),
                    entry.get(news_key, None),  
                )

                cursor.execute("""
                    INSERT INTO news (company_key, news) VALUES (?, ?)
                """, news_data)

    # Commit the changes and close the database connection
    conn.commit()
    conn.close()


insert_data_from_json_to_db_complete("companies.json", "companies.db")

