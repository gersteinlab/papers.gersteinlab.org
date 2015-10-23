#!/usr/bin/perl -w
print "Content-type: text/html\r\n\r\n";
print "Loading XML data.  (This may take awhile.)<br />\n";

system("cd /var/www/html/papers/update && /usr/bin/python /var/www/html/papers/update/reload_data.py");

print "<br />Loaded XML data.\n";
