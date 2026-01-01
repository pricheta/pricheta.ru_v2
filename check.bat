@echo off
set CODE=adapters apps

echo Running black...
black %CODE%
if errorlevel 1 (
    echo Black failed
    exit /b 1
)

echo Running pylint...
pylint %CODE%
if errorlevel 1 (
    echo Pylint failed
    exit /b 1
)

echo All checks passed!