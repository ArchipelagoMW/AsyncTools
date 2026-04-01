@echo off

@REM Small script that creates a python venv and executes the script inside that venv to not clutter the global
@REM package index.

@REM set directory the batch file is called from as current working directory
cd /d "%~dp0"

set "FOLDER=.venv"

@REM check if the venv already exists and if not create it
if exist "%FOLDER%\" (
    echo "venv-folder already present"
) else (
    echo "no venv-folder found. creating it"
    call python -m venv .venv
)
@REM active venv
call .\.venv\Scripts\activate

@REM update venv and install needed packages
call python.exe -m pip install --upgrade pip
call pip install -r requirements.txt

@REM actually execute the python script
call python csv_output_splitter.py
