from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from convert import *
import ntpath
import csv
from datetime import datetime
import time
import os
import sys

def get_app_path():
	"""Get the base application path."""
	if getattr(sys, 'frozen', False):
		# If the application is run as a bundle
		return os.path.dirname(sys.executable)
	else:
		# If the application is run from a Python interpreter
		return os.path.dirname(os.path.abspath(__file__))

def get_data_path(relative_path):
	"""Get the absolute path to a data directory."""
	base_path = get_app_path()
	return os.path.join(base_path, relative_path)

def ensure_directory_exists(path):
	"""Ensure a directory exists, create it if it doesn't."""
	if not os.path.exists(path):
		os.makedirs(path)

# Initialize paths
APP_PATH = get_app_path()
INPUT_DATA_PATH = get_data_path("input_data")
OUTPUTS_PATH = get_data_path("OUTPUTS")
EXCHANGE_RATES_PATH = get_data_path("exchange_rates")

# Ensure all required directories exist
for path in [INPUT_DATA_PATH, OUTPUTS_PATH, EXCHANGE_RATES_PATH]:
	ensure_directory_exists(path)

root = Tk()
widgets = []
labels = []
forms = []
subframes = []

new_rate_frame = Frame(root, bg="gray")
subframes.append(new_rate_frame)

convert_frame = Frame(root, bg="black")
subframes.append(convert_frame)

def check_curr_year_file_exists():
	exists = False
	curr_year = int(datetime.now().year)
	last_year = curr_year - 1
	in_file_name = "gain_loss_realized_"+str(last_year)+"-"+str(curr_year)+".csv"
	if os.path.exists(os.path.join(INPUT_DATA_PATH, in_file_name)):
		exists = True
	return exists

def store_new_rate(rate_value, month, year):
	save_rate(rate_value, month, year)

def upload_action(event=None):
	filepath = filedialog.askopenfilename()

	rows = []
	with open(filepath, "r") as f:
		csvreader = csv.reader(f)
		for row in csvreader:
			rows.append(row)
	curr_year = int(datetime.now().year)
	last_year = curr_year - 1
	in_file_name = "gain_loss_realized_"+str(last_year)+"-"+str(curr_year)+".csv"
	with open(os.path.join(INPUT_DATA_PATH, in_file_name), "w", encoding='utf-8', newline='') as csvfile:
		csvwriter = csv.writer(csvfile)
		csvwriter.writerows(rows)

	if widgets:
		destroy_widget = widgets.pop()
		destroy_widget.grid_forget()
		label_success = Label(root, text="✅ File Uploaded. Ready to convert.", fg="green", bg="black", font=("SF Pro", 12, "bold"))
		label_success.grid(row=1, column=1)
		convert_widget = widgets[0]
		convert_widget.config(state=NORMAL)
		label_reup = labels[0]
		label_reup.place(relx=0.5, rely=1.0, anchor="s")

def init_rate_frame():
	frame_init = subframes[0]
	frame_init.place(relx=0.5, rely=0.7, anchor=CENTER)
	frame_init.rowconfigure(0, weight=1)
	frame_init.columnconfigure(0, weight=1)
	frame_init.columnconfigure(1, weight=1)
	frame_init.columnconfigure(3, minsize=20)

def denit_rate_frame():
	frame_denit = subframes[0]
	frame_denit.place_forget()


def init_convert_frame():
	frame_init = subframes[1]
	frame_init.place(relx=0.5, rely=0.5, anchor=CENTER)
	convert_widget = widgets[0]
	convert_widget.grid(row=1, column=1)
	frame_init.rowconfigure(0, weight=1)
	frame_init.columnconfigure(0, weight=1)
	frame_init.columnconfigure(1, weight=1)

def denit_convert_frame():
	frame_denit = subframes[1]
	frame_denit.place_forget()

	
def denit_center_labels():
	convert_label = labels[1]
	location_label = labels[2]
	convert_label.config(text="✅ Succesfully converted.", fg="green", bg="black", font=("SF Pro", 12, "bold"))
	location_label.config(text="Find at './OUTPUTS/output_<lastyear>-<thisyear>.csv'", fg="orange", bg="black", font=("SF Pro", 12, "bold"))
	convert_label.place_forget()
	location_label.place_forget()
	
	
#def progress_bar():
#	progress.start()

#	for i in range(41):
#		time.sleep(0.05)
#		progress['value'] = i
#		root.update_idletasks()
#	progress.stop()

