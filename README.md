# Music Catalog

This app curates a catalog of music artists, storing information about their most popular songs and displaying music videos corresponding to those songs. The app populates all artist metadata through calls to the Spotify API then to the Youtube API. Artist genre infromation is also derived from Spotify, and genres can be applied to both artists and to other genres (e.g. Rock => Alternative Rock or Hip Hop => West Coast Hip Hop). App views are fully responsive through use of Twitter Bootstrap v4 Alpha.

This catalog was created as a project for the Udacity Full Stack Nanodegree program. Original project specifications were expanded to include population of all data from API calls to Spotify and Youtube, and extensive responsive image handling.


# Libraries, APIs, and Modules

* Twitter Bootstrap v4 Alpha: CSS Framework for creating responsive views
* SQLAlchemy: Python ORM for interfacing with SQLite database
* Flask: Python microframework for routing web requests
* Jinja2: HTML Templating framework built into Flask

* Spotify - All artist and genre metadata is derived from the Spotify API
* Youtube - Youtube video ids are obtained through Google's Youtube API

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
* __api_keys.py__ - Defines constants used for Flask secure cookies and Google Signin. __IMPORTANT: See installation instructions for file configuration__.
* __application.py__ - Primary application file, contains HTTP handlers
* __database_controller.py__ - Controller for database operations, interfaces between HTTP handlers and model
* __database_setup.py__ - Contains Model class definitions __IMORTANT: Must be run using `python database_setup.py` before application can start__
* __requirements.txt__ - Allows for installation of required modules with the command `pip install -r requirements.txt` from application directory


# Requirements:
* __Python 2.7.x and pip__
* Active project in Google developer's console: __https://console.developers.google.com/__
    * Under Credentials, click the dropdown next to 'Create credentials' and select 'OAuth client ID'
* Active application with Facebook developer, Facebook Login product enabled: __https://developers.facebook.com/__


# Installation Instructions
1. Install Python 2.7.x and pip
2. Fork and clone repository to your local machine
3. In `templates/login.html` change `data-clientid` to equal your Google project's `client_id`
4. In main application diretory:
    1. Run `pip install -r requirements.txt` to install dependencies
    2. Edit __client_secrets.json__ with your Google project's `client_id`, `project_id`, and `client_secret`
    3. Edit __fb_client_secrets__ with your Facebook app's `app_id`, and `app_secret`
    4. (Optional) Add `*client_secrets.json` to your .gitignore to prevent private data from being uploaded to your git repository
    5. (Optional) Application is currently configured to run on Heroku, please contact for support on how to deploy the application to your own Heroku instance
    __5. Run `python application.py`__ to start the application locally


# Author

David A. House

davidhousedev@gmail.com

@davidhousedev


# Contact
For support and other inquiries, please contact me via e-mail or on Twitter
    Email: davidhousedev@gmail.com
    Twitter: @davidhousedev


# LICENSE
Copyright (c) 2016 David Alexander House

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

All data derived from Spotify and Youtube APIs subject to original respective copyright.