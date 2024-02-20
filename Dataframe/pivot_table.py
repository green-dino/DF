import streamlit as st
import pandas as pd

def create_pivot_table(df, index_columns, columns, values, agg_func, fill_value):
    """
    Create a pivot table from the given DataFrame.

    Parameters:
        df (pd.DataFrame): The DataFrame to create the pivot table from.
        index_columns (str): The column to use for the index in the pivot table.
        columns (str): The column to use for the columns in the pivot table.
        values (list of str): The columns to use for the values in the pivot table.
        agg_func (str): The aggregation function to use.
        fill_value: The value to replace missing values with.

    Returns:
        pd.DataFrame: The resulting pivot table.
    """
    try:
        pivot_table = df.pivot_table(index=index_columns, columns=columns, values=values, aggfunc=agg_func, fill_value=fill_value)
        return pivot_table
    except Exception as e:
        raise ValueError(f"Error creating pivot table: {e}")

def main():
    st.title("Pivot Table")

    # Upload data file
    data_file = st.file_uploader("Upload data file (CSV, Excel)", type=["csv", "xlsx"])
    if data_file is not None:
        df = pd.read_csv(data_file) if data_file.name.endswith('csv') else pd.read_excel(data_file)

        st.write("Original DataFrame:")
        st.write(df)

        st.subheader("Pivot Table Settings:")
        index_columns = st.selectbox("Select index column", df.columns.tolist())
        columns = st.selectbox("Select columns (optional)", ["None"] + df.columns.tolist())
        values = st.multiselect("Select values column(s)", df.columns.tolist())
        agg_func = st.selectbox("Select aggregation function", ["sum", "mean", "count", "min", "max"])
        fill_value = st.text_input("Fill missing values with", "")

        if columns == "None":
            columns = None

        if st.button("Create Pivot Table"):
            try:
                pivot_table = create_pivot_table(df, index_columns, columns, values, agg_func, fill_value)
                st.write("Pivot Table:")
                st.write(pivot_table)
            except ValueError as ve:
                st.error(str(ve))

if __name__ == "__main__":
    main()
