; Script generated by the Inno Script Studio Wizard.
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!

[Setup]
AppName=PayTheBillsReminder
AppVersion=1.0
AppCopyright=Rada Berar
PrivilegesRequired=none
RestartIfNeededByRun=False
DefaultDirName={pf}\PayTheBillsReminder
AppPublisher=Rada Berar
AppPublisherURL=ujagaga@gmail.com
CreateUninstallRegKey=no
UpdateUninstallLogAppName=False
UninstallDisplayName=PayTheBillsReminderUninstaller
UninstallDisplayIcon={uninstallexe}
OutputDir=..\
OutputBaseFilename=PayTheBillsReminder_winInstall
AlwaysShowGroupOnReadyPage=True
DefaultGroupName=PayTheBills Reminder
AppContact=ujagaga@gmail.com
DisableWelcomePage=True
AppId={{717B0A65-05D2-49D0-8C9C-FF4DE997097C}
VersionInfoVersion=1.0
VersionInfoDescription=PayTheBills Reminder 
VersionInfoCopyright=Rada Berar
SourceDir=PayTheBillsReminder
VersionInfoCompany=Private indipendent endevor
CloseApplications=False
RestartApplications=False

[Files]
Source: "paythebillsreminder.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "icon.gif"; DestDir: "{app}"; Flags: ignoreversion
Source: "readme.txt"; DestDir: "{app}"; Flags: ignoreversion
Source: "cleanup.bat"; DestDir: "{app}"

[UninstallRun]
Filename: "{app}\cleanup.bat"

[Run]
Filename: "{app}\paythebillsreminder.exe"; WorkingDir: "{app}"; Flags: nowait

[Icons]
Name: "{group}\PayTheBills Reminder"; Filename: "{app}\paythebillsreminder.exe"; WorkingDir: "{app}"; IconFilename: "{app}\paythebillsreminder.exe"
Name: "{group}\Uninstall"; Filename: "{uninstallexe}"; IconFilename: "{app}\paythebillsreminder.exe"
Name: "{userstartup}\PayTheBills Reminder"; Filename: "{app}\paythebillsreminder.exe"; WorkingDir: "{app}"; IconFilename: "{app}\paythebillsreminder.exe"; Parameters: "silent"