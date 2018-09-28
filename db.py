from sqlalchemy import Column, Integer, Sequence
from sqlalchemy.dialects.postgresql import REAL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.sql import func
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import datetime
from pandas import read_sql
from os.path import join
from os import getcwd

Base = declarative_base()

from sqlalchemy.sql import expression
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.types import DateTime

class utcnow(expression.FunctionElement):
    type = DateTime()

@compiles(utcnow, 'postgresql')
def pg_utcnow(element, compiler, **kw):
    return "TIMEZONE('utc', CURRENT_TIMESTAMP)"

class Measurements(Base):
    __tablename__ = 'Measurements'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, Sequence('id_Measurements'), primary_key=True)
    temperature = Column(REAL(precision=1), nullable=False)
    humidity = Column(REAL(precision=1), nullable=False)
    luminosity = Column(REAL(precision=1), nullable=False)
    date = Column(DateTime(), server_default=utcnow())

class Db():
    def __init__(self,url):
        # self.Base = declarative_base()

        self.engine = create_engine(url)
        #initialisation de la base
        Base.metadata.create_all(self.engine)

        # Bind the engine to the metadata of the Base class so that the
        # declaratives can be accessed through a DBSession instance
        Base.metadata.bind = self.engine

        DBSession = sessionmaker(bind=self.engine)
        # A DBSession() instance establishes all conversations with the database
        # and represents a "staging zone" for all the objects loaded into the
        # database session object. Any change made against the objects in the
        # session won't be persisted into the database until you call
        # session.commit(). If you're not happy about the changes, you can
        # revert all of them back to the last commit by calling
        # session.rollback()
        self.session = DBSession()

    def add(self,temperature,humidity,luminosity):
        new = Measurements(temperature=temperature,humidity=humidity,luminosity=luminosity)
        self.session.add(new)
        self.session.commit()

    def rb(self):
        self.session.rollback()

    def all(self):
        return read_sql(self.session.query(Measurements).statement,self.session.bind)

    def since(self,delta):
        t1 = datetime.datetime.utcnow().replace(microsecond=0) - datetime.timedelta(minutes=5)
        query = self.session.query(Measurements).filter(Measurements.date >= t1)
        return read_sql(query.statement,self.session.bind)

    def last(self):
        return read_sql(self.session.query(Measurements).order_by(Measurements.id).first(),self.session.bind)

instance = Db('postgresql://pi:raspberry@192.168.1.45:5432/measurements')