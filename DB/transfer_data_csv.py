import pandas as pd
import sqlite3
import csv
from io import StringIO


csv_file_path = 'Locations-Overview.csv'
df = pd.read_csv(csv_file_path)


print("CSV Columns: ", df.columns)


df.columns = df.columns.str.strip()


df = df[['Country', 'Incidents']]


df = df.dropna(subset=['Incidents'])  

def split_incidents(incident_string):

    f = StringIO(incident_string)
    reader = csv.reader(f, skipinitialspace=True)
    return next(reader)

df['Incidents'] = df['Incidents'].apply(split_incidents)  
df = df.explode('Incidents')  


df['Incidents'] = df['Incidents'].str.strip()


db_path = 'companies.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()


def populate_table(table_name, data_frame, cursor):
    data = [tuple(row) for row in data_frame.itertuples(index=False)]
    placeholders = ','.join('?' * len(data_frame.columns))
    query = f'INSERT INTO {table_name} VALUES ({placeholders})'
    cursor.executemany(query, data)


populate_table('country_data', df, cursor)


conn.commit()
conn.close()
