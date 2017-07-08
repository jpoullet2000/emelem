import unittest
import logging


from flask import redirect, request, session

logging.basicConfig(format='%(asctime)s:%(levelname)s:%(name)s:%(message)s')
logging.getLogger().setLevel(logging.DEBUG)


DEFAULT_ADMIN_USER = 'jbp'
DEFAULT_ADMIN_PASSWORD = 'jbp'
# DEFAULT_ADMIN_USER = 'admin'
# DEFAULT_ADMIN_PASSWORD = 'general'

log = logging.getLogger(__name__)

class EmelemAPITest(unittest.TestCase):
    def setUp(self):
        from flask import Flask
        from flask_appbuilder import AppBuilder
        from flask_appbuilder.models.sqla.interface import SQLAInterface
        from flask_appbuilder.views import ModelView

        self.app = Flask(__name__)
        self.basedir = os.path.abspath(os.path.dirname(__file__))
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'
        self.app.config['CSRF_ENABLED'] = False
        self.app.config['SECRET_KEY'] = 'thisismyscretkey'
        self.app.config['WTF_CSRF_ENABLED'] = False

        self.db = SQLA(self.app)
        self.appbuilder = AppBuilder(self.app, self.db.session)

        sess = PSSession()

        class PSView(ModelView):
            datamodel = GenericInterface(PSModel, sess)
            base_permissions = ['can_list', 'can_show']
            list_columns = ['UID', 'C', 'CMD', 'TIME']
            search_columns = ['UID', 'C', 'CMD']

    def login(self, client, username, password):
        # Login with default admin
        return client.post('/login/',
                           data=dict(
                               username=username,
                               password=password
                           ), follow_redirects=True)

    
    def logout(self, client):
        return client.get('/logout/')

    def test_back(self):
        """
            Test Back functionality
        """
        with self.app.test_client() as c:
            self.login(c, DEFAULT_ADMIN_USER, DEFAULT_ADMIN_PASSWORD)
            rv = c.get('/mlmmodelview/list/?_flt_0_field_string=f')
            rv = c.get('/mlmmodelview/list/')
            rv = c.get('/back', follow_redirects=True)
            assert request.args['_flt_0_field_string'] == u'f'
            assert '/mlmmodelview/list/' == request.path    
