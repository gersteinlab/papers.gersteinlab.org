#!/usr/bin/python
# -*- coding: UTF-8 -*-

import cgitb, os, re, csv
from datetime import datetime

# enable debugging
cgitb.enable()

print "Content-Type: text/plain;charset=utf-8"
print

##############################

###
### build html
###

##############################

pubmed_spreadsheet = list(csv.DictReader(open('../html/papers/update/pubmed.tsv'), delimiter='\t'))
master_spreadsheet = list(csv.DictReader(open('../html/papers/update/master_gsheet.csv')))
subject_spreadsheet = list(csv.DictReader(open('../html/papers/update/subject_gsheet.csv')))

timestamp = str(datetime.now().ctime())

summaryPath = "../html/papers/papers/"
summaryFile = open("../html/papers/index.html", 'w')

simpleFile = open("../html/papers/simple.html", 'w')
simpleFile2 = open("../html/papers/papers/papers-simple.html", 'w')

subjectPath = "../html/papers/subject/"
subjectFile = open("../html/papers/subject/index.html", 'w')
subjectSummaryFile = open("../html/papers/subject/index.html", 'w')

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
<script>
  (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
  (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
  m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
  })(window,document,'script','//www.google-analytics.com/analytics.js','ga');

  ga('create', 'UA-72218887-2', 'auto');
  ga('send', 'pageview');

