import socket
import threading
import os


# Function to handle client connections
def handle_client(conn, addr):
    print(f"New connection from {addr}")

    # Send list of available commands to the client
    send_commands(conn)

    # Broadcast new connection to all clients
    broadcast(f"{addr} has joined the chat")

    try:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            message = data.decode("utf-8")
            command_handler = {
                'exit': lambda: exit_command(conn, addr),
                'send_file': lambda: send_file(conn),
                'list_files': lambda: list_files(conn),
            }
            if message.lower() in command_handler:
                command_handler[message.lower()]()
            else:
                broadcast(f"{addr}: {message}")
    except:
        pass

    # Close the connection
    conn.close()

    if addr in clients:
        del clients[addr]
        # Broadcast client disconnection to all clients
        broadcast(f"{addr} has left the chat")
        print(f"{addr} has left the chat")


# Function to send list of available commands to the client
def send_commands(conn):
    commands = [
        ("exit", "Disconnect from the server"),
        ("send_file", "Request a file from the server"),
        ("list_files", "List available files on the server"),
        # Add more commands and descriptions here
    ]
    command_list = "\n".join([f"{cmd[0]}: {cmd[1]}" for cmd in commands])
    conn.send(command_list.encode("utf-8"))


# Function to handle the 'exit' command
def exit_command(conn, addr):
    conn.send("Exiting...".encode("utf-8"))
    broadcast(f"{addr} has disconnected from the server")
    conn.close()


# Function to send the requested file to the client
def send_file(conn):
    conn.send("Enter filename: ".encode("utf-8"))
    filename = conn.recv(1024).decode("utf-8")
    try:
        with open(filename, "rb") as file:
            data = file.read()
            conn.send(data)
    except FileNotFoundError:
        conn.send("File not found".encode("utf-8"))


# Function to list available files on the server
def list_files(conn):
    files = [filename for filename in os.listdir() if os.path.isfile(filename)]
    files_str = "\n".join(files)
    conn.send(files_str.encode("utf-8"))


# Function to broadcast messages to all clients
def broadcast(message):
    for client_conn in clients.values():
        try:
            client_conn.send(message.encode("utf-8"))
        except:
            pass


# Function to accept incoming connections from other clients
def accept_connections():
    while True:
        conn, addr = server.accept()
        clients[addr] = conn
        threading.Thread(target=handle_client, args=(conn, addr)).start()


# Main function to start the server
def main():
    host = '127.0.0.1'
    port = 5555

    global server
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen()

    print(f"Server listening on {host}:{port}")

    # Start accepting incoming connections in a separate thread
    threading.Thread(target=accept_connections).start()


# Dictionary to keep track of connected clients
clients = {}
# Dictionary to keep track of busy clients
busy_clients = {}

if __name__ == "__main__":
    main()