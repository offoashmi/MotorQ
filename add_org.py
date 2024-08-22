from moretorq.organizations_db.org_model import Organization
from moretorq.organizations_db.db_setup import create_orgs_table

# Ensure the table is created
create_orgs_table()

def add_org(name, account, website, fuel_reimbursement_policy=1000, speed_limit_policy=None, parent_org=None):
    # Create an organization object with the provided parameters
    org = Organization(
        name=name,
        account=account,
        website=website,
        fuel_reimbursement_policy=fuel_reimbursement_policy,
        speed_limit_policy=speed_limit_policy,
        parent_org=parent_org
    )
    
    # Save the organization to the database
    org.save()

if __name__ == "__main__":
    # Example usage
   # add_org("Org1", "acc1", "www.org1.com", speed_limit_policy=25)
   # add_org("ChildOrg1", "acc2", "www.childorg1.com", parent_org="Org1")

    # Test 1: Create a parent organization with specific policies
   add_org("Org1", "acc1", "www.org1.com", fuel_reimbursement_policy=1500, speed_limit_policy=30)

# Test 2: Create a child organization that inherits the parent's policies
   add_org("ChildOrg1", "acc2", "www.childorg1.com", parent_org="Org1")

# Test 3: Create a child organization with an overridden speed_limit_policy (but no fuel_reimbursement_policy set)
   add_org("ChildOrg2", "acc3", "www.childorg2.com", speed_limit_policy=40, parent_org="Org1")

# Test 4: Attempt to create a child organization with a direct fuel_reimbursement_policy (should fail)
   add_org("InvalidChildOrg", "acc4", "www.invalidchildorg.com", fuel_reimbursement_policy=2000, parent_org="Org1")
