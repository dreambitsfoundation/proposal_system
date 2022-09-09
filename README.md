# Proposal Manager

This application is meat to expose a set of APIs to manage proposals into
a system and also manage the users attempting various activities on the system.

## Installation

Following are the instructions the are used for installation of the system.

### Setup

#### Step 1:

Check the system compatibity

This application requires python 3.9.X and above.

### Step 2:

1. Clone the application code into your local.
2. `cd` into the root directory of the project.
3. type `virtualenv venv` to create the virtual environment.
4. activate the virtual environment `source venv/bin/activate` (MacOS/Linux) and `venv/Scripts/activate.bat` (Windows).
5. install all the dependencies using `pip install -r requirements.txt`.

### Step 4:

Run the server using
`python manage.py runserver`

This will start a development server in `http://localhost:8000/`

### Step 5:

Import the Postman script to access all the APIs.

### Step 6:

Visit `localhost:8000/redoc-doc` for Redoc documents and `localhost:8000/swagger-doc` for Swagger doc.

### Step 7:

Run `python manage.py test` to run the tests.

You have 2 apps in the project `api` and `auth`.

You can run tests for individual apps by typeing

`python manage.py test <app_name>`

## Development

This application is developed using _Django Framework_ of Python.
For database we are usig _sqlite_ file database.

## Design:

I have tried to keep the Loosly Coupled design where the dependecy of
each component is negligle if not they share database relation into
their view logic.

## Special Info

1. Ideally, the report generation needs to be done using a background
   job scheduler or prefect automation flow. But since we have limited
   data and hence the queries are practically less costly, hence we can
   have implementation within the request-response cycle only within a
   test environment. Not recommened for prod environment.

2. Currently when you hit the API `/api/proposal_download/` with the request body `{'start_date': 'YYYY-MM-DD', 'end_date': 'YYYY-MM-DD'}` is generate a csv file containing all the proposals having proposal date within the scope and
   returns you the file in response.

3. Pagination is added in the APIs `/api/user_search/?email='<email_id>'` and `/api/proposal_search/?name='<proposal_name>'`.

4. We're using JWT for authentication.


## Dependencies Used in this project

1. django - Django Framework - It helps to host a WSGI application server and contains all the necessary modules needed to create interaction with the server.
2. djangorestframework - Django Rest Framework - This package contains all the required modules needed to create REST APIs.
3. djangorestframework_simplejwt - Simple JWT - Used to generate JWT tokens.
4. dtf-yasg - API Document Generator - This module helps to generate Swagger and Redoc document for all the API endpoints.


