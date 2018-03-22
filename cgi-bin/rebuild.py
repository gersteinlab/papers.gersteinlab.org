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

def system_call(command):
    p = subprocess.Popen([command], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    print p.communicate()[0]
    return p.returncode

overallRC = 0
if overallRC == 0:
    print "========== STEP 1 =========="
    overallRC+=system_call('/var/www/cgi-bin/1_gsheet2csv.py')

if overallRC == 0:
    print "========== STEP 2 =========="
    overallRC+=system_call('/var/www/cgi-bin/2_csv2xml.py')

if overallRC == 0:
    print "========== STEP 3 =========="
    overallRC+=system_call('/var/www/cgi-bin/3_xml2tsv.py')

if overallRC == 0:
    print "========== STEP 4 =========="
    overallRC+=system_call('/var/www/cgi-bin/4_update.py')

if overallRC == 0:
    print "========== Rebuild Complete! =========="
else:
    print "========== Rebuild FAILED =========="