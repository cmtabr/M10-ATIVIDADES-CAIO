from sqlalchemy import create_engine, MetaData, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
import datetime

# Conexão com o banco de dados
engine = create_engine("mysql+pymysql://admin:admin@database:3306/banco", pool_pre_ping=True, pool_recycle=3600)
metadata = MetaData()
Base = declarative_base()

# Tabela de usuários
class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    email = Column(String(50))
    password = Column(String(50))
    created_at = Column(DateTime, default=datetime.datetime.now())

# Tabela de to-do
class Todos(Base):
    __tablename__ = 'todos'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(50))
    description = Column(String(50))
    done = Column(Integer)
    user_id = Column(Integer)
    created_at = Column(DateTime, default=datetime.datetime.now())

# Criação do banco de dados
metadata.create_all(bind=engine, tables=[Users.__table__, Todos.__table__])

# Sessão do banco de dados
session = Session(bind=engine)

# Sessão do banco de dados
conn = engine.connect()