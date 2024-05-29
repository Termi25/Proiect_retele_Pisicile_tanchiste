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


def main():
    host = '127.0.0.1'
    server_port = 5555

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, server_port))

    threading.Thread(target=receive_messages, args=(client,)).start()

    try:
        while True:
            message = input()
            if message.lower() == 'exit':
                client.send('exit'.encode("utf-8"))
                break
            elif message.lower() == 'calculate_distance':
                client.send('calculate_distance'.encode("utf-8"))

                def get_coordinates():
                    while True:
                        coordinates = input()
                        if ',' in coordinates and len(coordinates.split(',')) == 2:
                            try:
                                lat, lon = map(float, coordinates.split(','))
                                if -90 <= lat <= 90 and -180 <= lon <= 180:
                                    return coordinates
                                else:
                                    print("Coordinates are out of bounds.")
                            except ValueError:
                                print("Invalid numbers in coordinates.")
                        else:
                            print("Invalid format. Use latitude,longitude")
                
                point1 = get_coordinates()
                client.send(point1.encode("utf-8"))
                
                point2 = get_coordinates()
                client.send(point2.encode("utf-8"))
            else:
                client.send(message.encode("utf-8"))
    finally:
        client.close()
if __name__ == "__main__":
    main()