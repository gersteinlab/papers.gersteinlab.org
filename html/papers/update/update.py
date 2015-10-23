#!/usr/bin/python

import os, sys, re
from GoogleSpreadsheet import GoogleSpreadsheet
from datetime import datetime

pubmed_spreadsheet_id = "11-0Vzp45Ery-VP9K9Qk3FXjZPWHeOIGuN3MxY1_8MRs" #"0AiiHlTECOi8edHFxQWRwN0kxeTQ3ZzdCOXhQX2Z1ZGc"
#pubmed_spreadsheet_id = "tGxc76uq9kKl80_MJHPISug"
master_spreadsheet_id = "113627mM7y_fvLAcSpf-vlMIEsZodV6c9aXjTaGqaLU4" #"thsIyYg12E8Px0zGJQsAopg"
subject_spreadsheet_id = "1fl9mWn-vaVCTO0OXEDFyAAYAjAmOtsh8gyYJe0LbPC8" #"0AiiHlTECOi8edDBCUUhtMFZzRFVMaVlxZ1JrNGp1b0E"
worksheet_id = "od6"
pubmed_spreadsheet = GoogleSpreadsheet(pubmed_spreadsheet_id, worksheet_id)
master_spreadsheet = GoogleSpreadsheet(master_spreadsheet_id, worksheet_id)
subject_spreadsheet = GoogleSpreadsheet(subject_spreadsheet_id, worksheet_id)
timestamp = str(datetime.now().ctime())

summaryPath = "/var/www/html/papers/papers/"
summaryIndex = "/var/www/html/papers/index.html"
summaryFile = open(summaryIndex,'w')
simpleIndex = "/var/www/html/papers/simple.html"
simpleFile = open(simpleIndex,'w')
simpleIndex2 = "/var/www/html/papers/papers/papers-simple.html"
simpleFile2  = open(simpleIndex2,'w')  
subjectPath = "/var/www/html/papers/subject/"
subjectIndex = subjectPath + "index.html"
subjectFile = open(subjectIndex,'w')
subjectSummaryIndex = "/var/www/html/papers/subject/index.html"
subjectSummaryFile = open(subjectSummaryIndex,'w')

header = '''<STYLE TYPE="text/css">
A { text-decoration:none; }
.headerMenu A:link { color:#993333; }
.headerMenu A:visited { color:#993333; }
.headerMenu A:active { color:#334499; }
.headerMenu A:hover { color:#334499; }
.headerMenu A:sansserif{ font-family:Arial,Helvetica,sans-serif; }
.papersList { margin-left:0px; }
.paperTitle { margin-left:50px; }
.paperTitle A:link { color:#000000; }
.paperTitle A:visited { color:#000000; }
.paperTitle A:active { color:#000000; }
.paperTitle A:hover { color:#000000; }
.paperCite { margin-left:100px; }
div#medline a {font-size:small;font-family:sans-serif,Arial,Helvetica;float:left;color:#933;padding:1px 3px;margin:2px;border:2px solid #933;}
div#null a {font-size:small;font-family:sans-serif,Arial,Helvetica;float:left;color:#000;padding:1px 23px;margin:2px;border:2px solid #F0EEE4;}
div#website a {font-size:small;font-family:sans-serif,Arial,Helvetica;float:left;color:#3ba63c;padding:1px 3px;margin:2px;border:2px solid #3ba63c;}
div#preprint a {font-size:small;font-family:sans-serif,Arial,Helvetica;float:left;color:#349;padding:1px 3px;margin:2px;border:2px solid #349;}
div#arrow-right a {font-size:small;font-family:sans-serif,Arial,Helvetica;float:left;width:0;height:0;margin:5 0 0 2;border-top:7px solid transparent;border-bottom:7px solid transparent;border-left:14px solid #F0EEE4;}
</STYLE>
</HEAD>
<BODY BGCOLOR="white">
<CENTER>
<BR />
<FONT SIZE=+2 FACE='sans-serif, Arial, Helvetica' COLOR="#334499">Gerstein Lab Publications</FONT>
<BR /><BR />
<!-- Buttons for individual sections -->
<FONT FACE='sans-serif, Arial, Helvetica' COLOR="#993333">
<SPAN CLASS="headerMenu"><A HREF="/">Main</A></SPAN>
&nbsp;&#8226;&nbsp;
<SPAN CLASS="headerMenu"><A HREF="/subject">By Subject</A></SPAN>
&nbsp;&#8226;&nbsp;
<SPAN CLASS="headerMenu"><A HREF="http://info.gersteinlab.org/Pubmed_query">Queries</A></SPAN>
&nbsp;&#8226;&nbsp;
<SPAN CLASS="headerMenu"><A HREF="http://info.gersteinlab.org/Papers_Page_Code">Code</A></SPAN>
&nbsp;&#8226;&nbsp;
<!--
<SPAN CLASS="headerMenu"><A HREF="http://wiki.gersteinlab.org/pubinfo/Paper_search">Search</A></SPAN>
&nbsp;&#8226;&nbsp;
--><SPAN CLASS="headerMenu"><A HREF="http://wiki.gersteinlab.org/pubinfo/Other_Papers">Other Writings</A></SPAN>
</FONT>
</CENTER>
<HR>
'''

