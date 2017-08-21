#!/usr/bin/env python
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging
from celery.bin import worker as celery_worker
from datetime import datetime
from subprocess import Popen

from colorama import Fore, Style
from flask_migrate import MigrateCommand
from flask_script import Manager

from emelem import app, db, security, utils  
from emelem.models import core as models

config = app.config
#celery_app = utils.get_celery_app(config)

manager = Manager(app)
manager.add_command('db', MigrateCommand)


@manager.command
def init():
    """Inits the Emelem application"""
    allowed_mlm_types = ['spark', 'sklearn']
    for i in allowed_mlm_types:
        mlm_type =  models.MLMType(name=i)
        db.session.add(mlm_type)
    db.session.commit()

    allowed_mlm_categories = ['classification',
                              'regression',
                              'clustering',
                              'dimensionality reduction',
                              'model selection',
                              'preprocessing'
    ]
    for i in allowed_mlm_categories:
        mlm_category =  models.MLMCategory(name=i)
        db.session.add(mlm_category)
    db.session.commit()
	                                
    allowed_mlm_metric_types = ['area_under_roc_curve',
			        'average_cost',
                                'binominal_test',
                                'build_cpu_time',
	                        'build_memory',
                                'c_index',
                                'chi-squared',
                                'class_complexity',
                                'class_complexity_gain',
                                'confusion_matrix',
                                'correlation_coefficient',
                                'cortana_quality',
                                'coverage',
                                'f_measure',
                                'information_gain',
                                'jaccard',
                                'kappa',
                                'kb_relative_information_score',
				'kohavi_wolpert_bias_squared',
				'kohavi_wolpert_error',
                                'kohavi_wolpert_sigma_squared',
                                'kohavi_wolpert_variance',
				'kononenko_bratko_information_score',
				'matthews_correlation_coefficient',
				'mean_absolute_error',
				'mean_class_complexity',
				'mean_class_complexity_gain',
				'mean_f_measure',
				'mean_kononenko_bratko_information_score',
				'mean_precision',
				'mean_prior_absolute_error',
                                'mean_prior_class_complexity',
                                'mean_recall',
                                'mean_weighted_area_under_roc_curve',
				'mean_weighted_f_measure',						        'mean_weighted_precision',							'mean_weighted_recall',
                                'number_of_instances',
				'os_information',
                                'positives',
				'precision',
                                'predictive_accuracy',
				'prior_class_complexity',
				'prior_entropy',
				'probability',
                                'quality',
                                'ram_hours',
                                'recall',
				'relative_absolute_error',
                                'root_mean_prior_squared_error',
				'root_mean_squared_error',
				'root_relative_squared_error',
				'run_cpu_time',
                                'run_memory',
				'run_virtual_memory',
                                'scimark_benchmark',
                                'single_point_area_under_roc_curve',
                                'total_cost',
                                'nclassified_instance_count',
                                'usercpu_time_millis',
                                'usercpu_time_millis_testing',
                                'usercpu_time_millis_training',
				'webb_bias',
                                'webb_error',
                                'webb_variance',
                                'joint_entropy',
				'pattern_team_auroc10']

    # for i in allowed_mlm_metric_types:
    #     mlm_metric_types = models.MLMMetricType(name=i)
    #     db.session.add(mlm_metric_type)
    # db.session.commit()

@manager.option(
    '-d', '--debug', action='store_true',
    help="Start the web server in debug mode")
@manager.option(
    '-n', '--no-reload', action='store_false', dest='no_reload',
    default=config.get("FLASK_USE_RELOAD"),
    help="Don't use the reloader in debug mode")
@manager.option(
    '-a', '--address', default=config.get("EMELEM_WEBSERVER_ADDRESS"),
    help="Specify the address to which to bind the web server")
@manager.option(
    '-p', '--port', default=config.get("EMELEM_WEBSERVER_PORT"),
    help="Specify the port on which to run the web server")
@manager.option(
    '-w', '--workers',
    default=config.get("EMELEM_WORKERS", 2),
    help="Number of gunicorn web server workers to fire up")
@manager.option(
    '-t', '--timeout', default=config.get("EMELEM_WEBSERVER_TIMEOUT"),
    help="Specify the timeout (seconds) for the gunicorn web server")
@manager.option(
    '-s', '--socket', default=config.get("EMELEM_WEBSERVER_SOCKET"),
    help="Path to a UNIX socket as an alternative to address:port, e.g. "
         "/var/run/emelem.sock. "
"Will override the address and port values.")
def runserver(debug, no_reload, address, port, timeout, workers, socket):
    """Starts a Emelem web server."""
    debug = debug or config.get("DEBUG")
    if debug:
        print(Fore.BLUE + '-=' * 20)
        print(
            Fore.YELLOW + "Starting Emelem server in " +
            Fore.RED + "DEBUG" +
            Fore.YELLOW + " mode")
        print(Fore.BLUE + '-=' * 20)
        print(Style.RESET_ALL)
        app.run(
            host='0.0.0.0',
            port=int(port),
            threaded=True,
            debug=True,
            use_reloader=no_reload)
    else:
        addr_str = " unix:{socket} " if socket else" {address}:{port} "
        cmd = (
            "gunicorn "
            "-w {workers} "
            "--timeout {timeout} "
            "-b " + addr_str +
            "--limit-request-line 0 "
            "--limit-request-field_size 0 "
            "emelem:app").format(**locals())
        print(Fore.GREEN + "Starting server with command: ")
        print(Fore.YELLOW + cmd)
        print(Style.RESET_ALL)
        Popen(cmd, shell=True).wait()
