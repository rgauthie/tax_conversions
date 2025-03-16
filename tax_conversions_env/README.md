# Tax Conversions Tool

A Python-based GUI application for converting USD to GBP tax data. This tool helps process and convert tax-related data between USD and GBP currencies.

## Features

- User-friendly graphical interface
- CSV file upload and processing
- Automatic currency conversion using exchange rates
- Support for multiple tax years
- Standalone executable available

## Prerequisites

- Python 3.6 or higher
- Required Python packages (installed automatically during build)

## Installation

### Option 1: Running from Source

1. Clone or download this repository
2. Install the required packages using one of these methods:

   **Method A - Using pip (recommended for first-time users):**
   ```bash
   pip install -r requirements.txt
   ```

   **Method B - Using pip with --user flag (if you encounter permission issues):**
   ```bash
   pip install --user -r requirements.txt
   ```

   **Method C - Using a virtual environment (recommended for developers):**
   ```bash
   # Create a virtual environment
   python -m venv venv

   # Activate the virtual environment
   # On Windows:
   .\venv\Scripts\activate
   # On Unix or MacOS:
   source venv/bin/activate

   # Install requirements
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python gui.py
   ```

### Option 2: Using the Executable

1. Download the latest release from the releases page
2. Extract the executable to your desired location
3. Double-click the executable to run the application

## Building the Executable

To create your own executable, follow these steps:

### Method 1: Using the Build Script (Recommended)

1. Make sure you have Python 3.6 or higher installed
2. Open a terminal/command prompt in the project directory
3. Run the build script:
   ```bash
   python build.py
   ```

The script will:
- Check your Python version
- Install required dependencies
- Create necessary directories
- Build the executable

### Method 2: Manual Build (Alternative)

If you encounter permission issues with the build script, you can build manually:

1. Open Command Prompt as Administrator
2. Navigate to your project directory
3. Run these commands:
   ```bash
   pip install -r requirements.txt
   pyinstaller --onefile --windowed --add-data=input_data;input_data --add-data=OUTPUTS;OUTPUTS --add-data=exchange_rates;exchange_rates gui.py
   ```

### Method 3: Using Virtual Environment (Recommended for Developers)

1. Create and activate a virtual environment:
   ```bash
   # Create virtual environment
   python -m venv venv

   # Activate it
   # On Windows:
   .\venv\Scripts\activate
   # On Unix or MacOS:
   source venv/bin/activate
   ```

2. Install requirements and build:
   ```bash
   pip install -r requirements.txt
   pyinstaller --onefile --windowed --add-data=input_data;input_data --add-data=OUTPUTS;OUTPUTS --add-data=exchange_rates;exchange_rates gui.py
   ```

### Build Output

The executable will be created in the `dist` directory and will be named:
- Windows: `Tax_Conversions.exe`
- Unix/MacOS: `Tax_Conversions`

## Directory Structure

- `input_data/`: Directory for uploading CSV files
- `OUTPUTS/`: Directory where converted files are saved
- `exchange_rates/`: Directory containing exchange rate data
- `gui.py`: Main application file
- `convert.py`: Core conversion logic
- `build.py`: Build automation script
- `requirements.txt`: Python package dependencies

## Usage

1. Launch the application
2. Click "Open File" to upload your CSV data
3. Click "Convert" to process the data
4. Find the converted file in the `OUTPUTS` directory

## File Naming Convention

- Input files should be named: `gain_loss_realized_<lastyear>-<thisyear>.csv`
- Output files will be named: `output_<lastyear>-<thisyear>.csv`

## Troubleshooting

If you encounter any issues:

1. Permission Issues:
   - Try using the `--user` flag with pip
   - Use a virtual environment
   - Run commands with administrator privileges

2. Build Issues:
   - Ensure all required directories exist
   - Check that your input CSV file follows the correct format
   - Verify that exchange rates are available for the required time period
   - Make sure you have sufficient permissions to read/write files
   - If you get PyInstaller errors, try running the build command with administrator privileges

3. Runtime Issues:
   - Verify Python version is 3.6 or higher
   - Check that all required packages are installed
   - Ensure all necessary directories exist

## Support

For issues or questions, please open an issue in the repository.

## License

[Your License Here] 