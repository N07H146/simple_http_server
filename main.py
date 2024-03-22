import socket
import threading
import sys
import os

def handle_connection(connection: socket.socket, directory: str = None):
    # Receive data from the client
    data = connection.recv(1024)
    # Extract method and path from the request
    method, path = data.split(b" ")[:2]
    path = path.decode()

    # Handle different types of requests
    if path == "/":
        # Handle root path
        send_response(connection, b"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\nHello World!")
    elif path.startswith("/echo"):
        # Handle echo path
        message = path.split("/echo/")[1] if "/echo/" in path else ""
        send_response(connection, f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(message)}\r\n\r\n{message}".encode())
    elif path == "/user-agent":
        # Handle user-agent path
        user_agent = data.split(b"User-Agent: ")[1].split(b"\r\n")[0] if b"User-Agent: " in data else b""
        send_response(connection, f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(user_agent)}\r\n\r\n{user_agent}".encode())
    elif path.startswith("/files"):
        # Handle file-related requests
        handle_file_request(connection, method.decode(), directory, path, data)
    else:
        # Handle unknown paths
        send_response(connection, b"HTTP/1.1 404 Not Found\r\n\r\n")

    # Close the connection
    connection.close()

def handle_file_request(connection: socket.socket, method: str, directory: str, path: str, data: bytes):
    filename = os.path.basename(path.split("/files/")[1])
    filepath = os.path.join(directory, filename)

    if method == "GET":
        handle_get_file(connection, filepath)
    elif method == "POST":
        handle_post_file(connection, filepath, data)

def handle_get_file(connection: socket.socket, filepath: str):
    if os.path.isfile(filepath):
        with open(filepath, "rb") as file:
            file_content = file.read()
        response = f"HTTP/1.1 200 OK\r\nContent-Type: application/octet-stream\r\nContent-Length: {len(file_content)}\r\n\r\n".encode() + file_content
    else:
        response = b"HTTP/1.1 404 Not Found\r\n\r\n"
    send_response(connection, response)

def handle_post_file(connection: socket.socket, filepath: str, data: bytes):
    if not os.path.isfile(filepath):
        content_length = int(data.split(b"Content-Length: ")[1].split(b"\r\n")[0])
        file_content = data.split(b"\r\n\r\n")[1]
        with open(filepath, "wb") as file:
            file.write(file_content)
        response = b"HTTP/1.1 201 Created\r\n\r\n"
    else:
        response = b"HTTP/1.1 409 Conflict\r\n\r\n"
    send_response(connection, response)

def send_response(connection: socket.socket, response: bytes):
    connection.send(response)

def main(directory: str = None):
    # Create a server socket
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    server_socket.listen()

    # Accept incoming connections and handle them in separate threads
    while True:
        connection, _ = server_socket.accept()
        thread = threading.Thread(target=handle_connection, args=(connection, directory))
        thread.start()

if __name__ == "__main__":
    # Run the server
    try:
        directory = sys.argv[sys.argv.index("--directory") + 1]
        main(directory)
    except ValueError:
        main()
