import socket
import selectors


selector = selectors.DefaultSelector()


def server():
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind(('localhost', 5000))
    server_sock.listen()

    selector.register(fileobj=server_sock, events=selectors.EVENT_READ, data=accept_connection)


def accept_connection(server_socket):
    client, client_addr = server_socket.accept()
    print(f'Connection from {client_addr}!')
    selector.register(fileobj=client, events=selectors.EVENT_READ, data=send_message)


def send_message(client):
    print('Before .recv()')
    request = client.recv(4096)

    if request:
        response = f'Hello, world!'.encode()
        client.send(response)
    else:
        selector.unregister(client)
        client.close()


def event_loop():
    while True:
        events = selector.select()

        for key, _ in events:
            callback = key.data
            callback(key.fileobj)


if __name__ == '__main__':
    server()
    event_loop()


