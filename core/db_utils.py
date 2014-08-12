from sqlalchemy import create_engine, Column, Integer, String, MetaData, ForeignKey, MetaData, Table
from sqlalchemy.orm import sessionmaker, mapper
from entities import *

class DBUtil:

    def __init__(self, path):
        self._engine = create_engine('sqlite:///' + path + 'store.db')

        create_db(_engine)

    def insert_image(self, name, image_path):
        Session = sessionmaker(bind = _engine)
        image = Image(name, image_path)
        session = Session()
        session.add(image)
        session.commit()

        t = session.query(Image).order_by(Image.id)[0]
        print (t)

    def create_db(engine):
        metadata = MetaData()
        
        image_table = Table('image', metadata,
                            Column('id', Integer, primary_key = True),
                            Column('name', String)
        )
        
        group_table = Table('group', metadata, 
                            Column('id', Integer, primary_key = True),
                            Column('name', String)
        )

        image_group_table = Table('image_group', metadata, 
                                  Column('image_id', Integer, ForeignKey('image.id'), primary_key = True),
                                  Column('group_id', Integer, ForeignKey('group.id'), primary_key = True)
        )

        operation_type_table = Table('operation_type', metadata,
                                     Column('id', Integer, primary_key = True),
                                     Column('name', String)
        )

        operation_table = Table('operation', metadata, 
                                Column('id', Integer, primary_key = True),
                                Column('name', String),
                                Column('operation_type_id', Integer, ForeignKey('operation_type.id'))
        )

        operation_group_table = Table('operation_group', metadata, 
                                      Column('operation_id', Integer, ForeignKey('operation.id'), primary_key = True),
                                      Column('group_id', Integer, ForeignKey('group.id'), primary_key = True)
        )

        metadata.create_all(engine)
        mapper(Image, image_table)
        mapper(Group, group_table)
        mapper(ImageGroup, image_group_table)
        mapper(OperationType, operation_type_table)
        mapper(Operation, operation_table)
        mapper(OperationGroup, operation_group_table)


