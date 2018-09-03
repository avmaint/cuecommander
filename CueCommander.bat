REM backup qwx file

ipconfig | find "IPv4"

d:
cd \Dropbox\UAC_Software\CueCommander\

set qxw=CueCommander.qxw

start C:\QLC+\qlcplus.exe -o %qxw%  --operate --web

py \Dropbox\UAC_Software\github\cuecommander\CueCommander.py
