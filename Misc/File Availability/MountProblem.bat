@echo off

rem This script will keep track when, if ever, a file goes missing.
rem Mainly it helps in situations where a file server or network might
rem be a bit flakey. 

set PATH_TO_CHECK=Z:\settings\dbConnect.xml

set TIMEOUT_SECS=60
set LOG_LOCATION=%HOMEPATH%\Desktop\times_missing.txt

rem ==============================================

echo Here are the times we couldn't find the file %PATH_TO_CHECK: > %LOG_LOCATION%

:1

time /T

if exist %PATH_TO_CHECK% (
    echo Exists
) else (
    time /T >> %LOG_LOCATION%
    echo Missing
)

timeout %TIMEOUT_SECS% > NUL

GOTO 1