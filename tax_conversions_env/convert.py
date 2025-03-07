import json
import csv
from datetime import datetime
import ntpath


# grab and return exchange rate data from exchange_rates.json
def get_rates():
	with open("./exchange_rates/exchange_rates.json", "r") as f:
		data = json.load(f)

	if isinstance(data, dict):
		return data["rates"]
	else:
		print("JSON Error: Check validity of conversion rate data, or repopulate the data by referring to help.")

# populate exchange_rates.json with data taken from exchange_rates.txt
## format needed in exchange_rates.txt:
###!<year>
###<month>: <rate_value>
###...
def populate_rates():
	rates_fmt = {}
	rows_for_csv = []
	with open("./exchange_rates/exchange_rates.txt", "r") as f:
		rates = ""
		for line in f:
			to_add = line.strip()+","
			rates += to_add
		rates = rates[:-1]
		rates = rates.split("!")
		rates = rates[1:]

		for year in rates:
			if len(year) < 2:
				continue
			curr_values = {}
			year_data = year.split(",")
			curr_year = year_data.pop(0)
			for month in year_data:
				if len(month) < 1:
					continue
				month_to_value = month.split(": ")
				curr_values[month_to_value[0]] = float(month_to_value[1])
				curr_month_year = month_to_value[0] + " " + curr_year
				rows_for_csv.append(["USD", float(month_to_value[1]), curr_month_year])
			rates_fmt[curr_year] = curr_values
	to_out = {"rates": rates_fmt}
	with open("./exchange_rates/exchange_rates.json", "w") as out:
		json.dump(to_out, out, indent=4, sort_keys=False)

	with open("./exchange_rates/exchange_rates.csv", "w", encoding='utf-8', newline='') as csvfile:
		fields = ["Currency Code", "Currency units per £1", "Month/Year"]
		csvwriter = csv.writer(csvfile)
		csvwriter.writerow(fields)
		csvwriter.writerows(rows_for_csv)


# grab and return data from gain_loss_realized.csv in dictionary format
## reads then rewrites to remove header before formatting the dictionary to prevent loss of field names
def get_realized():
	curr_year = int(datetime.now().year)
	last_year = curr_year - 1
	in_file_name = "gain_loss_realized_"+str(last_year)+"-"+str(curr_year)+".csv"
	headless_file_name = "gain_loss_realized_headless"+str(last_year)+"-"+str(curr_year)+".csv"
	if not ntpath.exists("./input_data/"+in_file_name):
		return

	fields = []
	rows = []
	with open("./input_data/"+in_file_name, "r") as f:
		csvreader = csv.reader(f)
		header = next(csvreader)
		if "Realized" in header[0]:
			fields = next(csvreader)
		else:
			fields = header
		
		for row in csvreader:
			rows.append(row)



	with open("./input_data/"+headless_file_name, "w", encoding='utf-8', newline='') as out:
		csvwriter = csv.writer(out)
		csvwriter.writerow(fields)
		csvwriter.writerows(rows)

	with open("./input_data/"+headless_file_name, "r") as csvfile:
		csvreader = csv.DictReader(csvfile)
		data = []
		for row in csvreader:
			data.append(row)
	return data

# convert mm/dd/yyyy value to {Year: Month}
def get_year_month(from_date):
	mm_dd_yyyy = from_date.split("/")
	date = datetime(int(mm_dd_yyyy[2]), int(mm_dd_yyyy[0]), int(mm_dd_yyyy[1]))
	month = date.strftime("%B")
	year_month = {mm_dd_yyyy[2]: month}
	return year_month

def get_rate_value(dataset, year_month):
	year = list(year_month.keys())[0]
	month = year_month[year]
	return dataset[year][month]

def calc_usd_gbp(usd_value_str, exchange_rate):
	if ',' in usd_value_str:
		usd_value_str = usd_value_str.replace(",", "")
	usd_value = float(usd_value_str[1:])
	return round(usd_value / exchange_rate, 2)

