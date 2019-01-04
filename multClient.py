import socket,selectors,types
from threading import Thread
import tkinter

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432
name=input('Enter your name')

stringy="%s joined the chat"%name
messages = [bytes(stringy,'utf8')]


def receive():

	while True:
		events=sel.select(timeout=1)
		if events:
			for key,mask in events:
				serviceConnection(key,mask)



def send(event=None):
    msg=my_msg.get()
    my_msg.set("")
    sock.connect_ex(server_addr)

    msg= name+ msg

    sock.send(bytes(msg,'utf8'))
    

   
def on_closing(event=None):
	my_msg.set("quit")
	send()


def serviceConnection(key,mask,message=None):
	sock=key.fileobj
	data=key.data

	if message:
		print("Got my message ",message)

		data.messages.append(bytes(message,"utf8"))

		message=None
		

	if mask & selectors.EVENT_READ:
		recv_data=sock.recv(1024)

		if recv_data:
			print('recieved',repr(recv_data))
			msg_list.insert(tkinter.END,recv_data)
		if not recv_data :

			print("Connection closed")
			sel.unregister(sock)
			sock.close()

	if mask & selectors.EVENT_WRITE:
		if not data.outb and data.messages:
			data.outb=data.messages.pop()

		if data.outb:

			sent=sock.send(data.outb)
			data.outb=data.outb[sent:]

#sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sel=selectors.DefaultSelector()

server_addr = (HOST, PORT)

print('starting connection to', server_addr)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setblocking(False)    
sock.connect_ex(server_addr)
events = selectors.EVENT_READ | selectors.EVENT_WRITE
data = types.SimpleNamespace(connid=1,
                             msg_total=sum(len(m) for m in messages),
                             recv_total=0,
                             messages=list(messages),
                             outb=b'')
sel.register(sock, events, data=data)






top=tkinter.Tk()
top.title("Chatter")
messages_frame=tkinter.Frame(top)
my_msg=tkinter.StringVar()

my_msg.set("")

scrollbar=tkinter.Scrollbar(messages_frame)
msg_list = tkinter.Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()
messages_frame.pack()


entry_field = tkinter.Entry(top, textvariable=my_msg)
entry_field.bind("<Return>", send)
entry_field.pack()
send_button = tkinter.Button(top, text="Send", command=send)
send_button.pack()

top.protocol("WM_DELETE_WINDOW", on_closing)

recieveThread=Thread(target=receive)

recieveThread.start()

tkinter.mainloop()

















