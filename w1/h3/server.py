import socket

ADDRESS = '127.114.51.41:9198'

server = socket.socket()
server.bind(tuple(map(lambda x: int(x) if x.isdecimal() else x, ADDRESS.split(':'))))  # bind to the address
server.listen(1)  # listen for one connection
print(f'Listening on {ADDRESS}')
connection, _ = server.accept()  # accept the connection
print('Connection established')

try:
    while True:
        data = connection.recv(128)  # read up to 128 bytes once a time
        if not data:
            raise OSError('Connection closed')
        print('Received:', data.decode(), end='')
except KeyboardInterrupt:
    pass
finally:
    connection.close()
    server.close()
