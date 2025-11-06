"""
Main ETL Pipeline orchestrator
Coordinates the entire data processing workflow
"""
import logging
from config import Config
from data_cleaners import CustomerCleaner, OrderCleaner
from database_loader import DatabaseLoader
from dashboard_launcher import DashboardLauncher

class ETLPipeline:
    """Main ETL Pipeline class that orchestrates the data processing workflow"""
    
    def __init__(self):
        """Initialize pipeline with configuration and database connection"""
        self.config = Config()
        self.engine = self.config.get_database_engine()
        self.db_loader = DatabaseLoader(self.engine)
        self.customer_cleaner = CustomerCleaner()
        self.order_cleaner = OrderCleaner()
        self.dashboard_launcher = DashboardLauncher()
    
    def run(self, customers_csv: str, orders_xml: str, launch_dashboard: bool = False):
        """
        Execute the complete ETL pipeline
        
        Args:
            customers_csv (str): Path to customers CSV file
            orders_xml (str): Path to orders XML file
            launch_dashboard (bool): Whether to launch dashboard after processing
        """
        logging.info("Starting ETL pipeline...")
        
        try:
            # Extract and clean customer data
            logging.info("Processing customer data...")
            customers_df = self.customer_cleaner.clean_customers(customers_csv)
            
            # Extract and clean order data
            logging.info("Processing order data...")
            orders_df = self.order_cleaner.clean_orders(orders_xml)
            
            # Load data to database
            logging.info("Loading data to database...")
            self.db_loader.load_customers(customers_df)
            self.db_loader.load_orders(orders_df)
            
            logging.info("ETL pipeline completed successfully!")
            
            # Launch dashboard if requested
            if launch_dashboard:
                logging.info("Launching dashboard...")
                dashboard_process = self.dashboard_launcher.launch_dashboard()
                if dashboard_process:
                    logging.info("Dashboard launched successfully!")
                    return dashboard_process
            
        except Exception as e:
            logging.error(f"Pipeline failed: {e}")
            raise
        finally:
            # Clean up database connection
            if hasattr(self, 'engine'):
                self.engine.dispose()
    
    def launch_dashboard_only(self):
        """Launch only the dashboard without running ETL"""
        logging.info("Launching dashboard...")
        return self.dashboard_launcher.launch_dashboard()