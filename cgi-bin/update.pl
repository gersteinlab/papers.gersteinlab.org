#!/usr/bin/perl -w
print "Content-type: text/html\r\n\r\n";
print "Rebuilding papers<br />\n";

my $status = system("cd /var/www/html/papers/update/ && /var/www/html/papers/update/update.py");
#if ($status2 % 256 == 0) {
#	my $status2 = system("/var/www/html/papers/update/update.py");
#}

if ($status % 256 != 0) { print "Error! CODE: ", $status; }
else { print "<br />Papers updated.\n"; }
