 #!/bin/bash
# Change directory to the location of your app
cd "$(dirname "$0")"  # This changes to the directory where the script is located

# Activate the virtual environment
source ./Scripts/activate  # Update this path if your venv is located elsewhere

# Run the Streamlit app
streamlit run app.py