@echo off
setlocal
cd /d "%~dp0\.."

if not exist ".venv\Scripts\python.exe" (
    echo [1/3] Creating virtual environment...
    py -3 -m venv .venv
    if errorlevel 1 goto :error

    echo [2/3] Installing dependencies...
    ".venv\Scripts\python.exe" -m pip install --upgrade pip
    ".venv\Scripts\python.exe" -m pip install -r requirements.txt
    if errorlevel 1 goto :error
) else (
    echo [1/3] Virtual environment found.
    echo [2/3] Dependencies assumed installed. Run pip install -r requirements.txt if requirements changed.
)

echo [3/3] Starting MLA-C02 Command Center...
".venv\Scripts\python.exe" -m streamlit run app\command_center.py
exit /b %errorlevel%

:error
echo.
echo Command Center setup failed. Review the error above.
exit /b 1
