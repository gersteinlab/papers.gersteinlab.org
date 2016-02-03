# papers.gersteinlab.org

This is a GitHub repository for papers page scripts used to generate http://papers.gersteinlab.org/

For more information, please visit our lab's [public wiki](http://info.gersteinlab.org/Papers_Page_Code) and [private wiki](http://wiki.gersteinlab.org/labinfo/Papers_Page_Documentation)

## Contents
Contains the following directories from lectures.gersteinlab.org

* /var/www
* /var/www/cgi-bin
* /var/www/html/papers/update

## Papers 2.0 (under development @ dev.papers)

### What's New
* Papers 2.0 is now version controlled under GitHub: https://github.com/gersteinlab/papers.gersteinlab.org
* Dedicated development instance is available at dev.papers.gersteinlab.org
* Papers page under development is accessed via http://dev.papers.gersteinlab.org/
* Production server (lectures.gersteinlab.org) is synced with development via Git

### How to Execute
* STEP 1. Download Master Google spreadsheet as a CSV file
 * **Executable: http://dev.papers.gersteinlab.org/cgi-bin/1_gsheet2csv.py**
 * CSV output 1: http://dev.papers.gersteinlab.org/update/master_gsheet.csv
 * CSV output 2: http://dev.papers.gersteinlab.org/update/subject_gsheet.csv
* STEP 2. Build a PubMed query and retrieve results as XML
 * **Executable: http://dev.papers.gersteinlab.org/cgi-bin/2_csv2xml.py**
 * XML output: http://dev.papers.gersteinlab.org/update/pubmed.xml
* STEP 3. Parse PubMed XML into TSV file
 * **Executable: http://dev.papers.gersteinlab.org/cgi-bin/3_xml2tsv.py**
 * TSV output: http://dev.papers.gersteinlab.org/update/pubmed.tsv
* STEP 4. Merge Master Google spreadsheet with PubMed data and create HTMLs
 * **Executable: http://dev.papers.gersteinlab.org/cgi-bin/4_update.py**
 * CSV output: http://dev.papers.gersteinlab.org/update/merged.csv
