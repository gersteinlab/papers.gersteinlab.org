#!/usr/bin/python
# -*- coding: UTF-8 -*-

# enable debugging
import cgitb
cgitb.enable()

print "Content-Type: text/plain;charset=utf-8"
print

import os, sys
# from GoogleSpreadsheet import GoogleSpreadsheet
from datetime import datetime
import pytz
import subprocess
import urllib2
import csv

# spreadsheet_id = "1Py9qFry1U6e5HNFXQ4vhDDnBf_5YtZSEBbZNeGXreLI" #"tgxpfFr0btZRRifLzIclNEA" #"o01144401739050618778.7867533471924312515"
# worksheet_id = "od6"
# spreadsheet = GoogleSpreadsheet(spreadsheet_id, worksheet_id)
timestamp = str(datetime.now(pytz.timezone('US/Eastern')).ctime())
#timestamp = str(datetime.now().ctime())
# lecturepage = "http://lectures.gersteinlab.org/summary/"

paperpage = "http://papers.gersteinlab.org/papers/"
# paperHTML = "/var/www/html/lectures/new_lectures/update/paper-index.html"

sbjpage = "http://papers.gersteinlab.org/subject/"
# sbjTSV = "/var/www/html/lectures/new_lectures/update/subject.tsv"
sbjTSV = "../html/lectures/update/subject_gsheet.csv"

summaryIndex = "/var/www/html/lectures/summary/index.html"
summaryPath = "/var/www/html/lectures/summary/"
summaryFile = open(summaryIndex,'w')

### Download Google Spreadsheet for paper subjects
print "#########    1.Preparing paper information    #########"
print "###--- Downloading Spreadshet for paper subjects ---###"
command = 'sh -c \'curl https://docs.google.com/a/yale.edu/spreadsheets/d/1fl9mWn-vaVCTO0OXEDFyAAYAjAmOtsh8gyYJe0LbPC8/pub?output=tsv > subject.tsv\''
p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
out, err = p.communicate()

### Download papers page index
print "###--------- Downloading papers page index ---------###"
response = urllib2.urlopen('http://papers.gersteinlab.org/papers/')
html_text = response.read()

print "###----------- Loading paper information -----------###"
href_dict = {} # Dictionary for paper reference
#with open(paperHTML, 'r') as f:
#	html_text = f.read()

html_text_split = html_text.split('table>')
table_text = html_text_split[1].split('</tr>')[3:-2]
for line in table_text:
    	tmp = line.split('<a')[1].split('</a>')[0]
    	href = tmp.split('href=\"')[1].split('\">')[0]
    	name = tmp.split('\">')[1].split('/')[0]
	name = name.lower()
    	href_dict[name] = href