def printPapers(master_spreadsheet,summaryFile, header):
	out = "<HTML>\n"
	out += "<HEAD>\n"
	out += "<TITLE>Gerstein Lab Publications</TITLE>\n"
	out += header
	out += "\n"
	out += "<CENTER>\n"
	out += "<FONT FACE='sans-serif, Arial, Helvetica'><FONT SIZE=+2 COLOR=993333>Main Scientific Publications</FONT>\n"
	out += "\n"
	out += "<H3><FONT SIZE=\"4\" COLOR=\"#334499\">Total papers: " + str(len(master_spreadsheet)) + "</FONT></H3></FONT>\n"
	out += "<p>(Last updated " + timestamp + ")</CENTER>\n"
	years = {}
	currentYear = 0
	for row in master_spreadsheet:
		rowYear = row['year']
		if years.has_key(rowYear):
			years[rowYear] += 1
		else:
			years[rowYear] = 1
	for row in master_spreadsheet:
		pubmed = pubmed_spreadsheet
		if currentYear != row['year']:
			currentYear = row['year']
			out += "<H3 ALIGN=center><FONT FACE='arial,helvetica,sans-serif' COLOR=000000 SIZE=4>-- " + currentYear + " (" + str(years[currentYear]) + ") --</FONT></H3>"
		summaryFile.write(out)
		simpleFile.write(out)
		simpleFile2.write(out)	
		out = ""
		printPaperEntry(row, summaryFile, pubmed)
		printSimpleEntry2(row, simpleFile, pubmed)
		printSimpleEntry(row,simpleFile2,pubmed)	
		printEntrySummary(row, header, pubmed)
		printEntryExtended(row)
	out = "</BODY></HTML>"
	summaryFile.write(out)
	simpleFile.write(out)

def printEntrySummary(row,header,pubmed):
	#if row['pmid']:
		#print 'pES first: ' + row['pmid']
	#else:
		#print 'pES first: no pmid'
	pubmed.count = 0
	if not row['title']:
		for pubmed_row in pubmed:
			#print 'pES pubmed: ' + pubmed_row['pmid']
			if row['pmid'] == pubmed_row['pmid']:
				row['title'] = pubmed_row['title']
				row['citation'] = pubmed_row['citation']
				row['authors'] = pubmed_row['authors']
				#row['year'] = pubmed_row['year']
				break
	# create summary directory
	entrySummary = summaryPath + row['labid'].lstrip('\'')
	if not os.path.exists(entrySummary):
		os.makedirs(entrySummary)
	entrySummaryIndex = entrySummary + "/index.html"
	entrySummaryFile = open(entrySummaryIndex,'w')
    
	out = "<HTML>\n"
	out += "<HEAD>\n"
	out += "<TITLE>" + row['title'].lstrip('\'') + "</TITLE>"
	out += header
	out += "\n"
	out += "<blockquote>\n"
	out += "<font size=+3><tt>" + row['labid'] + "</tt></font><p />"
	out += "\n"
	# print title and citation
	out += "<DIV CLASS=\"paperTitle\"><FONT SIZE=+1><B><A HREF=\"/papers/" + row['labid'].lstrip('\'') + "/index.html\">" + row['title'].lstrip('\'') + "</A></B></FONT></DIV>\n"
	if row.has_key('authors'):		
		out += "<DIV CLASS=\"paperCite\">" +row['authors'].lstrip('\'')+ " " +row['citation'].lstrip('\'') + "</DIV>\n"	
	else:		
		out += "<DIV CLASS=\"paperCite\">" + " " + row['citation'].lstrip('\'') + "</DIV>\n"	
	# print links
	out += "<DIV CLASS=\"paperCite\">"
	if not row['website']:
		#out += "<IMG SRC=\"/papers/null.gif\" HEIGHT=\"23\" WIDTH=\"56\" BORDER=\"0\">"
		out += "<div id=\"null\"><A>&nbsp;</A></div>"
	else:
		#out += "<A HREF=\"" + row['website'].lstrip('\'')  + "\"><IMG SRC=\"/papers/website.jpg\" HEIGHT=\"23\" WIDTH=\"56\" BORDER=\"0\"></A>"
		out += "<div id=\"website\"><A HREF=\"" + row['website'].lstrip('\'')  + "\">website</A></div>"
	if not row['preprint']:
		#out += "<IMG SRC=\"/papers/null.gif\" HEIGHT=\"23\" WIDTH=\"56\" BORDER=\"0\">"
		out += "<div id=\"null\"><A>&nbsp;</A></div>"
	else:
		#out += "<A HREF=\"" + row['preprint'].lstrip('\'') + "\"><IMG BORDER=\"0\" HEIGHT=\"23\" WIDTH=\"56\" SRC=\"/papers/preprint.jpg\"></A>"
		out += "<div id=\"preprint\"><A HREF=\"" + row['preprint'].lstrip('\'') + "\">preprint</A></div>"
	if not row['pmid']:
		#out += "<IMG SRC=\"/papers/null.gif\" HEIGHT=\"23\" WIDTH=\"56\" BORDER=\"0\">"
		out += "<div id=\"null\"><A>&nbsp;</A></div>"
	else:
		#out += "<A HREF=\"http://www.ncbi.nlm.nih.gov:80/entrez/query.fcgi?cmd=Retrieve&db=PubMed&list_uids=" + row['pmid'].lstrip('\'') + "&dopt=Abstract\"><IMG BORDER=\"0\" HEIGHT=\"23\" WIDTH=\"56\" SRC=\"/papers/medline.jpg\"></A>"
		out += "<div id=\"medline\"><A HREF=\"http://www.ncbi.nlm.nih.gov:80/entrez/query.fcgi?cmd=Retrieve&db=PubMed&list_uids=" + row['pmid'].lstrip('\'') + "&dopt=Abstract\">medline</A></div>"
	#if not labid:
	#	out += "<A HREF=\"#\">" + "<IMG BORDER=\"0\" WIDTH=\"23\" HEIGHT=\"23\" SRC=\"/papers/more.gif\"></A>"
	#else:
	#out += "<A HREF=\"/papers/" + row['labid'].lstrip('\'') + "/index-all.html\">" + "<IMG BORDER=\"0\" WIDTH=\"23\" HEIGHT=\"23\" SRC=\"/papers/more.gif\"></A>"
	out += "<div id=\"arrow-right\"><A HREF=\"/papers/" + row['labid'].lstrip('\'') + "/index-all.html\"></A></div>"
	out += '</DIV>\n<P style="margin: 35px;" />\n'
    
	out += "<hr><br><a href=index-all.html>View all citation information</a><br><a href='/'>Return to papers index</a><br>&nbsp;</blockquote></BODY></HTML>"
	entrySummaryFile.write(out)

