# instant-notes
A minimal web application for taking notes, built using Python Flask, ReactJS and uses MongoDB.
 

## Getting Started

Clone the project or optionally clone its fork if you wish to. [Install MongoDB](https://www.mongodb.com/try/download) on your system with minimal or default configurations.

Use the following reference to finally setup the project.

```shell script
$ git clone git@github.com:thec0sm0s/instant-notes.git
$ cd instant-notes
$ python3 -m venv venv

# For windows users.
$ cd venv/Scripts/
$ activate
$ cd ../../

# For linux users.
$ source venv/bin/activate

$ pip install -r requirements.txt
```

Create a new `.env` file in the project root similar to [`.env.example`](.env.example) and configure the application secrets and variables.

```shell script
# Run the application.
$ python wsgi.py
``` 

## Manually building the ReactJS frontend.

Instant notes provides minimal REST API. Any types of client may utilize it to provide native user experience. There is web client implemented over this API which is served as default with the application.

Make sure you have NodeJS installed and properly configured to your path before proceeding.

```shell script
$ git clone git@github.com:thec0sm0s/instant-notes-web.git
$ cd instant-notes-web
$ npm install

# Debug the application with hot reload.
$ npm run dev

# Make the production ready build.
$ npm run build

# Copy the build files to Flask instant-notes server
$ mv instant-notes-web/build/static/* instant-notes/app/static/
$ mv instant-notes-web/build/* instant-notes/app/templates/
```
