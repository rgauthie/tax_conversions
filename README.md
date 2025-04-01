# Tax Conversions Tool

A Python-based GUI application for converting USD to GBP tax data. This tool helps process and convert tax-related data between USD and GBP currencies.

## Features

- User-friendly graphical interface
- CSV file upload and processing
- Automatic currency conversion using exchange rates
- Support for multiple tax years

## Prerequisites

- Python 3.6 or higher
- Required Python packages (installed automatically during build)

## Installation

1. Clone or download this repository.
2. If using Unix/MacOS, open terminal to folder containing run_app.command and enter the following: chmod +x run_app.command

## Directory Structure

- `input_data/`: Directory for uploading CSV files
- `OUTPUTS/`: Directory where converted files are saved
- `exchange_rates/`: Directory containing exchange rate data
- `app.py`: Main application file
- `convert.py`: Core conversion logic
- `requirements.txt`: Python package dependencies

## Usage

1. If on Windows, double click the run_app batch file, if Unix/MacOS double click the run_app command file.
2. Navigate to the page of type that you need to convert
2. Click "Upload" to upload your CSV data, or drag and drop
3. Click "Convert" to process the data
4. Find the converted file in the `OUTPUTS` directory