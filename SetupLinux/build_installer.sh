#!/bin/sh

pyinstaller3 -F ../paythebillsreminder.py

cp -f ../icon.gif dist/

rm -f *.spec
rm -fr build/
rm -fr __pycache__/
rm -fr ./deb_package/paythebill-1.1/opt/paythebill/

mv dist/ ./deb_package/paythebill-1.1/opt/paythebill/

chmod 755 ./deb_package/paythebill-1.1/DEBIAN/postinst
chmod 755 ./deb_package/paythebill-1.1/DEBIAN/postrm
chmod 755 ./deb_package/paythebill-1.1/DEBIAN/prerm

dpkg-deb --build ./deb_package/paythebill-1.1/

mv ./deb_package/paythebill-1.1.deb ./
