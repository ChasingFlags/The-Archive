from sqlalchemy.orm import (scoped_session, relationship, sessionmaker)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import *
import os

basedir=os.getcwd()
engine=create_engine(f"sqlite:///{basedir}/dev.db")
session=scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base=declarative_base(bind=engine)
Base.query=session.query_property()

#Note class
class Notes(Base):
    __tablename__ = 'notes'
    id=Column(Integer, primary_key=True)
    title=Column(String(100))
    body=Column(Text)
    user_id=Column(Integer, ForeignKey('user.id'))
    user=relationship('User', back_populates="notes")

class FlagTable(Base):
    __tablename__ = 'flagtable'
    id = Column(Integer, primary_key=True)
    flag=Column(String(100))

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(100))
    last_name = Column(String(100))
    is_admin = Column(Boolean)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(200))
    notes=relationship('Notes', back_populates="user")

class Token(Base):
    __tablename__ = 'token'
    id = Column(Integer, primary_key=True)
    user = Column(String(100))
    access_token = Column(Text)
    refresh_token = Column(Text)