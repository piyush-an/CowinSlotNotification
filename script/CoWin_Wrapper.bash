#!/bin/bash

cd ~/sandbox/CoWin
echo "`date` | Python Call" >> log_python.log
/Users/anku/sandbox/CoWin/cowin_py-env/bin/python /Users/anku/sandbox/CoWin/app.py >> log_python.log 2>&1

exit