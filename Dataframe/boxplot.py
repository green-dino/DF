# boxplot.py

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def plot_boxplot(dataframe, x_column, y_column, color='blue', title=None, figsize=(8, 6)):
    """
    Plot boxplot.

    Parameters:
        dataframe (DataFrame): Input DataFrame.
        x_column (str): Name of the column for x-axis.
        y_column (str): Name of the column for y-axis.
        color (str, optional): Color of the boxplot.
        title (str, optional): Title of the plot.
        figsize (tuple, optional): Figure size.
    """
    fig, ax = plt.subplots(figsize=figsize)
    try:
        if dataframe.empty:
            raise ValueError("DataFrame is empty.")

        if not all(col in dataframe.columns for col in [x_column, y_column]):
            raise ValueError(f"Columns '{x_column}' or '{y_column}' not found in DataFrame.")

        dataframe = dataframe.dropna(subset=[x_column, y_column])
        sns.boxplot(data=dataframe, x=x_column, y=y_column, color=color, ax=ax)
        ax.set(title=f"Boxplot of {y_column} grouped by {x_column}" if title is None else title,
               xlabel=x_column, ylabel=y_column)
        return fig  # Return the figure object
    except ValueError as ve:
        print(f"Error plotting boxplot: {ve}")

def test_boxplot():
    """Test the plot_boxplot function."""
    data = {'group': ['A', 'A', 'B', 'B', 'B'], 'value': [1, 2, 3, 4, 5]}
    df = pd.DataFrame(data)
    fig = plot_boxplot(df, 'group', 'value')
    plt.show()

if __name__ == "__main__":
    test_boxplot()
