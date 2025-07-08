import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
from ydata_profiling import ProfileReport
import streamlit.components.v1 as components
from datetime import datetime

# --- Page Configuration ---
st.set_page_config(
    page_title="InsightiGraph: Automated EDA & Visualization",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS for a modern UI ---
st.markdown("""
<style>
    /* General Styles */
    .stApp {
        background-color: #f0f2f6;
    }
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1e3a8a; /* Dark Blue */
        text-align: center;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px #cccccc;
    }
    .section-header {
        font-size: 1.75rem;
        font-weight: bold;
        color: #3b82f6; /* Bright Blue */
        border-bottom: 2px solid #3b82f6;
        padding-bottom: 0.5rem;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #ffffff;
        padding: 1.5rem;
        border-radius: 0.75rem;
        border: 1px solid #e0e0e0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        text-align: center;
    }
    .metric-card .stMetricLabel {
        font-size: 1.1rem;
        font-weight: bold;
        color: #4b5563; /* Gray */
    }
    .metric-card .stMetricValue {
        font-size: 2.5rem;
        color: #1e3a8a;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: transparent;
        border-radius: 4px 4px 0px 0px;
        border-bottom: 2px solid #e0e0e0;
        padding: 10px 16px;
    }
    .stTabs [aria-selected="true"] {
        border-bottom: 4px solid #3b82f6;
        color: #3b82f6;
        font-weight: bold;
    }
    .stButton>button {
        background-color: #3b82f6;
        color: white;
        border-radius: 0.5rem;
        padding: 0.75rem 1.5rem;
        font-weight: bold;
        border: none;
        transition: background-color 0.3s;
    }
    .stButton>button:hover {
        background-color: #1e3a8a;
    }
    .welcome-container {
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
        color: white;
        padding: 4rem;
        border-radius: 1rem;
        text-align: center;
    }
    .welcome-container h1 {
        font-size: 3.5rem;
        font-weight: bold;
    }
    .welcome-container p {
        font-size: 1.25rem;
        max-width: 700px;
        margin: 1rem auto;
    }
</style>
""", unsafe_allow_html=True)

# --- Session State Initialization ---
if 'df' not in st.session_state:
    st.session_state.df = None

# --- Helper Functions ---

def display_welcome_message():
    """Shows a visually appealing welcome screen."""
    st.markdown("""
    <div class="welcome-container">
        <h1>✨ Welcome to InsightiGraph!</h1>
        <p>Your intelligent assistant for automated Exploratory Data Analysis (EDA) and stunning visualizations. 
        Simply upload your CSV file to unlock insights and create beautiful, interactive charts in seconds.</p>
        <p><strong>Get started by dragging and dropping your file on the left.</strong></p>
    </div>
    """, unsafe_allow_html=True)

def display_data_overview(df):
    """Displays data metrics, preview, and statistics."""
    st.markdown('<h2 class="section-header">📊 Data Overview</h2>', unsafe_allow_html=True)

    # Key Metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f'<div class="metric-card">📈<br><b>Rows</b><br><h2>{len(df)}</h2></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="metric-card">📊<br><b>Columns</b><br><h2>{len(df.columns)}</h2></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="metric-card">🔢<br><b>Numeric Cols</b><br><h2>{len(df.select_dtypes(include=["number"]).columns)}</h2></div>', unsafe_allow_html=True)
    with col4:
        st.markdown(f'<div class="metric-card">📝<br><b>Text Cols</b><br><h2>{len(df.select_dtypes(include=["object"]).columns)}</h2></div>', unsafe_allow_html=True)

    # Data Preview & Info
    with st.expander("📋 Data Preview and Types", expanded=True):
        st.dataframe(df.head(10), use_container_width=True)
        st.info(f"**Shape of the dataset:** {df.shape}")

    # Statistics
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 📈 Descriptive Statistics")
        st.dataframe(df.describe(), use_container_width=True)
    with col2:
        st.markdown("### 🔍 Missing Values")
        missing_data = df.isnull().sum().reset_index()
        missing_data.columns = ['Column', 'Missing Count']
        missing_data['Missing %'] = (missing_data['Missing Count'] / len(df)) * 100
        st.dataframe(missing_data[missing_data['Missing Count'] > 0], use_container_width=True)
        if missing_data['Missing Count'].sum() == 0:
            st.success("✅ No missing values found!")

def display_visualizations(df, graph_type):
    """Handles the creation and display of various plots."""
    st.markdown('<h2 class="section-header">🎨 Visualization Studio</h2>', unsafe_allow_html=True)
    
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
    all_cols = df.columns.tolist()

    fig = None
    # --- Plotting Logic ---
    if graph_type == 'Scatter Plot':
        st.sidebar.subheader("Scatter Plot Options")
        x_col = st.sidebar.selectbox('X-Axis', all_cols, key='scatter_x')
        y_col = st.sidebar.selectbox('Y-Axis', all_cols, key='scatter_y')
        color_col = st.sidebar.selectbox('Color By (Optional)', ['None'] + all_cols, key='scatter_color')
        color_arg = None if color_col == 'None' else color_col
        fig = px.scatter(df, x=x_col, y=y_col, color=color_arg, title=f'{x_col} vs. {y_col}')

    elif graph_type == 'Line Plot':
        st.sidebar.subheader("Line Plot Options")
        x_col = st.sidebar.selectbox('X-Axis', all_cols, key='line_x')
        y_col = st.sidebar.selectbox('Y-Axis', all_cols, key='line_y')
        fig = px.line(df, x=x_col, y=y_col, title=f'{y_col} over {x_col}')

    elif graph_type == 'Bar Chart':
        st.sidebar.subheader("Bar Chart Options")
        x_col = st.sidebar.selectbox('X-Axis', all_cols, key='bar_x')
        y_col = st.sidebar.selectbox('Y-Axis', all_cols, key='bar_y')
        fig = px.bar(df, x=x_col, y=y_col, title=f'Average {y_col} by {x_col}')

    elif graph_type == 'Histogram':
        st.sidebar.subheader("Histogram Options")
        col = st.sidebar.selectbox('Select Column', numeric_cols, key='hist_col')
        bins = st.sidebar.slider('Number of Bins', 5, 100, 20, key='hist_bins')
        fig = px.histogram(df, x=col, nbins=bins, title=f'Distribution of {col}')

    elif graph_type == 'Box Plot':
        st.sidebar.subheader("Box Plot Options")
        y_col = st.sidebar.selectbox('Y-Axis', numeric_cols, key='box_y')
        x_col = st.sidebar.selectbox('X-Axis (Optional)', ['None'] + categorical_cols, key='box_x')
        color_arg = None if x_col == 'None' else x_col
        fig = px.box(df, y=y_col, x=color_arg, title=f'Box Plot of {y_col}')

    elif graph_type == 'Pie Chart':
        st.sidebar.subheader("Pie Chart Options")
        col = st.sidebar.selectbox('Select Column', categorical_cols, key='pie_col')
        counts = df[col].value_counts()
        fig = px.pie(values=counts.values, names=counts.index, title=f'Distribution of {col}')

    elif graph_type == 'Heatmap':
        if len(numeric_cols) > 1:
            corr = df[numeric_cols].corr()
            fig = px.imshow(corr, text_auto=True, aspect="auto", title="Correlation Heatmap")
        else:
            st.warning("Heatmap requires at least 2 numeric columns.")

    elif graph_type == 'Pair Plot':
        if len(numeric_cols) >= 2:
            st.info("Generating Pair Plot... This might take a moment.")
            pair_plot_fig = sns.pairplot(df[numeric_cols])
            st.pyplot(pair_plot_fig)
        else:
            st.warning("Pair Plot requires at least 2 numeric columns.")

    elif graph_type == 'Area Chart':
        st.sidebar.subheader("Area Chart Options")
        x_col = st.sidebar.selectbox('X-Axis', all_cols, key='area_x')
        y_col = st.sidebar.selectbox('Y-Axis', all_cols, key='area_y')
        fig = px.area(df, x=x_col, y=y_col, title=f'Area Chart of {y_col} over {x_col}')

    elif graph_type == 'Violin Plot':
        st.sidebar.subheader("Violin Plot Options")
        x_col = st.sidebar.selectbox('X-Axis', all_cols, key='violin_x')
        y_col = st.sidebar.selectbox('Y-Axis', all_cols, key='violin_y')
        fig = px.violin(df, x=x_col, y=y_col, title=f'Violin Plot of {y_col} by {x_col}')

    elif graph_type == 'Strip Plot':
        st.sidebar.subheader("Strip Plot Options")
        x_col = st.sidebar.selectbox('X-Axis', all_cols, key='strip_x')
        y_col = st.sidebar.selectbox('Y-Axis', all_cols, key='strip_y')
        fig = px.strip(df, x=x_col, y=y_col, title=f'Strip Plot of {y_col} by {x_col}')

    # Display the plot if one was created
    if fig:
        st.plotly_chart(fig, use_container_width=True)
        
        # --- Download Options ---
        st.sidebar.header("💾 Download Plot")
        img_bytes = fig.to_image(format="png", scale=2)
        st.sidebar.download_button(
            label="🖼️ Download as PNG",
            data=img_bytes,
            file_name=f"{graph_type.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png",
            mime="image/png"
        )
        html_bytes = fig.to_html()
        st.sidebar.download_button(
            label="🌐 Download as HTML",
            data=html_bytes,
            file_name=f"{graph_type.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html",
            mime="text/html"
        )


def display_eda_report(df):
    """Generates and displays the ydata-profiling report."""
    st.markdown('<h2 class="section-header">🤖 Automated EDA Report</h2>', unsafe_allow_html=True)
    if st.button("Generate Detailed EDA Report"):
        with st.spinner("Generating report... This may take a few moments for large datasets."):
            profile = ProfileReport(df, title="Automated EDA Report", explorative=True)
            components.html(profile.to_html(), height=800, scrolling=True)
    else:
        st.info("Click the button above to generate a comprehensive automated report of your dataset.")


def main():
    """Main function to run the Streamlit application."""
    
    graph_type = None
    # --- Sidebar ---
    with st.sidebar:
        st.markdown('<h1 style="font-weight:bold;color:#1e3a8a;">InsightiGraph</h1>', unsafe_allow_html=True)
        uploaded_file = st.file_uploader(
            '📁 Upload your CSV file',
            type=['csv'],
            help="Upload a CSV file to start visualizing your data"
        )
        st.sidebar.markdown("---")

        if uploaded_file is not None:
            st.sidebar.header("🎨 Chart Controls")
            graph_type = st.sidebar.selectbox(
                'Select Graph Type',
                ['Scatter Plot', 'Line Plot', 'Bar Chart', 'Histogram', 'Box Plot', 'Pie Chart', 'Heatmap', 'Pair Plot', 'Area Chart', 'Violin Plot', 'Strip Plot']
            )
            st.sidebar.markdown("---")


    # --- Main Content ---
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            st.session_state.df = df
            
            # --- Download CSV ---
            csv = df.to_csv(index=False)
            st.sidebar.download_button(
                label="📥 Download Processed CSV",
                data=csv,
                file_name=f"processed_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
            

            # --- Main Application Tabs ---
            tab1, tab2, tab3 = st.tabs(["📊 Data Overview", "🎨 Visualization Studio", "🤖 Auto EDA Report"])

            with tab1:
                display_data_overview(df)
            with tab2:
                display_visualizations(df, graph_type)
            with tab3:
                display_eda_report(df)

        except Exception as e:
            st.error(f"❌ An error occurred: {e}")
            st.info("Please ensure you've uploaded a valid CSV file.")
            st.session_state.df = None
    else:
        st.session_state.df = None
        display_welcome_message()


if __name__ == "__main__":
    main()