def system_call(command):
    p = subprocess.Popen([command], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    out, err = p.communicate()
    if p.returncode==0:
        print "Success!"
    else:
        print "Failed!", out, err

## prod
master_gsheet_csv_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQVy7MPn5kFq3dX6i_LayO13qXayd_QppgJL9sREsDxCrPl4op3LZHNSrHeIuVjvnQ64cK6ggCbNagA/pub?gid=0&single=true&output=csv" 
## testing
# master_gsheet_csv_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRICN2-3zxLo59HPwiSV9XvrdO8KF2AHtPNf7dV4gp69QkOxlGAFW1iU0JPyqUFJc0D9vo2rAeYOWQ9/pub?gid=0&single=true&output=csv"

subject_gsheet_csv_url = "https://docs.google.com/spreadsheets/u/2/d/1fl9mWn-vaVCTO0OXEDFyAAYAjAmOtsh8gyYJe0LbPC8/export?format=csv&id=1fl9mWn-vaVCTO0OXEDFyAAYAjAmOtsh8gyYJe0LbPC8&gid=0"

master_csv_file = "../html/lectures/update/master_gsheet.csv"
subject_csv_file = "../html/lectures/update/subject_gsheet.csv"

curl = "/usr/bin/curl"
cmd1 = curl+" -L '"+master_gsheet_csv_url+"' > "+master_csv_file
cmd2 = curl+" -L '"+subject_gsheet_csv_url+"' > "+subject_csv_file

print "Downloading Master Google spreadsheet as CSV:", cmd1
system_call(cmd1)
print "File saved to", master_csv_file
print

print "Downloading Subject Google spreadsheet as CSV:", cmd2
system_call(cmd2)
print "File saved to", subject_csv_file
print

print "Done"

master_spreadsheet = list(csv.DictReader(open('../html/lectures/update/master_gsheet.csv')))
# master_spreadsheet = [{k.lower():v for k,v in d.items()} for d in master]
for d in master_spreadsheet:
	for key in d.keys():
		d[key.lower()] = d.pop(key)
	

subject_spreadsheet = list(csv.DictReader(open('../html/lectures/update/subject_gsheet.csv')))

sbj_dict = {} # Dictionary for paper subjects
with open(sbjTSV, 'r') as f:
    for line in f:
        tmp = line.split('\n')[0].split(',')
        if len(tmp) < 2:
            continue
        labid = tmp[1]
        
        sbj_dict[labid.lower()] = labid + '/index.html'
print "###----------- Loading paper information -----------###"
print "####################    Done    #######################\n"

### Write to summary html
banner = '''<div id="header">
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
        </div>
        <BR><BR><BR><BR>'''

def printSubject(subject):
	out = ''
	subject_list = subject.split(",")
	for s in subject_list:
		s = s.lstrip(' ')
		s = s.lower()
		if s in href_dict:
			out += "<A HREF=\"" + paperpage + href_dict[s]  + "\" NAME=\"" + s.lstrip('\'') + "\">" + s.lstrip('\'') + "</A>"
		elif s in sbj_dict:
			out += "<A HREF=\"" + sbjpage + sbj_dict[s]  + "\" NAME=\"" + s.lstrip('\'') + "\">" + s.lstrip('\'') + "</A>"
		else:
			out += s
		out += ", "
	out = out[:-2]
	out += "\n" 
	return out

	
def printLectures(spreadsheet,summaryFile):
	print "###-------- Writing to lectures summary page -------###"
	out = "<HTML>\n"
	out += "<HEAD>\n"
	out += "<TITLE>Gerstein Lab Lecture Summary</TITLE>\n"
	out += "<LINK REL=\"shortcut icon\" HREF=\"/favicon.ico\" >\n"
	out += "<link rel=\"stylesheet\" href=\"/style.css\">"
	out += "</HEAD>\n"
	out += "<BODY BGCOLOR=\"white\">\n"
	out += banner
	out += "<CENTER><FONT FACE=\"sans-serif, Arial, Helvetica\"><FONT SIZE=\"+2\" COLOR=\"993333\">Main Scientific Lectures</FONT>\n"
        out += "<H3><FONT SIZE=\"4\" COLOR=\"#334499\">Total Lectures: " + str(len(spreadsheet)) + "</FONT></H3></FONT>\n"
        out += "<p>(Last updated " + timestamp + " (EST))</CENTER>\n"
        #out += "<H3 ALIGN=center><FONT FACE=\"arial,helvetica,sans-serif\" COLOR=\"334499\" SIZE=\"4\">-- 2008 (37) --</FONT></H3>\n"
	years = {}
	currentYear = 0
	for row in spreadsheet:
		rowYear = row['date'].lstrip('\'')[-4:]
		if years.has_key(rowYear):
			years[rowYear] += 1
		else:
			years[rowYear] = 1

	print "###-------- Writing to lectures detail page --------###"
	for row in spreadsheet:
		if currentYear != row['date'].lstrip('\'')[-4:]:
			currentYear = row['date'].lstrip('\'')[-4:]
			out += "<H3 ALIGN=center><FONT FACE='arial,helvetica,sans-serif' COLOR=334499 SIZE=4>-- " + currentYear + " (" + str(years[currentYear]) + ") --</FONT></H3>"
		summaryFile.write(out)
		out = ""
		printLectureEntry(row, summaryFile)
		printEntrySummary(row)
		printEntryExtended(row)
	out = "</BODY></HTML>"
	summaryFile.write(out)
	print out

def printEntrySummary(row):
	# create summary directory
	entrySummary = summaryPath + row['labid'].lstrip('\'')
	if not os.path.exists(entrySummary):
		os.makedirs(entrySummary)
	entrySummaryIndex = entrySummary + "/index.html"
	entrySummaryFile = open(entrySummaryIndex,'w')
	out = "<HTML>"
	out += "<HEAD>"
	out += "<TITLE>" + row['title'].lstrip('\'') + "</TITLE>"
	out += "<LINK REL=\"shortcut icon\" HREF=\"/favicon.ico\" >"
	out += "<link rel=\"stylesheet\" href=\"/style.css\">"
	out += "</HEAD>"
	out += "<BODY BGCOLOR=\"white\">"
        out += banner
	out += "<BLOCKQUOTE>"
	if not row['title']:
		out += "<blockquote><font size=+1>&nbsp;</font>"
	else:
		out += "<blockquote><font size=+1><B>" + row['title'].lstrip('\'') + "</B></font>"
	if not row['description']:
		out += "<DD>&nbsp;</DD>"
	else:
		out += "<DD>" + row['description'].lstrip('\'') + "</DD>"
	if not row['subject']:
		out += "<DD><I>Subject</I>: <FONT FACE='courier'>&nbsp;</FONT> <I>Date Given</I>: " + row['date'].lstrip('\'') + "</DD>"
	else:
		out += "<DD><I>Subject</I>: <FONT FACE='courier'>" + printSubject(row['subject']) + "</FONT> <I>Date Given</I>: " + row['date'].lstrip('\'')  + "</DD>"
        if not row['labid']:
                out += "<DD>&nbsp;</DD>"
        else:
                out +="<DD><I>Lecture ID</I>: <FONT FACE='courier'; SIZE=-1>" + row['labid'].lstrip('\'') + "</FONT></DD>"

	out += "<DD>"
	out += printButtons(row)
	out += "</DD>"

	out += "<hr><br><a href=index-all.html>View all citation information</a><br><a href='/summary/'>Return to lectures index</a><br>&nbsp;</blockquote></BODY></HTML>"
	entrySummaryFile.write(out)

def printButtons(row):
	out = ""
	if not row['abstract']:
		out += "<IMG SRC=\"/null.gif\" HEIGHT=\"23\" WIDTH=\"56\" BORDER=\"0\">"
	else:
		out += "<A HREF=\"" + row['abstract'].lstrip('\'')  + "\"><IMG SRC=\"/abstract.jpg\" HEIGHT=\"23\" WIDTH=\"56\" BORDER=\"0\"></A>"
	if not row['pdf']:
		out += "<IMG SRC=\"/null.gif\" HEIGHT=\"23\" WIDTH=\"56\" BORDER=\"0\">"
	else:
		out += "<A HREF=\"" + row['pdf'].lstrip('\'') + "\"><IMG BORDER=\"0\" HEIGHT=\"23\" WIDTH=\"56\" SRC=\"/pdf.png\"></A>"
	if not row['ppt']:
		out += "<IMG SRC=\"/null.gif\" HEIGHT=\"23\" WIDTH=\"56\" BORDER=\"0\">"
	else:
		out += "<A HREF=\"" + row['ppt'].lstrip('\'') + "\"><IMG BORDER=\"0\" HEIGHT=\"23\" WIDTH=\"56\" SRC=\"/ppt.jpg\"></A>"
	# if not row['extra']:
	# 	out += "<IMG SRC=\"/null.gif\" HEIGHT=\"23\" WIDTH=\"56\" BORDER=\"0\">"
	# else:
	# 	out += "<A HREF=\"" + row['extra'].lstrip('\'') + "\"><IMG BORDER=\"0\" HEIGHT=\"23\" WIDTH=\"56\" SRC=\"/extra.png\"></A>"

	if row['extra1 link']:
		out += "<span class=\"buttoncontainer\">"
		out += "<A HREF=\"" + row['extra1 link'].lstrip('\'') + "\"><IMG BORDER=\"0\" HEIGHT=\"23\" WIDTH=\"56\" SRC=\"/null.gif\"></A>"
		if not row['extra1']:
			out += "<span class=\"buttontext\"><A HREF=\"" + row['extra1 link'].lstrip('\'') + "\">extra</A>"
		else:
			out += "<span class=\"buttontext\"><A HREF=\"" + row['extra1 link'].lstrip('\'') + "\">"+ row['extra1'].lstrip('\'') + "</A>"
		out += "</span>"
		out += "</span>"

	if row['extra2 link']:
		out += "<span class=\"buttoncontainer\">"
		out += "<A HREF=\"" + row['extra2 link'].lstrip('\'') + "\"><IMG BORDER=\"0\" HEIGHT=\"23\" WIDTH=\"56\" SRC=\"/null.gif\"></A>"
		if not row['extra2']:
			out += "<span class=\"buttontext\"><A HREF=\"" + row['extra2 link'].lstrip('\'') + "\">extra</A>"
		else:
			out += "<span class=\"buttontext\"><A HREF=\"" + row['extra2 link'].lstrip('\'') + "\">"+ row['extra2'].lstrip('\'') + "</A>"
		out += "</span>"
		out += "</span>"

	if row['extra3 link']:
		out += "<span class=\"buttoncontainer\">"
		out += "<A HREF=\"" + row['extra3 link'].lstrip('\'') + "\"><IMG BORDER=\"0\" HEIGHT=\"23\" WIDTH=\"56\" SRC=\"/null.gif\"></A>"
		if not row['extra3']:
			out += "<span class=\"buttontext\"><A HREF=\"" + row['extra3 link'].lstrip('\'') + "\">extra</A>"
		else:
			out += "<span class=\"buttontext\"><A HREF=\"" + row['extra3 link'].lstrip('\'') + "\">"+ row['extra3'].lstrip('\'') + "</A>"
		out += "</span>"
		out += "</span>"

	if row['extra4 link']:
		out += "<span class=\"buttoncontainer\">"
		out += "<A HREF=\"" + row['extra4 link'].lstrip('\'') + "\"><IMG BORDER=\"0\" HEIGHT=\"23\" WIDTH=\"56\" SRC=\"/null.gif\"></A>"
		if not row['extra3']:
			out += "<span class=\"buttontext\"><A HREF=\"" + row['extra4 link'].lstrip('\'') + "\">extra</A>"
		else:
			out += "<span class=\"buttontext\"><A HREF=\"" + row['extra4 link'].lstrip('\'') + "\">"+ row['extra4'].lstrip('\'') + "</A>"
		out += "</span>"
		out += "</span>"


	out += "<A HREF=\"/summary/" + row['labid'].lstrip('\'') + "/index-all.html\">" + "<IMG BORDER=\"0\" WIDTH=\"23\" HEIGHT=\"23\" SRC=\"/more.gif\"></A>"

	return out


def printEntryExtended(row):
	# create summary directory
	entryExtended = summaryPath + row['labid'].lstrip('\'')
	if not os.path.exists(entryExtended):
		os.makedirs(entryExtended)
	entryExtendedIndex = entryExtended + "/index-all.html"
	entryExtendedFile = open(entryExtendedIndex,'w')
	out = "<HTML>"
	out += "<HEAD>"
	out += "<TITLE>" + row['title'].lstrip('\'') + "</TITLE>"
	out += "<LINK REL=\"shortcut icon\" HREF=\"/favicon.ico\" >"
	out += "<link rel=\"stylesheet\" href=\"/style.css\">"
	out += "</HEAD>"
	out += "<BODY BGCOLOR=\"white\">"
        out += banner
	out += "<BLOCKQUOTE>"
	if not row['title']:
		out += "<blockquote><font size=+1>&nbsp;</font>"
	else:
		out += "<blockquote><font size=+1><B>" + row['title'].lstrip('\'') + "</B></font>"
	if not row['description']:
		out += "<DD>&nbsp;</DD>"
	else:
		out += "<DD>" + row['description'].lstrip('\'') + "</DD>"
        if not row['subject']:
                out += "<DD><I>Subject</I>: <FONT FACE='courier'>&nbsp;</FONT> <I>Date Given</I>: " + row['date'].lstrip('\'') + "</DD>"
        else:
                out += "<DD><I>Subject</I>: <FONT FACE='courier'>" + printSubject(row['subject']) + "</FONT> <I>Date Given</I>: " + row['date'].lstrip('\'')  + "</DD>"
        if not row['labid']:
                out += "<DD>&nbsp;</DD>"
        else:
                out +="<DD><I>Lecture ID</I>: <FONT FACE='courier'; SIZE=-1>" + row['labid'].lstrip('\'') + "</FONT></DD>"

        # print links
	out += "<DD>"
	out += printButtons(row)
	out += "</DD>"

	out += "<A HREF=index.html>Switch to compact view</A><hr><table>"
	if not row['labid']:
		out += "<tr><td width=100><b><font color=gray>labid</font></b></td><td><b><font color=#000077>&nbsp;</font></b></td></tr>\n"
	else:
		out += "<tr><td width=100><b><font color=gray>labid</font></b></td><td><b><font color=#000077>" + row['labid'].lstrip('\'') + "</font></b></td></tr>\n"
	if not row['title']:
		out += "<tr><td width=100><b><font color=gray>title</font></b></td><td><b><font color=#000077>&nbsp;</font></b></td></tr>\n"
	else:
		out += "<tr><td width=100><b><font color=gray>title</font></b></td><td><b><font color=#000077>" + row['title'].lstrip('\'') + "</font></b></td></tr>\n"
	if not row['subject']:
		out += "<tr><td width=100><b><font color=gray>subject</font></b></td><td><b><font color=#000077>&nbsp;</font></b></td></tr>\n"
	else:
		out += "<tr><td width=100><b><font color=gray>subject</font></b></td><td><b><font color=#000077>" + row['subject'].lstrip('\'') + "</font></b></td></tr>\n"
	if not row['description']:
		out += "<tr><td width=100><b><font color=gray>description</font></b></td><td><b><font color=#000077>&nbsp;</font></b></td></tr>\n"
	else:
		out += "<tr><td width=100><b><font color=gray>description</font></b></td><td><b><font color=#000077>" + row['description'].lstrip('\'') + "</font></b></td></tr>\n"
	if not row['date']:
		out += "<tr><td width=100><b><font color=gray>date given</font></b></td><td><b><font color=#000077>&nbsp;</font></b></td></tr>\n"
	else:
		out += "<tr><td width=100><b><font color=gray>date given</font></b></td><td><b><font color=#000077>" + row['date'].lstrip('\'') + "</font></b></td></tr>\n"
	if not row['abstract']:
		out += "<tr><td width=100><b><font color=gray>abstract</font></b></td><td><b><font color=#000077>&nbsp;</font></b></td></tr>\n"
	else:
		out += "<tr><td width=100><b><font color=gray>abstract</font></b></td><td><b><font color=#000077>" + row['abstract'].lstrip('\'') + "</font></b></td></tr>\n"
	out += "</table><hr><a href='/summary/'>Return to lectures index</a><br>&nbsp;</blockquote></BODY></HTML>"
	entryExtendedFile.write(out)

def printLectureEntry(row, summaryFile):
	out = "<DIV CLASS=\"paperCite\">"
	# print title and citation
	if not row['title']:
		out += "<DT><FONT SIZE=\"+1\"><B>&nbsp;</B></FONT></DT>\n"
	else:
		out += "<DT><A HREF=\"/summary/" + row['labid'].lstrip('\'') + "\" STYLE=\"text-decoration:none; color:black\" NAME=\"" + row['labid'].lstrip('\'') + "\"><FONT SIZE=\"+1\"><B>" + row['title'].lstrip('\'') + "</B></FONT></A></DT>\n"
	if not row['description']:
		out += "<DD>&nbsp;</DD>\n"
	else:
		out += "<DD>" + row['description'].lstrip('\'') + "</DD>\n"
        if not row['subject']:
                out += "<DD><I>Subject</I>: <FONT FACE='courier'>&nbsp;</FONT> <I>Date Given</I>: " + row['date'].lstrip('\'') + "</DD>"
        else:
                out += "<DD><I>Subject</I>: <FONT FACE='courier'>" + printSubject(row['subject'])  + "</FONT> <I>Date Given</I>: " + row['date'].lstrip('\'')  + "</DD>"
        if not row['labid']:
                out += "<DD>&nbsp;</DD>"
        else:
                out +="<DD><I>Lecture ID</I>: <FONT FACE='courier'; SIZE=-1>" + row['labid'].lstrip('\'') + "</FONT></DD>"
        # print links
	out += "<DD>"
	out += printButtons(row)
	out += "</DD>"


	out += "</DIV><BR>"
	summaryFile.write(out)

print "########### 2. Writing the lectures page html #########"
printLectures(master_spreadsheet, summaryFile)
print "####################    Done    #######################\n"
