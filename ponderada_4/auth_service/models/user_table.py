from sqlalchemy import Column, Integer, String, MetaData, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import DeclarativeBase

metadata = MetaData()
engine = create_engine("mysql+pymysql://admin:admin@database:3306/p3", 
                        pool_pre_ping=True, 
                        pool_recycle=3600
                    )

class Base(DeclarativeBase):
    pass 

class UserTable(Base):
    __tablename__ = "users"
    metadata
    id = Column(Integer,primary_key=True, autoincrement=True)
    email = Column(String(100), nullable=False)
    password = Column(String(100), nullable=False)

metadata.create_all(bind=engine, tables=[UserTable.__table__])

conn = engine.connect()