Installation & Configuration
============================

Getting Started
---------------

Emelem is tested against Python ``2.7`` and Python ``3.4``.

Python virtualenv
-----------------
It is recommended to install Emelem inside a virtualenv. Python 3 already ships virtualenv, for
Python 2 you need to install it. If it's packaged for your operating systems install it from there
otherwise you can install from pip: ::

    pip install virtualenv

You can create and activate a virtualenv by: ::

    # virtualenv is shipped in Python 3 as pyvenv
    virtualenv venv
    . ./venv/bin/activate

On windows the syntax for activating it is a bit different: ::

    venv\Scripts\activate

Once you activated your virtualenv everything you are doing is confined inside the virtualenv.
To exit a virtualenv just type ``deactivate``.

Python's setup tools and pip
----------------------------
Put all the chances on your side by getting the very latest ``pip``
and ``setuptools`` libraries.::

    pip install --upgrade setuptools pip

Emelem installation and initialization
----------------------------------------
Follow these few simple steps to install Emelem.::

    # Install Emelem
    pip install emelem

    # Create an admin user (you will be prompted to set username, first and last name before setting a password)
    fabmanager create-admin --app emelem

    # Initialize the database -- TO BE DONE 
    # emelem db upgrade

    # Create default roles and permissions
    emelem init

    # Start the web server on port 8099, use -p to bind to another port
    emelem runserver

    # To start a development web server, use the -d switch
    # emelem runserver -d


After installation, you should be able to point your browser to the right
hostname:port `http://localhost:8099 <http://localhost:8099>`_, login using
the credential you entered while creating the admin account.

Please note that *gunicorn*, Emelem default application server, does not
work on Windows so you need to use the development web server.
The development web server though is not intended to be used on production systems
so better use a supported platform that can run *gunicorn*.

Configuration behind a load balancer
------------------------------------

If you are running emelem behind a load balancer or reverse proxy (e.g. NGINX
or ELB on AWS), you may need to utilise a healthcheck endpoint so that your
load balancer knows if your superset instance is running. This is provided
at ``/health`` which will return a 200 response containing "OK" if the
webserver is running.

If the load balancer is inserting X-Forwarded-For/X-Forwarded-Proto headers, you
should set `ENABLE_PROXY_FIX = True` in the emelem config file to extract and use
the headers.


Configuration
-------------

To configure your application, you need to create a file (module)
``emelem_config.py`` and make sure it is in your PYTHONPATH. Here are some
of the parameters you can copy / paste in that configuration module: ::

    #---------------------------------------------------------
    # Emelem specific config
    #---------------------------------------------------------
    ROW_LIMIT = 5000
    EMELEM_WORKERS = 4

    EMELEM_WEBSERVER_PORT = 8099
    #---------------------------------------------------------

    #---------------------------------------------------------
    # Flask App Builder configuration
    #---------------------------------------------------------
    # Your App secret key
    SECRET_KEY = '\2\1thisismyscretkey\1\2\e\y\y\h'

    # The SQLAlchemy connection string to your database backend
    # This connection defines the path to the database that stores your
    # emelem metadata (mlm, project, tag, ...).
    # Note that the connection information to connect to the datasources
    # you want to explore are managed directly in the web UI
    SQLALCHEMY_DATABASE_URI = 'sqlite:////path/to/emelem.db'

    # Flask-WTF flag for CSRF
    WTF_CSRF_ENABLED = True

    # Set this API key to enable Mapbox visualizations
    MAPBOX_API_KEY = ''

This file also allows you to define configuration parameters used by
Flask App Builder, the web framework used by Emelem. Please consult
the `Flask App Builder Documentation
<http://flask-appbuilder.readthedocs.org/en/latest/config.html>`_
for more information on how to configure Emelem.

Please make sure to change:

* *SQLALCHEMY_DATABASE_URI*, by default it is stored at *~/.emelem/emelem.db*
* *SECRET_KEY*, to a long random string


Making your own build
---------------------

For more advanced users, you may want to build Emelem from sources. That
would be the case if you fork the project to add features specific to
your environment.::

    # assuming $EMELEM_HOME as the root of the repo
    cd $EMELEM_HOME/emelem/assets
    npm install
    npm run build
    cd $EMELEM_HOME
    python setup.py install

