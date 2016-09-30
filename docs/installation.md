## Installation
This section guides you through the steps needed to get *ner-tagger* to work in a development environment.

*Ner-tagger* requires python 3.4 and postgres 9.5.
So first, install python, postgres and create a new database *nertagger*.

Download *ner-tagger* from *github*:

    $ git clone https://github.com/estnltk/ner-tagger
    $ cd ner-tagger

Install bootstrap:

    $ python bootstrap.py

Create a configuration file with the database connection parameters.
Use *conf/dev.cnf* as a template.
Next, specify a full path to the configuration file in *buildout-development.cfg*.

    initialization =
        import os
        os.environ['CONFIG'] = 'path to configuration file'

Install an application and dependencies:

    $ ./bin/buildout -c buildout-development.cfg

Setup a database schema:

    $ ./bin/django migrate
    $ ./bin/django migrate makemigrations ui
    $ ./bin/django migrate ui

Create a super-user:

    $ ./bin/django createsuperuser

Import a demo corpus:

    $ ./bin/django import_corpus "corpus-name" data/demo-corpus.csv

Run a development server:

    $ ./bin/django runserver

So far, you can login to *http://localhost:8000/admin* and inspect the imported corpus.
Now, lets create a new user and assign him a corpus for annotation.
First, go to *http://localhost:8000/admin/auth/user* and add a new user.
Next, assign the corpus:

    $ ./bin/django assign_corpus "user-name" "corpus-name"

Now, you can login with the newly created user to *http://localhost:8000/* and start annotating the corpus.

## Production installation

Prerequisites: python3.4, Apache 2.4, mod_wsgi and postgres 9.5.

See [instructions](production.md) on production environment setup.

Download *Ner-tagger*:

    $ git clone https://github.com/estnltk/ner-tagger
    $ cd ner-tagger

Setup bootstrap:

    $ python bootstrap.py

Create a configuration file with the database connection properties.
Use *conf/prod.cnf* as a template.
Next, specify a full path to the configuration file in *buildout-production.cfg*.

Install an application and dependencies:

    $ ./bin/buildout -c buildout-production.cfg

Edit app settings at *nertagger/settings/prod.conf* and Apache configuration file *nertagger/settings/nertagger.conf* as required.
Then copy *nertagger/settings/nertagger.conf* to */etc/httpd/conf.d/*.

Setup a database schema:

    $ ./bin/django migrate
    $ ./bin/django migrate makemigrations ui
    $ ./bin/django migrate ui

Copy static files to a apache webroot directory:

    $ ./bin/django collectstatic

Start Apache:

    $ service apachectl start

Ner-tagger should now be available at *http://yourhost:80/*.

Next, follow the steps in section [Getting Started](#getting-started) to create users, import a corpus, etc.
