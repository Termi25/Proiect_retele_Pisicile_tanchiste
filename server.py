import socket
import threading
import os
from distance_calculator import calculate_distance


def handle_client(conn, addr):
    print(f"New connection from {addr}")

    send_commands(conn)

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
                'calculate_distance': lambda: calculate_distance_command(conn),
            }
            if message.lower() in command_handler:
                command_handler[message.lower()]()
            else:
                broadcast(f"{addr}: {message}")
    except:
        pass

    conn.close()

    if addr in clients:
        del clients[addr]
        broadcast(f"{addr} has left the chat")
        print(f"{addr} has left the chat")


def send_commands(conn):
    commands = [
        ("exit", "Disconnect from the server"),
        ("send_file", "Request a file from the server"),
        ("list_files", "List available files on the server"),
        ("calculate_distance", "Calculate the distance between two geographic coordinates"),
    ]
    command_list = "\n".join([f"{cmd[0]}: {cmd[1]}" for cmd in commands])
    conn.send(command_list.encode("utf-8"))


def calculate_distance_command(conn):
    try:
        conn.send("Enter the latitude and longitude of the first point (lat1,lon1): ".encode("utf-8"))
        point1 = conn.recv(1024).decode("utf-8")
        lat1, lon1 = map(float, point1.split(','))

        conn.send("Enter the latitude and longitude of the second point (lat2,lon2): ".encode("utf-8"))
        point2 = conn.recv(1024).decode("utf-8")
        lat2, lon2 = map(float, point2.split(','))

        distance = calculate_distance(lat1, lon1, lat2, lon2)
        result = f"The distance between the points is {distance:.2f} km."
        conn.send(result.encode("utf-8"))
    except Exception as e:
        conn.send(f"Error calculating distance: {str(e)}".encode("utf-8"))


def exit_command(conn, addr):
    conn.send("Exiting...".encode("utf-8"))
    broadcast(f"{addr} has disconnected from the server")
    conn.close()


def send_file(conn):
    conn.send("Enter filename: ".encode("utf-8"))
    filename = conn.recv(1024).decode("utf-8")
    try:
        with open(filename, "rb") as file:
            data = file.read()
            conn.send(data)
    except FileNotFoundError:
        conn.send("File not found".encode("utf-8"))


def list_files(conn):
    files = [filename for filename in os.listdir() if os.path.isfile(filename)]
    files_str = "\n".join(files)
    conn.send(files_str.encode("utf-8"))


def broadcast(message):
    for client_conn in clients.values():
        try:
            client_conn.send(message.encode("utf-8"))
        except:
            pass


def accept_connections():
    while True:
        conn, addr = server.accept()
        clients[addr] = conn
        threading.Thread(target=handle_client, args=(conn, addr)).start()


def main():
    host = '127.0.0.1'
    port = 5555

    global server
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen()

    print(f"Server listening on {host}:{port}")

    threading.Thread(target=accept_connections).start()


clients = {}
busy_clients = {}

if __name__ == "__main__":
    main()