def printEntryExtended(row):
	title = ''
	citation = ''
	authors = ''
	journal = ''
	pages = ''
	volume = ''
	year = ''
	pmcid = ''

	if not row['title']:
		for pubmed_row in pubmed_spreadsheet:
			if row['pmid'] == pubmed_row['pmid']:
				title = pubmed_row['title']
				citation = pubmed_row['citation']
				authors = pubmed_row['authors']
				year = row['year']	
				#year = pubmed_row['year']
				journal = pubmed_row['journal']
				pages = pubmed_row['pages'].lstrip("#")
				volume = pubmed_row['volume'].lstrip("#")
				pmcid = pubmed_row['pmcid']

	# create summary directory
	entryExtended = summaryPath + row['labid'].lstrip('\'')
	if not os.path.exists(entryExtended):
		os.makedirs(entryExtended)
	entryExtendedIndex = entryExtended + "/index-all.html"
	entryExtendedFile = open(entryExtendedIndex,'w')

	out = "<HTML>\n"
	out += "<HEAD>\n"
	if not title:
		out += "<TITLE>" + row['title'].lstrip('\'') + "</TITLE>"
	else:
		out += "<TITLE>" + title.lstrip('\'') + "</TITLE>"
	out += header
	out += "\n"
	out += "<blockquote>\n"
	if not row['labid']:
		out += "<font size=+3><tt>" + row['pmid'].lstrip('\'') + "</tt></font><p />"
	else:
		out += "<font size=+3><tt>" + row['labid'] + "</tt></font><p />"
	out += "\n"
	# print title and citation
	if not title:
		out += "<DIV CLASS=\"paperTitle\"><FONT SIZE=+1><B><A HREF=\"/papers/" + row['labid'].lstrip('\'') + "/index.html\">" + row['title'].lstrip('\'') + "</A></B></FONT></DIV>\n"
	else:
		out += "<DIV CLASS=\"paperTitle\"><FONT SIZE=+1><B><A HREF=\"/papers/" + row['labid'].lstrip('\'') + "/index.html\">" + title.lstrip('\'') + "</A></B></FONT></DIV>\n"
	if not citation:
	 	if not row.has_key('authors'):		
	 		out += "<DIV CLASS=\"paperCite\">" + " " + row['citation'].lstrip('\'') + "</DIV>\n"	
	#	out += "<DIV CLASS=\"paperCite\">" + " " + row['citation'].lstrip('\'') + "</DIV>\n"	
	 	else:		
	 		out += "<DIV CLASS=\"paperCite\">" + row['authors'].lstrip('\'') + " " +row['citation'].lstrip('\'') + "</DIV>\n"	
	else:
		out += "<DIV CLASS=\"paperCite\">" + authors.lstrip('\'') + ' ' + citation.lstrip('\'') + "</DIV>\n"
	# print links
	out += "<DIV CLASS=\"paperCite\">"
	if not row['website']:
		#out += "<IMG SRC=\"/papers/null.gif\" HEIGHT=\"23\" WIDTH=\"56\" BORDER=\"0\">"
		out += "<div id=\"null\"><A>&nbsp;</A></div>"
	else:
		#out += "<A HREF=\"" + row['website'].lstrip('\'')  + "\"><IMG SRC=\"/papers/website.jpg\" HEIGHT=\"23\" WIDTH=\"56\" BORDER=\"0\"></A>"
		out += "<div id=\"website\"><A HREF=\"" + row['website'].lstrip('\'')  + "\">website</A></div>"
	if not row['preprint']:
		#out += "<IMG SRC=\"/papers/null.gif\" HEIGHT=\"23\" WIDTH=\"56\" BORDER=\"0\">"
		out += "<div id=\"null\"><A>&nbsp;</A></div>"
	else:
		#out += "<A HREF=\"" + row['preprint'].lstrip('\'') + "\"><IMG BORDER=\"0\" HEIGHT=\"23\" WIDTH=\"56\" SRC=\"/papers/preprint.jpg\"></A>"
		out += "<div id=\"preprint\"><A HREF=\"" + row['preprint'].lstrip('\'') + "\">preprint</A></div>"
	if not row['pmid']:
		#out += "<IMG SRC=\"/papers/null.gif\" HEIGHT=\"23\" WIDTH=\"56\" BORDER=\"0\">"
		out += "<div id=\"null\"><A>&nbsp;</A></div>"
	else:
		#out += "<A HREF=\"http://www.ncbi.nlm.nih.gov:80/entrez/query.fcgi?cmd=Retrieve&db=PubMed&list_uids=" + row['pmid'].lstrip('\'') + "&dopt=Abstract\"><IMG BORDER=\"0\" HEIGHT=\"23\" WIDTH=\"56\" SRC=\"/papers/medline.jpg\"></A>"
		out += "<div id=\"medline\"><A HREF=\"http://www.ncbi.nlm.nih.gov:80/entrez/query.fcgi?cmd=Retrieve&db=PubMed&list_uids=" + row['pmid'].lstrip('\'') + "&dopt=Abstract\">medline</A></div>"
	#if not labid:
	#       out += "<A HREF=\"#\">" + "<IMG BORDER=\"0\" WIDTH=\"23\" HEIGHT=\"23\" SRC=\"/papers/more.gif\"></A>"
	#else:
	#out += "<A HREF=\"/papers/" + row['labid'].lstrip('\'') + "/index-all.html\">" + "<IMG BORDER=\"0\" WIDTH=\"23\" HEIGHT=\"23\" SRC=\"/papers/more.gif\"></A>"
	out += "<div id=\"arrow-right\"><A HREF=\"/papers/" + row['labid'].lstrip('\'') + "/index-all.html\"></A></div>"
	out += '</DIV>\n<P style="margin: 35px;" />\n'

	out += '<A HREF="index.html">Switch to compact view</A><hr>\n<table>\n'
	if not authors:
		out += '<tr><td width=100><b><font color=gray>Authors</font></b></td><td><b><font color=#000077>&nbsp;</font></b></td></tr>\n'
	else:
		out += '<tr><td width=100><b><font color=gray>Authors</font></b></td><td><b><font color=#000077>'
		link = '<A HREF="http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=PureSearch&db=PubMed&details_term=%s">%s</A>'
		authorlinks = [link % (a.lstrip('\'').strip().replace(' ','%20'),a.lstrip('\'').strip()) for a in authors.split(',')]
		# print authorlinks
		out += ', '.join(authorlinks)
		out += '</font></b></td></tr>\n'
	if not journal:
		out += '<tr><td width=100><b><font color=gray>Journal</font></b></td><td><b><font color=#000077>&nbsp;</font></b></td></tr>\n'
	else:
		out += '<tr><td width=100><b><font color=gray>Journal</font></b></td><td><b><font color=#000077>'
		out += '<A HREF="http://locatorplus.gov/cgi-bin/Pwebrecon.cgi?DB=local&v2=1&ti=1,1&Search_Arg=9808944&Search_Code=0359&CNT=20&SID=1">'
		out += journal + '</A></font></b></td></tr>'
	if not row['pmid']:
		out += "<tr><td width=100><b><font color=gray>PMID</font></b></td><td><b><font color=#000077>&nbsp;</font></b></td></tr>\n"
	else:
		out += '<tr><td width=100><b><font color=gray>PMID</font></b></td><td><b><font color=#000077>'
		out += '<A HREF="http://www.ncbi.nlm.nih.gov:80/entrez/query.fcgi?cmd=Retrieve&db=PubMed&list_uids=' + row['pmid'].lstrip('\'') + '&dopt=Abstract">'
		out +=  row['pmid'].lstrip('\'') + '</A></font></b></td></tr>\n'
	if not pages:
		out += "<tr><td width=100><b><font color=gray>Pages</font></b></td><td><b><font color=#000077>&nbsp;</font></b></td></tr>\n"
	else:
		out += "<tr><td width=100><b><font color=gray>Pages</font></b></td><td><b><font color=#000077>" + pages.lstrip('\'') + "</font></b></td></tr>\n"
	if not volume:
		out += "<tr><td width=100><b><font color=gray>Volume</font></b></td><td><b><font color=#000077>&nbsp;</font></b></td></tr>\n"
	else:
		out += "<tr><td width=100><b><font color=gray>Volume</font></b></td><td><b><font color=#000077>" + volume.lstrip('\'') + "</font></b></td></tr>\n"
	if not year:
		out += "<tr><td width=100><b><font color=gray>Year</font></b></td><td><b><font color=#000077>&nbsp;</font></b></td></tr>\n"
	else:
		out += "<tr><td width=100><b><font color=gray>Year</font></b></td><td><b><font color=#000077>" + year.lstrip('\'') + "</font></b></td></tr>\n"
	out += "<tr><td width=100><b><font color=gray>labcite</font></b></td><td><b><font color=#000077>" + citation.lstrip('\'') + "</font></b></td></tr>\n"
	if not row['labid']:
		out += "<tr><td width=100><b><font color=gray>labid</font></b></td><td><b><font color=#000077>&nbsp;</font></b></td></tr>\n"
	else:
		out += "<tr><td width=100><b><font color=gray>labid</font></b></td><td><b><font color=#000077>" + row['labid'].lstrip('\'') + "</font></b></td></tr>\n"
	if not title:
		out += "<tr><td width=100><b><font color=gray>labtitle</font></b></td><td><b><font color=#000077>&nbsp;</font></b></td></tr>\n"
	else:
		out += "<tr><td width=100><b><font color=gray>labtitle</font></b></td><td><b><font color=#000077>" + title.lstrip('\'') + "</font></b></td></tr>\n"
	if not row['subject']:
		out += "<tr><td width=100><b><font color=gray>subject</font></b></td><td><b><font color=#000077>&nbsp;</font></b></td></tr>\n"
	else:
		subjects = row['subject'].split(',')
		num_subjects = len(subjects)
		out += '<tr><td width=100><b><font color=gray>subject</font></b></td><td><b><font color=#000077>'
		subject_count = 0
		for subject in subjects:
			out += '<A HREF="/subject/' + subject.lstrip('\' ') + '">' + subject.lstrip('\' ') + '</A>'
			subject_count += 1
			if subject_count < num_subjects:
				out += ', '
		out += '</font></b></td></tr>\n'
	if not row['website']:
		out += "<tr><td width=100><b><font color=gray>website</font></b></td><td><b><font color=#000077>&nbsp;</font></b></td></tr>\n"
	else:
		out += '<tr><td width=100><b><font color=gray>website</font></b></td><td><b><font color=#000077><A HREF="'+row['website'].lstrip('\'')+'">'+row['website'].lstrip('\'')+'</A></font></b></td></tr>\n'
	
	out += "</table><br><font color=gray>Unused tags: <i>e-print footnote grant ignore preprint sortval target website2</i></font><hr><a href='/'>Return to papers index</a><br>&nbsp;</blockquote></BODY></HTML>"
	entryExtendedFile.write(out)

