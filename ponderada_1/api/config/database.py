from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base 

engine = create_engine("mysql+pymysql://admin:admin@database:3306/banco", pool_pre_ping=True, pool_recycle=3600)

metadata = MetaData()
base = declarative_base()

conn = engine.connect()