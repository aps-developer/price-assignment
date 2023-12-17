1. Download python.
2. clone repository (if clone not working. Download zip file)
3. RUN command in CMD "python -m venv <your_env_name>"
4. RUN "<your_env_name>\Scripts\activate" to activate environment.
5. RUN "pip install -r requirements.txt"
6. Go to project directory (at the same level where "manage.py" file is present)
7. RUN "python manage.py migrate"
8. RUN "python manage.py createsuperuser" and create a super user for admin panel.
9. RUN "python manage.py runserver"
10. Go to Django Admin Panel and configure "Price Configuration instance." and MAKE INSTANCE ACTIVE.  *** NOTE: Make only one instance active at a time. ***
11. Fill the values as per the assignment example.
12. Go to "127.0.0.1:8000"
13. fill values and check result.
