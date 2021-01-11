# E-shop
<img src="shopart.png" width="500px">

## [Preview E-shop](https://itzomen.pythonanywhere.com)

## TODO
- Add translation feature to the website

# Set up
Steps:

1. Clone/pull/download this repository
2. Create a virtualenv with `python -m venv env`
3. Activate virtual environment `source env/bin/activate`
4. Install dependencies with `pip install -r requirements.txt`

### Create superuser
`python manage.py createsuper`

### Collect Static
`python manage.py collectstatic`

### Finally runserver
`python manage.py runserver`

#### NB
For Testing use 'http://localhost:8000/' as that is the domain URL in the settings.py
