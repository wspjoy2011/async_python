import socket
from select import select

data_monitoring = []

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(('localhost', 5000))
server.listen()


def accept_connection(server_socket):
    client, client_addr = server.accept()
    print(f'Connection from {client_addr}!')
    data_monitoring.append(client)


def send_message(client):
    print('Before .recv()')
    request = client.recv(4096)

    if request:
        response = f'Hello, world!'.encode()
        client.send(response)
    else:
        client.close()


def event_loop():
    while True:
        ready_to_read, _, _ = select(data_monitoring, [], [])

        for sock in ready_to_read:
            if sock is server:
                accept_connection(sock)
            else:
                send_message(sock)


if __name__ == '__main__':
    data_monitoring.append(server)
    event_loop()


