import sqlite3
import requests
from db_setup import get_db_connection

class Vehicle:
    def __init__(self, vin, org):
        self.vin = vin
        self.org = org
        self.manufacturer = None
        self.model = None
        self.year = None

    def fetch_existing_vehicle(self):
        """Fetches vehicle details from the vehicles table if it already exists."""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT manufacturer, model, year FROM vehicles WHERE vin = ?', (self.vin,))
        result = cursor.fetchone()
        conn.close()
        if result:
            self.manufacturer, self.model, self.year = result
            return True
        return False

    def decode_vin(self):
        """Fetches vehicle details from the external API using the VIN."""
        url = f"https://vpic.nhtsa.dot.gov/api/vehicles/DecodeVinValues/{self.vin}?format=json"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            self.manufacturer = data['Results'][0]['Manufacturer']
            self.model = data['Results'][0]['Model']
            self.year = data['Results'][0]['ModelYear']
        else:
            raise Exception("Failed to decode VIN. Check the API or the VIN provided.")

    def save(self):
        """Saves the vehicle details to the vehicles table."""
        # Check if vehicle already exists
        if not self.fetch_existing_vehicle():
            # If not, call the API to get vehicle details
            self.decode_vin()

            # Save the vehicle details to the vehicles table
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO vehicles (vin, manufacturer, model, year, org)
                VALUES (?, ?, ?, ?, ?)
            ''', (self.vin, self.manufacturer, self.model, self.year, self.org))
            conn.commit()
            conn.close()
        else:
            print(f"Vehicle with VIN {self.vin} already exists in the database.")

def list_vehicles():
    """Fetches all vehicles from the vehicles table."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM vehicles')
    vehicles = cursor.fetchall()
    conn.close()
    return vehicles


