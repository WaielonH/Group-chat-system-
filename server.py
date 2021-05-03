import socket
import threading

host = '127.0.0.1' #localhost
port = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
nicknames = []

#function to broadcast to all the clients
def broadcast(message):
    for client in clients:
        client.send(message)

#function to handle individual client
def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f'{nickname} left the chat!\n'.encode('utf-8'))
            nicknames.remove(nickname)
            break

def receive():
    while True:
        client, address = server.accept() #accept clients all the time
        print(f'Connected with {str(address)}') 

        client.send('NICK'.encode('utf-8')) #send keyword NICK to client

        nickname = client.recv(1024).decode('utf-8') #recieve nickname from client

        nicknames.append(nickname) #add nickname to nicknames list
        clients.append(client) #add client to connected clients list

        print(f'Nickname of the client is {nickname}!')
        broadcast(f'{nickname} joined the chat!\n'.encode('utf-8')) #tell everyone that the client has joined
        client.send('Connected to the server!'.encode('utf-8')) #confirm to the client that it is connected

        thread = threading.Thread(target=handle, args=(client,)) #create sepereate thread to handle client
        thread.start() #start the thread

print('server is listening...')
receive()
