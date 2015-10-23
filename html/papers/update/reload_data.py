#!/usr/bin/python

from GoogleSpreadsheet import GoogleSpreadsheet#, SpreadsheetRow
# import time
import csv

# spreadsheet_id = '0AiiHlTECOi8edHFxQWRwN0kxeTQ3ZzdCOXhQX2Z1ZGc'
spreadsheet_id = '11-0Vzp45Ery-VP9K9Qk3FXjZPWHeOIGuN3MxY1_8MRs'
worksheet_id = 'od6'
gs = GoogleSpreadsheet(spreadsheet_id, worksheet_id)

### read input file & build dictionary

file_in = open('/var/www/html/papers/update/export_out.tab', 'r')
headers = [str(x).upper() for x in file_in.readline().rstrip('\n').split('\t')]
#total_lines = 0
total_dict = {}
order = [] # order of PMID
for line_num, line in enumerate(file_in):
	fields = line.rstrip('\n').split('\t')
	row_dict = {}

	for i, val in enumerate(fields):
		row_dict[headers[i]] = val
	# if row_dict["pmid"] == "":
	order.append(row_dict["PMID"])
	total_dict[row_dict["PMID"]] = row_dict
	# else:
		# order.append(row_dict["labid"])
		# total_dict[row_dict["labid"]] = row_dict
file_in.close()

### prepare to write gsheet

gs.reinitial()

### write to CSV file

file_out = open('/var/www/html/papers/update/papers.csv', 'w')
writer = csv.writer(file_out)
writer.writerow(headers) # print header

while len(order) > 0:
	new_entry = []
	tab_entry = total_dict[order.pop(0)]
	for k in headers:
		if k == "PAGES" or k == "VOLUME":
			new_entry.append("#"+tab_entry[k])
		else:
			new_entry.append(tab_entry[k])
	# time.sleep(2)
	writer.writerow(new_entry) # write to CSV
	gs.add_row(new_entry) # write to gsheet
file_out.close()

### END

'''		
# Remove excess 		
for row in gs:
	if row["pmid"] not in row_dict.keys():
		gs.delete_row(key)

	r = SpreadsheetRow(line_num, row_dict)
	print r.index, r.row_dict
	if line_num < len(gs):
		gs.update_row(r)
	else:
		gs.add_row(r)

if total_lines < len(gs):
	for r in gs[:total_lines-1:-1]:
		gs.delete_row(r)
'''		
