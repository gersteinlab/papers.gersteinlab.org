#!/bin/bash -norc

DIR="$( cd "$( dirname "$0" )" && pwd )"

cat <<EOF

Trying to establish local installations of any missing Perl modules
(as logged in $DIR/setup-deps.log).
Please be patient, as this step may take a little while.
EOF

cd "$DIR"

mkdir -p _cpan/CPAN
echo '1;' >> _cpan/CPAN/MyConfig.pm
if ! perl -I_cpan -Iaux/lib/perl5 setup-deps.pl </dev/null >setup-deps.log 2>&1
then
  if grep '^read timeout.*HTTP' setup-deps.log >/dev/null
  then
    cat <<EOF
Unable to access the Comprehensive Perl Archive Network.  You might
need to set http_proxy and/or ftp_proxy in your user environment.
Please consult your network administrator for suitable values.
EOF
  elif grep '^SSLeay\.xs:.*[Ee]rror:' setup-deps.log >/dev/null
  then
    cat <<EOF
Unable to build Net::SSLeay.  Please install either a prebuilt version
of this module or OpenSSL development files to build it against.
EOF
  fi
fi
rm -rf _cpan

if ! perl -Iaux/lib/perl5 -MMozilla::CA -e '1;' 2>/dev/null
then
  gzip -cd Mozilla-CA.tar.gz | tar xvf -
fi

osname=`uname -s | sed -e 's/_NT-.*$/_NT/; s/^MINGW[0-9]*/CYGWIN/'`
cputype=`uname -m`

case "$osname-$cputype" in
  Linux-x86_64 | Darwin-x86_64 | CYGWIN_NT-* )
    ./ftp-cp ftp.ncbi.nlm.nih.gov /entrez/entrezdirect xtract."$osname".gz
    gunzip -f xtract."$osname".gz
  ;;
esac
if [ -f xtract."$osname" ]
then
  chmod +x xtract."$osname"
else
  echo "Unable to download xtract executable."
fi

case "$osname-$cputype" in
  Linux-x86_64 | Darwin-x86_64 | CYGWIN_NT-* )
    ./ftp-cp ftp.ncbi.nlm.nih.gov /entrez/entrezdirect rchive."$osname".gz
    gunzip -f rchive."$osname".gz
  ;;
esac
if [ -f rchive."$osname" ]
then
  chmod +x rchive."$osname"
else
  echo "Unable to download rchive executable."
fi

echo ""
echo "Entrez Direct has been successfully downloaded and installed."
echo ""

prfx="In order to complete the configuration process, please execute the following:\n"

target=bash_profile
if ! grep "$target" "$HOME/.bashrc" >/dev/null 2>&1
then
  if [ ! -f $HOME/.$target ] || grep 'bashrc' "$HOME/.$target" >/dev/null 2>&1
  then
    target=bashrc
  else
    if [ -n "$prfx" ]
    then
      echo -e "$prfx"
      prfx=""
    fi
    echo "  echo \"source ~/.bash_profile\" >>" "\$HOME/.bashrc"
  fi
fi
if ! grep "PATH.*edirect" "$HOME/.$target" >/dev/null 2>&1
then
  if [ -n "$prfx" ]
  then
    echo -e "$prfx"
    prfx=""
  fi
  echo "  echo \"export PATH=\\\${PATH}:$DIR\" >>" "\$HOME/.$target"
fi

if [ -z "$prfx" ]
then
echo ""
echo "or manually edit the PATH variable assignment in your .bash_profile file."
echo ""
fi
