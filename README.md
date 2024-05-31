# Hi Mo!

Let's go over the project setup.

We have two ways of running the project, either by using docker or by setting up the project locally.

1. [Local setup](#local-setup)
2. [Docker setup](#docker-setup)
3. [Project structure](#project-structure)

## Local setup

```sh
# Clone the project
git clone git@github.com:fromagge/mo_backend_test.git

# Change directory
cd mo_backend_test

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install requirements
pip install -r requirements.txt

```

Up to this point everything is installed, now we just need to run the migrations and start the server

```sh
# Run migrations
python manage.py migrate

# (Optional) Create a superuser
python manage.py createsuperuser

# (Optional) Seed the database with dummy data
python manage.py seed

# Start the server
python manage.py runserver
```

Once the server is running, you can access the admin panel at http://localhost:8000/admin/ or the API itself
at http://localhost:8000.

If you are good with this setup, you can stop reading here. And go further down into
the [project structure](#project-structure).

# Docker setup

```sh
# Clone the project

git clone 

# Change directory
cd mo_backend_test

# Run docker compose (make sure that docker is installed and running)
docker-compose up -d
```

If everything goes well, you should be able to access the API at http://localhost:8000 and the admin panel
at http://localhost:8000/admin/. By default, this docker container creates a database and seeds it with dummy data.

To run the test simply run

`python manage.py test`

# API structure

The API is structured as follows:

- `/customer/` - Create a new customer
- `/customer/<id>/` - Retrieve a customer
- `/customer/<id>/loans/` - Retrieve all loans for a customer
- `/loan/` - Create a new loan
- `/loan/<id>/` - Retrieve a loan
- `/loan/<id>/status/` - Change the status of a loan
- `/loan/<id>/repayments/` - Retrieve all repayments for a loan
- `/payment/` - Create a new repayment
- `/payment/<id>/` - Retrieve a repayment
- `/swagger/` - Swagger documentation - All of this information ☝🏽 but more organized.

# Login

To get the credentials to the API (not admin panel) use the route /auth/token and send a POST request with the following
body:

```json
{
  "username": "your_username",
  "id": "id_number",
  "password": "your_password"
}
```

If you haven't set up one but followed the instructions to docker and locally, you can use the following credentials:

```json
{
  "username": "test_drive",
  "id": 1,
  "password": "password"
}
 ```

The project also includes a file called `Insomnia_WeAreMo.json` which you can import into Insomnia or Postman to test
the API.


Enjoy! 🚀
