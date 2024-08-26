@echo off
set filename=%1
set should_run=%2
for /f "tokens=2,* delims= " %%a in ("%*") do set ALL_BUT_FIRST=%%b
gcc c_testing/%filename%.c -o c_testing/%filename%.exe %ALL_BUT_FIRST%
if "%should_run%"=="1" (
    .\c_testing\%filename%.exe
)
