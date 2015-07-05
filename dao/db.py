from sqlalchemy import create_engine, Column, Integer, String, \
     MetaData, ForeignKey, MetaData, Table, DateTime
from sqlalchemy.orm import sessionmaker, mapper
from entities import *

from sys import path as sys_path
sys_path.append('../')

from util.fs_util import mkdir

import logging

logging.basicConfig(format = u'%(filename)s[LINE:%(lineno)d]# \
%(levelname)-8s [%(asctime)s]  %(message)s', level = logging.DEBUG)

class DBUtil:

    def __init__(self, path):
        logging.info("DB path = " + path)
        self._engine = create_engine('sqlite:///' + mkdir(path) +
                                     '/store.db')
        self.Session = sessionmaker(bind = self._engine)
        self.map_objects()

    def insert_image(self, name, create_date):
        image = Image(name, create_date)
        #logging.info("Insert image: " + image.serialize())
        session = self.Session()
        session.add(image)
        session.commit()

        t = session.query(Image).order_by(Image.id)[0]
        print t

    def create_db(self):
        self.metadata.create_all(self._engine)

    def get_image_by_id(self, id):
        logging.info("Get image by id = " + str(id))
        session = self.Session()
        return session.query(Image).filter(Image.id == id).first()

    def get_images(self):
        logging.info("Get all images")
        session = self.Session()
        return session.query(Image).all()

    def get_group_by_id(self, id):
        logging.info("Get groups by id = " + str(id))
        session = self.Session()
        return session.query(Group).filter(Group.id == id).first()
        
    def get_groups(self):
        logging.info("Get all groups")
        session = self.Session()
        return session.query(Group).all()

    def map_objects(self):
        self.metadata = MetaData()
        
        image_table = Table('image', self.metadata,
                            Column('id', Integer, primary_key = True),
                            Column('name', String),
                            Column('create_date', String)
        )
        
        group_table = Table('group', self.metadata, 
                            Column('id', Integer, primary_key = True),
                            Column('name', String)
        )

        image_group_table = Table('image_group', self.metadata, 
                                  Column('image_id', Integer,
                                         ForeignKey('image.id'),
                                         primary_key = True),
                                  Column('group_id', Integer,
                                         ForeignKey('group.id'),
                                         primary_key = True)
        )

        operation_type_table = Table('operation_type', self.metadata,
                                     Column('id', Integer, primary_key = True),
                                     Column('name', String)
        )

        operation_table = Table('operation', self.metadata, 
                                Column('id', Integer, primary_key = True),
                                Column('name', String),
                                Column('operation_type_id', Integer,
                                       ForeignKey('operation_type.id'))
        )

        operation_group_table = Table('operation_group', self.metadata, 
                                      Column('operation_id', Integer,
                                             ForeignKey('operation.id'),
                                             primary_key = True),
                                      Column('group_id', Integer,
                                             ForeignKey('group.id'),
                                             primary_key = True),
                                      Column('sort_index', Integer,
                                             default=0)
        )

        mapper(Image, image_table)
        mapper(Group, group_table)
        mapper(ImageGroup, image_group_table)
        mapper(OperationType, operation_type_table)
        mapper(Operation, operation_table)
        mapper(OperationGroup, operation_group_table)
