from flask import Flask, url_for, render_template, request,
from flask import redirect, flash, jsonify

# Initializes python shell to interface with database
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Artist, ArtistGenre, Genre, Influence, TopSongs

# Connect to database
engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

# Establish database connection session
DBSession = sessionmaker(bind=engine)
session = DBSession()

app = Flask(__name__)


# Routes go here


if __name__ == '__main__':
    app.secret_key = 'turtles'  # TODO: Change me for production
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
