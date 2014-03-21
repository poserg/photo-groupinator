from sqlalchemy import create_engine, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///store.db')

Base = declarative_base()

class Image(Base):
    __tablename__ = 'image'
    id = Column(Integer, primary_key = True)
    name = Column(String)
    
    def __init__(self, name):
        self.name = name
        
    def __repr__(self):
        return "<Image('%s')>" % (self.name)
        
class Group(Base):
    __tablename__ = 'group'
    id = Column(Integer, primary_key = True)
    name = Column(String)
    
    def __init__(self, name):
        self.name = name
        
    def __repr__(self):
        return "<Group('%s')>" % (self.name)

class ImageGroup(Base):
    __tablename__ = 'image_group'
    image_id = Column(Integer, ForeignKey('image.id'), primary_key = True)
    group_id = Column(Integer, ForeignKey('group.id'), primary_key = True)

    def __init__(self, image_id, group_id):
        self.image_id = image_id
        self.group_id = group_id

class OperationType(Base):
    __tablename__ = 'operation_type'
    id = Column(Integer, primary_key = True)
    name = Column(String)

    def __init__(self, name):
        self.name = name

class Operation(Base):
    __tablename__ = 'operation'
    id = Column(Integer, primary_key = True)
    name = Column(String)
    operation_type_id = Column(Integer, ForeignKey('operation_type.id'))

    def __init__(self, name, operation_type_id):
        pass

class OperationGroup(Base):
    __tablename__ = 'operation_group'
    operation_id = Column(Integer, ForeignKey('operation.id'), primary_key = True)
    group_id = Column(Integer, ForeignKey('group.id'), primary_key = True)

    def __init__(self, operation_id, group_id):
        self.operation_id = operation_id
        self.group_id = group_id

metadata = Base.metadata
metadata.create_all(engine)

Session = sessionmaker(bind = engine)
image = Image('Hello')
session = Session()
session.add(image)
session.commit()

t = session.query(Image).order_by(Image.id)
print (t)
