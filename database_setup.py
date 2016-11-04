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
        * emergence: Str, Aproximate date when
            genre emerged in history
        * created: Str, time genre created in database
        * updated: Str, last update time in database,
            defaults to datetime.utcnow """
    __tablename__ = 'genre'

    gen_id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    emergence = Column(String(100))
    created = Column(String(100))
    updated = Column(String(100), default=datetime.datetime.utcnow)


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
    parent = Column(Integer, ForeignKey('genre.gen_id'), nullable=False)
    child = Column(Integer, ForeignKey('genre.gen_id'), nullable=False)


class Artist(Base):

    """ Database table for music artist
    This table will store information related to specific artists

    Columns:
        * (PRIMARY) art_id: Int, database id for artist
        * (REQ) name: Str, text name of artist
        * (REQ) url_name: Str, artist's name as it appears in a URL
        * emergence: Str, aproximate date when artist began playing music
        * (REQ) created: Str, time created in database, set to datetime.utcnow
            when creating an artist in DB"""
    __tablename__ = 'artist'

    art_id = Column(Integer, primary_key=True)
    name = Column(String(300), nullable=False)
    url_name = Column(String(3000), nullable=False)
    emergence = Column(String(100))
    created = Column(String(100), nullable=False)
    updated = Column(String(100), default=datetime.datetime.utcnow)


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

    artist = Column(Integer, ForeignKey('artist.art_id'), primary_key=True)
    rank = Column(Integer, nullable=False, primary_key=True)
    name = Column(String(300), nullable=False)
    url = Column(String(250))

class ArtistGenre(Base):

    """ Database table to list all relevant genres to a specific artist
    This table will contain a single row for every genre that is relevant
    to a specific artist.

    Columns:
        * (REQ) artist: Int, database id for artist
        * (REQ) genre: Int, database id for genre """
    __tablename__ = 'artistgenre'

    artist = Column(Integer, ForeignKey('artist.art_id'), primary_key=True)
    genre = Column(Integer, ForeignKey('genre.gen_id'), primary_key=True)

engine = create_engine('sqlite:///catalog.db')

Base.metadata.create_all(engine)