def printPaperEntry(row, summaryFile, pubmed):
	title = ''
	citation = ''
	authors = ''
	year = ''
	if not row['title']:
		for pubmed_row in pubmed:
			if row['pmid'] == pubmed_row['pmid']:
				title = pubmed_row['title']
				citation = pubmed_row['citation']
				authors = pubmed_row['authors']
				year = row['year']	
				#year = pubmed_row['year']
	  			break
	# print title and citation
	if not title:
		out = "<DIV CLASS=\"paperTitle\"><FONT SIZE=+1><B><A HREF=\"/papers/" + row['labid'].lstrip('\'') + "/index.html\">" + row['title'] + "</A></B></FONT></DIV>\n"
	else:
		out = "<DIV CLASS=\"paperTitle\"><FONT SIZE=+1><B><A HREF=\"/papers/" + row['labid'].lstrip('\'') + "/index.html\">" + title.lstrip('\'') + "</A></B></FONT></DIV>\n"
	if not citation:
		if not row.has_key('authors'):	
			out += "<DIV CLASS=\"paperCite\">" + row['citation'].lstrip('\'') + "</DIV>\n"	
		else:	
			out += "<DIV CLASS =\"paperCite\">" + row['authors'].lstrip('\'') + " " + row['citation'].lstrip('\'') + "</DIV>\n"			
	else:
		p = re.compile("\(\d+\)\.")
		p2 = re.compile(":")
		citation = p.sub("",citation)
		citation = p2.sub(": ",citation)  	
		out += "<DIV CLASS=\"paperCite\">" + authors.lstrip('\'') + "&nbsp;" + "(" + row['year'] + ")." +   citation.lstrip('\'') + "</DIV>\n"
	# print links
	out += "<DIV CLASS=\"paperCite\">"
	if not row['website']:
		#out += "<IMG SRC=\"/papers/null.gif\" HEIGHT=\"23\" WIDTH=\"56\" BORDER=\"0\">"
		out += "<div id=\"null\"><A>&nbsp;</A></div>"
	else:
		#out += "<A HREF=\"" + row['website'].lstrip('\'')  + "\"><IMG SRC=\"/papers/website.jpg\" HEIGHT=\"23\" WIDTH=\"56\" BORDER=\"0\"></A>"
		out += "<div id=\"website\"><A HREF=\"" + row['website'].lstrip('\'')  + "\">website</A></div>"
	if not row['preprint']:
		#out += "<IMG SRC=\"/papers/null.gif\" HEIGHT=\"23\" WIDTH=\"56\" BORDER=\"0\">"
		out += "<div id=\"null\"><A>&nbsp;</A></div>"
	else:
		#out += "<A HREF=\"" + row['preprint'].lstrip('\'') + "\"><IMG BORDER=\"0\" HEIGHT=\"23\" WIDTH=\"56\" SRC=\"/papers/preprint.jpg\"></A>"
		out += "<div id=\"preprint\"><A HREF=\"" + row['preprint'].lstrip('\'') + "\">preprint</A></div>"
	if not row['pmid']:
		#out += "<IMG SRC=\"/papers/null.gif\" HEIGHT=\"23\" WIDTH=\"56\" BORDER=\"0\">"
		out += "<div id=\"null\"><A>&nbsp;</A></div>"
	else:
		#out += "<A HREF=\"http://www.ncbi.nlm.nih.gov:80/entrez/query.fcgi?cmd=Retrieve&db=PubMed&list_uids=" + row['pmid'].lstrip('\'') + "&dopt=Abstract\"><IMG BORDER=\"0\" HEIGHT=\"23\" WIDTH=\"56\" SRC=\"/papers/medline.jpg\"></A>"
		out += "<div id=\"medline\"><A HREF=\"http://www.ncbi.nlm.nih.gov:80/entrez/query.fcgi?cmd=Retrieve&db=PubMed&list_uids=" + row['pmid'].lstrip('\'') + "&dopt=Abstract\">medline</A></div>"
	#if not labid:
	#	out += "<A HREF=\"#\">" + "<IMG BORDER=\"0\" WIDTH=\"23\" HEIGHT=\"23\" SRC=\"/papers/more.gif\"></A>"
	#else:
	#out += "<A HREF=\"/papers/" + row['labid'].lstrip('\'') + "/index-all.html\">" + "<IMG BORDER=\"0\" WIDTH=\"23\" HEIGHT=\"23\" SRC=\"/papers/more.gif\"></A>"
	out += "<div id=\"arrow-right\"><A HREF=\"/papers/" + row['labid'].lstrip('\'') + "/index-all.html\"></A></div>"
	out += '</DIV>\n<P style="margin: 35px;" />\n'
	summaryFile.write(out)

