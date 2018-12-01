# Mastermind API

REST API that simulates the role of Mastermind's codemaker.

[Mastermind](https://en.wikipedia.org/wiki/Mastermind_(board_game)) is a code-breaking game for two players. This API simulates the role of codemaker. As a codebreaker, you can guess the code by sending a four digit number to the codemaker where each digit is between 1 to 6. The API will respond with a list. This list will be empty in case non of the digits were guessed correctly or filled with a combination of ones and zeros for correctly guessed digits. One indicates that a digit has the correct position, and zero that it doesn't.

## Create a new game

```bash
$ curl http://127.0.0.1:5000/create/
```

Example response

```json
{
    "message": "A new game has been created. Good luck!",
    "token": "d9a831082a121dee...",
     ...
}
```

## Guess the code

PUT request. Use the token from the response to communicate with the server.

* code : four digit number
* token : hexadecimal string

```bash
$ curl -X PUT -d code=1234 -d token=d9a83... http://127.0.0.1:5000/guess/
```

Example response

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

## Unit tests

```bash
$ python -m unittest discover tests
```

