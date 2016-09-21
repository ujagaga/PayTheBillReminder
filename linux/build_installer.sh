#!/bin/sh

cd "$(dirname "$0")"

python3 ../PyInstaller/pyinstaller.py -F paythebillsreminder.py

cp -f icon.gif dist/

rm -f *.spec
rm -fr build/
rm -fr __pycache__/
rm -fr ./deb_package/paythebill-1.0/opt/paythebill/

mv dist/ ./deb_package/paythebill-1.0/opt/paythebill/

dpkg-deb --build ./deb_package/paythebill-1.0/

