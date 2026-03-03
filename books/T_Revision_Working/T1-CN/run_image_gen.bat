@echo off
chcp 65001 >nul 2>nul
setlocal enabledelayedexpansion

:: ===========================================================
:: Universal AI Image Generator v2.0 - Windows Batch Entry
:: ===========================================================

cd /d "%~dp0"

:: -- Load .env --
if "%NB_API_KEY%"=="" (
    if exist ".env" (
        for /f "usebackq tokens=1,* delims==" %%A in (".env") do (
            set "_key=%%A"
            set "_val=%%B"
            for /f "tokens=*" %%X in ("!_key!") do set "_key=%%X"
            for /f "tokens=*" %%X in ("!_val!") do set "_val=%%X"
            if "!_key!"=="NB_API_KEY" set "NB_API_KEY=!_val!"
            if "!_key!"=="NB_API_BASE" set "NB_API_BASE=!_val!"
            if "!_key!"=="NB_MODEL" set "NB_MODEL=!_val!"
        )
    )
)

:: -- Help --
if "%1"=="--help" goto :show_help
if "%1"=="-h" goto :show_help

:: -- Init project --
if "%1"=="--init" (
    echo [Init] Creating project config template...
    python generate_images_api.py --init-project
    goto :done
)

:: -- Check Python --
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found. Please install Python 3.8+
    pause
    exit /b 1
)

:: -- Install deps silently --
pip install requests pillow --quiet 2>nul

:: -- Show config --
echo.
echo ====================================================
echo   AI Image Generator v2.0
echo ====================================================
echo.

if defined NB_API_KEY (
    echo   API Key: %NB_API_KEY:~0,12%...
) else (
    echo   WARNING: API Key not set. Configure .env file.
)
if defined NB_MODEL echo   Model:   %NB_MODEL%
echo.

:: -- Parse arguments --
set "PY_ARGS="
set "HAS_SCOPE="
set "MODE=skip"
set "EXTRA_FILTERS="
set "UPDATE_MD=--update-md"
set "DRY_RUN="

:parse_args
if "%1"=="" goto :run

if "%1"=="--overwrite" (
    set "MODE=overwrite"
    shift
    goto :parse_args
)
if "%1"=="--regenerate" (
    set "MODE=regenerate"
    shift
    goto :parse_args
)
if "%1"=="--list" (
    set "HAS_SCOPE=1"
    set "PY_ARGS=--list"
    set "UPDATE_MD="
    shift
    goto :parse_args
)
if "%1"=="--dry-run" (
    set "DRY_RUN=--dry-run"
    shift
    goto :parse_args
)
if "%1"=="--chapter" (
    set "HAS_SCOPE=1"
    set "PY_ARGS=--chapter %2"
    shift
    shift
    goto :parse_args
)
if "%1"=="--keys" (
    set "HAS_SCOPE=1"
    set "PY_ARGS=--keys"
    shift
    goto :collect_keys
)
if "%1"=="--type" (
    set "EXTRA_FILTERS=!EXTRA_FILTERS! --type %2"
    shift
    shift
    goto :parse_args
)
if "%1"=="--missing" (
    set "EXTRA_FILTERS=!EXTRA_FILTERS! --status missing"
    shift
    goto :parse_args
)

set "PY_ARGS=!PY_ARGS! %1"
shift
goto :parse_args

:collect_keys
if "%1"=="" goto :run
if "%1"=="--overwrite" goto :parse_args
if "%1"=="--regenerate" goto :parse_args
if "%1"=="--update-md" goto :parse_args
if "%1"=="--dry-run" goto :parse_args
if "%1"=="--type" goto :parse_args
if "%1"=="--missing" goto :parse_args
set "PY_ARGS=!PY_ARGS! %1"
shift
goto :collect_keys

:run
if not defined HAS_SCOPE (
    set "PY_ARGS=--all"
    if "!MODE!"=="skip" (
        echo [Default] Generate missing images, skip existing ones.
        echo.
        echo   Regenerate all:     run_image_gen.bat --overwrite
        echo   Show status:        run_image_gen.bat --list
        echo   Missing only:       run_image_gen.bat --missing
        echo   Specific chapter:   run_image_gen.bat --chapter 03
        echo   Opener images:      run_image_gen.bat --type opener
        echo.
    )
)

set "CMD=python generate_images_api.py !PY_ARGS! --mode !MODE! !EXTRA_FILTERS! !UPDATE_MD! !DRY_RUN!"
echo Execute: !CMD!
echo.
!CMD!
goto :done

:show_help
echo.
echo AI Image Generator v2.0
echo ========================
echo.
echo Basic:
echo   run_image_gen.bat                           Generate missing images
echo   run_image_gen.bat --list                    Show all image status
echo   run_image_gen.bat --dry-run                 Preview prompts
echo   run_image_gen.bat --init                    Init project config
echo.
echo Scope:
echo   run_image_gen.bat --chapter 03              Chapter 3 only
echo   run_image_gen.bat --keys fig_ch01_1 ...     Specific image keys
echo   run_image_gen.bat --type opener             Opener images only
echo   run_image_gen.bat --type inline             Inline images only
echo   run_image_gen.bat --missing                 Missing images only
echo.
echo Mode:
echo   (default)                                   Skip existing images
echo   run_image_gen.bat --overwrite               Backup old + regenerate
echo   run_image_gen.bat --regenerate              Overwrite without backup
echo.
echo Combo:
echo   run_image_gen.bat --chapter 05 --overwrite
echo   run_image_gen.bat --type opener --dry-run
echo   run_image_gen.bat --chapter 01 --missing
echo   run_image_gen.bat --keys fig_ch03_1 fig_ch03_2 --overwrite
echo.
echo Config:
echo   .env                  API key and model
echo   image_project.json    Project-level style and paths
echo   image_manifest.json   Image definitions
echo.

:done
echo.
echo Done!
pause
