import streamlit as st
import pandas as pd
import networkx as nx
from data_frame_analyzer import DataFrameAnalyzer
from visualization import Visualization
from group_by_aggregation import group_by_and_aggregate
from data_analysis_options import display_data_analysis_options
from fromCSV import FileHandler

def analyze_dataframe(df, G):
    return DataFrameAnalyzer.analyze_dataframe(df)

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
    st.title("Pickle File Viewer & DataFrame Analyzer")

    analyzer = DataFrameAnalyzer()
    visualizer = Visualization()

    pickle_files = st.file_uploader("Upload Pickle File(s)", type="pickle", accept_multiple_files=True)

    if pickle_files:
        dataframes = []
        for file in pickle_files:
            try:
                df = pd.read_pickle(file)
                dataframes.append(df)
            except Exception as e:
                st.error(f"Error loading file: {e}")

        if dataframes:
            combined_df = pd.concat(dataframes)
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
                communities = analyze_dataframe(combined_df, G)
                st.write("Communities detected:")
                st.write(communities)
            st.markdown("---")

if __name__ == "__main__":
    run_app()