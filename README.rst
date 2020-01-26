Welcome to Quipu API
====================
This brief documentation will get you started on how to start contributing/testing our simple API.

Running with Docker
-------------------
If you want to try out our API, we have included a Dockerfile with which you can build and run
locally. By default, it will use production settings; however, you can only use http requests (for
now).

You can build the application image with:
``docker build -t quipu:prod .``

The application makes use of envirionment variables to control main settings. We have included
a sample. Feel free to look around the settings to see which other ones you can add. To run the
container you can use:
``docker run -it --rm --env-file conf/settings/sample-env -p 8000:8000 quipu:prod``

You can always use curl or Postman to interact with the API; however, we also provide a schema.
The schema can be found by navigating `here <http://localhost:8000/operations/openapi/>`_ .
If you would like to interact with it, you can always visit an endpoint with your favorite browser.
It should give you a small interface with which you can call the API.
You could also navigate to the `Swagger doc <http://localhost:8000/operations/swagger-ui/>`_ to
interact with the api; however, it doesn't show as much detail.

Development
-----------
If you would like to run the application locally, you can always run the Django server. This
application uses `pipenv <https://pipenv.kennethreitz.org/en/latest/>`_ to manage virtual
environments and dependencies.
You can install pipenv by: ``pip install --user pipenv``. Next, you will need to install
dependencies. You can use ``pipenv install --dev`` to install the required dependencies for
development. This command will create a virtual environment using the python mentioned in the
Pipfile (if you don't have that version of python installed, do so; or modify the file to include a
version that is available in your system).
You can now activate the virtual environment by using `pipenv shell` and exit from it with `exit`.

Before you start the application, you need to setup environment variables. Again, a sample is given
in the repository under `conf/settings/sample-env`. You would need to create a `.env` file in the
same location as the `sample-env` file for the application to read it automagically. Remember to
set your `DJANGO_SETTINGS_MODULE` to the development config file.

Finally, you can now run the application =)

Testing
-------
to test the application, we are using the basic django/python test framework. This are to be run
everytime someone makes a commit to the develop and master branches. Ensure you run this tests
locally before pushing your changes.
