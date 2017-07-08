"""A collection of ORM sqlalchemy models for Emelem"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from datetime import datetime, date
import textwrap
import enum
import os

from flask import Markup, url_for
from flask_appbuilder import Model
from flask_appbuilder.models.mixins import AuditMixin, FileColumn
from flask_appbuilder.filemanager import get_file_original_name
from flask_appbuilder.models.decorators import renders

from emelem import app, db
config = app.config

import sqlalchemy as sqla
from sqlalchemy import (
    Column, Integer, String, ForeignKey, Text, Boolean,
    DateTime, Date, Table, Enum, 
    create_engine, MetaData, select
)
from sqlalchemy.orm import backref, relationship

# class EmelemModels(enum.Enum):
#     spark = 'spark'
#     sklearn = 'sklearn'

class MLMType(Model):
    __tablename__ = 'mlmtype'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    def __repr__(self):
        return self.name

    
class Project(AuditMixin, Model):
    __tablename__ = 'project'
    id = Column(Integer, primary_key=True)
    name = Column(String(150), unique=True, nullable=False)
    def __repr__(self):
        return self.name

    
class MLMCategory(Model):
    __tablename__ = 'mlmcategory'
    id = Column(Integer, primary_key=True)
    name = Column(String(150), unique=True, nullable=False)
    def __repr__(self):
        return self.name

    
class Tag(AuditMixin, Model):
    __tablename__ = 'tag'
    id = Column(Integer, primary_key=True)
    name = Column(String(150), unique=True, nullable=False)
    def __repr__(self):
        return self.name

    
tags_mlms = Table('tags_mlms', Model.metadata,
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
    db.Column('mlm_id', db.Integer, db.ForeignKey('mlm.id'))
)


projects_mlms = Table('project_mlms', Model.metadata,
    db.Column('project_id', db.Integer, db.ForeignKey('project.id')),
    db.Column('mlm_id', db.Integer, db.ForeignKey('mlm.id'))
)

    
class MLM(Model, AuditMixin):
    """ A machine learning model """
    __tablename__ = 'mlm'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    type_id = Column(Integer, ForeignKey('mlmtype.id'), nullable=False)
    params =  Column(Text)
    type = relationship(
        'MLMType',
        foreign_keys=[type_id],
        backref=backref('queries', cascade='all, delete-orphan')
    )
    file = Column(FileColumn())
    tags = relationship('Tag',
                        secondary=tags_mlms,
                        backref=backref('mlm', lazy='dynamic'))
    projects = db.relationship('Project', secondary=projects_mlms,
                               backref=db.backref('mlm', lazy='dynamic'))
        
    #mlm_file = relationship('MLMFile', uselist=False, back_populates='mlm') 
    # mlm_file_id = Column(Integer, ForeignKey('mlmfile.id'), nullable=False)
    # mlm_file = relationship(
    #     'MLMFile',
    #     foreign_keys=[mlm_file_id],
    #     backref=backref('queries', cascade='all, delete-orphan')
    # )
 
    def __repr__(self):
        return self.name

    # def download(self):
    #     return Markup(
    #         '<a href="' + url_for('MLMModelView.download', filename=os.path.join(config['UPLOAD_FOLDER'],str(self.file))) + '">Download</a>')

    def file_name(self):
        return '<a href="' + url_for('Emelem.download', filename=str(self.file)) + '">' + get_file_original_name(str(self.file)) + '</a>' 


# class MLMFile(Model):
#     __tablename__ = "mlmfile"
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     file = Column(FileColumn(), nullable=False)
#     name = Column(String(100), nullable=False, unique=True)
#     #filename = Column(String(100), nullable=False)
#     description = Column(String(150))
#     #mlm_id = Column(Integer, ForeignKey('mlm.id'))
#     #mlm = relationship("MLM", back_populates='mlm_file')

#     # @renders('name')
#     # def filename(self):
#     #     # will render this columns as bold on ListWidget
#     #     return Markup('<b>' + name + '</b>')

#     def download(self):
#         return Markup(
#             '<a href="' + url_for('MLMFileModelView.download', filename=os.path.join(config['UPLOAD_FOLDER'],str(self.file))) + '">Download</a>')

#     def file_name(self):
#         return get_file_original_name(str(self.file))
    
#     def __repr__(self):
#         return self.name
#         #return self.filename


    # def get_file_name(self):
    #     return get_file_original_name(os.path.join(config['EMELEM_MODEL_FOLDER'],str(self.file_name)))
    

    
# class Estimator(Model):
#     """ A machine learning estimator """
#     __tablename__ = 'estimator'
#     id = Column(Integer, primary_key=True)
#     estimator_name = Column(String(100))
#     #est_type = Column(Enum('Transformer','Estimator'))
#     def transform(dataset, params):
#         datasource_id = Column(Integer)
#         datasource_type = Column(String(200))
    
#     def __repr__(self):
#         return self.estimator_name


# class Dataset(Model):
#     """ A dataset """
#     id = Column(Integer, primary_key=True)
#     status_column_count
#     status_row_count
#     status_value_count
#     config_type sparse mutable
#     config_id name of the dataset
#     state 'ok'





class QueryStatus(object):
    """Enum-type class for query statuses"""

    STOPPED = 'stopped'
    FAILED = 'failed'
    PENDING = 'pending'
    RUNNING = 'running'
    SCHEDULED = 'scheduled'
    SUCCESS = 'success'
    TIMED_OUT = 'timed_out'