def convert_float_to_currency(value, currency="gbp"):
	symbol = "£"
	if currency == "usd":
		symbol = "$"
	negative = False
	if value < 0:
		negative = True
	equiv = symbol + "{:,.2f}".format((abs(value)))
	if negative:
		equiv = "-"+equiv
	return equiv

def manip_data():
	exchanged_fmt = []
	
	totals_usd = []
	totals_gbp = []
	data = get_realized()
	rates = get_rates()
	for row in data:
		curr_exchange = {}
		curr_exchange["Symbol"] = row["Symbol"]
		
		curr_type = "Shares"
		if "call" == row["Name"].lower()[:4]:
			curr_type = "Call Option"
		elif "put" == row["Name"].lower()[:3]:
			curr_type = "Put Option"
		curr_exchange["Asset Type"] = curr_type
		
		open_date = row["Opened Date"]
		curr_exchange["Opened Date"] = open_date
		
		cost_basis_usd = row["Cost Basis (CB)"]
		curr_exchange["Cost Basis (USD)"] = cost_basis_usd

		opened_rate = get_rate_value(rates, get_year_month(open_date))
		curr_exchange["Opened Date GBP Rate"] = opened_rate

		cost_basis_gbp = calc_usd_gbp(cost_basis_usd, opened_rate)
		curr_exchange["Cost Basis (GBP)"] = convert_float_to_currency(cost_basis_gbp)

		close_date = row["Closed Date"]
		curr_exchange["Closed Date"] = close_date

		proceeds_usd = row["Proceeds"]
		curr_exchange["Proceeds (USD)"] = proceeds_usd

		closed_rate = get_rate_value(rates, get_year_month(close_date))
		curr_exchange["Closed Date GBP Rate"] = closed_rate

		proceeds_gbp = calc_usd_gbp(proceeds_usd, closed_rate)
		curr_exchange["Proceeds (GBP)"] = convert_float_to_currency(proceeds_gbp)

		gain_loss_usd = row["Gain/Loss ($)"]
		curr_exchange["Gain/Loss (USD)"] = gain_loss_usd

		gain_loss_gbp = proceeds_gbp - cost_basis_gbp
		curr_exchange["Gain/Loss (GBP)"] = convert_float_to_currency(gain_loss_gbp)

		if "," in gain_loss_usd:
			gain_loss_usd = gain_loss_usd.replace(",","")
		if "$" in gain_loss_usd:
			gain_loss_usd = gain_loss_usd.replace("$","")
		totals_usd.append(float(gain_loss_usd))
		totals_gbp.append(gain_loss_gbp)

		exchanged_fmt.append(curr_exchange)

	totals_row = {"Symbol": "", "Asset Type": "", "Opened Date": "", "Cost Basis (USD)": "", "Opened Date GBP Rate": "", "Cost Basis (GBP)": "", "Closed Date": "", "Proceeds (USD)": "", "Closed Date GBP Rate": "", "Proceeds (GBP)": "Total Gain/Loss", "Gain/Loss (USD)": convert_float_to_currency(sum(totals_usd), currency="usd"), "Gain/Loss (GBP)": convert_float_to_currency(sum(totals_gbp))}
	exchanged_fmt.append(totals_row)
	return exchanged_fmt



def write_output(csv_dicts):
	fields = ["Symbol", "Asset Type", "Opened Date", "Cost Basis (USD)", "Opened Date GBP Rate", "Cost Basis (GBP)", "Closed Date", "Proceeds (USD)", "Closed Date GBP Rate", "Proceeds (GBP)", "Gain/Loss (USD)", "Gain/Loss (GBP)"]
	curr_year = int(datetime.now().year)
	last_year = curr_year - 1
	out_file_name = "output_"+str(last_year)+"-"+str(curr_year)+".csv"
	with open("./OUTPUTS/"+out_file_name, "w", encoding='utf-8', newline='') as csvfile:
		writer = csv.DictWriter(csvfile, fieldnames=fields)
		writer.writeheader()
		writer.writerows(csv_dicts)

# populate json data, pull realized values, calculate exchange rates, format output csv, output
def convert_main():
	populate_rates()
	res = manip_data()
	write_output(res)