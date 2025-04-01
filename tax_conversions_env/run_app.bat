@echo off
REM Change directory to the location of your app
cd /d "%~dp0"  REM This changes to the directory where the batch file is located

REM Activate the virtual environment
call ".\Scripts\activate.bat"  REM Activating the virtual environment

REM Run the Streamlit app
streamlit run app.py

pause  REM Keeps the command window open after the script finishes