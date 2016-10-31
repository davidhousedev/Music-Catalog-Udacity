import sys
import datetime
from sqlalchemy import Column, ForeignKey, Integer, String

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import relationship

from sqlalchemy import create_engine

Base = declarative_base()


class Genre(Base):
    __tablename__ = 'genre'

    gen_id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    emergence = Column(Date)
    created = Column(DateTime)
    updated = Column(DateTime, default=datetime.datetime.utcnow)


class Influence(Base):
    __tablename__ = 'influence'

    inf_id = Column(Integer, primary_key=True)
    parent = Column(Integer, ForeignKey('genre.id'))
    child = Column(Integer, ForeignKey('genre.id'))


class Artist(Base):
    __tablename__ = 'artist'

    art_id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    emergence = Column(Date)
    created = Column(DateTime)
    updated = Column(DateTime, default=datetime.datetime.utcnow)


class TopSongs(Base):
    __tablename__ = 'topsongs'

    artist = Column(Integer, ForeignKey('artist.id'))
    rank = Column(Integer, nullable=False)
    name = Column(String(100), nullable=False)
    url = Column(String(250))

engine = create_engine('sqlite:///catalog.db')

Base.metadata.create_all(engine)
