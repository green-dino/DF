import streamlit as st
import pandas as pd
import networkx as nx
from data_frame_analyzer import DataFrameAnalyzer
from visualization import Visualization
from group_by_aggregation import group_by_and_aggregate
from data_analysis_options import display_data_analysis_options
from fromCSV import FileHandler
import compareDates
import dataProcessor
import data_analysis_options
import data_frame_analyzer
import data_operations
import fromCSV
import group_by_aggregation
import makeDF
import optimizedCSV
import pivot_table
from readDOCtoPickle import FileReader, DataProcessor, DataFrameHandler
import readWordtoPickle
import sorting
import visualization
import widget
from optimizedCSV import FileHandler, DataFrameHandler
import sortDF

def display_data_visualization_options(combined_dataframe, visualizer):
    selected_viz_option = st.sidebar.radio(
        "Select Visualization",
        ["Plot Histogram", "Plot Boxplot", "Plot Correlation Heatmap", "Plot Scatterplot"]
    )

    if selected_viz_option == "Plot Histogram":
        st.subheader("Histogram")
        column = st.sidebar.selectbox("Select column for histogram", combined_dataframe.columns.tolist())
        visualizer.plot_histogram(combined_dataframe, column)
    elif selected_viz_option == "Plot Boxplot":
        st.subheader("Boxplot")
        x_column = st.sidebar.selectbox("Select x-axis column", combined_dataframe.columns.tolist())
        y_column = st.sidebar.selectbox("Select y-axis column", combined_dataframe.columns.tolist())
        visualizer.plot_boxplot(combined_dataframe, x_column, y_column)
    elif selected_viz_option == "Plot Correlation Heatmap":
        st.subheader("Correlation Heatmap")
        visualizer.plot_correlation_heatmap(combined_dataframe)
    elif selected_viz_option == "Plot Scatterplot":
        st.subheader("Scatterplot")
        x_column = st.sidebar.selectbox("Select x-axis column", combined_dataframe.columns.tolist())
        y_column = st.sidebar.selectbox("Select y-axis column", combined_dataframe.columns.tolist())
        visualizer.plot_scatterplot(combined_dataframe, x_column, y_column)

def run_app():
    st.title("Data Analysis and Visualization")

    analyzer = DataFrameAnalyzer()
    visualizer = Visualization()

    # Upload CSV files
    csv_files = st.file_uploader("Upload CSV File(s)", type=["csv"], accept_multiple_files=True)

    # Combine CSV dataframes
    combined_df = pd.concat([pd.read_csv(file) for file in csv_files]) if csv_files else None

    if combined_df is not None:
        st.subheader("Combined DataFrame")
        st.write(combined_df)
        st.markdown("---")

        st.sidebar.subheader("Data Analysis")
        display_data_analysis_options(combined_df, analyzer)
        st.markdown("---")

        st.sidebar.subheader("Data Visualization")
        display_data_visualization_options(combined_df, visualizer)
        st.markdown("---")

        st.sidebar.subheader("Community Detection")
        if st.sidebar.button("Detect Communities"):
            G = nx.Graph()
            communities = analyzer.analyze_dataframe(combined_df, G)
            st.write("Communities detected:")
            st.write(communities)
        st.markdown("---")

    # Upload DOC files
    doc_files = st.file_uploader("Upload DOC File(s)", type=["doc", "docx"], accept_multiple_files=True)

    if doc_files:
        for doc_file in doc_files:
            try:
                paragraphs = FileReader.read_docx(doc_file) if doc_file.name.endswith('.docx') else FileReader.read_doc(doc_file)
                df = pd.DataFrame(paragraphs, columns=['Content'])

                processor = DataProcessor()
                processed_df = processor.process_data(df)

                if processed_df is not None:
                    st.subheader("Processed DataFrame")
                    st.write(processed_df)
                    st.markdown("---")

                    st.sidebar.subheader("Data Analysis")
                    display_data_analysis_options(processed_df, analyzer)
                    st.markdown("---")

                    st.sidebar.subheader("Data Visualization")
                    display_data_visualization_options(processed_df, visualizer)
                    st.markdown("---")

                    st.sidebar.subheader("Community Detection")
                    if st.sidebar.button("Detect Communities"):
                        G = nx.Graph()
                        communities = analyzer.analyze_dataframe(processed_df, G)
                        st.write("Communities detected:")
                        st.write(communities)
                    st.markdown("---")
                    
            except Exception as e:
                st.error(f"Error processing DOC file: {e}")

if __name__ == "__main__":
    run_app()