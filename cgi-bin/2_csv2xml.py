#!/usr/bin/python
# -*- coding: UTF-8 -*-

# enable debugging
import cgitb
cgitb.enable()

print "Content-Type: text/plain;charset=utf-8"
print

##############################

###
### build pubmed query from master gsheet csv file and save raw pubmed results as xml (pubmed.xml)
###

##############################

import csv, subprocess

def buildIdList(csv_file):
    idList=""
    with open(csv_file) as csvfile:
        reader = csv.DictReader(csvfile)
        for idx,row in enumerate(reader):
            pmid = row['PMID'].strip() # remove whitespace
            if pmid.isdigit(): # check if pmid is a digit
                idList += pmid+","
            elif pmid!="":
                print "Warning: PMID", pmid, "is not a digit."
    return idList[:-1]

def system_call(command):
    p = subprocess.Popen([command], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    out, err = p.communicate()
    if p.returncode==0:
        print "Success!"
    else:
        print "Failed!", out, err

csv_file = "../html/papers/update/master_gsheet.csv"
xml_file = "../html/papers/update/pubmed.xml"
efetch_cmd = "../html/papers/edirect/efetch -db pubmed -format xml -id "+buildIdList(csv_file)

print "Building a PubMed query using EDirect efetch"
print efetch_cmd
print

print "Downloading PubMed results as XML.. Please Wait.."
system_call(efetch_cmd+" > "+xml_file)
print

print "File saved to", xml_file
print "Done"
