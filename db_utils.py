from sqlalchemy import create_engine, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///store.db')

Base = declarative_base()

class Image(Base):
    __tablename__ = 'images'
    id = Column(Integer, primary_key = True)
    name = Column(String)
    
    def __init__(self, name):
        self.name = name
        
    def __repr__(self):
        return "<Image('%s')>" % (self.name)
        
class Group(Base):
    __tablename__ = 'groups'
    id = Column(Integer, primary_key = True)
    name = Column(String)
    
    def __init__(self, name):
        self.name = name
        
    def __repr__(self):
        return "<Group('%s')>" % (self.name)
        
metadata = Base.metadata
metadata.create_all(engine)

Session = sessionmaker(bind = engine)
image = Image('Hello')
session = Session()
session.add(image)
session.commit()

t = session.query(Image).order_by(Image.id)
print (t)
