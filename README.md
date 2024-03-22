# Simple HTTP Server with Python

This is a simple HTTP server implemented in Python using the `socket` module. It can handle basic HTTP requests such as GET and POST and serves static files from a specified directory.

## Features

- Supports basic HTTP GET and POST methods
- Handles requests for the root path ("/"), echo ("/echo"), user-agent ("/user-agent"), and static files ("/files")
- Returns appropriate HTTP status codes and responses
- Multi-threaded to handle multiple client connections concurrently

## Requirements

- Python ^3.10

## Usage

- git clone https://github.com/N07H146/simple_http_server.git
- cd simple-http-server
- python main.py [--directory {directory_path}]

## When is all said and done

- Test it on localhost:4221
- curl -X POST -d "file contents" http://localhost:4221/files/example.txt

