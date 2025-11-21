from pathlib import Path
import pandas as pd
from app.data.schema import create_all_tables
from app.data.db import connect_database, DATA_DIR



def load_csv_to_table(conn, csv_path, table_name):
    """
    Load a CSV file into a database table using pandas.

    Args:
        conn: Database connection
        csv_path: Path to CSV file
        table_name: Name of the database table

    Returns:
        int: Number of rows loaded
    """
    path = Path(csv_path)

    # Check if file exists
    if not path.exists():
        print(f"Warning: {csv_path} not found. Skipping.")
        return 0

    # Read CSV into DataFrame
    df = pd.read_csv(path)

    # Clean column names (remove extra whitespace)
    df.columns = df.columns.str.strip()

    # Preview data
    print(f"\nLoading {csv_path}...")
    print(f"  Columns: {list(df.columns)}")
    print(f"  Rows: {len(df)}")

    if "id" in df.columns:
        print("  Removing 'id' column to avoid PRIMARY KEY conflicts...")
        df = df.drop(columns=["id"])

    # Load into database
    df.to_sql(table_name, conn, if_exists='append', index=False)
    print(f"Loaded {len(df)} rows into '{table_name}' table.")

    return len(df)

def load_all_csv_data(conn):
    """
    Load all three domain CSV files into the database.
    """
    print("\nStarting CSV data loading...")
    total_rows = 0

    # Load cyber incidents
    total_rows += load_csv_to_table(
        conn,
        DATA_DIR / "cyber_incidents.csv",
        "cyber_incidents"
    )

    # Load datasets metadata
    total_rows += load_csv_to_table(
        conn,
        DATA_DIR / "datasets_metadata.csv",
        "datasets_metadata"
    )

    # Load IT tickets
    total_rows += load_csv_to_table(
        conn,
        DATA_DIR / "it_tickets.csv",
        "it_tickets"
    )

    print(f"\nTotal rows loaded: {total_rows}")
    return total_rows


# Test: Load all CSV files
conn = connect_database()
create_all_tables(conn)  # Ensure tables exist
load_all_csv_data(conn)
conn.close()