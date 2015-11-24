#!/usr/bin/python
# -*- coding: UTF-8 -*-

# enable debugging
import cgitb
cgitb.enable()

print "Content-Type: text/plain;charset=utf-8"
print

##############################

###
### build pubmed query from csv file
###

##############################

from PubmedHandler import PubmedHandler
from xml import sax
import os
import codecs
import unicodedata
import re

def parse(input_file, output_file):
    parser = sax.make_parser()
    handler = PubmedHandler(output_file)
    parser.setContentHandler(handler)
    parser.parse(input_file)

def unicode2ascii(input_file, output_file):
	out = open(output_file, 'w')
	with codecs.open(tmp_file, encoding='utf-8') as tmp:
		for line in tmp:
			original = line.encode('utf-8')
			non_ascii = re.sub(r'[ -~]', '', original).strip() # matches all non-ascii characters
			if non_ascii:
				print non_ascii

			normalized = unicodedata.normalize('NFKD', line).encode('ascii', 'ignore') # clean up non-ascii characters
			out.write(normalized+"\n")
	out.close()

xml_file = "/var/www/html/papers/update/NCBIData.xml"
tmp_file = "/var/www/html/papers/update/export.tmp"
tsv_file = "/var/www/html/papers/update/export.tsv"

print "Parsing XML to TSV file"
parse(xml_file, tmp_file)
print

print "Cleaning up unicode characters"
unicode2ascii(tmp_file, tsv_file)
print

print "File saved to", tsv_file
print "Done"