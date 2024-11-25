@echo off
set filename=%1
set should_run=%2
for /f "tokens=2,* delims= " %%a in ("%*") do set ALL_BUT_FIRST=%%b
@echo on
gcc c_testing/%filename%.c -o c_testing/%filename%.exe -I include/ %ALL_BUT_FIRST%
@echo off
if "%should_run%"=="1" (
    @echo on
    .\c_testing\%filename%.exe
)
