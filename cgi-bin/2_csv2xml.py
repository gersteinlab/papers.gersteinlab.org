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

    idList = idList[:-1]
    return idList

# def buildQuery(csv_file):
#
#     api_key = "7ed7d0b92dec9fd5e111d4da0f75e225cf09" ### new requirement as of May 2018, this is DL's API key
#     start = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id="
#     idList = buildIdList(csv_file)
#     end = "&rettype=xml&retmode=file&api_key="+api_key
#
#     out = start + idList + end
#     return out

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

# print "Building a PubMed query"
# print
# query = buildQuery(csv_file)
# print query
# print
#
# xml_file = "../html/papers/update/pubmed.xml"
# cmd = curl+" '"+query+"' > "+xml_file

print "Building a PubMed query using EDirect efetch"
print efetch_cmd

print

print "Downloading PubMed results as XML.. Please Wait.."
# cmd = "/usr/bin/curl '"+query+"' > "+xml_file
cmd = efetch_cmd+" > "+xml_file
system_call(cmd)
print

print "File saved to", xml_file
print "Done"
