import os
import pandas as pd
import re

class DataProcessor:
    def __init__(self):
        self.ePatt = re.compile(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}')
        self.wPatt = re.compile(r'[a-zA-Z]{5,15}')
        self.uPatt = re.compile(r'\w+:\/\/[\w@][\w.:@]+\/?[\w.\.?=%&=\-@$,]*')

    def read_file_to_dataframe(self, file_path):
        """
        Read a file into a DataFrame.

        Parameters:
        - file_path (str): The path to the file to be read.

        Returns:
        - DataFrame: The DataFrame containing the data from the file.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError("File not found.")

        # Determine file format and read accordingly
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
        elif file_path.endswith('.xls') or file_path.endswith('.xlsx'):
            df = self.read_excel_to_dataframe(file_path)
        else:
            raise ValueError("Unsupported file format. Please provide a CSV or XLS/XLSX file.")

        # Process data using regular expressions
        df = self.process_data(df)

        return df

    def read_excel_to_dataframe(self, file_path):
        """
        Read an Excel file into a DataFrame.

        Parameters:
        - file_path (str): The path to the Excel file to be read.

        Returns:
        - DataFrame: The DataFrame containing the data from the Excel file.
        """
        # Convert Excel file to CSV
        temp_csv_file = file_path[:-5] + '.csv'
        excel_data = pd.read_excel(file_path)
        excel_data.to_csv(temp_csv_file, index=False)

        # Read the CSV file into a DataFrame
        df = pd.read_csv(temp_csv_file)

        # Remove the temporary CSV file
        os.remove(temp_csv_file)

        return df

    def process_data(self, df):
        """
        Process the data in the DataFrame using regular expressions.

        Parameters:
        - df (DataFrame): The DataFrame containing the data to be processed.

        Returns:
        - DataFrame: The DataFrame with processed data.
        """
        # Apply regular expression patterns to relevant columns
        for column in df.columns:
            if df[column].dtype == 'object':
                df[column + '_emails'] = df[column].apply(lambda x: self.ePatt.findall(str(x)))
                df[column + '_words'] = df[column].apply(lambda x: self.wPatt.findall(str(x)))
                df[column + '_urls'] = df[column].apply(lambda x: self.uPatt.findall(str(x)))
        return df

    def save_dataframe(self, df, filename, format='csv'):
        """
        Save the DataFrame to a file.

        Parameters:
        - df (DataFrame): The DataFrame to be saved.
        - filename (str): The name of the output file.
        - format (str): The format in which to save the DataFrame ('csv' or 'pickle').

        Returns:
        - None
        """
        # Save DataFrame based on format
        if format == 'csv':
            df.to_csv(filename, index=False)
        elif format == 'pickle':
            df.to_pickle(filename)
        else:
            raise ValueError("Unsupported format. Please choose 'csv' or 'pickle'.")

def main():
    processor = DataProcessor()

    while True:
        try:
            # Ask user for directory containing files
            file_dir = input("Enter the directory where the file is stored (type 'exit' to quit): ")

            if file_dir.lower() == 'exit':
                break

            # List CSV and XLS files in the directory
            files = [f for f in os.listdir(file_dir) if f.endswith(('.csv', '.xls', '.xlsx'))]

            if not files:
                print("No CSV or XLS/XLSX files found in the specified directory.")
                continue

            print("Files found in the directory:")
            for i, file in enumerate(files):
                print(f"{i+1}. {file}")

            # Prompt user to select file
            file_choice = int(input("Enter the number corresponding to the file you want to use: "))
            file_path = os.path.join(file_dir, files[file_choice - 1])

            # Read file to DataFrame
            dataframe = processor.read_file_to_dataframe(file_path)

            # Enter the filename for the output file
            output_filename = input("Enter the filename for the output file (without extension): ")
            output_dir = os.path.join(file_dir, "output")

            # Check if the output directory exists, if not, create it
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)

            # Choose output format
            format_choice = input("Choose output format ('csv' or 'pickle'): ")

            # Save DataFrame
            if format_choice.lower() == 'csv':
                output_file = os.path.join(output_dir, f"{output_filename}.csv")
                processor.save_dataframe(dataframe, output_file, 'csv')
                print(f"DataFrame saved as CSV: {output_file}")
            elif format_choice.lower() == 'pickle':
                output_file = os.path.join(output_dir, f"{output_filename}.pickle")
                processor.save_dataframe(dataframe, output_file, 'pickle')
                print(f"DataFrame saved as pickle: {output_file}")
            else:
                print("Unsupported format. Please choose 'csv' or 'pickle'.")
        except (FileNotFoundError, ValueError) as e:
            print(f"Error: {e}")
        except KeyboardInterrupt:
            print("\nExiting...")
            break

if __name__ == "__main__":
    main()