def printSimpleEntry2(row, simpleFile, pubmed):
	pmid = ''
	title = ''
	citation = ''
	authors = ''
	year = ''
	pmcid = ''	
	#if row['pmid']:
		#print 'pSE first: ' + row['pmid']
	#else:
		#print 'pSE first: no pmid'
	pubmed.count = 0
	if not row['title']:
		for pubmed_row in pubmed:
		#print 'pSE pubmed: ' + pubmed_row['pmid']
			if row['pmid'] == pubmed_row['pmid']:
				pmid = pubmed_row['pmid']
				title = pubmed_row['title']
				citation = pubmed_row['citation']
				authors = pubmed_row['authors']
				year = row['year']	
		#		year = pubmed_row['year']
				pmcid = pubmed_row['pmcid']
				break
		#else:
			#print 'no match'
	if row['pmid']:
		if not row['title']:
			out = '<P style="line-height: 6pt "><DL COMPACT>' + '"' + title.lstrip('\'') + '" ' + authors.lstrip('\'') + ' (' + year.lstrip('\'') + '). '
			p = re.compile("\(\d+\)\.")	
			p2 = re.compile(":")
			citation = p.sub("",citation)
			citation = p2.sub(": ",citation)
			if pmcid:	
				out += citation.lstrip('\'') + ' <FONT SIZE=-2>[PMID: ' + pmid + '][PMCID: ' + pmcid +']</FONT></DL>\n'  
			else:
				out += citation.lstrip('\'') + ' <FONT SIZE=-2>[PMID: ' + pmid + ']</FONT></DL>\n'  	
		else:
			out = '<P style="line-height: 6pt "><DL COMPACT>' +'"' + row['title'].lstrip('\'') + '" '
			out += row['citation'].lstrip('\'') + ' <FONT SIZE=-2>[PMID: ' + row['pmid'].lstrip('\'') + ']</FONT></DL></P>\n'
	else:
		#if not row['authors']:
		out = '<P style="line-height: 6pt "><DL COMPACT>' +'"' + row['title'].lstrip('\'') + '" '
			#out = '<DL COMPACT>' + ' (' + row['year'].lstrip('\'') + '). "' + row['title'].lstrip('\'') +'" '
		#else:
			#out = '<DL COMPACT>' + row['authors'].lstrip('\'') + ' (' + row['year'].lstrip('\'') + '). "' + row['title'].lstrip('\'') +'" '
		out += row['citation'].lstrip('\'') + '</DL></P>\n'
	simpleFile.write(out)

