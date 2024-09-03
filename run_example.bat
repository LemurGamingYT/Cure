@echo off
@echo off
set filename=%1
set should_run=%2
for /f "tokens=2,* delims= " %%a in ("%*") do set ALL_BUT_FIRST=%%b
python main.py examples/%filename%.cure
if "%should_run%"=="1" (
    .\examples\%filename%.exe
)
