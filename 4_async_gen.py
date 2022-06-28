import socket
from select import select

tasks = []

to_read = {}
to_write = {}


def runserver():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('localhost', 5000))
    server.listen()

    while True:
        yield 'read', server
        client, client_addr = server.accept()

        print(f'Connection from {client_addr}!')
        tasks.append(accept_client(client, client_addr))


def accept_client(client, client_addr):
    while True:
        yield 'read', client
        request = client.recv(8096)

        if not request or 'stop' in str(request):
            client.send('Bye!'.encode())
            break

        response = f'Hello, {client_addr}'.encode()
        yield 'write', client
        client.send(response)

    client.close()


def event_loop():

    while any([tasks, to_read, to_write]):
        while not tasks:
            ready_to_read, ready_to_write, _ = select(to_read, to_write, [])

            for sock in ready_to_read:
                tasks.append(to_read.pop(sock))

            for sock in ready_to_write:
                tasks.append(to_write.pop(sock))

        try:
            task = tasks.pop(0)
            reason, sock = next(task)

            if reason == 'read':
                to_read[sock] = task

            if reason == 'write':
                to_write[sock] = task
        except StopIteration:
            print('Done!')


if __name__ == "__main__":
    tasks.append(runserver())
    event_loop()
