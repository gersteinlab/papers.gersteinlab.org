#!/usr/bin/python

from GoogleSpreadsheet import GoogleSpreadsheet#, SpreadsheetRow
import time

#spreadsheet_id = '0AiiHlTECOi8edHFxQWRwN0kxeTQ3ZzdCOXhQX2Z1ZGc'
spreadsheet_id = '11-0Vzp45Ery-VP9K9Qk3FXjZPWHeOIGuN3MxY1_8MRs'
worksheet_id = 'od6'

gs = GoogleSpreadsheet(spreadsheet_id, worksheet_id)
f = open('/var/www/html/papers/update/export_out.tab', 'r')

headers = [str(x).lower() for x in f.readline().rstrip('\n').split('\t')]
total_lines = 0

total_dict = {}
order = []
for line_num, line in enumerate(f):
	fields = line.rstrip('\n').split('\t')
	row_dict = {}
	for i, val in enumerate(fields):
		row_dict[headers[i]] = val
	if row_dict["pmid"] == "":
	#	order.append(row_dict["pmid"])
	#	total_dict[row_dict["pmid"]] = row_dict
#	else:
		order.append(row_dict["labid"])
		total_dict[row_dict["labid"]] = row_dict


gs.reinitial()
while len(order) > 0:
	new_entry = []
	tab_entry = total_dict[order.pop(0)]
	for k in gs.get_row(1):
		if k == "Pages" or k == "Volume":
			new_entry.append("#"+tab_entry[k.lower()])
		else:
			new_entry.append(tab_entry[k.lower()])
	#time.sleep(2)
	gs.add_row(new_entry)

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
