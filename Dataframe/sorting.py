# sorting.py
import streamlit as st
import pandas as pd

def sort_dataframe(dataframe, sort_by_column, ascending=True):
    """
    Sort the DataFrame based on the selected column.

    Parameters:
        dataframe (pd.DataFrame): The DataFrame to sort.
        sort_by_column (str): The column to sort by.
        ascending (bool, optional): Whether to sort in ascending order.

    Returns:
        pd.DataFrame: The sorted DataFrame.
    """
    sorted_df = dataframe.sort_values(by=sort_by_column, ascending=ascending).reset_index(drop=True)
    return sorted_df

def main():
    st.title("Sorting DataFrame")

    # Upload data file
    data_file = st.file_uploader("Upload data file (CSV, Excel)", type=["csv", "xlsx"])
    if data_file is not None:
        df = pd.read_csv(data_file) if data_file.name.endswith('csv') else pd.read_excel(data_file)

        st.write("Original DataFrame:")
        st.write(df)

        st.subheader("Sorting Settings:")
        sort_by_column = st.selectbox("Select column to sort by", df.columns.tolist())

        ascending = st.checkbox("Sort in ascending order", value=True)

        if st.button("Apply Sorting"):
            sorted_df = sort_dataframe(df, sort_by_column, ascending)
            st.write("Sorted DataFrame:")
            st.write(sorted_df)

if __name__ == "__main__":
    main()
