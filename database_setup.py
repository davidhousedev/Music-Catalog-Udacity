""" Database model for music catalog
Tables:
    * Genre: Each row corresponds to a specific genre or sub-genre
    * Influence: Each row denotes a one-way influence between music genres
    * Artist: Each row corresponds to a specific music artist
    * TopSongs: Each row corresponds to one song of an artist's top songs
"""

import sys
import datetime

# Initialize SQLalchemy database
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
Base = declarative_base()


class Genre(Base):

    """ Database table for music genres

    Columns:
        * (PRIMARY) gen_id: Int, database id for genre
        * (REQ) name: Str, text name of genre
        * emergence: Date, Aproximate date when
            genre emerged in history
        * created: DateTime, time genre created in database
        * updated: DateTime, last update time in database,
            defaults to datetime.utcnow """
    __tablename__ = 'genre'

    gen_id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    emergence = Column(Date)
    created = Column(DateTime)
    updated = Column(DateTime, default=datetime.datetime.utcnow)


class Influence(Base):

    """ Database table for music genre influences
    This table will track the influences between different genres.
    Each row representes an influence relationship from parent to child.

    Columns:
        * (PRIMARY) inf_id: Int, database id for influence
        * (REQ) parent: Int, database genre id for preceeding genre
        * (REQ) child: Int, database genre id for resulting genre """

    __tablename__ = 'influence'

    inf_id = Column(Integer, primary_key=True)
    parent = Column(Integer, ForeignKey('genre.id'), nullable=False)
    child = Column(Integer, ForeignKey('genre.id'), nullable=False)


class Artist(Base):

    """ Database table for music artist
    This table will store information related to specific artists

    Columns:
        * (PRIMARY) art_id: Int, database id for artist
        * (REQ) name: Str, text name of artist
        * emergence: Date, aproximate date when artist began playing music
        * (REQ) created: DateTime, time created in database, set to datetime.utcnow
            when creating an artist in DB"""
    __tablename__ = 'artist'

    art_id = Column(Integer, primary_key=True)
    name = Column(String(300), nullable=False)
    emergence = Column(Date)
    created = Column(DateTime, nullable=False)
    updated = Column(DateTime, default=datetime.datetime.utcnow)


class TopSongs(Base):

    """ Database table for an artist's top songs
    This table will store the listing of an artist's most popular song titles.
    It will also contain links youtube links where the song can be streamed.

    Columns:
        * (REQ) artist: Int, database id for artist
        * (REQ) rank: Int, relative rank of song
        * (REQ) name: Str, Text name of song
        * url: Str, Youtube URL of song video """
    __tablename__ = 'topsongs'

    artist = Column(Integer, ForeignKey('artist.id'))
    rank = Column(Integer, nullable=False)
    name = Column(String(300), nullable=False)
    url = Column(String(250))

# TODO: Add artist genre table
# TODO: Increase artist name length

engine = create_engine('sqlite:///catalog.db')

Base.metadata.create_all(engine)
