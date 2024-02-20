import streamlit as st
import pandas as pd
import networkx as nx
from networkx.algorithms import community

class DataFrameAnalyzer:
    @staticmethod
    def read_pickle_to_dataframe(pickle_file):
        """Reads a pickle file into a DataFrame."""
        try:
            df = pd.read_pickle(pickle_file)
            return df
        except Exception as e:
            st.error(f"Error reading pickle file: {e}")
            return None

    @staticmethod
    def derive_column(dataframe, formula, new_column_name):
        """Derives a new column based on a formula."""
        try:
            derived_column = eval(formula, globals(), {'dataframe': dataframe})
            dataframe[new_column_name] = derived_column
            return dataframe
        except Exception as e:
            st.error(f"Error deriving column: {e}")
            return None

    @staticmethod
    def handle_null_values(dataframe, action, axis=None, fill_value=None):
        """Handles null values in the DataFrame."""
        try:
            if action == "Drop":
                new_dataframe = dataframe.dropna(axis=axis)
            elif action == "Fill" and fill_value is not None:
                new_dataframe = dataframe.fillna(fill_value)
            else:
                new_dataframe = dataframe
            return new_dataframe
        except Exception as e:
            st.error(f"Error handling null values: {e}")
            return None

    @staticmethod
    def filter_dataframe(dataframe, condition):
        """Filters DataFrame based on a condition."""
        try:
            if condition:
                filtered_df = dataframe.query(condition)
                return filtered_df
            else:
                return None
        except Exception as e:
            st.error(f"Error filtering DataFrame: {e}")
            return None

    @staticmethod
    def describe_dataframe(dataframe):
        """Generates descriptive statistics for DataFrame."""
        try:
            stats = dataframe.describe(include='all').transpose()
            stats['NaN Count'] = dataframe.isna().sum()
            return stats
        except Exception as e:
            st.error(f"Error describing DataFrame: {e}")
            return None

    @staticmethod
    def select_rows_columns(dataframe, start_row, end_row, start_col, end_col):
        """Selects rows and columns from the DataFrame."""
        try:
            return dataframe.iloc[start_row:end_row+1, start_col:end_col+1]
        except Exception as e:
            st.error(f"Error selecting rows and columns: {e}")
            return None

    @staticmethod
    def inspect_specific_columns(dataframe, header_list):
        """Inspects specific columns of the DataFrame."""
        try:
            return dataframe[header_list]
        except Exception as e:
            st.error(f"Error inspecting specific columns: {e}")
            return None

    @staticmethod
    def drop_rows_columns(dataframe, rows_to_drop, cols_to_drop):
        """Drops rows and columns from the DataFrame."""
        try:
            if rows_to_drop:
                dataframe = dataframe.drop(dataframe.index[rows_to_drop])
            if cols_to_drop:
                dataframe = dataframe.drop(columns=dataframe.columns[cols_to_drop])
            return dataframe
        except Exception as e:
            st.error(f"Error dropping rows and columns: {e}")
            return None

    @staticmethod
    def upload_multiple_files(file_type):
        """Uploads multiple files via Streamlit."""
        try:
            files = st.file_uploader(f"Upload {file_type} Files", type=[file_type], accept_multiple_files=True)
            return files
        except Exception as e:
            st.error(f"Error uploading files: {e}")
            return None

    @staticmethod
    def analyze_dataframe(df):
        """Analyzes DataFrame and detects communities."""
        try:
            G = nx.Graph()
            for index, row in df.iterrows():
                identifier, related_items = DataFrameAnalyzer.find_identifier_and_related_items(row)
                if identifier is not None and related_items is not None:
                    G.add_node(identifier)
                    for related_item in related_items:
                        G.add_node(related_item)
                        G.add_edge(identifier, related_item)
            communities = list(community.greedy_modularity_communities(G))
            return communities
        except Exception as e:
            st.error(f"Error analyzing DataFrame: {e}")
            return None

    @staticmethod
    def find_identifier_and_related_items(row):
        """Finds identifier and related items in a row."""
        try:
            identifier = None
            related_items = None
            for col, value in row.items():
                if isinstance(value, str) and value.strip():
                    if identifier is None:
                        identifier = value
                    else:
                        if related_items is None:
                            related_items = []
                        related_items.extend(value.split(','))
            return identifier, related_items
        except Exception as e:
            st.error(f"Error finding identifier and related items: {e}")
            return None, None
