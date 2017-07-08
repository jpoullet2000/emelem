from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging
import json
import os
import unittest
import logging

from emelem import app, cli, db, appbuilder, security, sm

logging.basicConfig(format='%(asctime)s:%(levelname)s:%(name)s:%(message)s')
logging.getLogger().setLevel(logging.DEBUG)

os.environ['EMELEM_CONFIG'] = 'tests.emelem_test_config'

BASE_DIR = app.config.get("BASE_DIR")
DEFAULT_ADMIN_USER = 'admin'
DEFAULT_ADMIN_PASSWORD = 'general'

log = logging.getLogger(__name__)

class EmelemTestCase(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        # if (
        #                 self.requires_examples and
        #                 not os.environ.get('SOLO_TEST') and
        #                 not os.environ.get('examples_loaded')
        # ):
            # logging.info("Loading examples")
            # cli.load_examples(load_test_data=True)
            # logging.info("Done loading examples")
            # sync_role_definitions()
            # os.environ['examples_loaded'] = '1'
        # else:
        #     sync_role_definitions()
        super(EmelemTestCase, self).__init__(*args, **kwargs)
        self.client = app.test_client()
        # self.maxDiff = None

    
    def get_resp(
            self, url, data=None, follow_redirects=True, raise_on_error=True):
        """Shortcut to get the parsed results while following redirects"""
        if data:
            resp = self.client.post(
                url, data=data, follow_redirects=follow_redirects)
        else:
            resp = self.client.get(url, follow_redirects=follow_redirects)
        if raise_on_error and resp.status_code > 400:
            raise Exception(
                "http request failed with code {}".format(resp.status_code))
        return resp.data.decode('utf-8')
    
    def login(self, username=DEFAULT_ADMIN_USER, password=DEFAULT_ADMIN_PASSWORD):
        resp = self.get_resp(
            '/login/',
            data=dict(username=username, password=password))
        self.assertIn('Welcome', resp)

    def test_login(self):
        resp = self.get_resp(
            '/login/',
            data=dict(username=DEFAULT_ADMIN_USER, password=DEFAULT_ADMIN_PASSWORD))
        self.assertIn('Welcome', resp)   


    def test_model_explore_json(self):
        self.login()
        resp = self.get_resp('/emelem/models/4/')
        log.info(resp)
        self.assertIn('"sklearn"', resp)
