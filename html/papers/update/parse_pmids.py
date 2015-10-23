#!/usr/bin/python
import os, sys
from GoogleSpreadsheet import GoogleSpreadsheet
from datetime import datetime

master_spreadsheet_id = "113627mM7y_fvLAcSpf-vlMIEsZodV6c9aXjTaGqaLU4" #"thsIyYg12E8Px0zGJQsAopg"
worksheet_id = "od6"
master_spreadsheet = GoogleSpreadsheet(master_spreadsheet_id, worksheet_id)

ncbiquery = "/var/www/html/papers/update/ncbiquery.txt"
ncbiFile = open(ncbiquery,'w')

def buildQuery(master_spreadsheet, ncbiFile):
	start = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id="
	pmids = ''
	end = "&rettype=xml&retmode=file"
	for row in master_spreadsheet:
		if row['pmid']:
			pmids += row['pmid'].lstrip('\'') + ','
	pmids = pmids[:-1] 
	out = start + pmids + end + '\n'
	ncbiFile.write(out)

buildQuery(master_spreadsheet, ncbiFile)
