cd %~dp0
python manage.py test functional_tests
pause
::for /l %%a in (1,1,100) do (
::python manage.py test functional_tests
::pause
::)
