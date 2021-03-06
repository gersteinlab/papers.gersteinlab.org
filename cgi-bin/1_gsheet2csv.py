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

import subprocess

def system_call(command):
    p = subprocess.Popen([command], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    out, err = p.communicate()
    if p.returncode==0:
        print "Success!"
    else:
        print "Failed!", out, err

master_gsheet_csv_url = "https://docs.google.com/spreadsheets/u/2/d/113627mM7y_fvLAcSpf-vlMIEsZodV6c9aXjTaGqaLU4/export?format=csv&id=113627mM7y_fvLAcSpf-vlMIEsZodV6c9aXjTaGqaLU4&gid=0"
subject_gsheet_csv_url = "https://docs.google.com/spreadsheets/u/2/d/1fl9mWn-vaVCTO0OXEDFyAAYAjAmOtsh8gyYJe0LbPC8/export?format=csv&id=1fl9mWn-vaVCTO0OXEDFyAAYAjAmOtsh8gyYJe0LbPC8&gid=0"

master_csv_file = "../html/papers/update/master_gsheet.csv"
subject_csv_file = "../html/papers/update/subject_gsheet.csv"

curl = "/usr/bin/curl"
cmd1 = curl+" -L '"+master_gsheet_csv_url+"' > "+master_csv_file
cmd2 = curl+" -L '"+subject_gsheet_csv_url+"' > "+subject_csv_file

print "Downloading Master Google spreadsheet as CSV:", cmd1
system_call(cmd1)
print "File saved to", master_csv_file
print

print "Downloading Subject Google spreadsheet as CSV:", cmd2
system_call(cmd2)
print "File saved to", subject_csv_file
print

print "Done"
