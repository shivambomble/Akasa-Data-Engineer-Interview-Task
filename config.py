"""
Configuration module for Akasa Air ETL Pipeline
Handles environment variables and database connection setup
"""
import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

class Config:
    """Configuration class for database and environment settings"""
    
    def __init__(self):
        load_dotenv()
        self.mysql_user = os.getenv("MYSQL_USER")
        self.mysql_password = os.getenv("MYSQL_PASSWORD")
        self.mysql_db = os.getenv("MYSQL_DB")
        self.mysql_host = os.getenv("MYSQL_HOST")
        
        # Validate required environment variables
        self._validate_config()
    
    def _validate_config(self):
        """Validate that all required environment variables are set"""
        required_vars = [
            self.mysql_user, self.mysql_password, 
            self.mysql_db, self.mysql_host
        ]
        if not all(required_vars):
            raise ValueError("Missing required environment variables. Check your .env file.")
    
    def get_database_engine(self):
        """Create and return SQLAlchemy database engine"""
        connection_string = (
            f"mysql+mysqlconnector://{self.mysql_user}:{self.mysql_password}"
            f"@{self.mysql_host}/{self.mysql_db}"
        )
        return create_engine(connection_string)