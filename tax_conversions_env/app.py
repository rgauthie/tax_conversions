import streamlit as st
import pandas as pd
from datetime import datetime
import os
import sys
from convert import *  # assuming you keep your conversion logic
import webbrowser
from time import sleep


# Set page config
st.set_page_config(
    page_title="USD to GBP Conversions",
    page_icon="logo.ico",
    layout="centered"
)

# Initialize paths (similar to your original code)
def get_app_path():
    return os.path.dirname(os.path.abspath(__file__))

def ensure_directories():
    paths = {
        "input_data": "input_data",
        "outputs": "OUTPUTS",
        "exchange_rates": "exchange_rates"
    }
    
    for path in paths.values():
        if not os.path.exists(path):
            os.makedirs(path)



ensure_directories() 

def reset_conversion_state():
    if 'conversion_attempted' in st.session_state:
        del st.session_state['conversion_attempted']
    if 'missing_rate_info' in st.session_state:
        del st.session_state['missing_rate_info']
    if 'new_rate' in st.session_state:
        del st.session_state['new_rate']
    if 'file_exists' in st.session_state:
        del st.session_state['file_exists']
    if 'rate_submitted' in st.session_state:
        del st.session_state['rate_submitted']
    if 'uploader_key' in st.session_state:
        del st.session_state['uploader_key']


def store_new_rate(rate_value, month, year):
	save_rate(rate_value, month, year)


def open_outputs_folder():
    abs_path = os.path.abspath("OUTPUTS")
    webbrowser.open(f'file://{abs_path}')


def gain_loss_page():
    st.title("Gain/Loss Conversions")
    
    # Initialize session state variables
    if 'conversion_attempted' not in st.session_state:
        st.session_state.conversion_attempted = False
    if 'missing_rate_info' not in st.session_state:
        st.session_state.missing_rate_info = None
    if 'new_rate' not in st.session_state:
        st.session_state.new_rate = 0.0  # Default value for the new rate
    if 'file_exists' not in st.session_state:
        st.session_state.file_exists = False
    if 'rate_submitted' not in st.session_state:
        st.session_state.rate_submitted = ""
    if 'uploader_key' not in st.session_state:
        st.session_state.uploader_key = 1


    # File handling section
    curr_year = datetime.now().year
    last_year = curr_year - 1
    in_file_name = f"gain_loss_realized_{last_year}-{curr_year}.csv"
    file_exists = os.path.exists(os.path.join("input_data", in_file_name))
    st.session_state.file_exists = file_exists
    

    if st.session_state.file_exists:
            st.success("Data for this year already exists! Convert now, or upload again to rewrite.")
            uploaded_file = st.file_uploader("Upload input data CSV", type=['csv'], key=st.session_state['uploader_key'])
    else:
        uploaded_file = st.file_uploader("Upload input data CSV", type=['csv'], key=st.session_state['uploader_key'])

    if uploaded_file is not None:
        with st.spinner("Processing"):
            sleep(1.5)

        df = pd.read_csv(uploaded_file)
        df.to_csv(os.path.join("input_data", in_file_name), index=False)
        st.success("✅ File Uploaded. Ready to convert.")
        file_exists = True
        st.session_state.file_exists = file_exists
        st.session_state['uploader_key'] += 1

    # Convert Button and Error Handling
    if file_exists:
        col1, col2 = st.columns([2, 1])
        with col1:
            if st.button("Convert"):
                st.session_state.conversion_attempted = True
                try:
                    with st.spinner("Converting..."):
                        convert_main()  # Your existing conversion function
                    st.success("✅ Successfully converted.")
                    st.info(f"Find in the OUTPUTS folder of the project.")
                    st.session_state.missing_rate_info = None  # Clear any previous missing rate info
                    st.session_state.rate_submitted = ""
                except Exception as e:
                    error_msg = str(e)
                    rate_missing_label = error_msg.split("ERROR: ")[1]
                    st.error(f"❌ M{rate_missing_label[1:]}")
                    
                    missing_date = error_msg.split(" ")
                    missing_month = missing_date[-2]
                    missing_year = missing_date[-1]              
                    st.session_state.missing_rate_info = (missing_month, missing_year)
            if st.session_state.rate_submitted != "":
                with col2:
                    st.success(f"Rate for {st.session_state.rate_submitted} submitted successfully! Try converting again.")

            if st.session_state.conversion_attempted and st.session_state.missing_rate_info:
                missing_month, missing_year = st.session_state.missing_rate_info
                st.markdown("### Add Missing Rate")
                with st.form(key='add_rate_form'):
                    st.session_state.new_rate = st.number_input(
                        f"Rate for {missing_month} {missing_year}:",
                        min_value=0.0,
                        step=0.01,
                        format="%.4f",
                        value=st.session_state.new_rate  # Retain the value
                    )
                    submit_button = st.form_submit_button(label="Add Exchange Rate")
                    st.session_state.rate_submitted = f"{missing_month} {missing_year}"
                    
                    if submit_button:
                        try:
                            store_new_rate(st.session_state.new_rate, missing_month, missing_year)
                            st.success("Rate added successfully!")
                            # Clear the conversion attempted flag to reset the form
                            st.session_state.conversion_attempted = False
                            st.session_state.missing_rate_info = None
                            st.session_state.new_rate = 0.0  # Reset the new rate
                            st.rerun()  # Refresh the page
                        except Exception as e:
                            st.error(f"Failed to add rate: {str(e)}")

    st.markdown("---")
    st.warning("To open the OUTPUTS folder at any time, click here:")
    st.button("Open OUTPUTS folder", on_click=open_outputs_folder)

