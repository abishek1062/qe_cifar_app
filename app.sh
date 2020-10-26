export LC_ALL=C.UTF-8
export LANG=C.UTF-8
export FLASK_APP=run.py
pip install -r requirements_apps.txt --user
python -m flask run --host=0.0.0.0 --port=8888