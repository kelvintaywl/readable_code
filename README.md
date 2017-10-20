# Readable Code

Server that parses a source code and extracts words from class and

function names, summarising for the top N words that are used.

This service assumes the source code is open-sourced and hosted on Github.


Inspired by [a Kevlin Henney talk](https://www.youtube.com/watch?v=ZsHMHukIlJY).

## Motivation

This can help us figure out if our source code is really modeled around its

business logic. E.g., a comment microservice should have source code with class

and function names related to comment, reply, response, etc.

## Dependencies

- Python 3
- Redis

## Usage

Assuming your local Redis server is on default port and host settings,

```
$ pip install -r requirements.txt
$ FLASK_APP=server.py flask run
```

```
$ curl http://localhost:5000/github/kelvintaywl/jsonresume-validator\?top_n\=3 | python -m json.tool

[
    [
        "valid",
        6
    ],
    [
        "invalid",
        4
    ],
    [
        "resume",
        4
    ],
    [
        "resumes",
        4
    ],
    [
        "experiences",
        3
    ],
    [
        "schema",
        3
    ],
    [
        "validate",
        2
    ],
    [
        "work",
        2
    ],
    [
        "volunteer",
        2
    ],
    [
        "education",
        2
    ]
]

```