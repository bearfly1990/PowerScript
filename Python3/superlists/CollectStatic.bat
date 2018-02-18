cd /d %~dp0
python manage.py collectstatic
pause
::timeout 100