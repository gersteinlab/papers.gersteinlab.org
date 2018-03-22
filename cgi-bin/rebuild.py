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

overallRC = 0

if overallRC == 0:
    step1 = subprocess.Popen('/var/www/cgi-bin/1_gsheet2csv.py', stdout=subprocess.PIPE)
    print step1.stdout.read()
    overallRC=overallRC+step1.returncode

if overallRC == 0:
    step2 = subprocess.Popen('/var/www/cgi-bin/2_csv2xml.py', stdout=subprocess.PIPE)
    print step2.stdout.read()
    overallRC=overallRC+step2.returncode

if overallRC == 0:
    step3 = subprocess.Popen('/var/www/cgi-bin/3_xml2tsv.py', stdout=subprocess.PIPE)
    print step3.stdout.read()
    overallRC=overallRC+step3.returncode

if overallRC == 0:
    step4 = subprocess.Popen('/var/www/cgi-bin/4_update.py', stdout=subprocess.PIPE)
    print step4.stdout.read()
    overallRC=overallRC+step4.returncode

if overallRC == 0:
    print "Rebuild Complete!"
else:
    print "Rebuild FAILED"