def printSimpleEntry(row, simpleFile, pubmed):
	pmid = ''
	title = ''
	citation = ''
	authors = ''
	year = ''
	pmcid = ''	
	#if row['pmid']:
		#print 'pSE first: ' + row['pmid']
	#else:
		#print 'pSE first: no pmid'
	pubmed.count = 0
	if not row['title']:
		for pubmed_row in pubmed:
		#print 'pSE pubmed: ' + pubmed_row['pmid']
			if row['pmid'] == pubmed_row['pmid']:
				pmid = pubmed_row['pmid']
				title = pubmed_row['title']
				citation = pubmed_row['citation']
				authors = pubmed_row['authors']
				year = row['year']	
		#		year = pubmed_row['year']
				break
		#else:
			#print 'no match'
	if row['pmid']:
		if not row['title']:
			out = '<P style="line-height: 6pt "><DL COMPACT>' + authors.lstrip('\'') + ' (' + year.lstrip('\'') + '). "' + title.lstrip('\'') +'" '
			p = re.compile("\(\d+\)\.")	
			p2 = re.compile(":")
			citation = p.sub("",citation)
			citation = p2.sub(": ",citation)
			if pmcid:	
				out += citation.lstrip('\'') + ' <FONT SIZE=-2>[PMID: ' + pmid + '][PMCID: ' + pmcid +']</FONT></DL>\n'  
			else:
				out += citation.lstrip('\'') + ' <FONT SIZE=-2>[PMID: ' + pmid + ']</FONT></DL>\n'  	
		else:
			out = '<P style="line-height: 6pt "><DL COMPACT>' +'"' + row['title'].lstrip('\'') + '" '
			out += row['citation'].lstrip('\'') + ' <FONT SIZE=-2>[PMID: ' + row['pmid'].lstrip('\'') + ']</FONT></DL></P>\n'
	else:
		#if not row['authors']:
		out = '<P style="line-height: 6pt "><DL COMPACT>' +'"' + row['title'].lstrip('\'') + '" '
			#out = '<DL COMPACT>' + ' (' + row['year'].lstrip('\'') + '). "' + row['title'].lstrip('\'') +'" '
		#else:
			#out = '<DL COMPACT>' + row['authors'].lstrip('\'') + ' (' + row['year'].lstrip('\'') + '). "' + row['title'].lstrip('\'') +'" '
		out += row['citation'].lstrip('\'') + '</DL></P>\n'
	simpleFile.write(out)

