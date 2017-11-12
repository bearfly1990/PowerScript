python %~dp0\functional_tests.py
pause
::for /l %%a in (1,1,100) do (
::python functional_tests.py
::pause
::)
