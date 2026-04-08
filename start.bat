@echo off
setlocal

set "REPO_ROOT=%~dp0"
cd /d "%REPO_ROOT%"
set "VENV_DIR=%REPO_ROOT%.venv"
set "NEEDS_INSTALL=0"

if /I "%~1"=="--refresh" (
  set "NEEDS_INSTALL=1"
  shift
)

if not exist "%VENV_DIR%\Scripts\python.exe" (
  echo [Narrative Pipeline] Creating virtual environment...
  where py >nul 2>nul
  if errorlevel 1 (
    python -m venv "%VENV_DIR%"
  ) else (
    py -3 -m venv "%VENV_DIR%"
  )
  if errorlevel 1 goto :error
  set "NEEDS_INSTALL=1"
)

call "%VENV_DIR%\Scripts\activate.bat"
if errorlevel 1 goto :error

if not exist "%VENV_DIR%\Scripts\pip.exe" set "NEEDS_INSTALL=1"
if not exist "%VENV_DIR%\Scripts\narrative-pipeline.exe" set "NEEDS_INSTALL=1"

if "%NEEDS_INSTALL%"=="1" (
  echo [Narrative Pipeline] Installing local package...
  python -m pip install --upgrade pip >nul
  if errorlevel 1 goto :error
  python -m pip install -e .
  if errorlevel 1 goto :error
)

if "%~1"=="" goto :summary

echo [Narrative Pipeline] Running command: %*
python -m narrative_pipeline %*
if errorlevel 1 goto :error
goto :end

:summary
echo.
echo [Narrative Pipeline] Setup complete.
echo Try one of these next:
echo   start.bat init my_story
echo   start.bat status projects\my_story
echo   python -m narrative_pipeline --help
goto :end

:error
echo.
echo [Narrative Pipeline] Setup failed.
exit /b 1

:end
exit /b 0
