#!/usr/bin/python
# -*- coding: UTF-8 -*-

# enable debugging
import cgitb
cgitb.enable()

print "Content-Type: text/plain;charset=utf-8"
print

##############################

###
### master rebuild script that executes script 1, 2, 3, and 4
###

##############################

import subprocess

step1 = subprocess.Popen('/var/www/cgi-bin/1_gsheet2csv.py', stdout=subprocess.PIPE)
print step1.stdout.read()

step2 = subprocess.Popen('/var/www/cgi-bin/2_csv2xml.py', stdout=subprocess.PIPE)
print step2.stdout.read()

step3 = subprocess.Popen('/var/www/cgi-bin/3_xml2tsv.py', stdout=subprocess.PIPE)
print step3.stdout.read()

step4 = subprocess.Popen('/var/www/cgi-bin/4_update.py', stdout=subprocess.PIPE)
print step4.stdout.read()

print "Rebuild Complete!"