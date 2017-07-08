#!/usr/bin/env bash
echo $DB
rm ~/.emelem/unittests.db
#rm ~/.emelem/celerydb.sqlite
#rm ~/.emelem/celery_results.sqlite
rm -f .coverage
export EMELEM_CONFIG=tests.emelem_test_config
set -e
#emelem/bin/emelem db upgrade
emelem/bin/emelem version -v
python setup.py nosetests
coveralls
