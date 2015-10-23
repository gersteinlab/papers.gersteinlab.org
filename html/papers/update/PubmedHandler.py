#!/usr/bin/python
# -*- coding: utf-8 -*-
from datetime import date
from xml.sax import ContentHandler
import xml.sax.saxutils

class PubmedHandler(ContentHandler):
    def __init__(self,output_file = 'export.tab'):
        self.file = file(output_file,'w')
        self.sep = '\t'

        
        self.data = {}
        self.key = ''
        self.pmid = False
        self.authors = []
        self.handling = False
        self.elements = ['Initials',    #multiple, name unique
                         'LastName',    #multiple, name unique
                         'MedlineTA',   #unique
                         'PMID',        #unique
                         'OtherID',     #unique
                         'MedlinePgn',  #unique
                         'Volume',      #unique
                         'Issue',       #unique
                         'Year',        #inside DateCreated
                         'Month',       #inside DateCreated
                         'Day',         #inside DateCreated
                         'ArticleTitle', #unique
                         'CollectiveName',#unique
                         'ArticleId',
                         'DateCreated',
                         ]
        self.file.write(self.get_header())
        
    def __del__(self):
        self.file.close()
    
    def startElement(self,name,attrs):
        if name == 'PubmedArticle':
            self.data = {'PMID':''}
            self.authors = []
            self.is_articledate = False
            self.is_pubdate = False
            self.pmid = 0
            self.handling = False
            
        elif name == 'DateCreated':
        	self.is_pubdate = True
        	self.data['Year'] = ''
        	self.data['Month']= ''
        	self.data['Day'] = ''
                    
        elif name in self.elements:
            if name == 'ArticleId':
                if attrs.getValue('IdType') == 'pmc':
                    self.key = 'PMCID'
                    self.data['PMCID'] = ''
                    self.handling = True
            else:    
                self.key = name
                self.handling = True
            if name == 'PMID':
                self.pmid += 1
            if name not in ['Year','Month','Day','PMID']:
                self.data[name] = ''
            
    def endElement(self,name):
        
        if name == 'PubmedArticle':
            self.write_to_file()
        elif name == 'DateCreated':
            self.is_pubdate = False
        elif name == 'Author': #merge author
            if self.get_data('CollectiveName'):
                self.authors.append(self.get_data('CollectiveName'))
            elif self.get_data('Initials'):
                self.authors.append(self.get_data('Initials') + ' ' + self.get_data('LastName'))
            self.data['CollectiveName'] = ''
        self.handling = False
        
    def characters(self,content):
        
        if self.handling:
            if self.key in ['Year','Month','Day']:
                if self.is_pubdate:
                    self.data[self.key] += content
            elif self.key == 'PMID':
                if self.pmid == 1:
                    self.data[self.key] += content
            else:
                self.data[self.key] += xml.sax.saxutils.escape(content)
    
    def write_to_file(self):
        try:
            self.file.write(self.get_row().encode('utf-8'))
        except UnicodeEncodeError as anomerr:
            print anomerr
            print self.get_row()
            return[]
    
    def get_row(self):
        return self.sep.join([', '.join(self.authors),
                self.get_data('MedlineTA'),
                self.get_data('PMID'),
                self.get_data('MedlinePgn'),
                self.get_data('Volume'),
                self.get_data('Year'),
                self.get_citation(),
                self.get_data('ArticleTitle'),
                self.get_data('PMCID')]) + '\n'
                
    
    def get_citation(self):
	citation = ''
	if self.get_data('Year'):
		citation += '(' + self.get_data('Year') + ').' + ' '
        citation += '<i>' + self.get_data('MedlineTA') + '</i>' + '&nbsp;'
        date_str = ''
        ref_str = ''
        #build date string
        if self.get_data('Year'):
            date_str += self.get_data('Year')
        if self.get_data('Month'):
            date_str += ' ' + self.get_data('Month')
        if self.get_int_data('Day'):
            date_str += ' %d' % self.get_int_data('Day')
        date_str = date_str.strip()
        
        #build ref string
        if self.get_data('Volume'):
            ref_str += self.get_data('Volume')
        #if self.get_data('Issue'):
        #    ref_str += '('+self.get_data('Issue')+')'
        if self.get_data('MedlinePgn'):
            ref_str += ':' + self.get_data('MedlinePgn')
            
        ref_str = ref_str.strip()
        
        #if date_str:
            #citation += date_str
        if ref_str:
            #if date_str:
                #citation += ';'
            citation += ref_str
        if citation[-1] != '.':
            citation += '.'
        return citation
                
    def get_data(self,key):
        if self.data.has_key(key):
            return self.data[key]
        return ''
    
    def get_int_data(self,key):
        val = self.get_data(key)
        try:
            val = int(val)
            return val
        except ValueError:
            pass
        return 0
        
    def get_header(self):
        return self.sep.join(['Authors','Journal','PMID','Pages','Volume','Year','Citation','Title','PMCID']) + '\n'
