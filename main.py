"""
Entry point for the Akasa Air ETL Pipeline
Handles command line arguments and initializes the pipeline
"""
import argparse
import logging
from pipeline import ETLPipeline

def setup_logging():
    """Configure logging for the application"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="Akasa Air ETL Pipeline - Process customer and order data"
    )
    parser.add_argument(
        "--customers", 
        help="Path to customers CSV file"
    )
    parser.add_argument(
        "--orders", 
        help="Path to orders XML file"
    )
    parser.add_argument(
        "--dashboard", 
        action="store_true",
        help="Launch dashboard after ETL processing"
    )
    parser.add_argument(
        "--dashboard-only", 
        action="store_true",
        help="Launch only the dashboard (skip ETL processing)"
    )
    return parser.parse_args()

def main():
    """Main entry point for the application"""
    setup_logging()
    args = parse_arguments()
    
    try:
        pipeline = ETLPipeline()
        
        if args.dashboard_only:
            # Launch only dashboard
            dashboard_process = pipeline.launch_dashboard_only()
            if dashboard_process:
                try:
                    dashboard_process.wait()
                except KeyboardInterrupt:
                    logging.info("Dashboard stopped by user")
        else:
            # Validate required arguments for ETL
            if not args.customers or not args.orders:
                logging.error("--customers and --orders are required for ETL processing")
                exit(1)
            
            # Run ETL pipeline
            dashboard_process = pipeline.run(args.customers, args.orders, args.dashboard)
            
            # If dashboard was launched, wait for user to stop it
            if dashboard_process:
                try:
                    dashboard_process.wait()
                except KeyboardInterrupt:
                    logging.info("Dashboard stopped by user")
                    
    except Exception as e:
        logging.error(f"Application failed: {e}")
        exit(1)

if __name__ == "__main__":
    main()