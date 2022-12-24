python3 -m venv venv
source venv/bin/activate
python3 -m pip install --upgrade pip
pip install -r requirements.txt
cd yatube_api
python3 manage.py migrate
python3 manage.py runserver