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
if not os.path.exists(summaryPath):
    os.makedirs(summaryPath)
summaryFile = open("../html/papers/index.html", 'w')

simpleFile = open("../html/papers/simple.html", 'w')
simpleFile2 = open("../html/papers/papers/papers-simple.html", 'w')

subjectPath = "../html/papers/subject/"
subjectFile = open("../html/papers/subject/index.html", 'w')
subjectSummaryFile = open("../html/papers/subject/index.html", 'w')

metricsPath = "../html/papers/metrics/"
if not os.path.exists(metricsPath):
    os.makedirs(metricsPath)
metricsFile = open("../html/papers/metrics/index.html", 'w')

# Read funding subjects
funding_subject = []
for row in subject_spreadsheet:
    if 'Grants' in row['Category'].strip():
        funding_subject.append(row['LabID'].strip())

# Read image list (https://stackoverflow.com/questions/11023530/python-to-list-http-files-and-directories)
import requests
import re

url = 'http://www.gersteinlab.org/media/images/thumbs/'

response = requests.get(url)
if response.ok:
    response_text = response.text
else:
    response.raise_for_status()
   
re_raw=re.findall('<a href=.*</a>',response_text)
images_name = [f.split('"')[1] for f in re_raw]

images_url_thumbnail = [url+f for f in images_name]
images_url_gallery = ['http://www.gersteinlab.org/media/images/'+f for f in images_name]
images_id = [f.split('_')[0] for f in images_name]
images_dict_thumbnail = dict(zip(images_id,images_url_thumbnail))
images_dict_gallery =  dict(zip(images_id,images_url_gallery))

# Write HTML
def makeHeader(title):
    header = '''<HTML>
    <HEAD>
    <TITLE>'''+title+'''</TITLE>
    <link rel="stylesheet" href="/style.css">

    <!-- google analytics -->
    <script>
      (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
      (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
      m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
      })(window,document,'script','//www.google-analytics.com/analytics.js','ga');

      ga('create', 'UA-72218887-2', 'auto');
      ga('send', 'pageview');
    </script>

    <!-- altmetric -->
    <script type='text/javascript' src='https://d1bxh8uas1mnw7.cloudfront.net/assets/embed.js'></script>

    </HEAD>
    
    <BODY BGCOLOR="white">
    <div id="header">
        <div id="global-title-container">
            <div id="title-wrapper" class="clearfix">
                <div id="title-left">
                    <a href="http://www.gersteinlab.org/"><strong>Gerstein</strong> Lab</a>
                </div>
                <div id="title-right">
                    <a href="http://cbb.yale.edu/">Bioinformatics</a>
                </div>
            </div>
        </div>

        <CENTER>
            <BR>
            <!-- Buttons for individual sections -->
            <FONT SIZE=+1 FACE='sans-serif, Arial, Helvetica' COLOR="#993333">
                <SPAN CLASS="headerMenu"><A HREF="/">Main</A></SPAN>
                &nbsp;&#8226;&nbsp;
                <SPAN CLASS="headerMenu"><A HREF="/subject">By Subject</A></SPAN>
                &nbsp;&#8226;&nbsp;
                <SPAN CLASS="headerMenu"><A HREF="/metrics">Metrics</A></SPAN>
                &nbsp;&#8226;&nbsp;
                <SPAN CLASS="headerMenu"><A HREF="http://info.gersteinlab.org/Pubmed_query">Queries</A></SPAN>
                &nbsp;&#8226;&nbsp;
                <SPAN CLASS="headerMenu"><A HREF="http://info.gersteinlab.org/Papers_Page_Code">Code</A></SPAN>
                &nbsp;&#8226;&nbsp;
                <SPAN CLASS="headerMenu"><A HREF="http://wiki.gersteinlab.org/pubinfo/Other_Papers">Other Writings</A></SPAN>
            </FONT>
            <BR><BR>
        </CENTER>
    </div>
    <div id="content">
    '''
    return header

def mergeData(master, pubmed):
    for row in master:
        if row['PMID']: ### if PMID is present, use the data from pubmed
            for pubmed_row in pubmed:
                # print 'Processing PMID: ' + pubmed_row['PMID']
                if row['PMID'] == pubmed_row['PMID']:

                    # if title is not user-provided, get title from pubmed
                    if not row['title']:
                        row['title'] = pubmed_row['Title']

                    # get citation from pubmed
                    citation = pubmed_row['Citation']
                    citation = re.compile("\(\d+\)\.").sub("", citation)
                    citation = re.compile(":").sub(": ", citation)
                    citation = re.compile("&nbsp;").sub(" ", citation)
                    citation = re.compile("\.").sub("", citation)
                    row['citation'] = pubmed_row['Authors'].lstrip('\'')+" ("+row['Year']+"). "+citation.lstrip('\'').strip()+"."

                    row['authors'] = pubmed_row['Authors']
                    row['journal'] = pubmed_row['Journal']
                    row['pages'] = pubmed_row['Pages'].lstrip("#")
                    row['volume'] = pubmed_row['Volume'].lstrip("#")
                    row['pmcid'] = pubmed_row['PMCID']

