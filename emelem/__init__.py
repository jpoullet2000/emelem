"""Package's main module!"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging
import os
import json

from flask import Flask, redirect
from flask_appbuilder import SQLA, AppBuilder, IndexView
from flask_migrate import Migrate
from flask_appbuilder.baseviews import expose
from flask_wtf.csrf import CSRFProtect

from emelem import utils, config

APP_DIR = os.path.dirname(__file__)
CONFIG_MODULE = os.environ.get('EMELEM_CONFIG', 'emelem.config')


app = Flask(__name__)
app.config.from_object(CONFIG_MODULE)
conf = app.config

db = SQLA(app)


@app.context_processor
def get_js_manifest():
    manifest = {}
    manifest_file_path = os.path.join(APP_DIR, 'static/assets/dist/manifest.json')
    try:
        with open(manifest_file_path, 'r') as f:
            manifest = json.load(f)
    except Exception as e:
        print(
            "no manifest file found at " +
            manifest_file_path
        )
    return dict(js_manifest=manifest)


if conf.get('WTF_CSRF_ENABLED'):
    csrf = CSRFProtect(app)


migrate = Migrate(app, db, directory=APP_DIR + "/migrations")

class MyIndexView(IndexView):
    @expose('/')
    def index(self):
        return redirect('/emelem/welcome')


appbuilder = AppBuilder(
    app, db.session,
    base_template='emelem/base.html',
    indexview=MyIndexView,
    security_manager_class=app.config.get("CUSTOM_SECURITY_MANAGER"))


if app.config.get('UPLOAD_FOLDER'):
    try:
        os.makedirs(app.config.get('UPLOAD_FOLDER'))
    except OSError:
        pass

sm = appbuilder.sm

get_session = appbuilder.get_session
results_backend = app.config.get("RESULTS_BACKEND")


from emelem import views
