import socket
import os
from time import sleep

ADDRESS = '127.114.51.41:9198'

client = socket.socket()
client.connect(tuple(map(lambda x: int(x) if x.isdecimal() else x, ADDRESS.split(':'))))  # connect to the server
print(f'Connected to {ADDRESS}')

i = 0
try:
    while True:
        data = f'{i} {os.urandom(16).hex()}\n'
        client.send(data.encode())
        print(f'Sending: {data}', end='')
        sleep(1)
        i += 1
except KeyboardInterrupt:
    pass
finally:
    client.close()
