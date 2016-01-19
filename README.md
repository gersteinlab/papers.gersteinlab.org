# papers.gersteinlab.org

This is a GitHub repository for papers page scripts used to generate http://papers.gersteinlab.org/

For more information, please visit our lab's [public wiki](http://info.gersteinlab.org/Papers_Page_Code) and [private wiki](http://wiki.gersteinlab.org/labinfo/Papers_Page_Documentation)

## Contents
Contains the following directories from lectures.gersteinlab.org

* /var/www
* /var/www/cgi-bin
* /var/www/html/papers/update

## Execution

1. http://dev.papers.gersteinlab.org/cgi-bin/1_gsheet2csv.py
- http://dev.papers.gersteinlab.org/update/master_gsheet.csv
2. http://dev.papers.gersteinlab.org/cgi-bin/2_csv2xml.py
3. http://dev.papers.gersteinlab.org/cgi-bin/3_xml2tsv.py
4. http://dev.papers.gersteinlab.org/cgi-bin/4_update.py