</script>
</HEAD>
<BODY BGCOLOR="white">
<CENTER>
<BR>
<FONT SIZE=+2 FACE='sans-serif, Arial, Helvetica' COLOR="#334499">Gerstein Lab Publications</FONT>
<BR><BR>
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
-->
<SPAN CLASS="headerMenu"><A HREF="http://wiki.gersteinlab.org/pubinfo/Other_Papers">Other Writings</A></SPAN>
</FONT>
</CENTER>
<HR>
'''

def mergeData(master, pubmed):
    for row in master:

        if row['PMID']:
            for pubmed_row in pubmed:
                # print 'Processing PMID: ' + pubmed_row['PMID']
                if row['PMID'] == pubmed_row['PMID']:

                    # if title is not user-provided
                    if not row['title']:

                        # get title from pubmed
                        row['title'] = pubmed_row['Title']

                        # get citation from pubmed
                        citation = pubmed_row['Citation']
                        p = re.compile("\(\d+\)\.")
                        p2 = re.compile(":")
                        p3 = re.compile("&nbsp;")
                        citation = p.sub("", citation)
                        citation = p2.sub(": ", citation)
                        citation = p3.sub(" ", citation)
                        row['citation'] = pubmed_row['Authors'].lstrip('\'')+" ("+row['Year']+")."+citation.lstrip('\'')

                    row['authors'] = pubmed_row['Authors']
                    row['journal'] = pubmed_row['Journal']
                    row['pages'] = pubmed_row['Pages'].lstrip("#")
                    row['volume'] = pubmed_row['Volume'].lstrip("#")
                    row['pmcid'] = pubmed_row['PMCID']

def printLink(row):
    out = ""
    out += "<DIV CLASS=\"paperCite\">"
    if not row['website']:
        out += "<div id=\"null\"><A>&nbsp;</A></div>"
    else:
        out += "<div id=\"website\"><A HREF=\"" + row['website'].lstrip('\'') + "\">website</A></div>"
    if not row['preprint']:
        out += "<div id=\"null\"><A>&nbsp;</A></div>"
    else:
        out += "<div id=\"preprint\"><A HREF=\"" + row['preprint'].lstrip('\'') + "\">preprint</A></div>"
    if not row['PMID']:
        out += "<div id=\"null\"><A>&nbsp;</A></div>"
    else:
        out += "<div id=\"medline\"><A HREF=\"http://www.ncbi.nlm.nih.gov:80/entrez/query.fcgi?cmd=Retrieve&db=PubMed&list_uids=" + row['PMID'].lstrip('\'') + "&dopt=Abstract\">medline</A></div>"
    out += "<div id=\"arrow-right\"><A HREF=\"/papers/" + row['labid'].lstrip('\'') + "/index-all.html\"></A></div>"
    out += "</DIV>\n<P style=\"margin: 35px;\" />\n"
    return out

def printPapers(summaryFile, header):
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
        rowYear = row['Year']
        if years.has_key(rowYear):
            years[rowYear] += 1
        else:
            years[rowYear] = 1

    for row in master_spreadsheet:
        pubmed = pubmed_spreadsheet
        if currentYear != row['Year']:
            currentYear = row['Year']
            out += "<H3 ALIGN=center><FONT FACE='arial,helvetica,sans-serif' COLOR=000000 SIZE=4>-- " + currentYear + " ("+str(years[currentYear])+") --</FONT></H3>\n"
        summaryFile.write(out)
        simpleFile.write(out)
        simpleFile2.write(out)

        out = ""
        printPaperEntry(row, summaryFile, pubmed)

        # generate simple.html and papers-simple.html
        printSimpleEntry(row, simpleFile, pubmed)
        printSimpleEntry(row, simpleFile2, pubmed)

        printEntrySummary(row, header, pubmed)
        printEntryExtended(row, pubmed)

    summaryFile.write("</BODY>\n</HTML>")
    simpleFile.write("</BODY>\n</HTML>")

def printEntrySummary(row, header, pubmed):

    # create summary directory
    entrySummary = summaryPath + row['labid'].lstrip('\'')
    if not os.path.exists(entrySummary):
        os.makedirs(entrySummary)
    entrySummaryIndex = entrySummary + "/index.html"
    entrySummaryFile = open(entrySummaryIndex, 'w')

    out = "<HTML>\n<HEAD>\n<TITLE>"+row['title'].lstrip('\'')+"</TITLE>"
    out += header
    out += "<blockquote>\n<font size=+3><tt>" + row['labid'] + "</tt></font><p>\n"

    # print title and citation
    out += "<DIV CLASS=\"paperTitle\"><FONT SIZE=+1><B><A HREF=\"/papers/" + row['labid'].lstrip('\'') + "/index.html\">" + row['title'].lstrip('\'') + "</A></B></FONT></DIV>\n"
    out += "<DIV CLASS=\"paperCite\">" + " " + row['citation'].lstrip('\'') + "</DIV>\n"

    # print links
    out += printLink(row)

    out += "<hr><br><a href=index-all.html>View all citation information</a><br><a href='/'>Return to papers index</a><br>&nbsp;</blockquote>\n</BODY>\n</HTML>"
    entrySummaryFile.write(out)

def printEntryExtended(row, pubmed):

    # create summary directory
    entryExtended = summaryPath + row['labid'].lstrip('\'')
    if not os.path.exists(entryExtended):
        os.makedirs(entryExtended)
    entryExtendedIndex = entryExtended + "/index-all.html"
    entryExtendedFile = open(entryExtendedIndex, 'w')

    out = "<HTML>\n"
    out += "<HEAD>\n"
    out += "<TITLE>" + row['title'].lstrip('\'') + "</TITLE>"
    out += header
    out += "\n"
    out += "<blockquote>\n"
    if not row['labid']:
        out += "<font size=+3><tt>" + row['PMID'].lstrip('\'') + "</tt></font><p>"
    else:
        out += "<font size=+3><tt>" + row['labid'] + "</tt></font><p>"
    out += "\n"

    # print title and citation
    out += "<DIV CLASS=\"paperTitle\"><FONT SIZE=+1><B><A HREF=\"/papers/" + row['labid'].lstrip('\'') + "/index.html\">" + row['title'].lstrip('\'') + "</A></B></FONT></DIV>\n"
    out += "<DIV CLASS=\"paperCite\">" + row['citation'].lstrip('\'') + "</DIV>\n"

    # print links
    out += printLink(row)

    # print details
    out += '<A HREF="index.html">Switch to compact view</A><hr>\n<table>\n'
    if not row.has_key('authors'):
        out += '<tr><td width=100><b><font color=gray>Authors</font></b></td><td><b><font color=#000077>&nbsp;</font></b></td></tr>\n'
    else:
        out += '<tr><td width=100><b><font color=gray>Authors</font></b></td><td><b><font color=#000077>'
        link = '<A HREF="http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=PureSearch&db=PubMed&details_term=%s">%s</A>'
        authorlinks = [link % (a.lstrip('\'').strip().replace(' ', '%20'), a.lstrip('\'').strip()) for a in row['authors'].split(',')]

        # print authorlinks
        out += ', '.join(authorlinks)
        out += '</font></b></td></tr>\n'

    if not row.has_key('journal'):
        out += '<tr><td width=100><b><font color=gray>Journal</font></b></td><td><b><font color=#000077>&nbsp;</font></b></td></tr>\n'
    else:
        out += '<tr><td width=100><b><font color=gray>Journal</font></b></td><td><b><font color=#000077>'
        out += '<A HREF="http://locatorplus.gov/cgi-bin/Pwebrecon.cgi?DB=local&v2=1&ti=1,1&Search_Arg=9808944&Search_Code=0359&CNT=20&SID=1">'
        out += row['journal'] + '</A></font></b></td></tr>'

    if not row['PMID']:
        out += "<tr><td width=100><b><font color=gray>PMID</font></b></td><td><b><font color=#000077>&nbsp;</font></b></td></tr>\n"
    else:
        out += '<tr><td width=100><b><font color=gray>PMID</font></b></td><td><b><font color=#000077>'
        out += '<A HREF="http://www.ncbi.nlm.nih.gov:80/entrez/query.fcgi?cmd=Retrieve&db=PubMed&list_uids=' + row['PMID'].lstrip('\'') + '&dopt=Abstract">'
        out += row['PMID'].lstrip('\'') + '</A></font></b></td></tr>\n'

    if not row.has_key('pages'):
        out += "<tr><td width=100><b><font color=gray>Pages</font></b></td><td><b><font color=#000077>&nbsp;</font></b></td></tr>\n"
    else:
        out += "<tr><td width=100><b><font color=gray>Pages</font></b></td><td><b><font color=#000077>" + row['pages'].lstrip('\'') + "</font></b></td></tr>\n"

    if not row.has_key('volume'):
        out += "<tr><td width=100><b><font color=gray>Volume</font></b></td><td><b><font color=#000077>&nbsp;</font></b></td></tr>\n"
    else:
        out += "<tr><td width=100><b><font color=gray>Volume</font></b></td><td><b><font color=#000077>" + row['volume'].lstrip('\'') + "</font></b></td></tr>\n"

    if not row['Year']:
        out += "<tr><td width=100><b><font color=gray>Year</font></b></td><td><b><font color=#000077>&nbsp;</font></b></td></tr>\n"
    else:
        out += "<tr><td width=100><b><font color=gray>Year</font></b></td><td><b><font color=#000077>" + row['Year'].lstrip('\'') + "</font></b></td></tr>\n"

    out += "<tr><td width=100><b><font color=gray>labcite</font></b></td><td><b><font color=#000077>" + row['citation'].lstrip('\'') + "</font></b></td></tr>\n"

    if not row['labid']:
        out += "<tr><td width=100><b><font color=gray>labid</font></b></td><td><b><font color=#000077>&nbsp;</font></b></td></tr>\n"
    else:
        out += "<tr><td width=100><b><font color=gray>labid</font></b></td><td><b><font color=#000077>" + row['labid'].lstrip('\'') + "</font></b></td></tr>\n"

    if not row['title']:
        out += "<tr><td width=100><b><font color=gray>labtitle</font></b></td><td><b><font color=#000077>&nbsp;</font></b></td></tr>\n"
    else:
        out += "<tr><td width=100><b><font color=gray>labtitle</font></b></td><td><b><font color=#000077>" + row['title'].lstrip('\'') + "</font></b></td></tr>\n"

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
        out += '<tr><td width=100><b><font color=gray>website</font></b></td><td><b><font color=#000077><A HREF="' + row['website'].lstrip('\'') + '">' + row['website'].lstrip('\'') + '</A></font></b></td></tr>\n'

    out += "</table><br><font color=gray>Unused tags: <i>e-print footnote grant ignore preprint sortval target website2</i></font><hr><a href='/'>Return to papers index</a><br>&nbsp;</blockquote>\n</BODY>\n</HTML>"
    entryExtendedFile.write(out)

def printPaperEntry(row, summaryFile, pubmed):

    # print title and citation
    if row['title']:
        out = "<DIV CLASS=\"paperTitle\"><FONT SIZE=+1><B><A HREF=\"/papers/" + row['labid'].lstrip('\'') + "/index.html\">" + row['title'].lstrip('\'') + "</A></B></FONT></DIV>\n"
    else:
        print "Warning: Title Empty!"
        print row

    if row['citation']:
        out += "<DIV CLASS=\"paperCite\">" + row['citation'].lstrip('\'') + "</DIV>\n"
    else:
        print "Warning: Citation Empty!"
        print row

    # print links
    out += printLink(row)

    summaryFile.write(out)

def printSimpleEntry(row, simpleFile, pubmed):

    if row['PMID']:
        out = '<P style="line-height: 6pt "><DL COMPACT>"'+row['title'].lstrip('\'')+'" '+row['citation'].lstrip('\'')+' <FONT SIZE=-2>[PMID: '+row['PMID'].lstrip('\'')+']'
        if row.has_key('pmcid') and row['pmcid']:
            out += '[PMCID: '+row['pmcid']+']</FONT></DL></P>\n'
        else:
            out += '</FONT></DL></P>\n'
    else:
        out = '<P style="line-height: 6pt "><DL COMPACT>"'+row['title'].lstrip('\'')+'" '+row['citation'].lstrip('\'')+'</DL></P>\n'

    simpleFile.write(out)

def printSubject(master_spreadsheet, header):
    allsubjects = []
    subjectpapers = []
    for i, row in enumerate(master_spreadsheet):
        if row.has_key('subject') and row['subject']:  # and row['pmid'].isdigit():
            subjects = row['subject'].split(',')
            for subject in subjects:
                subject = subject.strip()
                if subject not in allsubjects:
                    allsubjects.append(subject)
                    subjectpapers.append([i])
                else:
                    index = allsubjects.index(subject)
                    subjectpapers[index].append(i)

    for row in subject_spreadsheet:
        subject = row['LabID'].strip()
        if subject not in allsubjects:
            path = subjectPath + subject
            if not os.path.exists(path):
                os.makedirs(path)
            subjectFile = open(path + '/index.html', 'w')

            out = '''<HTML>
