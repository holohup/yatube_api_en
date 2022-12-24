python3 -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
cd yatube_api
python manage.py migrate
python manage.py loaddata fixtures.json
python manage.py runserver
