django_shell:
	. venv/bin/activate && python manage.py shell

django_runserver:
	. venv/bin/activate && python manage.py runserver

django_startapp:
	. venv/bin/activate && python manage.py startapp ${app}

django_make_migrations:
	. venv/bin/activate && python manage.py makemigrations

django_migrate:
	. venv/bin/activate && python manage.py migrate