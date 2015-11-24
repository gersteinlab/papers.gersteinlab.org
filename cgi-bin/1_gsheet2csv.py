#!/usr/bin/python
# -*- coding: UTF-8 -*-

# enable debugging
import cgitb
cgitb.enable()

print "Content-Type: text/plain;charset=utf-8"
print

##############################

###
### get master google spreadsheet and save it as CSV
###

##############################

import os
import subprocess

def system_call(command):
	p = subprocess.Popen([command], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
	out, err = p.communicate()
	print out

print "Downloading master Google spreadsheet as CSV";
print
master_gsheet_csv_url = "https://docs.google.com/spreadsheets/u/2/d/113627mM7y_fvLAcSpf-vlMIEsZodV6c9aXjTaGqaLU4/export?format=csv&id=113627mM7y_fvLAcSpf-vlMIEsZodV6c9aXjTaGqaLU4&gid=0"
curl = "/usr/bin/curl"
csv_file = "/var/www/html/papers/update/master_gsheet.csv"
cmd = curl+" '"+master_gsheet_csv_url+"' > "+csv_file
print "Running a command:", cmd
print

system_call(cmd)

print "File saved to", csv_file
print "Done"
