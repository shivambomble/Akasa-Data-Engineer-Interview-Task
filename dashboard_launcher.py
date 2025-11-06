"""
Dashboard launcher module for the ETL pipeline
Provides functionality to launch the Streamlit dashboard
"""
import subprocess
import logging
import os
import time
import webbrowser
from pathlib import Path

class DashboardLauncher:
    """Handles launching and managing the Streamlit dashboard"""
    
    def __init__(self, port=8501):
        """
        Initialize dashboard launcher
        
        Args:
            port (int): Port to run Streamlit on (default: 8501)
        """
        self.port = port
        self.dashboard_file = "dashboard_app.py"
    
    def check_streamlit_installed(self):
        """Check if Streamlit is installed"""
        try:
            import streamlit
            return True
        except ImportError:
            return False
    
    def install_streamlit_dependencies(self):
        """Install required dashboard dependencies"""
        dependencies = ["streamlit", "plotly", "mysql-connector-python"]
        
        for dep in dependencies:
            try:
                subprocess.check_call(["pip", "install", dep])
                logging.info(f"Installed {dep}")
            except subprocess.CalledProcessError as e:
                logging.error(f"Failed to install {dep}: {e}")
                return False
        return True
    
    def launch_dashboard(self, auto_open=True):
        """
        Launch the Streamlit dashboard
        
        Args:
            auto_open (bool): Whether to automatically open browser
        """
        if not self.check_streamlit_installed():
            logging.info("Streamlit not found. Installing dashboard dependencies...")
            if not self.install_streamlit_dependencies():
                logging.error("Failed to install dashboard dependencies")
                return False
        
        if not Path(self.dashboard_file).exists():
            logging.error(f"Dashboard file {self.dashboard_file} not found")
            return False
        
        try:
            logging.info(f"Launching dashboard on port {self.port}...")
            
            # Build streamlit command
            cmd = [
                "streamlit", "run", self.dashboard_file,
                "--server.port", str(self.port),
                "--server.headless", "true" if not auto_open else "false"
            ]
            
            # Launch dashboard
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Wait a moment for startup
            time.sleep(3)
            
            if auto_open:
                dashboard_url = f"http://localhost:{self.port}"
                logging.info(f"Opening dashboard at {dashboard_url}")
                webbrowser.open(dashboard_url)
            
            logging.info(f"Dashboard launched successfully on port {self.port}")
            logging.info(f"Access at: http://localhost:{self.port}")
            logging.info("Press Ctrl+C to stop the dashboard")
            
            return process
            
        except Exception as e:
            logging.error(f"Failed to launch dashboard: {e}")
            return None
    
    def launch_dashboard_background(self):
        """Launch dashboard in background mode"""
        return self.launch_dashboard(auto_open=False)