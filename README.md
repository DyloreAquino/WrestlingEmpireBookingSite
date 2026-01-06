# WrestlingEmpireBookingSite
Website for assisting bookings in Wrestling Empire, written in Django

HOW TO SETUP

1. Create a virtual environment on your repo. The venv's name should be "akashic_env"

    py -m venv akashic_env

2. activate this venv (go to akaschi_env\Scripts, activate)

3. Install all libraries from requirements.txt

    pip install -r requirements.txt

4. Create a .env file including your secret key in the format

    SECRET_KEY="skandkahbdwkabksdjn"

5. To generate your secret key, plug this into your terminal:

    python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

This should output your generated secret_key, so just place this in the .env file.

6. Try running py manage.py runserver and check.