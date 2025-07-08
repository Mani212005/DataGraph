# DataGraph
# InsightiGraph: Automated EDA & Visualization Tool

✨ Welcome to InsightiGraph! This Streamlit application provides a user-friendly interface for performing Exploratory Data Analysis (EDA) and creating insightful visualizations from your CSV files. Simply upload your data and unlock valuable insights in seconds.

## Getting Started

1.  **Prerequisites:** Make sure you have Python installed on your system. You'll also need to install the required libraries. You can do this by running the following command in your terminal:

    ```bash
    pip install streamlit pandas seaborn matplotlib plotly ydata-profiling
    ```

2.  **Run the Application:** Save the provided Python script (the code you shared) as a `.py` file (e.g., `insightigraph.py`). Open your terminal, navigate to the directory where you saved the file, and run the Streamlit application using the command:

    ```bash
    streamlit run insightigraph.py
    ```

    This command will automatically open the application in your web browser.

## How to Use InsightiGraph

1.  **Upload Your Data:** Drag and drop your CSV file into the designated upload area in the sidebar on the left.

2.  **Explore Data Overview:** Once the file is uploaded, the application will automatically display a summary of your data, including:
    * Key metrics like the number of rows and columns.
    * The count of numeric and text columns.
    * A preview of the first 10 rows.
    * The shape of the dataset.
    * Descriptive statistics for numeric columns.
    * Information about missing values in each column.

3.  **Visualize Your Data:**
    * In the sidebar, under "🎨 Chart Controls", select the type of graph you want to create from the dropdown menu (e.g., Scatter Plot, Bar Chart, Histogram).
    * Depending on the selected graph type, additional options will appear in the sidebar to customize the plot (e.g., selecting columns for the X and Y axes, choosing a color variable, adjusting the number of bins for a histogram).
    * The generated interactive plot will be displayed in the main area.
    * You can download the plot as a PNG or HTML file using the download buttons in the sidebar under "💾 Download Plot".

4.  **Generate Automated EDA Report:**
    * Navigate to the "🤖 Auto EDA Report" tab.
    * Click the "Generate Detailed EDA Report" button.
    * The application will use the `ydata-profiling` library to create a comprehensive HTML report with detailed statistics, visualizations, and insights about your dataset. This report will be embedded directly into the Streamlit application, allowing you to scroll through and analyze various aspects of your data.

5.  **Download Processed CSV (Optional):** In the sidebar, you'll find a button "📥 Download Processed CSV". This allows you to download the CSV file you uploaded. Note that this button provides the original uploaded CSV without any modifications from the application.

## Key Features

* **User-Friendly Interface:** Intuitive and easy-to-navigate design powered by Streamlit.
* **Automated Data Overview:** Get a quick understanding of your data with key metrics and summaries.
* **Interactive Visualizations:** Create various types of plots, including scatter plots, line plots, bar charts, histograms, box plots, pie charts, heatmaps, pair plots, area charts, violin plots, and strip plots using Plotly and Seaborn.
* **Customizable Plots:** Easily customize the axes, colors, and other parameters of your visualizations through the sidebar controls.
* **Downloadable Plots:** Save your generated visualizations as high-quality PNG or interactive HTML files.
* **Comprehensive EDA Report:** Generate a detailed Exploratory Data Analysis report using the `ydata-profiling` library, providing in-depth insights into your data's characteristics.
* **Modern UI:** Features a clean and modern user interface with custom CSS for an enhanced experience.

## Libraries Used

* **streamlit:** For building the interactive web application.
* **pandas:** For data manipulation and analysis.
* **seaborn:** For creating statistical visualizations.
* **matplotlib.pyplot:** For underlying plot customization (used by Seaborn).
* **plotly.express:** For creating interactive Plotly visualizations.
* **ydata\_profiling:** For generating the automated EDA report.
* **datetime:** For generating unique filenames for downloaded files.
* **streamlit.components.v1:** For embedding the HTML report.

## Potential Improvements

* **More Advanced Plot Customization:** Allow users to customize plot titles, legends, tooltips, and more.
* **Data Cleaning Features:** Integrate basic data cleaning functionalities like handling missing values or duplicate rows.
* **Statistical Tests:** Include options to perform basic statistical tests and display the results.
* **Support for More File Types:** Extend support to other data formats like Excel files.
* **Saving Application State:** Allow users to save their progress and visualizations.

## Author

This application was developed using Streamlit and other open-source Python libraries. 

Mani Joshi