def printSubject(master_spreadsheet,header):
	allsubjects = []
	subjectpapers = []
	for i,row in enumerate(master_spreadsheet):
		if row.has_key('subject') and row['subject']: #and row['pmid'].isdigit():
			subjects = row['subject'].split(',')
			for subject in subjects:
				subject = subject.strip( ) 
				if subject not in allsubjects:
					allsubjects.append(subject)
					subjectpapers.append([i])
				else:
					index = allsubjects.index(subject)
					subjectpapers[index].append(i)
 
	for row in subject_spreadsheet:
		subject = row['labid'].strip( )
		if subject not in allsubjects:
			path = subjectPath + subject
			if not os.path.exists(path):
				os.makedirs(path) 
			subjectFile = open(path + '/index.html', 'w')
			out = '''<HTML>
<HEAD>
<TITLE>%s</TITLE>
'''%subject.capitalize()

			out +=header
			include = ''
			if row['html']:
				include =row['html'].lstrip('\'')
			if include:
				out += include
			subjectFile.write(out)
			subjectFile.write('</FONT><HR><A HREF =        "/"><B>Return to front page</B></A>\n</BODY></HTML>')
			subjectFile.close()
	
	for i,subject in enumerate(allsubjects):
		printSubjectFile(subject,subjectpapers[i])
 
def printSubjectFile(subject,papers):
	path = subjectPath + subject
	if not os.path.exists(path):
		os.makedirs(path)
	subjectFile = open(path + '/index.html','w')
#	subjectInclude = path + '/include.html'
	out = '''<HTML>
<HEAD>
<TITLE>%s</TITLE>
''' % subject.capitalize()
	out += header
	
	#include include file if exists
#	if os.path.exists(subjectInclude):
#		includeFile = open(subjectInclude,'r')
#		for line in includeFile:
#			subjectFile.write(line + '\n')
#		includeFile.close()
#	subjectFile.write('\n\n')
	include = ''
	for row in subject_spreadsheet:
		if row['labid'] == subject:
			if row['html']:
				include	= row['html'].lstrip('\'')
	if include:
		out += include
	subjectFile.write(out)

	for r in papers:
		printSubjectEntry(subjectFile,r)
	subjectFile.write('	</FONT><HR><A HREF=       "/"><B>Return to front page</B></A>\n</BODY></HTML>')
	subjectFile.close()
	
def printSubjectEntry(subjectFile,r):
	row = master_spreadsheet.rows[r]
	title = ''
        citation = ''
        authors = ''
        year = ''
        if not row['title']:
		for pubmed_row in pubmed_spreadsheet:
                	if row['pmid'] == pubmed_row['pmid']:
                        	title = pubmed_row['title']
                        	citation = pubmed_row['citation']
                        	authors = pubmed_row['authors']
                       # 	year = pubmed_row['year']
				pmcid = pubmed_row['pmcid']
                #        break
        # print title and citation
        if not title:
		out = "<DIV CLASS=\"paperTitle\"><FONT SIZE=+1><B><A HREF=\"/papers/" + row['labid'].lstrip('\'') + "/index.html\">" + row['title'].lstrip('\'')  + "</A></B></FONT></DIV>\n"
	else:
                out = "<DIV CLASS=\"paperTitle\"><FONT SIZE=+1><B><A HREF=\"/papers/" + row['labid'].lstrip('\'') + "/index.html\">" + title.lstrip('\'') + "</A></B></FONT></DIV>\n"
        if not citation:
                if not row.has_key('authors'):
                        out += "<DIV CLASS=\"paperCite\">" + row['citation'].lstrip('\'') + "</DIV>\n"
                else:
                        out += "<DIV CLASS =\"paperCite\">" + row['authors'].lstrip('\'') + " " + row['citation'].lstrip('\'')+ "</DIV>\n"
        else:
                out += "<DIV CLASS=\"paperCite\">" + authors.lstrip('\'') + "&nbsp;" + citation.lstrip('\'') + "</DIV>\n"
        # print links
        out += "<DIV CLASS=\"paperCite\">"
        if not row['website']:
                #out += "<IMG SRC=\"/papers/null.gif\" HEIGHT=\"23\" WIDTH=\"56\" BORDER=\"0\">"
		out += "<div id=\"null\"><A>&nbsp;</A></div>"
        else:
                #out += "<A HREF=\"" + row['website'].lstrip('\'')  + "\"><IMG SRC=\"/papers/website.jpg\" HEIGHT=\"23\" WIDTH=\"56\" BORDER=\"0\"></A>"
		out += "<div id=\"website\"><A HREF=\"" + row['website'].lstrip('\'')  + "\">website</A></div>"
        if not row['preprint']:
                #out += "<IMG SRC=\"/papers/null.gif\" HEIGHT=\"23\" WIDTH=\"56\" BORDER=\"0\">"
		out += "<div id=\"null\"><A>&nbsp;</A></div>"
        else:
                #out += "<A HREF=\"" + row['preprint'].lstrip('\'') + "\"><IMG BORDER=\"0\" HEIGHT=\"23\" WIDTH=\"56\" SRC=\"/papers/preprint.jpg\"></A>"
		out += "<div id=\"preprint\"><A HREF=\"" + row['preprint'].lstrip('\'') + "\">preprint</A></div>"
        if not row['pmid']:

                #out += "<IMG SRC=\"/papers/null.gif\" HEIGHT=\"23\" WIDTH=\"56\" BORDER=\"0\">"
		out += "<div id=\"null\"><A>&nbsp;</A></div>"
        else:
                #out += "<A HREF=\"http://www.ncbi.nlm.nih.gov:80/entrez/query.fcgi?cmd=Retrieve&db=PubMed&list_uids=" + row['pmid'].lstrip('\'') + "&dopt=Abstract\"><IMG BORDER=\"0\" HEIGHT=\"23\" WIDTH=\"56\" SRC=\"/papers/medline.jpg\"></A>"
		out += "<div id=\"medline\"><A HREF=\"http://www.ncbi.nlm.nih.gov:80/entrez/query.fcgi?cmd=Retrieve&db=PubMed&list_uids=" + row['pmid'].lstrip('\'') + "&dopt=Abstract\">medline</A></div>"
  	#if not labid:
        #       out += "<A HREF=\"#\">" + "<IMG BORDER=\"0\" WIDTH=\"23\" HEIGHT=\"23\" SRC=\"/papers/more.gif\"></A>"
        #else:
        #out += "<A HREF=\"/papers/" + row['labid'].lstrip('\'') + "/index-all.html\">" + "<IMG BORDER=\"0\" WIDTH=\"23\" HEIGHT=\"23\" SRC=\"/papers/more.gif\"></A>"
	out += "<div id=\"arrow-right\"><A HREF=\"/papers/" + row['labid'].lstrip('\'') + "/index-all.html\"></A></div>"
        out += '</DIV>\n<P style="margin: 35px;" />\n'
	subjectFile.write(out)

