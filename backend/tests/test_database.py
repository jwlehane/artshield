import pytest
import os
from sqlalchemy import create_engine, inspect
from backend.database import init_db, SQLALCHEMY_DATABASE_URL

def test_database_initialization():
    # Ensure database file doesn't exist before test
    db_path = SQLALCHEMY_DATABASE_URL.replace("sqlite:///", "")
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
