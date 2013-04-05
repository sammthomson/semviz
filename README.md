SemViz
======

A web demo for visualizing Semafor parses

Uses [Flask](http://flask.pocoo.org/) as the web server.
Python requirements are in `requirements.txt`

To compile Coffeescripts:

    coffee --watch --compile --output semviz/static/js/compiled/ semviz/static/coffeescripts/

Coffeescript tests require
[jasmine-node](https://github.com/mhevery/jasmine-node).
To run:

    jasmine-node --coffee semviz/static/spec

Stylesheets use [Sass](http://sass-lang.com/).
To compile:

    sass --watch semviz/static/css/style.scss:semviz/static/css/style.css

Make sure `semviz.settings.SEMAFOR_HOME` points to a valid installation of
SEMAFOR (>= v3.0-alpha-03).

Make sure SEMAFOR is running in server mode:

    cd $SEMAFOR_HOME
    java -Xms4g -Xmx4g -jar target/Semafor-3.0-alpha-03.jar model-dir:<directory-of-trained-model> port:4444

and  `semviz.settings.SEMAFOR_HOST` and `semviz.settings.SEMAFOR_PORT` point to the running instance.

To start the (development) server:

    ./semviz/web_app.py
