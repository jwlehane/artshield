import pytest
import os
from sqlalchemy import create_engine, inspect
from backend.database import init_db, SQLALCHEMY_DATABASE_URL

def test_database_initialization():
    # Ensure database file doesn't exist before test
    db_path = SQLALCHEMY_DATABASE_URL.replace("sqlite:///", "")
    print(f"\nDEBUG: CWD={os.getcwd()}")
    print(f"DEBUG: db_path={db_path}")
    print(f"DEBUG: ABS db_path={os.path.abspath(db_path)}")
    if os.path.exists(db_path):
        os.remove(db_path)
    
    # Run initialization
    init_db()
    
    # Assert database file was created
    assert os.path.exists(db_path)
    
    # Assert 'protected_assets' table exists
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    assert "protected_assets" in tables
