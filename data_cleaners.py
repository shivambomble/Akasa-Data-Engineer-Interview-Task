"""
Data cleaning modules for customers and orders data
"""
import re
import logging
import pandas as pd
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

class CustomerCleaner:
    """Handles cleaning and validation of customer data from CSV files"""
    
    @staticmethod
    def clean_customers(csv_file):
        """
        Clean and validate customer data from CSV file
        
        Args:
            csv_file (str): Path to the CSV file containing customer data
            
        Returns:
            pd.DataFrame: Cleaned customer dataframe
        """
        df = pd.read_csv(csv_file)
        
        # Clean and strip whitespace from string columns
        for col in ["customer_id", "customer_name", "mobile_number", "region"]:
            df[col] = df[col].astype(str).str.strip()
        
        # Remove duplicates based on customer_id and mobile_number
        df = df.drop_duplicates(subset=['customer_id', 'mobile_number'])
        
        # Validate mobile numbers (Indian format: starts with 7, 8, or 9 and has 10 digits)
        df = df[df['mobile_number'].str.match(r'^[789]\d{9}$')]
        
        # Remove rows with missing critical data
        df = df.dropna(subset=['customer_id', 'customer_name', 'mobile_number', 'region'])
        
        # Standardize region names to title case
        df['region'] = df['region'].str.title()
        
        # Rename columns for database compatibility
        df = df.rename(columns={
            "customer_id": "customerid",
            "customer_name": "customername",
            "mobile_number": "mobilenumber"
        })
        
        logging.info(f"Cleaned customers: {len(df)} rows")
        return df


class OrderCleaner:
    """Handles cleaning and validation of order data from XML files"""
    
    @staticmethod
    def clean_orders(xml_file):
        """
        Clean and validate order data from XML file
        
        Args:
            xml_file (str): Path to the XML file containing order data
            
        Returns:
            pd.DataFrame: Cleaned orders dataframe
        """
        tree = ET.parse(xml_file)
        root = tree.getroot()
        records = []
        
        for order in root.findall('order'):
            try:
                # Extract and clean order data
                orderid = order.find('order_id').text.strip()
                mobilenumber = order.find('mobile_number').text.strip()
                dt = order.find('order_date_time').text.strip()
                skuid = order.find('sku_id').text.strip()
                skucount = int(order.find('sku_count').text.strip())
                totalamount = float(order.find('total_amount').text.strip())
                
                # Parse and format datetime
                dt_parsed = datetime.strptime(dt, "%Y-%m-%dT%H:%M:%S").replace(tzinfo=timezone.utc)
                orderdatetime = dt_parsed.strftime('%Y-%m-%d %H:%M:%S')
                
                # Validate order ID format
                if not re.match(r'^ORD-\d{4}-\d+$', orderid):
                    continue
                
                # Validate mobile number format
                if not re.match(r'^[789]\d{9}$', mobilenumber):
                    continue
                
                # Validate business logic constraints
                if skucount <= 0 or totalamount <= 0:
                    continue
                
                records.append([orderid, mobilenumber, orderdatetime, skuid, skucount, totalamount])
                
            except Exception as e:
                logging.error(f"Skipping order: {e}")
        
        df = pd.DataFrame(records, columns=[
            'orderid', 'mobilenumber', 'orderdatetime', 
            'skuid', 'skucount', 'totalamount'
        ])
        
        logging.info(f"Cleaned orders: {len(df)} rows")
        return df