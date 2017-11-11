for /l %%a in (1,1,100) do (
python manage.py test
pause
)
