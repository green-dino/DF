# data_operations.py
import streamlit as st
import pandas as pd

class DataOperations:
    @staticmethod
    def handle_null_values(dataframe, action, axis=None, fill_value=None):
        """
        Handle null values in the DataFrame based on the specified action.

        Parameters:
            dataframe (pd.DataFrame): The DataFrame to handle null values.
            action (str): The action to perform - "Drop" or "Fill".
            axis (int or str, optional): The axis along which to drop null values (0 or 'index' for rows, 1 or 'columns' for columns).
            fill_value (scalar, optional): The value to use for filling null values.

        Returns:
            pd.DataFrame: The DataFrame after handling null values.
        """
        try:
            if action == "Drop":
                if axis not in [0, 1, 'index', 'columns']:
                    raise ValueError("Invalid axis value. Use 0, 'index', 1, or 'columns'.")
                new_dataframe = dataframe.dropna(axis=axis)
            elif action == "Fill":
                if fill_value is None:
                    raise ValueError("Fill value must be provided.")
                new_dataframe = dataframe.fillna(fill_value)
            else:
                new_dataframe = dataframe
            return new_dataframe
        except Exception as e:
            st.error(f"Error handling null values: {e}")
            return None
    
    @staticmethod
    def filter_rows_based_on_condition(dataframe):
        """
        Filter rows in the DataFrame based on the provided condition.

        Parameters:
            dataframe (pd.DataFrame): The DataFrame to filter.

        Returns:
            pd.DataFrame: The filtered DataFrame.
        """
        try:
            condition = st.text_input("Enter condition (e.g., column_name > 5):")
            if st.button("Filter Rows"):
                filtered_df = DataOperations.filter_dataframe(dataframe, condition)
                if filtered_df is not None:
                    st.write("Filtered DataFrame:")
                    st.write(filtered_df)
        except Exception as e:
            st.error(f"Error filtering rows: {e}")

    @staticmethod
    def filter_dataframe(dataframe, condition):
        """
        Filter the DataFrame based on the given condition.

        Parameters:
            dataframe (pd.DataFrame): The DataFrame to filter.
            condition (str): The filtering condition.

        Returns:
            pd.DataFrame or None: The filtered DataFrame if condition is provided, otherwise None.
        """
        try:
            if condition:
                filtered_df = dataframe.query(condition)
                return filtered_df
            else:
                return None
        except Exception as e:
            st.error(f"Error occurred during filtering: {e}")
            return None

    @staticmethod
    def select_rows_columns(dataframe, start_row, end_row, start_col, end_col):
        """
        Select rows and columns from the DataFrame based on the specified ranges.

        Parameters:
            dataframe (pd.DataFrame): The DataFrame to select from.
            start_row (int): The starting row index.
            end_row (int): The ending row index.
            start_col (int): The starting column index.
            end_col (int): The ending column index.

        Returns:
            pd.DataFrame: The selected rows and columns.
        """
        try:
            selected_df = dataframe.iloc[start_row:end_row+1, start_col:end_col+1]
            return selected_df
        except Exception as e:
            st.error(f"Error occurred during selection: {e}")
            return None

    @staticmethod
    def inspect_specific_columns(dataframe, header_list):
        """
        Inspect specific columns from the DataFrame.

        Parameters:
            dataframe (pd.DataFrame): The DataFrame to inspect.
            header_list (list of str): The list of column names to inspect.

        Returns:
            pd.DataFrame: The DataFrame containing only the specified columns.
        """
        try:
            inspected_df = dataframe[header_list]
            return inspected_df
        except Exception as e:
            st.error(f"Error occurred during column inspection: {e}")
            return None

    @staticmethod
    def drop_rows_columns(dataframe, rows_to_drop, cols_to_drop):
        """
        Drop specified rows and columns from the DataFrame.

        Parameters:
            dataframe (pd.DataFrame): The DataFrame to modify.
            rows_to_drop (list of int): The list of row indices to drop.
            cols_to_drop (list of str): The list of column names to drop.

        Returns:
            pd.DataFrame: The DataFrame after dropping specified rows and columns.
        """
        try:
            if rows_to_drop:
                dataframe = dataframe.drop(index=rows_to_drop, errors='ignore')
            if cols_to_drop:
                dataframe = dataframe.drop(columns=cols_to_drop, errors='ignore')
            return dataframe
        except Exception as e:
            st.error(f"Error occurred during rows/columns dropping: {e}")
            return None
