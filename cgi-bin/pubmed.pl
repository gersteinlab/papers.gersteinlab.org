#!/usr/bin/perl -w
print "Content-type: text/html\r\n\r\n";
print "Downloading from PubMed<br />\n";

system("/usr/bin/python /var/www/html/papers/update/parse_pmids.py");
sleep(10);
system("/usr/bin/curl `cat /var/www/html/papers/update/ncbiquery.txt` > /var/www/html/papers/update/NCBIData.xml");
sleep(10);
system("cd /var/www/html/papers/update && /usr/bin/python /var/www/html/papers/update/import.py");

print "<br />Downloaded PubMed data.\n";
