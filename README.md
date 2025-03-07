# Installation

1. Download/Install Python 3.11.4   -- ENSURE ALL OPTIONS OTHER THAN [experimental] SELECTED ON INSTALL
   	- Download from: https://www.python.org/downloads/release/python-3114/
	- Installation instructions: https://docs.python.org/3/using/mac.html
				
3. Download this repository's code -- 
	- Click the green [<> Code] button above ^, then download ZIP. It might be flagged as a virus by chrome because it is a private code repository so it cannot be checked by  public scanners. If so, just turn off chrome safe browsing setting or change browser.
4. Unzip somewhere

# Usage

1. Open terminal to: `../tax_conversions/tax_conversions_env`
	- Open a Finder window, then navigate to the folder you want to use.
	- If you don’t see the path bar at the bottom of the Finder window, choose View > Show Path Bar.
	- Control-click the folder in the path bar, then do one of the following:
	- --   _Open a new window:_ Choose Open in Terminal.
	- --   _Open a new tab:_ Choose Services > New Terminal Tab at Folder. 
				
2. In the terminal run: `python3 gui.py`
3. In the GUI upload this year's realized gain loss csv file by clicking the Open button and selecting it. The example given was: `XXXX3297_GainLoss_Realized_Details_20250214-101959.csv`
4. Once uploaded, click the Convert button.
5. The formatted output is saved in the OUTPUTS folder at:  `../tax_conversions/tax_conversions_env/OUTPUTS/`

** if there are any issues, try deleting the files with `<last year>-<this year>` in the title in the input_data folder at: `../tax_conversions/tax_conversions_env/input_data/`


## Let me know of any additional features you need or any issues you run into! I only tested it on Windows, so I may need to bugfix for MacOS (although I made sure the libraries used are compatible on both). 

