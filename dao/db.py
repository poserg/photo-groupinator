from sqlalchemy import create_engine, Column, Integer, String, \
     MetaData, ForeignKey, MetaData, Table, DateTime
from sqlalchemy.orm import sessionmaker, mapper
from entities import *

from sys import path as sys_path
sys_path.append('../')

from util.fs_util import mkdir

import logging

from datetime import datetime

logging.basicConfig(format = u'%(filename)s[LINE:%(lineno)d]# \
%(levelname)-8s [%(asctime)s]  %(message)s', level = logging.DEBUG)

class DBUtil:

    def __init__(self, path):
        logging.info("DB path = " + path)
        self._engine = create_engine('sqlite:///' + mkdir(path) +
                                     '/store.db')
        self.Session = sessionmaker(bind = self._engine)
        Base.metadata.create_all(self._engine)

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

    def create_group(self, name):
        logging.info("Create group")
        session = self.Session()
        group = Group(name)
        session.add(group)
        session.commit()
        return group.id
