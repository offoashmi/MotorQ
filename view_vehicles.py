from moretorq.organizations_db.vehicle_model import list_vehicles

def view_vehicles():
    """View all vehicles from the `vehicles` table."""
    vehicles = list_vehicles()
    if vehicles:
        for vehicle in vehicles:
            print(f"VIN: {vehicle['vin']}, Manufacturer: {vehicle['manufacturer']}, Model: {vehicle['model']}, Year: {vehicle['year']}, Organization: {vehicle['org']}")
    else:
        print("No vehicles found.")

if __name__ == "__main__":
    view_vehicles()
