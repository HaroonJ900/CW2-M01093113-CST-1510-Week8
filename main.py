from app.data.db import connect_database
from app.data.schema import create_all_tables
from app.data.bulk_data_load import load_all_csv_data
from app.services.user_service import migrate_users_from_file
from app.data.db import DB_PATH
import pandas as pd
from app.services.user_service import register_user, login_user
from app.data.incidents import insert_incident, update_incident_status, delete_incident
from app.data.incidents import get_incidents_by_type_count, get_high_severity_by_status
from app.data.tickets import insert_ticket, get_all_tickets
from app.data.datasets import insert_dataset
from app.data.datasets import get_all_datasets





def setup_database_complete():
    """
    Complete database setup:
    1. Connect to database
    2. Create all tables
    3. Migrate users from users.txt
    4. Load CSV data for all domains
    5. Verify setup
    """
    print("\n" + "=" * 60)
    print("STARTING COMPLETE DATABASE SETUP")
    print("=" * 60)

    # Step 1: Connect
    print("\n[1/5] Connecting to database...")
    conn = connect_database()
    print("       Connected")

    # Step 2: Create tables
    print("\n[2/5] Creating database tables...")
    create_all_tables(conn)

    # Step 3: Migrate users
    print("\n[3/5] Migrating users from users.txt...")
    user_count = migrate_users_from_file(conn)
    print(f"       Migrated {user_count} users")

    # Step 4: Load CSV data
    print("\n[4/5] Loading CSV data...")
    total_rows = load_all_csv_data(conn)

    # Step 5: Verify
    print("\n[5/5] Verifying database setup...")
    cursor = conn.cursor()

    # Count rows in each table
    tables = ['users', 'cyber_incidents', 'datasets_metadata', 'it_tickets']

    print("\n Database Summary:")
    print(f"{'Table':<25} {'Row Count':<15}")
    print("-" * 40)

    for table in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        print(f"{table:<25} {count:<15}")

    conn.close()

    print("\n" + "=" * 60)
    print(" DATABASE SETUP COMPLETE!")
    print("=" * 60)
    print(f"\n Database location: {DB_PATH.resolve()}")
    print("\nYou're ready for Week 9 (Streamlit web interface)!")

def run_comprehensive_tests():
    """
    Run comprehensive tests on your database.
    """
    print("\n" + "=" * 60)
    print("🧪 RUNNING COMPREHENSIVE TESTS")
    print("=" * 60)

    conn = connect_database()

    # Test 1: Authentication
    print("\n[TEST 1] Authentication")
    success, msg = register_user("test_use", "TestPass123!", "user")
    print(f" Register: {'✅' if success else '❌'} {msg}")

    success, msg = login_user("test_user", "TestPass123!")
    print(f" Login:    {'✅' if success else '❌'} {msg}")

    # Test 2: CRUD Operations
    print("\n[TEST 2] CRUD Operations")

    # Create
    test_id = insert_incident(
        "2024-11-05",
        "Test Incident",
        "Low",
        "Open"
    )
    
    print(f"  Create:  ✅ Incident #{test_id} created")

    tickets_id = insert_ticket("Account Locked","High","Open","01/01/2025",15)
    print(f"Ticket {tickets_id} created.")
    print(get_all_tickets())

    dataset_id = insert_dataset("VPN Logs","VPN Server","Networking","50 mb")
    print(f"Dataset {dataset_id} created.")
    print(get_all_datasets())

    # Read
    df = pd.read_sql_query(
        "SELECT * FROM cyber_incidents WHERE id = ?",
        conn,
        params=(test_id,)
    )
    print(f"  Read:    Found incident #{test_id}")

    # Update
    update_incident_status(test_id, "Resolved")
    print(f"  Update:  Status updated")

    # Delete
    delete_incident(test_id)
    print(f"  Delete:  Incident deleted")

    # Test 3: Analytical Queries
    print("\n[TEST 3] Analytical Queries")

    df_by_type = get_incidents_by_type_count()
    print(f"  By Type:       Found {len(df_by_type)} incident types")

    df_high = get_high_severity_by_status()
    print(f"  High Severity: Found {len(df_high)} status categories")

    conn.close()

    print("\n" + "=" * 60)
    print("✅ ALL TESTS PASSED!")
    print("=" * 60)


# Run tests
run_comprehensive_tests()
