# Chatbot's structure

In this file will be described the project's structure and how to use or modify every component.

*Note: The root directory is `mynissan`, therefore every stated paths should be considered starting from here.*

## I. Root directory : mynissan

It contains, of course, all the folders used for the chatbot but it also has setup files :

* `README.md` is the main readme file (should be read first !)
* `manage.py` is django's manager, it is used for every prompt command you need to send
* `nltk_requirements.py` and `setup.py` are the requirements files, it helps you downloading every necessary librairies.
* `.flake8`, `.pre-commit` files, `mypy.ini` are linters files, to prevent commits that are not following our programming rules.

## II. Chatbot

It is a django app created into the project `mynissan`. It can be accessed via the url `/chatbot` and it contains :

* a `data` folder, with the description of every icons (it is directly found here, but it should be changed)
* the `features` folder, that is containing all features added to the chatbot (image analysis, qsearch, sentiment analysis...)
* a `rules` folder, containing a `.json` file to detect the user's intents for now, but this is meant to be changed.
* a `templates` folder that has... templates for the web page (associated to the `.css` file contained in `static`)
* the file `chatbot.py`, representing a class that is instantiated and called everytime there is a request.
* the `models.py` file, with the two models that are used in this project : `Question` and `Video`.
* `urls.py`, just a file to indicate all the possible routes.
* `views.py`, which contains the logic of all the routes and links it to the chatbot.

## III. Database

The database folder is only here to easily access the files used to create and fill the database.

*Note: changing the `database.csv` file will not update the database !*

## IV. Docs

This is the folder with all the MarkDown files to give further explanations on the project.

## V. mynissan

This folder contains all the settings and urls for the django project.

## VI. Static folder

In this folder, there are two directories :

* `js`: it contains all the files to make asynchronous queries to the chatbot, with `chat.js`, as well as voice records handling with `dynamics.js`...
* `uploads`: it stores all the uploads, such as audios, produced by the chatbot or the user, and pictures sent by the user.