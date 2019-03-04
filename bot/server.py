import socket                                         
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
host = '127.0.0.1'                      
port = 9999                                           
serversocket.bind((host, port))                                  
serversocket.listen(5)                                           
while True:
   # establish a connection
   clientsocket,addr = serversocket.accept()
   query = clientsocket.recv(8192)
   if query:
       print("User: ", str(query))
       clientsocket.send(input("Agent: ").encode('ascii'))
       clientsocket.close()