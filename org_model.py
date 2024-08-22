from db_setup import get_db_connection

class Organization:
    def __init__(self, name, account, website, fuel_reimbursement_policy=1000, speed_limit_policy=None, parent_org=None):
        self.name = name
        self.account = account
        self.website = website
        self.fuel_reimbursement_policy = fuel_reimbursement_policy
        self.speed_limit_policy = speed_limit_policy
        self.parent_org = parent_org

    def save(self):
        """Saves the organization details to the `orgs` table."""
        conn = get_db_connection()
        cursor = conn.cursor()

        # Check if parent_org is specified and exists in the table
        if self.parent_org:
            cursor.execute('SELECT id, fuel_reimbursement_policy, speed_limit_policy FROM orgs WHERE name = ?', (self.parent_org,))
            parent_data = cursor.fetchone()
            if not parent_data:
                print("Error: Parent organization does not exist.")
                conn.close()
                return
            parent_id, parent_fuel_policy, parent_speed_policy = parent_data

            # Check if the fuel_reimbursement_policy should be inherited
            if self.fuel_reimbursement_policy != 1000:
                print("Error: Cannot set fuel_reimbursement_policy directly on a child organization. It must be set on the parent.")
                conn.close()
                return
            self.fuel_reimbursement_policy = parent_fuel_policy

            # Check if the speed_limit_policy should be inherited
            if self.speed_limit_policy is None:
                self.speed_limit_policy = parent_speed_policy
        else:
            parent_id = None

        # Insert the new organization into the table
        cursor.execute('''
            INSERT INTO orgs (name, account, website, fuel_reimbursement_policy, speed_limit_policy, parent_org)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (self.name, self.account, self.website, self.fuel_reimbursement_policy, self.speed_limit_policy, parent_id))
        conn.commit()
        conn.close()
        print(f"Organization '{self.name}' added successfully!")