def dividends_page():
    st.title("Dividends Conversions")
    
    # Initialize session state variables
    if 'conversion_attempted' not in st.session_state:
        st.session_state.conversion_attempted = False
    if 'missing_rate_info' not in st.session_state:
        st.session_state.missing_rate_info = None
    if 'new_rate' not in st.session_state:
        st.session_state.new_rate = 0.0  # Default value for the new rate
    if 'file_exists' not in st.session_state:
        st.session_state.file_exists = False
    if 'rate_submitted' not in st.session_state:
        st.session_state.rate_submitted = ""
    if 'uploader_key' not in st.session_state:
        st.session_state.uploader_key = 2


    # File handling section
    curr_year = datetime.now().year
    last_year = curr_year - 1
    in_file_name = f"dividends_{last_year}-{curr_year}.csv"
    file_exists = os.path.exists(os.path.join("input_data", in_file_name))
    st.session_state.file_exists = file_exists
    

    if st.session_state.file_exists:
            st.success("Data for this year already exists! Convert now, or upload again to rewrite.")
            uploaded_file = st.file_uploader("Upload input data CSV", type=['csv'], key=st.session_state['uploader_key'])
    else:
        uploaded_file = st.file_uploader("Upload input data CSV", type=['csv'], key=st.session_state['uploader_key'])

    if uploaded_file is not None:
        with st.spinner("Processing"):
            sleep(1.5)

        df = pd.read_csv(uploaded_file)
        df.to_csv(os.path.join("input_data", in_file_name), index=False)
        st.success("✅ File Uploaded. Ready to convert.")
        file_exists = True
        st.session_state.file_exists = file_exists
        st.session_state['uploader_key'] += 1

    # Convert Button and Error Handling
    if file_exists:
        col1, col2 = st.columns([2, 1])
        with col1:
            if st.button("Convert"):
                st.session_state.conversion_attempted = True
                try:
                    with st.spinner("Converting..."):
                        convert_dividends()  # Your existing conversion function
                    st.success("✅ Successfully converted.")
                    st.info(f"Find in the OUTPUTS folder of the project.")
                    st.session_state.missing_rate_info = None  # Clear any previous missing rate info
                    st.session_state.rate_submitted = ""
                except Exception as e:
                    error_msg = str(e)
                    rate_missing_label = error_msg.split("ERROR: ")[1]
                    st.error(f"❌ M{rate_missing_label[1:]}")
                    
                    missing_date = error_msg.split(" ")
                    missing_month = missing_date[-2]
                    missing_year = missing_date[-1]              
                    st.session_state.missing_rate_info = (missing_month, missing_year)
            if st.session_state.rate_submitted != "":
                with col2:
                    st.success(f"Rate for {st.session_state.rate_submitted} submitted successfully! Try converting again.")

            if st.session_state.conversion_attempted and st.session_state.missing_rate_info:
                missing_month, missing_year = st.session_state.missing_rate_info
                st.markdown("### Add Missing Rate")
                with st.form(key='add_rate_form'):
                    st.session_state.new_rate = st.number_input(
                        f"Rate for {missing_month} {missing_year}:",
                        min_value=0.0,
                        step=0.01,
                        format="%.4f",
                        value=st.session_state.new_rate  # Retain the value
                    )
                    submit_button = st.form_submit_button(label="Add Exchange Rate")
                    st.session_state.rate_submitted = f"{missing_month} {missing_year}"
                    
                    if submit_button:
                        try:
                            store_new_rate(st.session_state.new_rate, missing_month, missing_year)
                            st.success("Rate added successfully!")
                            # Clear the conversion attempted flag to reset the form
                            st.session_state.conversion_attempted = False
                            st.session_state.missing_rate_info = None
                            st.session_state.new_rate = 0.0  # Reset the new rate
                            st.rerun()  # Refresh the page
                        except Exception as e:
                            st.error(f"Failed to add rate: {str(e)}")

    st.markdown("---")
    st.warning("To open the OUTPUTS folder at any time, click here:")
    st.button("Open OUTPUTS folder", on_click=open_outputs_folder)

def main():
    st.sidebar.image("logo.ico", use_container_width=True)
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Select a page", ["Gain/Loss", "Dividends"])
    st.sidebar.success("Select a conversion type above ⬆️.")

    if 'current_page' not in st.session_state:
        st.session_state.current_page = page
    elif st.session_state.current_page != page:
        reset_conversion_state()
        st.session_state.current_page = page

    if page == "Gain/Loss":
        gain_loss_page()
    elif page == "Dividends":
        dividends_page()


if __name__ == "__main__":
    main() 