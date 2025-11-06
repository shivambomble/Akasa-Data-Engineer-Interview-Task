# 🛩️ Akasa Air ETL Pipeline & Analytics Dashboard

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-red)](https://streamlit.io)
[![MySQL](https://img.shields.io/badge/MySQL-8.0%2B-orange)](https://mysql.com)

A production-ready, enterprise-grade ETL pipeline with integrated analytics dashboard for processing customer and order data. Built with modern Python practices, comprehensive error handling, and scalable architecture.

## 🚀 Features

### 🔧 **Core ETL Capabilities**
- **Modular Architecture**: Clean separation of concerns with single-responsibility components
- **Robust Data Validation**: Comprehensive validation for customer and order data integrity
- **Error Handling & Logging**: Production-grade error handling with detailed logging
- **Secure Configuration**: Environment-based credential management
- **Database Integration**: Optimized MySQL operations with SQLAlchemy
- **Batch Processing**: Efficient bulk data loading with transaction safety

### 📊 **Analytics Dashboard**
- **Interactive Visualizations**: Multiple chart types (bar, line, pie, area, funnel)
- **Real-time KPIs**: Key business metrics with dynamic filtering
- **Regional Analysis**: Geographic revenue and customer distribution
- **Trend Analysis**: Monthly order volume, revenue, and average order value trends
- **Customer Segmentation**: Order value distribution and spending patterns
- **Responsive Design**: Mobile-friendly interface with professional styling

### 🛡️ **Production Features**
- **Data Quality Assurance**: Input validation, duplicate detection, format verification
- **Scalable Design**: Handles large datasets with memory-efficient processing
- **Monitoring & Observability**: Comprehensive logging and error tracking
- **Configuration Management**: Environment-based settings with validation
- **Resource Management**: Proper connection pooling and cleanup

## 📁 Project Structure

```
akasa-air-etl/
├── 📄 main.py                    # Application entry point & CLI interface
├── 🔄 pipeline.py                # ETL orchestration engine
├── ⚙️  config.py                 # Configuration & database management
├── 🧹 data_cleaners.py           # Data validation & transformation modules
├── 💾 database_loader.py         # Database operations & batch loading
├── 📊 dashboard_app.py           # Streamlit analytics dashboard
├── 🚀 dashboard_launcher.py      # Dashboard lifecycle management
├── 📋 requirements.txt           # Python dependencies
├── 🔐 .env                       # Environment variables (excluded from repo)
├── 📊 task_DE_new_customers.csv  # Sample customer data
├── 📦 task_DE_new_orders.xml     # Sample order data
└── 📖 README.md                  # This documentation
```

## 🛠️ Installation & Setup

### Prerequisites
- **Python 3.8+**
- **MySQL 8.0+**
- **pip** package manager

### 1. Clone Repository
```bash
git clone <repository-url>
cd akasa-air-etl
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Database Setup
Create MySQL database and tables:
```sql
CREATE DATABASE akasa_db;
USE akasa_db;

-- Tables will be created automatically by the pipeline
```

### 4. Environment Configuration
Create `.env` file in project root:
```env
# Database Configuration
MYSQL_USER=your_username
MYSQL_PASSWORD=your_secure_password
MYSQL_DB=akasa_db
MYSQL_HOST=localhost

# Optional: Dashboard Configuration
DASHBOARD_PORT=8501
```

## 🚀 Usage Guide

### **ETL Pipeline Operations**

#### Run Complete ETL Pipeline
```bash
python main.py --customers task_DE_new_customers.csv --orders task_DE_new_orders.xml
```

#### ETL + Auto-Launch Dashboard
```bash
python main.py --customers task_DE_new_customers.csv --orders task_DE_new_orders.xml --dashboard
```

### **Dashboard Operations**

#### Launch Dashboard Only
```bash
python main.py --dashboard-only
```

#### Direct Streamlit Launch (Development)
```bash
streamlit run dashboard_app.py
```

### **Command Line Options**
```bash
python main.py [OPTIONS]

Options:
  --customers PATH     Path to customers CSV file
  --orders PATH        Path to orders XML file  
  --dashboard          Launch dashboard after ETL completion
  --dashboard-only     Launch dashboard without running ETL
  --help              Show help message
```

## 🏗️ Architecture Overview

### **ETL Components**

#### **Config Manager** (`config.py`)
- Environment variable validation and loading
- Database connection management with pooling
- Configuration error handling and validation

#### **Data Cleaners** (`data_cleaners.py`)
- **CustomerCleaner**: CSV processing, mobile number validation, duplicate removal
- **OrderCleaner**: XML parsing, business rule validation, data type conversion
- Comprehensive data quality checks and transformations

#### **Database Loader** (`database_loader.py`)
- Batch insertion with transaction management
- Connection pooling and resource optimization
- Error handling with rollback capabilities

#### **Pipeline Orchestrator** (`pipeline.py`)
- End-to-end workflow coordination
- Component integration and dependency management
- Resource cleanup and error propagation

### **Dashboard Components**

#### **Analytics Engine** (`dashboard_app.py`)
- Multi-dimensional data analysis
- Interactive filtering and real-time updates
- Professional visualization with Plotly
- Responsive design with custom CSS

#### **Dashboard Launcher** (`dashboard_launcher.py`)
- Automated dependency management
- Process lifecycle management
- Browser integration and port management

## 📊 Dashboard Features

### **Key Performance Indicators**
- 👥 **Top Repeat Customer**: Customer with most orders
- 🌍 **Highest Revenue Region**: Geographic performance leader  
- 💸 **Top Spender (30 days)**: Recent high-value customer

### **Analytics Visualizations**
- 📈 **Monthly Order Trends**: Bar charts with color intensity
- 💰 **Revenue Analysis**: Area charts showing growth patterns
- 📊 **Average Order Value**: Line charts tracking spending behavior
- 🥧 **Regional Distribution**: Pie charts for market share analysis
- 📊 **Order Value Segmentation**: Funnel analysis of spending tiers

### **Interactive Features**
- 🔍 **Regional Filtering**: Dynamic data filtering by geographic region
- 📋 **Tabbed Data Views**: Organized detailed data exploration
- 💱 **Currency Formatting**: Professional financial data presentation
- 📱 **Responsive Design**: Optimized for desktop and mobile devices

## 🔧 Data Processing Details

### **Customer Data Validation**
- Mobile number format validation (Indian 10-digit format)
- Duplicate detection and removal
- Missing data handling
- Region name standardization

### **Order Data Processing**
- XML parsing with error handling
- Order ID format validation (`ORD-YYYY-NNNN`)
- Business rule validation (positive amounts, valid quantities)
- DateTime parsing and timezone handling

### **Database Operations**
- Batch insertion for performance optimization
- Transaction management with rollback capability
- Connection pooling for scalability
- Proper resource cleanup

## 🚨 Error Handling & Monitoring

### **Logging Strategy**
- Structured logging with timestamps and levels
- Component-specific log messages
- Error tracking with stack traces
- Performance metrics logging

### **Error Recovery**
- Graceful degradation on data quality issues
- Transaction rollback on database errors
- Resource cleanup on application termination
- User-friendly error messages

## 🔒 Security & Best Practices

### **Security Measures**
- Environment-based credential management
- SQL injection prevention with parameterized queries
- Input validation and sanitization
- Secure database connection handling

### **Code Quality**
- Type hints and documentation
- Single responsibility principle
- Comprehensive error handling
- Resource management with context managers

## 📈 Performance Considerations

### **Optimization Features**
- Batch database operations
- Memory-efficient data processing
- Connection pooling
- Lazy loading of dashboard components

### **Scalability**
- Modular architecture for easy extension
- Configurable batch sizes
- Resource monitoring and cleanup
- Horizontal scaling capability

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request


## 🆘 Support & Troubleshooting

### **Common Issues**

#### Database Connection Errors
```bash
# Verify MySQL service is running
sudo systemctl status mysql

# Check environment variables
cat .env
```

#### Dashboard Launch Issues
```bash
# Install missing dependencies
pip install streamlit plotly

# Check port availability
netstat -tulpn | grep 8501
```

#### Data Processing Errors
- Verify CSV/XML file formats match expected schema
- Check file permissions and accessibility
- Validate data quality and completeness


---

**Built with ❤️ for Akasa Air Data Engineering Team**