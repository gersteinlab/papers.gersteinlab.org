#!/usr/bin/python
# -*- coding: utf-8 -*-
from PubmedHandler import PubmedHandler
from xml import sax
import sys
import os

def main(input_file,output_file) :
    parser = sax.make_parser()
    handler = PubmedHandler(output_file)
    parser.setContentHandler(handler)
    parser.parse(input_file)
    

if __name__ == '__main__':
    input_file = 'NCBIData.xml'
    output_file = 'export.tab'
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    if len(sys.argv) > 2:
        output_file = sys.argv[2]
    
    main(input_file,output_file)

    cmd = "sed -e 's/ä/\&#228;/g' -e 's/ç/\&#231;/g' -e 's/ü/\&#252;/g' -e 's/ó/\&#243;/g' -e 's/ö/\&#246;/g' -e 's/ş/\&#351;/g' -e 's/í/\&#237;/g' -e 's/é/\&#233;/g' -e 's/ô/\&#244;/g' -e 's/è/\&#232;/g' export.tab > export_out.tab"
    os.system(cmd)
