@echo off
REM Password Manager Batch Script
REM Windows alternative to the Makefile

if "%1"=="" goto help
if "%1"=="help" goto help
if "%1"=="install" goto install
if "%1"=="validate" goto validate
if "%1"=="quick-start" goto quick-start
if "%1"=="test" goto test
if "%1"=="cli" goto cli
if "%1"=="gui" goto gui
if "%1"=="clean" goto clean
if "%1"=="check" goto check
goto unknown

:help
echo Password Manager - Available Commands
echo ========================================
echo.
echo Setup Commands:
echo   install      - Install dependencies
echo   validate     - Validate project setup
echo   quick-start  - Quick start with validation
echo.
echo Development Commands:
echo   test         - Run all tests
echo.
echo Run Commands:
echo   cli          - Run CLI interface
echo   gui          - Run GUI interface
echo.
echo Utility Commands:
echo   clean        - Clean up temporary files
echo   check        - Run all checks
echo.
echo Usage: run.bat [command]
goto end

:install
echo Installing dependencies...
pip install -r requirements.txt
echo Dependencies installed
goto end

:validate
echo Validating project setup...
python scripts/validate_setup.py
goto end

:quick-start
echo Running quick start...
python scripts/quick_start.py
goto end

:test
echo Running tests...
python -m pytest tests/ -v
goto end

:cli
echo Starting CLI...
python -m cli.multi_vault_cli
goto end

:gui
echo Starting GUI...
python -m gui.app
goto end

:clean
echo Cleaning up...
for /r %%f in (*.pyc) do del "%%f" 2>nul
for /d /r %%d in (__pycache__) do rmdir /s /q "%%d" 2>nul
for /r %%f in (*.db) do del "%%f" 2>nul
echo Cleanup complete
goto end

:check
call :install
call :validate
call :test
echo All checks passed!
goto end

:unknown
echo Unknown command: %1
echo Run 'run.bat help' to see available commands
goto end

:end 