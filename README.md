# Readable Code

Collection of scripts to check how readable our source code can be.

Inspired by [a Kevlin Henney talk]().

## Available scripts

### [Top N Words used in Source Code](scripts/top_words.py)

This script parses the source code and extracts words from class and

function names, summarising for the top N words that are used.

This can help us figure out if our source code is really modeled around its

business logic. E.g., a comment microservice should have source code with class

and function names related to comment, reply, response, etc.

#### Usage:

```
$ python script/top_words.py /path/to/repository -l (php|python|go) -n 3

Count	| Word
----	| -----
1528	| comment
1093	| subject
897	  | user

```
