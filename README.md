# instant-notes
A minimal web application for taking notes, built using Python Flask, ReactJS and uses MongoDB.
 
See also [instant-notes-web](https://github.com/thec0sm0s/instant-notes-web).

## Prerequisites
A working Mongo DB setup
## Getting Started
Copy `sample-config.py` and fill in `SECRET_KEY`. Set the `MONGO_URI` if needed (generally you don't need to.)

Set the `INSTANT_NOTES_CONFIG` environment variable to the name of the file you copied. Already set when using PyCharm.
 
## Running
The easiest way to run/debug instant-notes is with PyCharm as there is already a run config added. 
Otherwise use `python wsgi.py` to run instant-notes locally.
