import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import io
import base64
from datetime import datetime
from ydata_profiling import ProfileReport
import streamlit.components.v1 as components

# Page configuration
st.set_page_config(
    page_title="CSV Graph Visualizer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sidebar-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #2c3e50;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Main title
st.markdown('<h1 class="main-header">📊 CSV Graph Visualizer</h1>', unsafe_allow_html=True)

# File uploader with better styling
uploaded_file = st.file_uploader(
    '📁 Upload your CSV file',
    type=['csv'],
    help="Upload a CSV file to start visualizing your data"
)

# Initialize session state
if 'df' not in st.session_state:
    st.session_state.df = None
if 'graph_type' not in st.session_state:
    st.session_state.graph_type = 'Scatter Plot'

if uploaded_file is not None:
    try:
        # Load data
        df = pd.read_csv(uploaded_file)
        st.session_state.df = df
        
        # Display data info
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("📈 Rows", len(df))
        with col2:
            st.metric("📊 Columns", len(df.columns))
        with col3:
            st.metric("🔢 Numeric Columns", len(df.select_dtypes(include=['number']).columns))
        with col4:
            st.metric("📝 Text Columns", len(df.select_dtypes(include=['object']).columns))
        
        # Data preview
        with st.expander("📋 Data Preview", expanded=False):
            st.dataframe(df.head(10), use_container_width=True)
            st.write(f"**Shape:** {df.shape}")
            st.write(f"**Data Types:**")
            st.write(df.dtypes)
        
        # Sidebar controls
        st.sidebar.markdown('<h2 class="sidebar-header">🎛️ Graph Controls</h2>', unsafe_allow_html=True)
        
        # Automated EDA Report
        if st.sidebar.button("Generate Auto EDA Report"):
            st.session_state.graph_type = 'Auto EDA Report'

        # Graph type selection
        graph_types = [
            'Auto EDA Report', 'Scatter Plot', 'Line Plot', 'Bar Chart', 'Histogram', 
            'Box Plot', 'Pie Chart', 'Heatmap', 'Pair Plot'
        ]
        
        current_index = 0
        if st.session_state.graph_type in graph_types:
            current_index = graph_types.index(st.session_state.graph_type)

        graph_type = st.sidebar.selectbox(
            '📈 Select Graph Type',
            graph_types,
            index=current_index
        )
        st.session_state.graph_type = graph_type
        
        # Get column types
        numeric_columns = df.select_dtypes(include=['number']).columns.tolist()
        categorical_columns = df.select_dtypes(include=['object']).columns.tolist()
        all_columns = df.columns.tolist()
        
        # Main content area
        st.markdown("---")
        st.markdown(f"### 📊 {graph_type}")
        
        # Graph rendering based on type
        if graph_type == 'Auto EDA Report':
            st.markdown("### 🤖 Automated EDA Report")
            st.info("Generating report... This may take a moment for larger datasets.")
            profile = ProfileReport(df, title="Automated EDA Report", explorative=True)
            report_html = profile.to_html()
            components.html(report_html, height=800, scrolling=True)

        elif graph_type == 'Scatter Plot':
            col1, col2 = st.sidebar.columns(2)
            with col1:
                x_col = st.selectbox('X Axis', numeric_columns, key='scatter_x')
            with col2:
                y_col = st.selectbox('Y Axis', numeric_columns, key='scatter_y')
            
            if len(categorical_columns) > 0:
                color_col = st.sidebar.selectbox('Color By (Optional)', ['None'] + categorical_columns)
            else:
                color_col = 'None'
            
            if color_col != 'None':
                fig = px.scatter(df, x=x_col, y=y_col, color=color_col, title=f'Scatter Plot: {x_col} vs {y_col}')
            else:
                fig = px.scatter(df, x=x_col, y=y_col, title=f'Scatter Plot: {x_col} vs {y_col}')
            
            st.plotly_chart(fig, use_container_width=True)
            
        elif graph_type == 'Line Plot':
            col1, col2 = st.sidebar.columns(2)
            with col1:
                x_col = st.selectbox('X Axis', all_columns, key='line_x')
            with col2:
                y_col = st.selectbox('Y Axis', numeric_columns, key='line_y')
            
            fig = px.line(df, x=x_col, y=y_col, title=f'Line Plot: {y_col} over {x_col}')
            st.plotly_chart(fig, use_container_width=True)
            
        elif graph_type == 'Bar Chart':
            col1, col2 = st.sidebar.columns(2)
            with col1:
                x_col = st.selectbox('X Axis', all_columns, key='bar_x')
            with col2:
                y_col = st.selectbox('Y Axis', numeric_columns, key='bar_y')
            
            # Aggregate data if needed
            if df[x_col].dtype == 'object':
                agg_df = df.groupby(x_col)[y_col].mean().reset_index()
                fig = px.bar(agg_df, x=x_col, y=y_col, title=f'Bar Chart: Average {y_col} by {x_col}')
            else:
                fig = px.bar(df, x=x_col, y=y_col, title=f'Bar Chart: {y_col} by {x_col}')
            
            st.plotly_chart(fig, use_container_width=True)
            
        elif graph_type == 'Histogram':
            col = st.sidebar.selectbox('Select Column', numeric_columns, key='hist_col')
            bins = st.sidebar.slider('Number of Bins', 5, 50, 20)
            
            fig = px.histogram(df, x=col, nbins=bins, title=f'Histogram: {col}')
            st.plotly_chart(fig, use_container_width=True)
            
        elif graph_type == 'Box Plot':
            col1, col2 = st.sidebar.columns(2)
            with col1:
                x_col = st.selectbox('X Axis (Optional)', ['None'] + categorical_columns, key='box_x')
            with col2:
                y_col = st.selectbox('Y Axis', numeric_columns, key='box_y')
            
            if x_col != 'None':
                fig = px.box(df, x=x_col, y=y_col, title=f'Box Plot: {y_col} by {x_col}')
            else:
                fig = px.box(df, y=y_col, title=f'Box Plot: {y_col}')
            
            st.plotly_chart(fig, use_container_width=True)
            
        elif graph_type == 'Pie Chart':
            col = st.sidebar.selectbox('Select Column', categorical_columns, key='pie_col')
            
            # Count values
            value_counts = df[col].value_counts()
            fig = px.pie(values=value_counts.values, names=value_counts.index, title=f'Pie Chart: {col}')
            st.plotly_chart(fig, use_container_width=True)
            
        elif graph_type == 'Heatmap':
            # Correlation heatmap for numeric columns
            if len(numeric_columns) > 1:
                corr_matrix = df[numeric_columns].corr()
                fig = px.imshow(
                    corr_matrix,
                    text_auto=True,
                    aspect="auto",
                    title="Correlation Heatmap"
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("Need at least 2 numeric columns for correlation heatmap")
                
        elif graph_type == 'Pair Plot':
            if len(numeric_columns) >= 2:
                # Use seaborn for pair plot
                fig = sns.pairplot(df[numeric_columns])
                st.pyplot(fig)
            else:
                st.warning("Need at least 2 numeric columns for pair plot")
        
        # Statistics section
        st.markdown("---")
        st.markdown("### 📈 Data Statistics")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**📊 Descriptive Statistics**")
            st.dataframe(df.describe(), use_container_width=True)
        
        with col2:
            st.markdown("**🔍 Missing Values**")
            missing_data = df.isnull().sum()
            missing_df = pd.DataFrame({
                'Column': missing_data.index,
                'Missing Count': missing_data.values,
                'Missing %': (missing_data.values / len(df)) * 100
            })
            st.dataframe(missing_df[missing_df['Missing Count'] > 0], use_container_width=True)
            
            if missing_df['Missing Count'].sum() == 0:
                st.success("✅ No missing values found!")
        
        # Download section
        st.markdown("---")
        st.markdown("### 💾 Download Options")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Download CSV
            csv = df.to_csv(index=False)
            st.download_button(
                label="📥 Download CSV",
                data=csv,
                file_name=f"processed_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
        
        with col2:
            # Download plot as PNG
            if 'fig' in locals() and graph_type not in ['Auto EDA Report', 'Pair Plot']:
                img_bytes = fig.to_image(format="png")
                st.download_button(
                    label="🖼️ Download Plot (PNG)",
                    data=img_bytes,
                    file_name=f"{graph_type.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png",
                    mime="image/png"
                )
        
        with col3:
            # Download plot as HTML
            if 'fig' in locals() and graph_type not in ['Auto EDA Report', 'Pair Plot']:
                html_bytes = fig.to_html()
                st.download_button(
                    label="🌐 Download Plot (HTML)",
                    data=html_bytes,
                    file_name=f"{graph_type.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html",
                    mime="text/html"
                )
        
    except Exception as e:
        st.error(f"❌ Error loading file: {str(e)}")
        st.info("Please make sure you've uploaded a valid CSV file.")

else:
    # Welcome message
    st.markdown("""
    <div style="text-align: center; padding: 2rem;">
        <h2>🎯 Welcome to CSV Graph Visualizer!</h2>
        <p style="font-size: 1.2rem; color: #666;">
            Upload a CSV file to start creating beautiful visualizations with multiple chart types.
        </p>
        <br>
        <h3>📊 Available Chart Types:</h3>
        <ul style="text-align: left; display: inline-block;">
            <li>🤖 Auto EDA Report</li>
            <li>📈 Scatter Plot</li>
            <li>📉 Line Plot</li>
            <li>📊 Bar Chart</li>
            <li>📋 Histogram</li>
            <li>📦 Box Plot</li>
            <li>🥧 Pie Chart</li>
            <li>🔥 Heatmap</li>
            <li>🔗 Pair Plot</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
