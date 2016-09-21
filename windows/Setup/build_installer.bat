pyinstaller -F --noconsole --icon="..\icon.ico" ..\paythebillsreminder.py
del "*.spec"
del "*.exe"
rmdir /s /q build
rmdir /s /q __pycache__

copy /y "..\icon.ico" "dist\icon.ico"
copy /y "..\..\README.md" "dist\readme.txt"

move dist PayTheBillReminder

"C:\Program Files (x86)\Inno Setup 5\compil32.exe" /cc installer_script.iss