def convert_action(event=None):
	denit_convert_frame()
	convert_widget = widgets[0]
	convert_widget.grid_forget()
	time.sleep(0.1)

	progress_widget = widgets[1]
	#progress_widget.place(relx=0.5, rely=0.5, anchor=CENTER)
	#progress_bar()
	#progress_widget.step(99.9)
	success = True
	try:
		convert_main()
	except Exception as e:
		success = False
		err_label = f"❌ Unsuccessful. {str(e)}"
		add_rate_label = "Update missing rate:"
		missing_date = err_label.split(" ")
		missing_month = missing_date[-2]
		missing_year = missing_date[-1]

	convert_label = labels[1]
	location_label = labels[2]
	if not success:
		convert_label.config(text=err_label)
		convert_label.config(fg="red")
		location_label.config(text=add_rate_label)
		#progress_widget.place_forget()

		new_exchange_widget = widgets[3]
		missing_rate_label = labels[3]
		missing_rate_label.config(text=missing_month + " " + missing_year + ":")
		missing_rate_form = forms[0]

		# was adding the widgets/labels/forms to enter new rate for missing month next make function to add them
		convert_label.place(relx=0.5, rely=0.5, anchor=CENTER)
		location_label.place(relx=0.5, rely=0.6, anchor=CENTER) 

		init_rate_frame()
		missing_rate_label.grid(row=1, column=1)
		missing_rate_form.grid(row=1, column=2)
		new_exchange_widget.grid(row=1, column=4)
		
		
		
	else:
		convert_label.place(relx=0.5, rely=0.4, anchor=CENTER)
		location_label.place(relx=0.5, rely=0.6, anchor=CENTER)

rate_form = Entry(new_rate_frame, width=10)

def new_exchange_action():
	form = forms[0]
	rate_value = form.get()
	rate_value = rate_value.strip()
	if rate_value:
		rate_value = float(rate_value)
		form.delete(0, END)
		missing_rate_label = labels[3]
		missing_rate_date = missing_rate_label.cget("text")
		missing_rate_date = missing_rate_date.replace(":", "")
		missing_rate_date = missing_rate_date.split(" ")
		missing_rate_month = missing_rate_date[0]
		missing_rate_year = missing_rate_date[1]

		#add confirmation page/label
		#display_new_rate_success()
		store_new_rate(rate_value, missing_rate_month, missing_rate_year)
		denit_rate_frame()
		denit_center_labels()
		init_convert_frame()
		

label_upload = Label(root, text="Upload input data csv: ", fg="white", bg="black", font=("SF Pro", 12, "bold"))
btn_upload = Button(root, text="Open File", command=upload_action)

label_converted = Label(root, text="✅ Succesfully converted.", fg="green", bg="black", font=("SF Pro", 12, "bold"))
label_location = Label(root, text="Find at './OUTPUTS/output_<lastyear>-<thisyear>.csv'", fg="orange", bg="black", font=("SF Pro", 12, "bold"))

btn_convert = Button(convert_frame, text="Convert", command=convert_action)
btn_new_exchange = Button(new_rate_frame, text="Add Exchange Rate", command=new_exchange_action)
progress = ttk.Progressbar(root, orient="horizontal", length=200, mode="determinate")
missing_label = Label(new_rate_frame, text="", fg="white", bg="grey", font=("SF Pro", 12, "bold"))

widgets.append(btn_convert)
widgets.append(progress)
widgets.append(btn_upload)
widgets.append(btn_new_exchange)
label_blank = Label(root, text="", bg="black")
label_blank.grid(row=0, column=0)
label_upload.grid(row=1, column=0)
label_exists = Label(root, text="✅ Data for this year already exists. :)", fg="green", bg="black", font=("SF Pro", 12, "bold"))
label_reupload = Label(root, text="* to reupload data for the year, delete the file './input_data/gain_loss_realized_<lastyear><thisyear>.csv'", fg="yellow", bg="black", font=("SF Pro", 12, "bold"))
labels.append(label_reupload)
labels.append(label_converted)
labels.append(label_location)
labels.append(missing_label)
forms.append(rate_form)
init_convert_frame()

exists_curr_year = check_curr_year_file_exists()
if not exists_curr_year: 
	btn_convert.config(state=DISABLED)
	btn_upload.grid(row=1, column=1)
else:
	label_exists.grid(row=1, column=1)
	label_reupload.place(relx=0.5, rely=1.0, anchor="s")

#btn_convert.grid(row=1, column=1)


root.title("USD to GBP Conversions for Ty")
root.geometry("800x450")
root.config(bg="black")
root.mainloop()