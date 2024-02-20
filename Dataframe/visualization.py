import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

class Visualization:
    @staticmethod
    def plot_histogram(dataframe, column, bins=None, color='blue', title=None, figsize=(8, 6)):
        """
        Plot histogram.

        Parameters:
            dataframe (DataFrame): Input DataFrame.
            column (str): Name of the column to plot.
            bins (int or sequence, optional): Number of histogram bins.
            color (str, optional): Color of the histogram.
            title (str, optional): Title of the plot.
            figsize (tuple, optional): Figure size.
        """
        fig, ax = plt.subplots(figsize=figsize)
        try:
            if dataframe.empty:
                raise ValueError("DataFrame is empty.")

            if column not in dataframe:
                raise ValueError(f"Column '{column}' not found in DataFrame.")

            dataframe[column] = pd.to_numeric(dataframe[column], errors='coerce')
            sns.histplot(data=dataframe, x=column, bins=bins, color=color, kde=True, ax=ax)
            ax.set(title=f"Histogram of {column}" if title is None else title, xlabel=column, ylabel="Frequency")
            st.pyplot(fig)
        except (TypeError, ValueError) as e:
            st.error(f"Error plotting histogram: {e}")

    @staticmethod
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
            st.pyplot(fig)
        except ValueError as ve:
            st.error(f"Error plotting boxplot: {ve}")

    @staticmethod
    def plot_correlation_heatmap(dataframe, title=None, figsize=(10, 8)):
        """
        Plot correlation heatmap.

        Parameters:
            dataframe (DataFrame): Input DataFrame.
            title (str, optional): Title of the plot.
            figsize (tuple, optional): Figure size.
        """
        fig, ax = plt.subplots(figsize=figsize)
        try:
            if dataframe.empty:
                raise ValueError("DataFrame is empty.")

            numeric_cols = dataframe.select_dtypes(include=['number']).columns
            if len(numeric_cols) == 0:
                raise ValueError("No numeric columns found for correlation calculation.")

            corr_data = dataframe[numeric_cols].corr()

            if corr_data.isnull().values.any():
                raise ValueError("NaN values found in correlation data.")

            sns.heatmap(corr_data, annot=True, cmap='coolwarm', linewidths=0.5, ax=ax)
            ax.set(title="Correlation Heatmap" if title is None else title)
            st.pyplot(fig)
        except ValueError as ve:
            st.error(f"Error plotting correlation heatmap: {ve}")

    @staticmethod
    def plot_scatterplot(dataframe, x_column, y_column, color='blue', title=None, figsize=(8, 6)):
        """
        Plot scatterplot.

        Parameters:
            dataframe (DataFrame): Input DataFrame.
            x_column (str): Name of the column for x-axis.
            y_column (str): Name of the column for y-axis.
            color (str, optional): Color of the scatterplot.
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
            sns.scatterplot(data=dataframe, x=x_column, y=y_column, color=color, ax=ax)
            ax.set(title=f"Scatterplot of {x_column} vs {y_column}" if title is None else title,
                   xlabel=x_column, ylabel=y_column)
            st.pyplot(fig)
        except ValueError as ve:
            st.error(f"Error plotting scatterplot: {ve}")

    @staticmethod
    def plot_barplot(dataframe, x_column, y_column, color='blue', title=None, figsize=(8, 6)):
        """
        Plot bar plot.

        Parameters:
            dataframe (DataFrame): Input DataFrame.
            x_column (str): Name of the column for x-axis.
            y_column (str): Name of the column for y-axis.
            color (str, optional): Color of the bars.
            title (str, optional): Title of the plot.
            figsize (tuple, optional): Figure size.
        """
        fig, ax = plt.subplots(figsize=figsize)
        try:
            if dataframe.empty:
                raise ValueError("DataFrame is empty.")

            if not all(col in dataframe.columns for col in [x_column, y_column]):
                raise ValueError(f"Columns '{x_column}' or '{y_column}' not found in DataFrame.")

            sns.barplot(data=dataframe, x=x_column, y=y_column, color=color, ax=ax)
            ax.set(title=f"Bar Plot of {y_column} grouped by {x_column}" if title is None else title,
                   xlabel=x_column, ylabel=y_column)
            st.pyplot(fig)
        except ValueError as ve:
            st.error(f"Error plotting bar plot: {ve}")

    
   
    @staticmethod
    def plot_pairplot(dataframe, columns=None, hue=None, palette='viridis', title=None):
        """
        Plot pair plot.

        Parameters:
            dataframe (DataFrame): Input DataFrame.
            columns (list, optional): Columns to include in the pair plot.
            hue (str, optional): Variable to map plot aspects to different colors.
            palette (str or dict, optional): Palette for mapping hue variable.
            title (str, optional): Title of the plot.
        """
        try:
            if dataframe.empty:
                raise ValueError("DataFrame is empty.")

            if columns is None:
                columns = dataframe.columns

            # Create a Streamlit sidebar for selecting options
            selected_columns = st.sidebar.radio("Select columns", dataframe.columns.tolist(), default=columns)
            selected_hue = st.sidebar.selectbox("Select hue", [None] + dataframe.columns.tolist(), index=dataframe.columns.tolist().index(hue) + 1 if hue else 0)

            # Plot within Streamlit
            st.set_option('deprecation.showPyplotGlobalUse', False)  # To hide the warning
            pairplot = sns.pairplot(data=dataframe[selected_columns], hue=selected_hue, palette=palette)
            if title:
                plt.title(title)
            st.pyplot(pairplot)

        except Exception as e:
            st.error(f"An error occurred: {e}")
