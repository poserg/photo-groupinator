from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relation, relationship, backref
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime

Base = declarative_base()

class ImageGroup(Base):
    __tablename__ = 'image_group'

    image_id=Column(Integer, ForeignKey('image.id'), primary_key = True)
    group_id = Column(Integer, ForeignKey('group.id'), primary_key = True)
    
    def __init__(self, image_id, group_id):
        self.image_id = image_id
        self.group_id = group_id

        
class Image(Base):
    __tablename__ = 'image'
    
    id = Column(Integer, primary_key = True)
    name = Column(String)
    create_date = Column(String)
    groups = relationship('ImageGroup')

    def __init__(self, name, create_date):
        self.name = name
        self.create_date = create_date
        
    def __repr__(self):
        return "<Image('%s', '%s')>" % (self.name, self.create_date)

    @property
    def serialize(self):
        """Returns object data in easily serializeable format"""
        return {"id" : self.id,
                "name" : self.name,
                "create_date" : self.create_date
        }
        
class Group(Base):
    __tablename__ = 'group'

    id = Column(Integer, primary_key = True)
    name = Column(String)
    images = relationship('ImageGroup')
    operations = relationship('OperationGroup',
                              order_by='OperationGroup.sort_index')

    def __init__(self, name):
        self.name = name
    
    def __repr__(self):
        return "<Group('%s')>" % (self.name)

    @property
    def serialize(self):
        return {"id" : self.id,
                "name" : self.name
        }

class OperationType(Base):
    __tablename__ = 'operation_type'
    # :TODO May be String?
    id = Column(Integer, primary_key = True)
    name = Column(String)

    def __init__(self, name):
        self.name = name

class Operation(Base):
    __tablename__ = 'operation'

    id = Column(Integer, primary_key = True)
    name = Column(String)
    operation_type_id = Column(Integer, ForeignKey('operation_type.id'))
    operation_type = relation('OperationType')
    
    def __init__(self, name, operation_type_id):
        pass

class OperationGroup(Base):
    __tablename__ = 'operation_group'

    operation_id = Column(Integer, ForeignKey('operation.id'),
                          primary_key = True)
    group_id = Column(Integer, ForeignKey('group.id'),
                      primary_key = True)
    sort_index = Column(Integer, default=0)

    def __init__(self, operation_id, group_id, sort_index):
        self.operation_id = operation_id
        self.group_id = group_id
        self.sort_index = sort_index

if __name__ == "__main__":
    engine = create_engine('sqlite:///store.db', echo = True)
    Base.metadata.create_all(engine)
