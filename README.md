# Item Catalog

This is an item catalog web application built as a project for the Udacity Full Stack Web Developer Nanodegree.

# Modules, Libraries and APIs
## Twitter Bootstrap v4 Alpha: CSS Framework for creating responsive views
## SQLAlchemy: Python ORM for interfacing with SQLite database
## Flask: Python microframework for routing web requests
## Jinja2: HTML Templating framework built into Flask

* __database__ - Handles SQAlchemy database sessions, interface between database controller and models
    * __create.py__ - Creates new entities in models
    * __get.py__ - Retrieves existing entities from models
    * __update.py__ - Makes changes to existing entities in models
    * __delete.py__ - Deletes entities from database models
    * __database_helpers.py__ - Helpers for text, list, and api operations used in all database functions
* __helpers__ - Contains helper file for HTTP operations in application controller
    * __http_helpers.py__ - Helpers for parsing url and form data, and data manipulation for front-end display
* __static__ - CSS and JavaScript Files, names correspond to .html view files
    * __js__ - Javascript files
        * __artist_create.js__ - AJAX functions and dynamic html functions used when adding artists to database
    * __artist.create.css__ - Styles used when creating artists
    * __artist.css__ - Styles specific to viewing an individual artist
    * __genre.css__ - Styles specific to viewing an individual genre
    * __styles.css__ - Main css file, applies to all pages
* __templates__ - Contains all Jinja2 HTML templates
    * __artist.html__ - HTML view for a specific artist
    * __artist_create.html__ - HTML view for artist creation
    * __artist_delete.html__ - HTML view for artist deletion
    * __artist_edit.html__ - HTML view for artist updating
    * __base.html__ - Base HTML view, all other views inherit from this base
    * __catalog.html__ - HTML view for catalog homepage
    * __genre.html__ - HTML view for a specific genre
    * __genre_create.html__ - HTML view for genre creation
    * __genre_delete.html__ - HTML view for genre deletion
    * __genre_edit.html__ - HTML view for genre edits
    * __login.html__ - HTML view for user login/logout
    * __user.html__ - HTML view for a user's profile page
* api_keys.py - IMPORTANT: This file must be created




name of the projects and all sub-modules and libraries (sometimes they are named different and very confusing to new users)
descriptions of all the project, and all sub-modules and libraries
5-line code snippet on how its used (if it's a library)
copyright and licensing information (or "Read LICENSE")
instruction to grab the documentation
instructions to install, configure, and to run the programs
instruction to grab the latest code and detailed instructions to build it (or quick overview and "Read INSTALL")
list of authors or "Read AUTHORS"
instructions to submit bugs, feature requests, submit patches, join mailing list, get announcements, or join the user or dev community in other forms
other contact info (email address, website, company name, address, etc)
a brief history if it's a replacement or a fork of something else
legal notices (crypto stuff)