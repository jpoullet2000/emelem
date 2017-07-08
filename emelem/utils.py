"""Utility functions used across Emelem"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import decimal
import functools
import json
import logging
import numpy
import os
import parsedatetime
import pytz
import smtplib
import sqlalchemy as sa
import signal
import uuid
import sys
import zlib

from builtins import object
from datetime import date, datetime, time

import celery
from dateutil.parser import parse
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.utils import formatdate
from flask import flash, Markup, render_template, url_for, redirect, request
from flask_appbuilder.const import (
    LOGMSG_ERR_SEC_ACCESS_DENIED,
    FLAMSG_ERR_SEC_ACCESS_DENIED,
    PERMISSION_PREFIX
)
from flask_cache import Cache
from flask_appbuilder._compat import as_unicode
from flask_babel import gettext as __
import markdown as md
from past.builtins import basestring
from pydruid.utils.having import Having
from sqlalchemy import event, exc
from sqlalchemy.types import TypeDecorator, TEXT

logging.getLogger('MARKDOWN').setLevel(logging.INFO)

PY3K = sys.version_info >= (3, 0)
EPOCH = datetime(1970, 1, 1)
DTTM_ALIAS = '__timestamp'


class EmelemException(Exception):
    pass



def json_int_dttm_ser(obj):
    """json serializer that deals with dates"""
    val = base_json_conv(obj)
    if val is not None:
        return val
    if isinstance(obj, datetime):
        obj = datetime_to_epoch(obj)
    elif isinstance(obj, date):
        obj = (obj - EPOCH.date()).total_seconds() * 1000
    else:
        raise TypeError(
            "Unserializable object {} of type {}".format(obj, type(obj))
        )
    return obj


def json_iso_dttm_ser(obj):
    """
    json serializer that deals with dates

    >>> dttm = datetime(1970, 1, 1)
    >>> json.dumps({'dttm': dttm}, default=json_iso_dttm_ser)
    '{"dttm": "1970-01-01T00:00:00"}'
    """
    val = base_json_conv(obj)
    if val is not None:
        return val
    if isinstance(obj, datetime):
        obj = obj.isoformat()
    elif isinstance(obj, date):
        obj = obj.isoformat()
    elif isinstance(obj, time):
        obj = obj.isoformat()
    else:
        raise TypeError(
            "Unserializable object {} of type {}".format(obj, type(obj))
        )
    return obj


def markdown(s, markup_wrap=False):
    s = md.markdown(s or '', [
        'markdown.extensions.tables',
        'markdown.extensions.fenced_code',
        'markdown.extensions.codehilite',
    ])
    if markup_wrap:
        s = Markup(s)
    return s