<HEAD>
<TITLE>%s</TITLE>
''' % subject.capitalize()

            out += header
            include = ''
            if row['HTML']:
                include = row['HTML'].lstrip('\'')
            if include:
                out += include
            subjectFile.write(out)
            subjectFile.write('</FONT><HR><A HREF="/"><B>Return to front page</B></A>\n</BODY>\n</HTML>')
            subjectFile.close()

    for i, subject in enumerate(allsubjects):
        printSubjectFile(subject, subjectpapers[i])

def printSubjectFile(subject, subject_papers):
    path = subjectPath + subject
    if not os.path.exists(path):
        os.makedirs(path)
    subjectDetailFile = open(path + '/index.html', 'w')

    #	subjectInclude = path + '/include.html'
    out = '''<HTML>
<HEAD>
<TITLE>%s</TITLE>
''' % subject.capitalize()
    out += header

    # include include file if exists
    #	if os.path.exists(subjectInclude):
    #		includeFile = open(subjectInclude,'r')
    #		for line in includeFile:
    #			subjectFile.write(line + '\n')
    #		includeFile.close()
    #	subjectFile.write('\n\n')

    include = ''
    for row in subject_spreadsheet:
        if row['LabID'] == subject:
            if row['HTML']:
                include = row['HTML'].lstrip('\'')
    if include:
        out += include
    subjectDetailFile.write(out)

    for paper_row in subject_papers:
        printSubjectEntry(master_spreadsheet[paper_row], subjectDetailFile)

    subjectDetailFile.write('	</FONT><HR><A HREF="/"><B>Return to front page</B></A>\n</BODY>\n</HTML>')
    subjectDetailFile.close()

def printSubjectEntry(row, subjectDetailFile):

    out = "<DIV CLASS=\"paperTitle\"><FONT SIZE=+1><B><A HREF=\"/papers/" + row['labid'].lstrip('\'') + "/index.html\">" + row['title'].lstrip('\'') + "</A></B></FONT></DIV>\n"
    out += "<DIV CLASS=\"paperCite\">" + row['citation'].lstrip('\'') + "</DIV>\n"

    # print links
    out += printLink(row)

    subjectDetailFile.write(out)

def printSubjectSummary(subject_spreadsheet, header):

    styleSubject = '''<BR>
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
    out += '<TABLE width="915" height="30" frame ="hsides" align="center" cellpadding="0" cellspacing="0">\n<TR>\n<TD width="6"></TD>\n'

    for row in subject_spreadsheet:
        if not category == row['Category'].lstrip('\''):
            if not category == '':
                outPart += "</TD></TR>\n"
            SubjectNumber += 1
            tableid = str(SubjectNumber)
            category = row['Category'].lstrip('\'')
            out += '<TD width="86" class="unsel" id="dh' + tableid + '"><DIV align="center"><FONT FACE=" sans-serif,arial, Helvetica" SIZE=3><A href="javascript:showdh(' + tableid + ');" _fcksavedurl="javascript:showdh(' + tableid + ');">' + row['Category'].lstrip('\'') + '</A></FONT></DIV></TD>\n'
            out += '<TD width="6"></TD>\n'
            outPart += '<TR id="menu' + tableid + '" style="display:none">\n'
            outPart += '<TD class="content" style="line-height:25px">\n'
        outPart += "<FONT FACE='times'><A HREF='/subject/" + row['LabID'].lstrip('\'') + "/index.html' STYLE='text-decoration:none; color:black'>"
        title = str(row['Title'])
        outPart += "<TT>[ " + row['LabID'].lstrip('\'') + " ]</TT>  " + title.lstrip('\'') + "</A></FONT><BR>\n"
    outPart += "</TD></TR>\n"
    out += '</TR></TABLE>\n<TABLE width="915" border="0" align="center" cellpadding="0" cellspacing="0">\n'
    out += outPart
    out += '''
<script language="javascript">
function showdh(n){
    for(var i=1;i<=''' + tableid + ''';i++){
        eval("dh" + i).className="unsel"
		eval("menu"+i).style.display="none";
	}
	eval("dh"+n).className="sel"
	eval("menu"+n).style.display="";
}
</script>
'''
    out += "</BODY>\n</HTML>"
    subjectSummaryFile.write(out)

### MAIN ###

mergeData(master_spreadsheet, pubmed_spreadsheet)
printSubjectSummary(subject_spreadsheet, header)
printSubject(master_spreadsheet, header)
printPapers(summaryFile, header)

# Fix permissions to make both apache and sudo users run updates
os.system("chmod -R 775 ../html/papers/papers")

print "Done"
