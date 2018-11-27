# Mastermind API

REST API that simulates the role of Mastermind's codemaker.

[Mastermind](https://en.wikipedia.org/wiki/Mastermind_(board_game)) is a code-breaking game for two players. This API simulates the role of codemaker. As a codebreaker, you can guess the code by sending a pattern of four color code "pegs" to the codemaker.

## Create a new game

```bash
$ curl http://127.0.0.1:5000/create/
```

## Guess a pattern

```bash
$ curl -X PUT -d pattern=ECHO http://127.0.0.1:5000/guess/
```

## Unit tests

```bash
$ python -m unittest discover tests
```

