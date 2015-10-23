import json
import gspread
from oauth2client.client import SignedJwtAssertionCredentials

class GoogleSpreadsheet:
	''' An iterable google spreadsheet object.  Each row is a dictionary with an entry for each field, keyed by the header.  GData libraries from Google must be installed.'''
	
	def __init__(self, spreadsheet_id, worksheet_id, source=''):
		json_key = json.load(open('/var/www/html/papers/update/Spreadsheet-1f439773fbf5.json'))
		scope = ['https://spreadsheets.google.com/feeds']
		credentials = SignedJwtAssertionCredentials(json_key['client_email'], 
							json_key['private_key'], scope)
		gc = gspread.authorize(credentials)
		# We can use url or the spreadsheet name directly
		self.count = 0
		self.gsheet = gc.open_by_key(spreadsheet_id).sheet1
		self.rows = self.formRows(self.gsheet.get_all_values())
		
	def formRows(self, ListFeed):
		rows = []
		keys = ListFeed.pop(0);
		for entry in ListFeed:
			d = {}
			for key in keys:
				d[key.lower()] = entry.pop(0)
			rows.append(d)
		return rows
			
	def __iter__(self):
		return self
		
	def next(self):
		if self.count >= len(self.rows):
			self.count = 0
			raise StopIteration
		else:
			self.count += 1
			return self.rows[self.count - 1]
	
	def __getitem__(self, item):
		return self.rows[item]
		
	def __len__(self):
		return len(self.rows)

	def add_row(self, row):
	#	try:
		self.gsheet.append_row(row)
	#		return
	#	except err:
	#		print "Error"
	#		exit(1)
	
	def reinitial(self):
		self.gsheet.resize(1,12)

	def get_row(self, rownum):
		return self.gsheet.row_values(rownum)


