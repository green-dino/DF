# Pickle File Viewer & DataFrame Analyzer

This Streamlit app allows users to upload and analyze Pickle files and Word documents, providing various data analysis and visualization options.

## Getting Started

To run this app locally, make sure you have Python installed. Then, follow these steps:

1. Clone this repository to your local machine.
2. Navigate to the project directory.
3. Install the required dependencies by running:
    ```
    pip install -r requirements.txt
    ```
4. Run the app by executing:
    ```
    streamlit run app.py
    ```

## Features

- **Upload Pickle Files:** Users can upload one or multiple Pickle files to analyze.
- **Upload DOC Files:** Users can upload one or multiple Word documents (DOC or DOCX) for analysis.
- **Data Analysis Options:** Provides various data analysis options such as sorting, group by aggregation, and community detection.
- **Data Visualization:** Offers visualization options including histograms, boxplots, correlation heatmaps, and scatterplots.
- **Community Detection:** Allows users to detect communities within the data using network analysis.

## Usage

1. Upload Pickle Files: Click on the "Upload Pickle File(s)" button and select one or more Pickle files.
2. Upload DOC Files: Click on the "Upload DOC File(s)" button and select one or more Word documents.
3. Explore Data Analysis Options: Use the sidebar to select data analysis options and visualize the results.
4. Detect Communities: Click the "Detect Communities" button to perform community detection on the uploaded data.

## Dependencies

- Streamlit
- Pandas
- NetworkX

## Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).
