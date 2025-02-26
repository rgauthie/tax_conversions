from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from convert import *
import ntpath
import csv
from datetime import datetime
import time

root = Tk()
widgets = []
labels = []

def check_curr_year_file_exists():
	exists = False
	curr_year = int(datetime.now().year)
	last_year = curr_year - 1
	in_file_name = "gain_loss_realized_"+str(last_year)+"-"+str(curr_year)+".csv"
	if ntpath.exists("./input_data/"+in_file_name):
		exists = True
	return exists

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
	with open("./input_data/"+in_file_name, "w", encoding='utf-8', newline='') as csvfile:
		csvwriter = csv.writer(csvfile)
		csvwriter.writerows(rows)

	if widgets:
		destroy_widget = widgets.pop()
		destroy_widget.destroy()
		label_success = Label(root, text="✅ File Uploaded. Ready to convert.", fg="green", bg="black", font=("SF Pro", 12, "bold"))
		label_success.grid(row=1, column=1)
		convert_widget = widgets[0]
		convert_widget.config(state=NORMAL)
		label_reup = labels[0]
		label_reup.place(relx=0.5, rely=1.0, anchor="s")

def progress_bar():
	progress.start()

	for i in range(41):
		time.sleep(0.05)
		progress['value'] = i
		root.update_idletasks()
	progress.stop()

def convert_action(event=None):
	convert_widget = widgets[0]
	convert_widget.destroy()
	time.sleep(0.1)

	progress_widget = widgets[1]
	progress_widget.place(relx=0.5, rely=0.5, anchor=CENTER)
	progress_bar()
	progress_widget.step(99.9)
	convert_main()
	convert_label = labels[1]
	convert_label.place(relx=0.5, rely=0.4, anchor=CENTER)
	location_label = labels[2]
	location_label.place(relx=0.5, rely=0.6, anchor=CENTER)



label_upload = Label(root, text="Upload input data csv: ", fg="white", bg="black", font=("SF Pro", 12, "bold"))
btn_upload = Button(root, text="Open File", command=upload_action)

label_converted = Label(root, text="✅ Succesfully converted.", fg="green", bg="black", font=("SF Pro", 12, "bold"))
label_location = Label(root, text="Find at './OUTPUTS/output_<lastyear>-<thisyear>.csv'", fg="orange", bg="black", font=("SF Pro", 12, "bold"))

btn_convert = Button(root, text="Convert", command=convert_action)
progress = ttk.Progressbar(root, orient="horizontal", length=200, mode="determinate")
widgets.append(btn_convert)
widgets.append(progress)
widgets.append(btn_upload)
label_blank = Label(root, text="", bg="black")
label_blank.grid(row=0, column=0)
label_upload.grid(row=1, column=0)
label_exists = Label(root, text="✅ Data for this year already exists. :)", fg="green", bg="black", font=("SF Pro", 12, "bold"))
label_reupload = Label(root, text="* to reupload data for the year, delete the file './input_data/gain_loss_realized_<lastyear><thisyear>.csv'", fg="yellow", bg="black", font=("SF Pro", 12, "bold"))
labels.append(label_reupload)
labels.append(label_converted)
labels.append(label_location)

exists_curr_year = check_curr_year_file_exists()
if not exists_curr_year: 
	btn_convert.config(state=DISABLED)
	btn_upload.grid(row=1, column=1)
else:
	label_exists.grid(row=1, column=1)
	label_reupload.place(relx=0.5, rely=1.0, anchor="s")

btn_convert.place(relx=0.5, rely=0.5, anchor=CENTER)


root.title("USD to GBP Conversions for Ty")
root.geometry("800x250")
root.config(bg="black")
root.mainloop()