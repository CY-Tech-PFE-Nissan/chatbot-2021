# Setting up database

For now, this API calls a database set up on local device, make sure you have PostgreSQL server installed !
(This should be changed to directly communicate with Heroku's database)

## I. Set up PostgreSQL on your local device

Follow this link :
https://www.digitalocean.com/community/tutorials/how-to-install-and-use-postgresql-on-ubuntu-18-04

*Notes: you should create a user 'datamanager' that is able to access the database 'mynissan' that will be created in next section (follow this link : https://www.digitalocean.com/community/tutorials/how-to-use-postgresql-with-your-django-application-on-ubuntu-14-04)*

## II. Create the database on local

Once PostgreSQL is installed, you should run (in root directory) :

```sh
sudo -i -u postgres
```

Then, to create a database :

```sh
createdb mynissan
exit
```

This should create a database that your user will be allowed to access. Once this is done, connect to the database with the previously created user :

```sh
psql -d mynissan -U datamanager -h localhost
```

Then create the table in itself (by copy/pasting the code in 'mynissan/database/create_db.sql') and finally run

```sh
\copy chatbot_question(topic, sub_topic, video_title, question, answer, sequence_tree, topic_terms) from 'path_to_/mynissan/database/database.csv' DELIMITER ',' CSV HEADER;
```

Database is now filled up with all needed data.

## III. Notes

This database can be updated with the admin side of the site.
