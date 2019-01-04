import selectors,socket,types


def broadcast(msg,socky=None):
	if socky:
		for sock in clients:
			if socky!=sock:
				sock.send(msg)
	else:
		for sock in clients:
			sock.send(msg)

def acceptWrapper(sock):
	conn,addr=sock.accept()
	print('accepted connection from ', addr)
	conn.setblocking(False)
	data=types.SimpleNamespace(addr=addr,inb=b'',outb=b'')
	events=selectors.EVENT_READ|selectors.EVENT_WRITE
	sel.register(conn,events,data=data)

def service_connection(key,mask):
	sock=key.fileobj
	data=key.data

	#msg="%s has joined the chat"% name 
	#broadcast(bytes(msg,"utf8"))

	clients.add(sock)

	if mask & selectors.EVENT_READ:
		recv_data=sock.recv(1024)
		if recv_data:
			key.data.outb+=recv_data
			print("recieved data is ",recv_data)
			#broadcast(recv_data)
		else:
			print('Closing connection to ',data.addr)
			sel.unregister(sock)
			sock.close()
	if mask & selectors.EVENT_WRITE:
		if data.outb:
			print('echoing ',repr(data.outb),' to all')
			sent=sock.send(data.outb)
			broadcast(data.outb,sock)
			data.outb=data.outb[sent:]
	
clients=set()
HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432      
sel=selectors.DefaultSelector()


lsock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
lsock.bind((HOST,PORT))
lsock.listen()

print ('listening on',(HOST,PORT))

lsock.setblocking(False)

sel.register(lsock,selectors.EVENT_READ,data=None)

while True:
	events=sel.select(timeout=None)
	for key,mask in events:
		if key.data  is None:
			acceptWrapper(key.fileobj)
		else:
			service_connection(key,mask)




