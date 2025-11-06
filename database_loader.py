"""
Database loading module for ETL pipeline
Handles data insertion into MySQL database
"""
import logging
import pandas as pd
from sqlalchemy import Engine

class DatabaseLoader:
    """Handles loading data into MySQL database"""
    
    def __init__(self, engine: Engine):
        """
        Initialize DatabaseLoader with database engine
        
        Args:
            engine (Engine): SQLAlchemy database engine
        """
        self.engine = engine
    
    def load_to_mysql(self, df: pd.DataFrame, table_name: str):
        """
        Load dataframe to MySQL table
        
        Args:
            df (pd.DataFrame): DataFrame to load
            table_name (str): Target table name
        """
        try:
            df.to_sql(
                table_name, 
                con=self.engine, 
                if_exists='append', 
                index=False, 
                method='multi'
            )
            logging.info(f"Successfully loaded {len(df)} rows into {table_name}")
        except Exception as e:
            logging.error(f"Failed to load data into {table_name}: {e}")
            raise
    
    def load_customers(self, customers_df: pd.DataFrame):
        """Load customers data to database"""
        self.load_to_mysql(customers_df, "customers")
    
    def load_orders(self, orders_df: pd.DataFrame):
        """Load orders data to database"""
        self.load_to_mysql(orders_df, "orders")