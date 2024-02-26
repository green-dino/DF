import os
import pandas as pd
import re

# Set the chained_assignment option to 'warn'
pd.options.mode.chained_assignment = 'warn'

class DataProcessor:
    def __init__(self, patterns):
        self.patterns = patterns

    def read_file_to_dataframe(self, file_path, sheet_name=None):
        # Determine file format and read accordingly
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
        elif file_path.endswith(('.xls', '.xlsx')):
            # If sheet_name is None, read all sheets
            if sheet_name is None:
                xls = pd.ExcelFile(file_path)
                sheet_name = xls.sheet_names
            # If sheet_name is a list, read each sheet separately and concatenate the results
            if isinstance(sheet_name, list):
                df = pd.concat([pd.read_excel(file_path, sheet_name=sheet) for sheet in sheet_name])
            else:
                df = pd.read_excel(file_path, sheet_name=sheet_name)
        else:
            raise ValueError("Unsupported file format. Please provide a CSV or XLS/XLSX file.")

        # Process data using regular expressions
        df = self.process_data(df)

        return df


    def process_data(self, df):
        # Apply regular expression patterns to relevant columns
        new_columns = {}
        for column in df.columns:
            if df[column].dtype == 'object':
                for pattern_name, pattern in self.patterns.items():
                    new_columns[column + '_' + pattern_name] = df[column].apply(lambda x: pattern.findall(str(x)))
        return pd.concat([df, pd.DataFrame(new_columns)], axis=1)

    def save_dataframe(self, df, filename, format='csv'):
        # Save DataFrame based on format
        if format == 'csv':
            df.to_csv(filename, index=False)
        elif format == 'pickle':
            df.to_pickle(filename)
        else:
            raise ValueError("Unsupported format. Please choose 'csv' or 'pickle'.")

if __name__ == "__main__":
    patterns = {
        'alpha_numeric': re.compile(b'[a-zA-Z]{5,15}'),
        'url': re.compile(b'\w+:\/\/[\w@][\w.:@]+\/?[\w.\.?=%&=\-@$,]*'),
        'email': re.compile(b'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}'),
        'phone_number': re.compile(b'\d{3}-\d{3}-\d{4}'),
        'ipv4_address': re.compile(b'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'),
        'folder_hierarchy': re.compile(b'.+(?=((\|\/).+){2})'),
        'email_address': re.compile(b'(([a-zA-Z0-9_\-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([a-zA-Z0-9\-]+\.)+))([a-zA-Z]{2,4}|[0-9]{1,3})(\]?)(\s*;\s*|\s*$))*'),
        'password': re.compile(b'^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$ %^&*-]).{8,}$'),
        'username_discord': re.compile(b'^.{3,32}#[0-9]{4}$'),
        'url': re.compile(b'(https?:\/\/)?(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()!@:%_\+.~#?&\/\/=]*)'),
        'mac_address': re.compile(b'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$'),
        'whitespace_leading': re.compile(b'^\s+'),
        'whitespace_trailing': re.compile(b'\s+$'),
        'whitespace_consecutive': re.compile(b'\s{2,}')
    }

    processor = DataProcessor(patterns)

    while True:
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

        # Prompt user to select sheet or read all sheets
        sheet_name = input("Enter the sheet name(s) you want to read (comma-separated, or leave blank to read all): ")
        sheet_name = None if not sheet_name else [s.strip() for s in sheet_name.split(',')]

        # Read file to DataFrame
        dataframe = processor.read_file_to_dataframe(file_path, sheet_name)

        # Enter the filename for the output file
        output_filename = input("Enter the filename for the output file (without extension): ")
        output_dir = os.path.join(file_dir, "output")

        # Check if the output directory exists, if not, create it
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Choose output format
        format_choice = input("Choose output format ('csv' or 'pickle'): ")

        # Save DataFrame
        try:
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
        except ValueError as ve:
            print(f"Error: {ve}")
