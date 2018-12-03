# Mastermind API

REST API that simulates the role of Mastermind's codemaker.

[Mastermind](https://en.wikipedia.org/wiki/Mastermind_(board_game)) is a code-breaking game for two players. This API simulates the role of codemaker. As a codebreaker, you can guess the code by sending a four digit number to the codemaker where each digit is between 1 to 6. The API will respond with a list. This list will be empty in case non of the digits were guessed correctly or filled with a combination of ones and zeros for correctly guessed digits. One indicates that a digit has the correct position, and zero that it doesn't.

## Requirements

* Python >= 3.6
* Packages: Flask, Flask-RESTful

## Installation

* Clone or download the repository.
* Install the necessary software packages.

```bash
$ pip install -r /path/to/requirements.txt
```

After a successful installation you are ready to run a local version of the application. You can run the API in the mastermind-api folder with the following command.

```bash
$ python app/api.py
```

## Unit tests

Once the API is running, you can run the unit tests in the mastermind-api folder.

```bash
$ python -m unittest discover tests
```

## Docker

Build a Docker image with the name `mastermind-api`.

```bash
$ docker build -t mastermind-api
```

Create a container from the `mastermind-api` image and run it as a daemon on port 80.

```bash
$ docker run -d -p 80:8000 mastermind-api
```

On a public domain it's probably best to use NGINX as a reverse proxy.

For more info: [docker-nginx-gunicorn-flask](https://github.com/basbiezemans/docker-nginx-gunicorn-flask)

## Create a new game

POST request. Creates a new game and returns a token as identifier.

```bash
$ curl -X POST http://127.0.0.1/game/
```

Example JSON response

```json
{
    "message": "A new game has been created. Good luck!",
    "token": "d9a831082a121dee..."
}
```

## Guess the code

PATCH request. Use the token from the response to communicate with the server.

* code : four digit number
* token : hexadecimal string

```bash
$ curl -X PATCH -d code=1234 http://127.0.0.1/game/d9a831082a121dee...
```

Example JSON response

```json
{
    "message": "Guess 1 of 10. You guessed: 1234",
    "token": "d9a831082a121dee...",
    "feedback": [
        1,
        0
    ]
}
```

## Game information

GET request. Retrieve game information with a token.

```bash
$ curl http://127.0.0.1/game/d9a831082a121dee...
```

Example JSON response

```json
{
    "message": "This game was created on 2018-12-02 12:04:44.596132",
    "token": "d9a831082a121dee...",
    "score": {
        "codemaker": 1,
        "codebreaker": 0
    }
}
```

## Delete a game

DELETE request. Delete a game with a token. The server will not respond to this request.

```bash
$ curl -X DELETE http://127.0.0.1/game/d9a831082a121dee...
```

