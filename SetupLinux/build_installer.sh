#!/bin/sh

python3 ../../PyInstaller/pyinstaller.py -F ../paythebillsreminder.py

cp -f ../icon.gif dist/

rm -f *.spec
rm -fr build/
rm -fr __pycache__/
rm -fr ./deb_package/paythebill-1.0/opt/paythebill/

mv dist/ ./deb_package/paythebill-1.0/opt/paythebill/

chmod 755 ./deb_package/paythebill-1.0/DEBIAN/postinst
chmod 755 ./deb_package/paythebill-1.0/DEBIAN/postrm
chmod 755 ./deb_package/paythebill-1.0/DEBIAN/prerm

dpkg-deb --build ./deb_package/paythebill-1.0/

mv ./deb_package/paythebill-1.0.deb ./
