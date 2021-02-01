from socket import *
import base64
import ssl
import sys

msg = "\r\n I love Computer Networks\r\n"
endmsg = "\r\n.\r\n"

mailserver = ('smtp.gmail.com', 587) #Fill in start #Fill in end

# Create socket called clientSocket and establish a TCP connection with mailserver
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect(mailserver)

recv = clientSocket.recv(1024)
print("Message after connection request:" + recv)
if recv[:3] != '220':
    print('220 reply not received from server.')

# Send HELO command and print server response.
heloCommand = 'HELO Alice\r\n'
clientSocket.send(heloCommand.encode())
recv1 = clientSocket.recv(1024)
print(recv1)
if recv1[:3] != '250':
    print('250 reply not received from server.')

# Sending STARTTLS command
command="STARTTLS\r\n"
clientSocket.send(command.encode())
recv1 = clientSocket.recv(1024)
print(recv1)
if recv1[:3] != '220':
    print('220 reply not received from server.')

tlsSocket=ssl.wrap_socket(clientSocket)


# Info for username and password
username =  "someMail@gmail.com"                    		 #the username for your server
password = "***somepassword***"                              #i changed the password after tests,for submission 
base64_str = ("\x00"+username+"\x00"+password).encode()
base64_str = base64.b64encode(base64_str)
authMsg = "AUTH PLAIN ".encode()+base64_str+"\r\n".encode()
tlsSocket.send(authMsg)
recv_auth = tlsSocket.recv(1024)
print(recv_auth.decode())
if recv_auth[:3] != '235':
    print('235 reply not received from server.')


# Send MAIL FROM command and print server response.
mailFrom = "MAIL FROM: <esrarican17@gmail.com> \r\n"
tlsSocket.send(mailFrom.encode())
recv_mail = tlsSocket.recv(1024)
print("After MAIL FROM command: "+recv_mail)
if recv_mail[:3] != '250':
    print('250 reply not received from server.')

# Send RCPT TO command and print server response.
rcptTo = "RCPT TO: <esranur.arican2016@gtu.edu.tr> \r\n"
tlsSocket.send(rcptTo.encode())
recv_rcpt = tlsSocket.recv(1024)
print("After RCPT TO command: "+recv_rcpt)
if recv_rcpt[:3] != '250':
    print('250 reply not received from server.')

# Send DATA command and print server response.
data = "DATA\r\n"
tlsSocket.send(data.encode())
recv_data = tlsSocket.recv(1024)
print("After DATA command: "+recv_data)
if recv_data[:3] != '354':
    print('354 reply not received from server.')

# Send message data.
subject = "Subject: SMTP mail client testing \r\n\r\n" 
tlsSocket.send(subject.encode())
tlsSocket.send(msg.encode())
#message = raw_input("Enter your message: \r\n")
#tlsSocket.send(message.encode())
tlsSocket.send(endmsg.encode())
recv_msg = tlsSocket.recv(1024)
print("Response after sending message body:"+recv_msg.decode())
if recv_msg[:3] != '250':
    print('250 reply not received from server.')

# Send QUIT command and get server response.
tlsSocket.send("QUIT\r\n".encode())
message=tlsSocket.recv(1024)
print (message)

tlsSocket.close()
