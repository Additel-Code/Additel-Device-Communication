# import the built-in socket library
import socket

# set the ip address and port
ip_address = '192.168.7.165'
port = 8000
command = 'DISP:LANG?\r\n'
# command asks the 875 to return the language the 875 is currently using (note that it ends in /r/n, that is important)

# connect to the Additel device over TCP
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(1)
s.connect((ip_address, port))

# send the command we want to send, in bytes
command_in_bytes =  bytes(command, 'utf-8')
s.send(command_in_bytes)

# recieve the response from the device and turn it into a string
data = s.recv(1024)
response_as_str = bytes.decode(data, 'utf-8')
print("recieved data:" + response_as_str)

# close the TCP connection
s.close()