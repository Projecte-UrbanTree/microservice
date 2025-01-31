import os
from sqlmodel import Session, SQLModel, create_engine, select
from dotenv import load_dotenv
from src.core.db.connection import engine

# Test the database connection
def test_database_connection():
    """
    Test the database connection by attempting to query the database.
    """
    try:
        with Session(engine) as session:
            # Example query to test connection (replace with actual table if available)
            result = session.exec(select(SQLModel))
            print("Database connection test succeeded. Query result:", list(result))
    except Exception as e:
        print(f"Database connection test failed: {e}")

if __name__ == "__main__":
    """
    Entry point for verifying the database connection.
    """
    test_database_connection()

    # Documentation and Instructions
    print("""
    Instructions:
    1. Create a .env file in the root directory with the following variable:
        SQLALCHEMY_DATABASE_URI=<your_database_uri>

    2. Install the required dependencies:
        pip install sqlmodel python-dotenv

    3. Run this script to test the database connection:
        python db_connection_setup.py

    4. Replace the example query in test_database_connection() with a valid table query if needed.
    """)