def write2csv(master):
    # write to CSV
    with open("../html/papers/update/merged.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerow( ('labid', 'PMID', 'title', 'citation', 'preprint', 'subject', 'website', 'Year', 'footnote', 'website2', 'coreTool') )

        for row in master:
            writer.writerow( (row['labid'],  row['PMID'], row['title'], row['citation'], row['preprint'], row['subject'], row['website'], row['Year'], row['footnote'], row['website2'], row['coreTool']) )

def printLink(row):

    out = "<DIV CLASS=\"paperCite\">"

    ### add link to website
    if not row['website']:
        out += "<div id=\"null\"><A>&nbsp;</A></div>"
    else:
        out += "<div id=\"website\"><A HREF=\"" + row['website'].lstrip('\'') + "\">website</A></div>"

    ### add link to preprint
    if not row['preprint']:
        out += "<div id=\"null\"><A>&nbsp;</A></div>"
    else:
        out += "<div id=\"preprint\"><A HREF=\"" + row['preprint'].lstrip('\'') + "\">preprint</A></div>"

    ### add link to pubmed, altmetric badge
    if not row['PMID']:
        out += "<div id=\"null\"><A>&nbsp;</A></div>"
    else:
        out += "<div id=\"medline\"><A HREF=\"http://www.ncbi.nlm.nih.gov:80/entrez/query.fcgi?cmd=Retrieve&db=PubMed&list_uids=" + row['PMID'].lstrip('\'') + "&dopt=Abstract\">medline</A></div>"

    ### add additional links (from website2 column)
    if not row['website2']:
        out += "<div id=\"null\"><A>&nbsp;</A></div>"
    else:
        out += "<div id=\"link\"><A HREF=\"" + row['website2'].lstrip('\'') + "\">link</A></div>"
           
        # ### add altmetric badge
        # out += "<div id=\"altmetric\" data-badge-popover=\"right\" data-badge-type=\"4\" data-pmid=\"" + row['PMID'].lstrip('\'') + "\" data-condensed=\"true\" data-hide-no-mentions=\"true\" class=\"altmetric-embed\"></div>"

    out += "<div id=\"arrow-right\"><A HREF=\"/papers/" + row['labid'].lstrip('\'') + "/index-all.html\"></A></div>"
    out += "</DIV>\n<P style=\"margin: 35px;\" />\n"
    return out


### MAIN FUNCTION
def printPapers(summaryFile):
    out = makeHeader("Gerstein Lab Publications")
    out += '''
    <CENTER>
        <FONT FACE='sans-serif, Arial, Helvetica'><FONT SIZE=+2 COLOR=993333>Main Scientific Publications</FONT>
            <H3>
                <FONT SIZE="4" COLOR="#334499">
                Total papers: ''' + str(len(master_spreadsheet)) + '''
                </FONT>
            </H3>
        </FONT>
        (Last updated ''' + timestamp + ''')
    </CENTER>
    '''

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
            out += '''
            <H3 ALIGN=center>
                <FONT FACE='arial,helvetica,sans-serif' COLOR=000000 SIZE=4>-- ''' + currentYear + " ("+str(years[currentYear])+''') --</FONT>
            </H3>
            '''
            
        summaryFile.write(out)
        simpleFile.write(out)
        simpleFile2.write(out)

        out=""

        # print each paper entry
        printPaperEntry(row, summaryFile, pubmed)

        # generate simple.html and papers-simple.html
        printSimpleEntry(row, simpleFile, pubmed)
        printSimpleEntry(row, simpleFile2, pubmed)

        printEntrySummary(row, pubmed)
        printEntryExtended(row, pubmed)


    summaryFile.write("</DIV>\n</BODY>\n</HTML>")
    simpleFile.write("</DIV>\n</BODY>\n</HTML>")
    simpleFile2.write("</DIV>\n</BODY>\n</HTML>")

def printPaperMetrics(summaryFile):
    out = makeHeader("Gerstein Lab Publications")
    out += '''
    <CENTER>
        <FONT FACE='sans-serif, Arial, Helvetica'>
            <FONT SIZE=+2 COLOR=993333>Metrics for Gerstein Lab Publications</FONT>
            <H3>
                <FONT SIZE="4" COLOR="#334499">
                Total papers: ''' + str(len(master_spreadsheet)) + '''
                </FONT>
            </H3>
        </FONT>
        (Last updated ''' + timestamp + ''')
    </CENTER>
    <table style="width:90%" align="center" cellpadding="5">
    '''

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
        
        ### add year at the top of each year block
        if currentYear != row['Year']:
            currentYear = row['Year']
            out += '''
        <tr valign="bottom">
            <th></th>
            <th>
                <H3 align="left">
                    <br><br>
                    <i>
                        <FONT FACE='arial,helvetica,sans-serif' COLOR=000000 SIZE=4>''' + currentYear + " ("+str(years[currentYear])+''')</FONT>
                    </i>
                </H3>
            </th>
        </tr>'''
            
        out += '''
        <tr align=left valign=middle>
            <th>'''
        
        if row['doi']:
            out += '''
                <div id="altmetric" data-badge-popover="right" data-badge-type="donut" data-doi="''' + row['doi'].lstrip('\'') + '''" data-condensed="true" data-hide-no-mentions="true" class="altmetric-embed"></div>
            </th>
            <td>'''
        else:
            out += '''
                <div id="altmetric" data-badge-popover="right" data-badge-type="donut" data-pmid="''' + row['PMID'].lstrip('\'') + '''" data-condensed="true" data-hide-no-mentions="true" class="altmetric-embed"></div>
            </th>
            <td>'''

        # print title and citation
        if row['title']:
            out += '''
            <DIV CLASS="paperTitle">
                <FONT SIZE=+1>
                    <B><A HREF="/papers/''' + row['labid'].lstrip('\'') + '''/index.html">''' + row['title'].lstrip('\'') + '''</A></B>
                </FONT>
            </DIV>
            '''
        else:
            print "Warning: Title Empty!"
            print row

        if row['citation']:
            out += '''
            <DIV CLASS="paperCite">
                ''' + row['citation'].lstrip('\'') + '''
            </DIV>
            '''
        else:
            print "Warning: Citation Empty!"
            print row

        out += '''
            </td>
        </tr>
        '''
    
    out += '''
    </table>
    </DIV>
    </BODY>
    </HTML>
    '''
    metricsFile.write(out)

def printEntrySummary(row, pubmed):

    # create summary directory
    entrySummary = summaryPath + row['labid'].lstrip('\'')
    if not os.path.exists(entrySummary):
        os.makedirs(entrySummary)
    entrySummaryIndex = entrySummary + "/index.html"
    entrySummaryFile = open(entrySummaryIndex, 'w')

    out = makeHeader(row['title'].lstrip('\''))
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

    out = makeHeader(row['title'].lstrip('\''))
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
        subjects_all = row['subject'].split(',')
        subjects_all = [i.strip() for i in subjects_all]
        subjects = []
        fundings = []
        for subject in subjects_all:
            if subject in funding_subject:
                fundings.append(subject)
            else:
                subjects.append(subject)

        num_subjects = len(subjects)
        out += '<tr><td width=100><b><font color=gray>subject</font></b></td><td><b><font color=#000077>'
        subject_count = 0
        for subject in subjects:
            out += '<A HREF="/subject/' + subject.lstrip('\' ') + '">' + subject.lstrip('\' ') + '</A>'
            subject_count += 1
            if subject_count < num_subjects:
                out += ', '
        out += '</font></b></td></tr>\n'

        num_fundings = len(fundings)
        out += '<tr><td width=100><b><font color=gray>funding</font></b></td><td><b><font color=#000077>'
        funding_count = 0
        for subject in fundings:
            out += '<A HREF="/subject/' + subject.lstrip('\' ') + '">' + subject.lstrip('\' ') + '</A>'
            funding_count += 1
            if funding_count < num_fundings:
                out += ', '
        out += '</font></b></td></tr>\n'

    if not row['website']:
        out += "<tr><td width=100><b><font color=gray>website</font></b></td><td><b><font color=#000077>&nbsp;</font></b></td></tr>\n"
    else:
        out += '<tr><td width=100><b><font color=gray>website</font></b></td><td><b><font color=#000077><A HREF="' + row['website'].lstrip('\'') + '">' + row['website'].lstrip('\'') + '</A></font></b></td></tr>\n'

    if not row['website2']:
        out += "<tr><td width=100><b><font color=gray>link</font></b></td><td><b><font color=#000077>&nbsp;</font></b></td></tr>\n"
    else:
        out += '<tr><td width=100><b><font color=gray>link</font></b></td><td><b><font color=#000077><A HREF="' + row['website2'].lstrip('\'') + '">' + row['website2'].lstrip('\'') + '</A></font></b></td></tr>\n'
    if not row['preprint']:
        out += "<tr><td width=100><b><font color=gray>preprint</font></b></td><td><b><font color=#000077>&nbsp;</font></b></td></tr>\n"
    else:
        out += '<tr><td width=100><b><font color=gray>preprint</font></b></td><td><b><font color=#000077><A HREF="' + row['preprint'].lstrip('\'') + '">' + row['preprint'].lstrip('\'') + '</A></font></b></td></tr>\n'

    if row['labid'] and row['labid'] in images_dict_thumbnail:
	out += '<tr><td width=100><b><font color=gray>image</font></b></td><td><b><font color=#000077><A HREF="'+images_dict_gallery[row['labid']]+'"><img src="'+images_dict_thumbnail[row['labid']]+'" alt="Image"></A></font></b></td></tr>\n'

    if row['footnote']:
	out += '<tr><td width=100><b><font color=gray>footnote</font></b></td><td><b><font color=#000077>' + row['footnote'].lstrip('\'') + '</A></font></b></td></tr>\n'

    out += "</table><br><font color=gray>Unused tags: <i>e-print grant ignore sortval target website2</i></font><hr><a href='/'>Return to papers index</a><br>&nbsp;</blockquote>\n</BODY>\n</HTML>"
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

    out = '<div id="simple"><P style="line-height: 6pt "><DL COMPACT>'

    if row['PMID']:

        citation_simple = row['citation'].replace(row['authors']+" ("+row['Year']+"). ","")
        out += row['authors']+" ("+row['Year']+"). \""+row['title']+"\" "+citation_simple

        # add PMID
        out += ' <FONT SIZE=-1>[PMID: '+row['PMID']+']'
        # add PMCID if available
        if row.has_key('pmcid') and row['pmcid']:
            out += '[PMCID: '+row['pmcid']+']'
        out += '</FONT>\n'

    else:
        # check if manually-written citation is in correct format
        if "). " not in row['citation']:
            print "Warning: Citation format incompatible. Please use the format: authors (year). <i>journal</i> issue: page."
            print row['citation']
            out += "\""+row['title']+'\" '+row['citation']
        else:
            author_year = row['citation'].split(").")[0]+"). "
            citation_simple = row['citation'].split("). ")[1]
            out += author_year+" \""+row['title']+'\" '+citation_simple

    out += '</DL></P></div><br>'

    simpleFile.write(out)

def printSubject(master_spreadsheet):
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

            out = makeHeader(subject.capitalize())

            include = ''
            if row['HTML']:
                include = row['HTML'].lstrip('\'')
            if include:
                out += include
            subjectFile.write(out)
            subjectFile.write('</FONT><HR><A HREF="/"><B>Return to front page</B></A>\n</DIV>\n</BODY>\n</HTML>')
            subjectFile.close()

    for i, subject in enumerate(allsubjects):
        printSubjectFile(subject, subjectpapers[i])

def printSubjectFile(subject, subject_papers):
    path = subjectPath + subject
    if not os.path.exists(path):
        os.makedirs(path)
    subjectDetailFile = open(path + '/index.html', 'w')

    #	subjectInclude = path + '/include.html'

    out = makeHeader(subject.capitalize())

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

    subjectDetailFile.write('	</FONT><HR><A HREF="/"><B>Return to front page</B></A>\n</DIV>\n</BODY>\n</HTML>')
    subjectDetailFile.close()

def printSubjectEntry(row, subjectDetailFile):

    out = "<DIV CLASS=\"paperTitle\"><FONT SIZE=+1><B><A HREF=\"/papers/" + row['labid'].lstrip('\'') + "/index.html\">" + row['title'].lstrip('\'') + "</A></B></FONT></DIV>\n"
    out += "<DIV CLASS=\"paperCite\">" + row['citation'].lstrip('\'') + "</DIV>\n"

    # print links
    out += printLink(row)

    subjectDetailFile.write(out)

def printSubjectSummary(subject_spreadsheet):

    category = ''
    SubjectNumber = 0
    outPart = ''

    out = makeHeader("Gerstein Lab Publications")
    
    out += "<BR>"
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
    out += "</DIV>\n</BODY>\n</HTML>"
    subjectSummaryFile.write(out)

### MAIN ###

print "Merging master Google spreadsheet and PubMed data.."
mergeData(master_spreadsheet, pubmed_spreadsheet)

print "Saving merged data as CSV file: merged.csv"
write2csv(master_spreadsheet)

print "Building Subject Summary HTML files.."
printSubjectSummary(subject_spreadsheet)

print "Building Subject HTML files.."
printSubject(master_spreadsheet)

print "Building Paper HTML files.."
printPapers(summaryFile)

print "Building Paper metrics HTML files.."
printPaperMetrics(summaryFile)

# Fix permissions to make both apache and sudo users run updates
print "Fixing permissions for HTML files.."
os.system("chmod -R 775 ../html/papers/papers")

print ""
print "Done"
