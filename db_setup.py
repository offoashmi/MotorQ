import sqlite3



import sqlite3

def get_db_connection():
    """Function to connect to the SQLite database."""
    conn = sqlite3.connect('organization.db')
    conn.row_factory = sqlite3.Row
    return conn

def create_orgs_table():
    """Function to create the `orgs` table in the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orgs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            account TEXT NOT NULL,
            website TEXT,
            fuel_reimbursement_policy INTEGER DEFAULT 1000,
            speed_limit_policy INTEGER,
            parent_org TEXT,
            FOREIGN KEY (parent_org) REFERENCES orgs (name)     
            
        )
    ''')
    conn.commit()
    conn.close()

def create_vehicles_table():
    """Function to create the `vehicles` table in the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS vehicles (
            vin TEXT PRIMARY KEY NOT NULL,
            manufacturer TEXT NOT NULL,
            model TEXT NOT NULL,
            year TEXT NOT NULL,
            org TEXT NOT NULL,
            FOREIGN KEY (org) REFERENCES orgs (name)
        )
    ''')
    conn.commit()
    conn.close()

# Automatically create the tables if they do not exist
if __name__ == '__main__':
    create_orgs_table()
    create_vehicles_table()
    print("Tables created successfully!")
