@echo off


:start
cls

set venvScripts="C:\Users\Public\.venv\pyprestation_DEAMKA\Scripts"


call %venvScripts%\activate
call Streamlit run code_files\run.py --server.port 80

@pause
