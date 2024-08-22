# view_orgs.py

import sqlite3

def view_orgs():
    # Connect to the SQLite database
    conn = sqlite3.connect('organization.db')
    cursor = conn.cursor()

    # Fetch all rows from the orgs table
    cursor.execute("SELECT * FROM orgs")
    rows = cursor.fetchall()

    if not rows:
        print("No organizations found.")
    else:
        # Print all organizations
        for row in rows:
            print(row)

    # Close the connection
    conn.close()

if __name__ == '__main__':
    view_orgs()