def printSubjectSummary(subject_spreadsheet, subjectSummaryFile, header):
	styleSubject = '''
	<BR>    
	<STYLE type="text/css">
	.unsel{background-color:#ffffff; background-position:top; background-repeat:repeat-x; color:#FFFFFF; font-weight:normal;}
	.sel {background-color:#3b5998; color:#FFFFFF; font-weight:normal;}
	.content{background-color:#ffffff; height:25px; padding-left:20px; padding-right:20px; padding-top:20px;color:#ffffff;}
        a{text-decoration:none;color:#ffffff;}
	.unsel a:link {color:#888888;text-decoration:none;}
	.sel a:visited {color:#ffffff;text-decoration:none;}
	.sel a:active {color:#ffffff;text-decoration:none;}
	.sel a:hover {color:#ffffff;text-decoration:underline;}
	</STYLE>
	'''

	category = ''
	SubjectNumber = 0
	outPart = ''
	out = "<HTML>\n"
	out += "<HEAD>\n"
	out += "<TITLE>Gerstein Lab Publications</TITLE>\n"
	out += header
	out += "\n"
	out += styleSubject
	out += '<BODY onload="javascript:showdh(3);">\n'
	out +=  '<TABLE width="915" height="30" frame ="hsides" align="center" cellpadding="0" cellspacing="0">\n<TR>\n<TD width="6"></TD>\n'

	for row in subject_spreadsheet:
		if not category == row['category'].lstrip('\''):
			if not category == '':
				outPart +=       "</TD></TR>\n"
			SubjectNumber +=1
			tableid = str(SubjectNumber)
			category = row['category'].lstrip('\'')
			out +='<TD width="86" class="unsel" id="dh'+tableid+'"><DIV align="center"><FONT FACE=" sans-serif,arial, Helvetica" SIZE=3><A href="javascript:showdh('+tableid+');" _fcksavedurl="javascript:showdh('+tableid+');">'+ row['category'].lstrip('\'') + '</A></FONT></DIV></TD>\n'
			out  += ' <TD width="6"></TD>\n'
			outPart +='<TR id="menu'+ tableid+'" style="display:none">\n'
			outPart +='<TD class="content" style="line-height:25px">\n'
		outPart +=  "<FONT FACE='times'>  <A HREF='/subject/" + row['labid'].lstrip('\'')+"/index.html' STYLE='text-decoration:none; color:black'>"
		title = str(row['title'])
		outPart +=    "<TT>[ "+row['labid'].lstrip('\'')+" ]</TT>  "+title.lstrip('\'')+"</A></FONT><BR>\n"
	outPart += "</TD></TR>\n"     
	out += '</TR></TABLE>\n<TABLE width="915" border="0" align="center" cellpadding="0" cellspacing="0">\n'

	out += outPart 
	out += ''' <script language="javascript">
		function showdh(n){
		for(var i=1;i<=''' + tableid+''';i++){
		eval("dh" + i).className="unsel"
		eval("menu"+i).style.display="none";
		}
		eval("dh"+n).className="sel"
		eval("menu"+n).style.display="";
		}
		</script>
		'''
	out += "</BODY></HTML>" 
	subjectSummaryFile.write(out)  

printSubjectSummary(subject_spreadsheet, subjectSummaryFile, header)
printSubject(master_spreadsheet,header)
printPapers(master_spreadsheet, summaryFile, header)

# Fix permissions to make both apache and sudo users run updates
os.system("chmod -R 777 /var/www/html/papers/papers")