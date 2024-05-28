# Initial System Setup
1. install python
2. pip install virtualenv

# Start venv
# Requirements.txt (pip freeze)

# install requirements
pip install -r requirements

# migrate
python manage.py migrate

# create superuser
python manage.py createsuperuser
super/super + email

# Seed Db with Countries and Cities
To seed database with country and cities after running migrations, run this command:
```sh
python manage.py cities_light

```

# Seed Local db with Fake Data
To seed local database with fake data after running migrations, run this command:
```sh
python manage.py seed_test_data  --number 20 #optional 10 is default

```


