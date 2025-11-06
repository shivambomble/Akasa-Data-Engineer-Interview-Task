"""
Streamlit Dashboard for Akasa Air ETL Pipeline
Displays KPIs and analytics from processed data
"""
import streamlit as st
import pandas as pd
import plotly.express as px
from config import Config

class DashboardApp:
    """Streamlit dashboard application for displaying ETL results"""
    
    def __init__(self):
        """Initialize dashboard with database configuration"""
        self.config = Config()
        self.setup_page_config()
        self.setup_custom_css()
    
    def setup_page_config(self):
        """Configure Streamlit page settings"""
        st.set_page_config(
            page_title="Akasa Air KPI Dashboard", 
            page_icon="✈️", 
            layout="wide"
        )
    
    def setup_custom_css(self):
        """Apply custom CSS styling"""
        st.markdown("""
            <style>
                .dashboard-header {
                    background: linear-gradient(to right, #405de6, #5851db, #833ab4, #c13584, #e1306c, #fd1d1d);
                    color:#fff;
                    padding: 24px 0;
                    margin-bottom: 20px;
                    text-align: center;
                    font-size: 48px;
                    font-weight: 900;
                    border-radius: 12px;
                }
                .section-card {
                    background: #f1f3f6;
                    border-radius: 10px;
                    padding: 20px;
                    margin-bottom: 18px;
                }
                .kpi-box {
                    padding: 18px;
                    border-radius: 10px;
                    background: linear-gradient(90deg, #38ef7d 0%, #11998e 100%);
                    color: white;
                    font-size: 22px;
                    font-weight: bold;
                    text-align:center;
                    margin-bottom:8px;
                }
                .kpi-label {
                    font-size: 16px; color: #333; font-weight: 600;
                }
            </style>
        """, unsafe_allow_html=True)
    
    def get_database_connection(self):
        """Get database connection using mysql-connector-python"""
        import mysql.connector
        try:
            conn = mysql.connector.connect(
                host=self.config.mysql_host,
                user=self.config.mysql_user,
                password=self.config.mysql_password,
                database=self.config.mysql_db
            )
            return conn
        except Exception as e:
            st.error(f"Error connecting to Database: {e}")
            st.stop()
    
    def run_query(self, query, params=None, conn=None):
        """Execute SQL query and return DataFrame"""
        cursor = conn.cursor()
        cursor.execute(query, params or ())
        cols = [desc[0] for desc in cursor.description]
        df = pd.DataFrame(cursor.fetchall(), columns=cols)
        cursor.close()
        return df
    
    def get_queries(self, region_clause="", params=None):
        """Get all dashboard queries with optional region filtering"""
        return {
            "Repeat Customers":
                f"""SELECT c.customerid, c.customername, COUNT(DISTINCT o.orderid) AS num_orders
                FROM customers c JOIN orders o ON c.mobilenumber = o.mobilenumber
                WHERE TRUE {region_clause}
                GROUP BY c.customerid, c.customername
                HAVING COUNT(DISTINCT o.orderid) > 1""",

            "Orders Month-by-Month":
                f"""SELECT 
                    DATE_FORMAT(orderdatetime, '%%Y-%%m') AS month,
                    COUNT(DISTINCT o.orderid) AS total_orders,
                    SUM(o.totalamount) AS total_revenue,
                    AVG(o.totalamount) AS avg_order_value,
                    SUM(o.skucount) AS total_items
                FROM customers c JOIN orders o ON c.mobilenumber = o.mobilenumber
                WHERE TRUE {region_clause}
                GROUP BY month ORDER BY month""",

            "Revenue by Region":
                f"""SELECT c.region, 
                    SUM(o.totalamount) AS total_revenue,
                    COUNT(DISTINCT o.orderid) AS total_orders,
                    COUNT(DISTINCT c.customerid) AS unique_customers
                FROM customers c JOIN orders o ON c.mobilenumber = o.mobilenumber
                WHERE TRUE {region_clause}
                GROUP BY c.region ORDER BY total_revenue DESC""",

            "Top Revenue Region":
                """SELECT c.region, SUM(o.totalamount) AS total_revenue 
                FROM customers c JOIN orders o ON c.mobilenumber = o.mobilenumber 
                GROUP BY c.region ORDER BY total_revenue DESC LIMIT 1""",

            "Top Spender (Last 30 Days)":
                f"""SELECT c.customerid, c.customername, SUM(o.totalamount) AS amount_spent
                FROM customers c JOIN orders o ON c.mobilenumber = o.mobilenumber
                WHERE o.orderdatetime >= DATE_SUB(NOW(), INTERVAL 30 DAY) {region_clause}
                GROUP BY c.customerid, c.customername
                ORDER BY amount_spent DESC LIMIT 1""",

            "Order Value Distribution":
                f"""SELECT 
                    CASE 
                        WHEN o.totalamount < 1000 THEN 'Under ₹1,000'
                        WHEN o.totalamount < 5000 THEN '₹1,000 - ₹5,000'
                        WHEN o.totalamount < 10000 THEN '₹5,000 - ₹10,000'
                        ELSE 'Above ₹10,000'
                    END AS order_range,
                    COUNT(DISTINCT o.orderid) AS order_count,
                    SUM(o.totalamount) AS total_revenue
                FROM customers c JOIN orders o ON c.mobilenumber = o.mobilenumber
                WHERE TRUE {region_clause}
                GROUP BY order_range
                ORDER BY MIN(o.totalamount)"""
        }
    
    def render_kpi_cards(self, repeat_df, region_df, spender_df):
        """Render KPI cards in the dashboard"""
        kpi_col1, kpi_col2, kpi_col3 = st.columns(3)

        with kpi_col1:
            if not repeat_df.empty:
                st.markdown(
                    f'<div class="kpi-box">👥 {repeat_df.iloc[0]["customername"]} ({repeat_df.iloc[0]["customerid"]})<br>'
                    f'<span class="kpi-label">Repeat Customer<br>Orders: <b>{repeat_df.iloc[0]["num_orders"]}</b></span></div>', 
                    unsafe_allow_html=True
                )
            else:
                st.warning("No repeat customers found.")

        with kpi_col2:
            if not region_df.empty:
                st.markdown(
                    f'<div class="kpi-box">🌍 {region_df.iloc[0]["region"]}<br>'
                    f'<span class="kpi-label">Top Revenue Region<br>Revenue: <b>{int(region_df.iloc[0]["total_revenue"]):,}</b></span></div>', 
                    unsafe_allow_html=True
                )
            else:
                st.warning("No region data found.")

        with kpi_col3:
            if not spender_df.empty:
                st.markdown(
                    f'<div class="kpi-box">💸 {spender_df.iloc[0]["customername"]} ({spender_df.iloc[0]["customerid"]})<br>'
                    f'<span class="kpi-label">Top Spender (30 days)<br>Spent: <b>{int(spender_df.iloc[0]["amount_spent"]):,}</b></span></div>', 
                    unsafe_allow_html=True
                )
            else:
                st.warning("No spender data in last 30 days.")
    
    def render_analytics_section(self, monthly_df, revenue_by_region_df, order_distribution_df):
        """Render focused analytics section with meaningful visualizations only"""
        st.markdown('<div class="section-card"><h2 style="color:#3a86ff;">📊 Business Analytics</h2>', unsafe_allow_html=True)
        
        # Only show monthly trend chart if there are multiple months (trend is meaningful)
        if not monthly_df.empty and len(monthly_df) > 1:
            st.subheader("📈 Monthly Business Trends")
            
            # Single meaningful chart showing both orders and revenue trend
            fig = px.line(
                monthly_df, 
                x="month", 
                y=["total_orders", "total_revenue"],
                title="Monthly Orders and Revenue Trend",
                labels={"value": "Count/Amount", "variable": "Metric"}
            )
            
            # Update traces for better readability
            fig.data[0].name = "Orders"
            fig.data[1].name = "Revenue (₹)"
            fig.data[1].yaxis = "y2"
            
            # Add secondary y-axis for revenue
            fig.update_layout(
                yaxis=dict(title="Number of Orders"),
                yaxis2=dict(title="Revenue (₹)", overlaying="y", side="right"),
                xaxis_title="Month",
                hovermode="x unified"
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        # Regional distribution - only use pie chart if there are multiple regions (distribution is meaningful)
        if not revenue_by_region_df.empty and len(revenue_by_region_df) > 1:
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("🌍 Revenue Distribution by Region")
                fig_pie = px.pie(
                    revenue_by_region_df, 
                    values="total_revenue", 
                    names="region",
                    title="Regional Revenue Share"
                )
                st.plotly_chart(fig_pie, use_container_width=True)
            
            with col2:
                st.subheader("📊 Regional Performance Summary")
                # Show regional data as formatted table instead of unnecessary bar chart
                display_regional = revenue_by_region_df.copy()
                display_regional['Revenue'] = display_regional['total_revenue'].apply(lambda x: f"₹{x:,.0f}")
                display_regional['Orders'] = display_regional['total_orders']
                display_regional['Customers'] = display_regional['unique_customers']
                display_regional['Avg Revenue/Customer'] = (display_regional['total_revenue'] / display_regional['unique_customers']).apply(lambda x: f"₹{x:,.0f}")
                
                # Show only relevant columns
                summary_table = display_regional[['region', 'Revenue', 'Orders', 'Customers', 'Avg Revenue/Customer']].rename(columns={'region': 'Region'})
                st.dataframe(summary_table, use_container_width=True, hide_index=True)
        
        # Monthly metrics table - more informative than multiple charts
        if not monthly_df.empty:
            st.subheader("📋 Monthly Performance Metrics")
            display_monthly = monthly_df.copy()
            display_monthly['Month'] = display_monthly['month']
            display_monthly['Orders'] = display_monthly['total_orders']
            display_monthly['Revenue'] = display_monthly['total_revenue'].apply(lambda x: f"₹{x:,.0f}")
            display_monthly['Avg Order Value'] = display_monthly['avg_order_value'].apply(lambda x: f"₹{x:,.0f}")
            display_monthly['Total Items'] = display_monthly['total_items']
            
            # Calculate month-over-month growth if multiple months
            if len(display_monthly) > 1:
                display_monthly['Revenue Growth'] = display_monthly['total_revenue'].pct_change().apply(
                    lambda x: f"{x:.1%}" if pd.notna(x) else "N/A"
                )
                display_monthly['Order Growth'] = display_monthly['total_orders'].pct_change().apply(
                    lambda x: f"{x:.1%}" if pd.notna(x) else "N/A"
                )
                
                summary_cols = ['Month', 'Orders', 'Revenue', 'Avg Order Value', 'Total Items', 'Revenue Growth', 'Order Growth']
            else:
                summary_cols = ['Month', 'Orders', 'Revenue', 'Avg Order Value', 'Total Items']
            
            st.dataframe(display_monthly[summary_cols], use_container_width=True, hide_index=True)
        
        # Order value distribution - show as simple table, chart not needed for 4 categories
        if not order_distribution_df.empty:
            st.subheader("💳 Order Value Analysis")
            
            col3, col4 = st.columns(2)
            
            with col3:
                display_distribution = order_distribution_df.copy()
                display_distribution['Value Range'] = display_distribution['order_range']
                display_distribution['Orders'] = display_distribution['order_count']
                display_distribution['Revenue'] = display_distribution['total_revenue'].apply(lambda x: f"₹{x:,.0f}")
                display_distribution['% of Total Orders'] = (display_distribution['order_count'] / display_distribution['order_count'].sum() * 100).apply(lambda x: f"{x:.1f}%")
                display_distribution['Avg Order Value'] = (display_distribution['total_revenue'] / display_distribution['order_count']).apply(lambda x: f"₹{x:,.0f}")
                
                st.dataframe(
                    display_distribution[['Value Range', 'Orders', '% of Total Orders', 'Revenue', 'Avg Order Value']], 
                    use_container_width=True, 
                    hide_index=True
                )
            
            with col4:
                # Key insights as text instead of unnecessary charts
                total_orders = order_distribution_df['order_count'].sum()
                total_revenue = order_distribution_df['total_revenue'].sum()
                high_value_orders = order_distribution_df[order_distribution_df['order_range'] == 'Above ₹10,000']['order_count'].sum()
                high_value_revenue = order_distribution_df[order_distribution_df['order_range'] == 'Above ₹10,000']['total_revenue'].sum()
                
                st.markdown("**📈 Key Insights:**")
                st.markdown(f"• **Total Orders:** {total_orders:,}")
                st.markdown(f"• **Total Revenue:** ₹{total_revenue:,.0f}")
                st.markdown(f"• **High-Value Orders (>₹10K):** {high_value_orders} ({high_value_orders/total_orders*100:.1f}%)")
                if high_value_orders > 0:
                    st.markdown(f"• **High-Value Revenue Share:** ₹{high_value_revenue:,.0f} ({high_value_revenue/total_revenue*100:.1f}%)")
                st.markdown(f"• **Average Order Value:** ₹{total_revenue/total_orders:,.0f}")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    def render_detail_sections(self, repeat_df, region_df, spender_df):
        """Render detailed data sections"""
        st.markdown('<div class="section-card"><h2 style="color:#6f42c1;">🧮 Repeat Customers</h2>', unsafe_allow_html=True)
        st.dataframe(repeat_df, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="section-card"><h2 style="color:#fa5252;">🏆 Top Revenue Region</h2>', unsafe_allow_html=True)
        st.dataframe(region_df, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="section-card"><h2 style="color:#ffc300;">💸 Top Spender (Last 30 Days)</h2>', unsafe_allow_html=True)
        st.dataframe(spender_df, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    def run(self):
        """Main dashboard application logic"""
        # Header
        st.markdown(
            '<div class="dashboard-header">✈️ Akasa Air Data Engineer | KPI Dashboard</div>', 
            unsafe_allow_html=True
        )
        
        # Database connection
        conn = self.get_database_connection()
        
        try:
            # Region filter
            regions_query = "SELECT DISTINCT region FROM customers"
            regions_df = pd.read_sql(regions_query, conn)
            region_options = ["All"] + regions_df['region'].tolist()
            region_filter = st.selectbox("Filter KPIs by Region (optional)", region_options)
            
            # Set up region filtering
            region_clause = ""
            params = []
            if region_filter != "All":
                region_clause = " AND c.region = %s "
                params.append(region_filter)
            
            # Get queries and execute them
            queries = self.get_queries(region_clause, params)
            
            repeat_df = self.run_query(queries["Repeat Customers"], params, conn)
            region_df = self.run_query(queries["Top Revenue Region"], conn=conn)
            spender_df = self.run_query(queries["Top Spender (Last 30 Days)"], params, conn)
            monthly_df = self.run_query(queries["Orders Month-by-Month"], params, conn)
            revenue_by_region_df = self.run_query(queries["Revenue by Region"], params, conn)
            order_distribution_df = self.run_query(queries["Order Value Distribution"], params, conn)
            
            # Render dashboard components
            self.render_kpi_cards(repeat_df, region_df, spender_df)
            st.markdown("---")
            self.render_analytics_section(monthly_df, revenue_by_region_df, order_distribution_df)
            self.render_detail_sections(repeat_df, region_df, spender_df)
            
        finally:
            conn.close()


def main():
    """Entry point for the dashboard application"""
    dashboard = DashboardApp()
    dashboard.run()


if __name__ == "__main__":
    main()