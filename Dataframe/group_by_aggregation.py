# group_by_aggregation.py
import streamlit as st
import pandas as pd

def group_by_and_aggregate(dataframe, group_by_columns, aggregation_functions):
    """
    Group a DataFrame by specified columns and aggregate using specified functions.

    Parameters:
        dataframe (pd.DataFrame): The DataFrame to group and aggregate.
        group_by_columns (list of str): The columns to group by.
        aggregation_functions (dict): A dictionary where keys are column names and values are aggregation functions.

    Returns:
        pd.DataFrame or None: The grouped and aggregated DataFrame, or None if an error occurs.
    """
    try:
        # Validate group_by_columns
        for column in group_by_columns:
            if column not in dataframe.columns:
                raise ValueError(f"Column '{column}' not found in the DataFrame")

        # Validate aggregation_functions
        if not isinstance(aggregation_functions, dict):
            raise ValueError("Aggregation functions must be provided as a dictionary")

        # Filter out columns that are incompatible with aggregation functions
        compatible_columns = [col for col in aggregation_functions.keys() if col in dataframe.columns]
        aggregation_functions = {col: func for col, func in aggregation_functions.items() if col in compatible_columns}

        # Check if there are compatible columns available for aggregation
        if not compatible_columns:
            raise ValueError("No compatible columns available for aggregation. Ensure that the specified columns exist in the DataFrame and contain numerical data.")

        # Check if all aggregation functions are valid
        valid_agg_functions = ['mean', 'sum', 'min', 'max', 'count']
        for func in aggregation_functions.values():
            if func not in valid_agg_functions:
                raise ValueError(f"Invalid aggregation function: {func}. Valid functions are: {', '.join(valid_agg_functions)}")

        # Group by the specified columns and aggregate using the specified functions
        grouped_df = dataframe.groupby(group_by_columns).agg(aggregation_functions)
        return grouped_df
    except Exception as e:
        st.error(f"Error occurred during grouping and aggregation: {str(e)}")
        return None
