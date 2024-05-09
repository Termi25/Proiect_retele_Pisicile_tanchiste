import socket
import threading


# Function to receive messages from the server
def receive_messages(sock):
    while True:
        try:
            message = sock.recv(1024).decode("utf-8")
            print(message)
        except:
            break


# Main function to start the client
def main():
    host = '127.0.0.1'
    server_port = 5555

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, server_port))

    # Start a thread to receive messages from the server
    threading.Thread(target=receive_messages, args=(client,)).start()

    try:
        while True:
            message = input()
            if message.lower() == 'exit':
                client.send('exit'.encode("utf-8"))
                break
            client.send(message.encode("utf-8"))
    finally:
        client.close()


if __name__ == "__main__":
    main()