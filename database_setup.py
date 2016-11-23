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


class User(Base):
    """ Database table for a user

    Columns:
        * (REQ) name: Str, user's full name
        * (REQ) email: Str, user's email address
        * (REQ) picture: Str, URL for user's picture
        * (PRIMARY) user_id: Int, database ID for user
    """
    __tablename__ = 'user'

    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    picture = Column(String(500), nullable=False)
    user_id = Column(Integer, primary_key=True)

    @property
    def serialize(self):
        # Returns object in easily serializable format
        return {
            'name': self.name,
            'email': self.email,
            'picture': self.picture,
            'user_id': self.user_id
        }

class Genre(Base):

    """ Database table for music genres

    Columns:
        * (PRIMARY) gen_id: Int, database id for genre
        * (REQ) name: Str, text name of genre
        * (REQ) url_name: Str, url-friendly name of genre
        * created: Str, time genre created in database
        * updated: Str, last update time in database,
            defaults to datetime.utcnow """
    __tablename__ = 'genre'

    gen_id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    url_name = Column(String(100), nullable=False, unique=True)
    created = Column(String(100))
    updated = Column(String(100), default=datetime.datetime.utcnow)
    user = Column(Integer, ForeignKey('user.user_id'), nullable=False)

    @property
    def serialize(self):
        # Returns object in easily serializable format
        return {
            'name': self.name,
            'url_name': self.url_name,
            'gen_id': self.gen_id,
            'created': self.created,
            'updated': self.updated
        }


class Influence(Base):

    """ Database table for music genre influences
    This table will track the influences between different genres.
    Each row representes an influence relationship from parent to child.

    Columns:
        * (REQ) parent: Int, database genre id for preceeding genre
        * (REQ) child: Int, database genre id for resulting genre """

    __tablename__ = 'influence'

    parent = Column(Integer, ForeignKey('genre.gen_id'), primary_key=True)
    child = Column(Integer, ForeignKey('genre.gen_id'), primary_key=True)

    @property
    def serialize(self):
        # Returns object in easily serializable format
        return {
            'parent': self.parent,
            'child': self.child
        }


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
    spotify_id = Column(String(50), unique=True)
    name = Column(String(300), nullable=False)
    url_name = Column(String(300), nullable=False, unique=True)
    created = Column(String(100), nullable=False)
    updated = Column(String(100), default=datetime.datetime.utcnow)
    user = Column(Integer, ForeignKey('user.user_id'), nullable=False)

    @property
    def serialize(self):
        # Returns object in easily serializable format
        return {
            'name': self.name,
            'url_name': self.url_name,
            'spotify_id': self.spotify_id,
            'art_id': self.art_id,
            'created': self.created,
            'updated': self.updated
        }


class TopSongs(Base):

    """ Database table for an artist's top songs
    This table will store the listing of an artist's most popular song titles.
    It will also contain links youtube links where the song can be streamed.

    Columns:
        * (REQ) artist: Int, database id for artist
        * (REQ) rank: Int, relative rank of song
        * (REQ) name: Str, Text name of song
        * youtube_id: Str, Youtube URL of song video """
    __tablename__ = 'topsongs'

    artist = Column(Integer, ForeignKey('artist.art_id'), primary_key=True)
    rank = Column(Integer, nullable=False, primary_key=True)
    name = Column(String(300), nullable=False)
    youtube_id = Column(String(50))

    @property
    def serialize(self):
        # Returns object in easily serializable format
        return {
            'name': self.name,
            'rank': self.rank,
            'artist': self.artist,
            'youtube_id': self.youtube_id
        }


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

    @property
    def serialize(self):
        # Returns object in easily serializable format
        return {
            'artist': self.artist,
            'genre': self.genre
        }

engine = create_engine('sqlite:///catalog.db')

Base.metadata.create_all(engine)
