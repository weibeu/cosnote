# Cosnote
A minimal web application for taking notes, built using Python Flask, ReactJS and uses MongoDB.
 

## Getting Started

Clone the project or optionally clone its fork if you wish to. [Install MongoDB](https://www.mongodb.com/try/download) on your system with minimal or default configurations.

Use the following reference to finally setup the project.

```shell script
$ git clone git@github.com:thec0sm0s/cosnote.git
$ cd cosnote
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

Cosnote provides minimal REST API. Any types of client may utilize it to provide native user experience. There is web client implemented over this API which is served as default with the application.

Make sure you have NodeJS installed and properly configured to your path before proceeding.

```shell script
$ git clone git@https://github.com/thec0sm0s/cosnote-react.git
$ cd cosnote-react
$ npm install

# Debug the application with hot reload.
$ npm run dev

# Make the production ready build.
$ npm run build

# Copy the build files to Flask cosnote server
$ mv cosnote-react/build/static/* cosnote/app/static/
$ mv cosnote-react/build/* cosnote/app/templates/
```

## API Endpoints

Minimal documentation of all API endpoints. To try out the API you may make use of this [Postman Collection](https://www.getpostman.com/collections/d6511a6f788cb9dc250c).

- **API BASE ROUTE:** `/api`
- **Content-Type** `application/json`

### Authorization


#### POST `/register/`

Registers a new user and returns the partial user object.

```json
{
    "username": "thecosmos",
    "password": "My.Very>Reallysecurepassword.F",
    "email": "tc@thecosmos.space"
}
```

#### POST `/authorize/`

Authorizes or logs in the user with provided credentials.

```json
{
    "username": "thecosmos",
    "password": "My.Very>Reallysecurepassword.F"
}
```

#### POST `/revoke/`

Revokes the authorization of current user.


#### POST `/notes/`

Creates or updates an existing note based on if the note ID is specified.

- **Create**
```json
{
    "title": "The meaning of life.",
    "content": "print(42)",
    "metadata": {
        "language": "python"
    }
}
```

- **Update**
```json
{
    "title": "The meaning of life.",
    "content": "console.log(42);",
    "metadata": {
        "language": "javascript",
        "shared": true
    },
    "id": "5f8311a767104fd7399d93cc"
}
```

#### GET `/notes/`

Returns list of all note objects of the current user.

#### GET `/note/note_id/`

Returns note object of a specific note.

```json
{
    "title": "The meaning of life.",
    "content": "console.log(42);",
    "metadata": {
        "language": "javascript",
        "shared": true
    },
    "id": "5f8311a767104fd7399d93cc"
}
```

#### GET `/notes/shared/note_id/`

Returns the note object with specified note ID only **if it has been shared**. This endpoint is open and doesn't requires authorization.

```json
{
    "title": "The meaning of life.",
    "content": "console.log(42);",
    "metadata": {
        "language": "javascript",
        "shared": true
    },
    "id": "5f8311a767104fd7399d93cc"
}
```

#### GET `/supported-languages/`

Basically returns list of all possible languages supported by the API.
