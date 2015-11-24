#!/usr/bin/python
# -*- coding: UTF-8 -*-

# enable debugging
import cgitb
cgitb.enable()

print "Content-Type: text/plain;charset=utf-8"
print

##############################

###
### build pubmed query from csv file and save pubmed results as xml
###

##############################

import csv
import os
import subprocess

def buildQuery(csv_file):
	start = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id="
	pmids = ''
	end = "&rettype=xml&retmode=file"
	with open(csv_file) as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			pmid = row['PMID'].strip() # remove whitespace
			if pmid: # if not empty
				if pmid.isdigit(): # check if pmid is a digit
					pmids += pmid + ','
				else:
					print "Warning: PMID", pmid, "is not a digit."
	pmids = pmids[:-1]
	out = start + pmids + end
	return out

def system_call(command):
	p = subprocess.Popen([command], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
	out, err = p.communicate()
	print out
    
csv_file = "/var/www/html/papers/update/master_gsheet.csv"
curl = "/usr/bin/curl"

print "Building a PubMed query"
print
query = buildQuery(csv_file)
print query
print

xml_file = "/var/www/html/papers/update/NCBIData.xml"
cmd = curl+" '"+query+"' > "+xml_file

print "Downloading PubMed results as XML"
print

system_call(cmd)

print "File saved to", xml_file
print "Done"
