import pandas as pd
import sqlite3

conn = sqlite3.connect('database/scp.db')

print("Opened database successfully")

# initalize schema
conn.execute('''CREATE TABLE IF NOT EXISTS SCP
         (  ID                     INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            SCP                    INTEGER    NOT NULL,
            item                   VARCHAR(50) NOT NULL,
            object_class           VARCHAR(50),
            containment_procedure  TEXT,
            description            TEXT,
            image                  TEXT );''')

conn.commit()
conn.close()
print ("Table created successfully")

def save_df(df: pd.DataFrame) -> bool:
    conn = sqlite3.connect('database/scp.db')
    print("Opened database successfully")   
    df.to_sql('SCP', conn, if_exists='replace', index = False)
    conn.commit()
    conn.close()

    return True