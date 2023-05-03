:a
@REM remove instance\
del /f /q /s instance\*
pytest -s -v
timeout /t 10
goto a