[Jump back to main readme.](../readme.md)

# Network Communication with Additel Calibrators and Devices

Many of the newer Additel devices can communicate with 3rd party programs over the Network.  In most cases, this means Wifi, although some of our devices also support RJ-45 (Ethernet) cables.  This method of communication is probably the most simple, as there is no drivers to install, and the tools you need are all part of the standard libraries of most programming languages.

## Setup

The only real setup step in this example program is installing the programming language.  In this example, we are going to use Python 3 (in this case, version 3.9.1, although newer versions should work fine too), which you can download [here](https://www.python.org/downloads/) or [here](https://www.microsoft.com/en-us/p/python-39/9p7qfqmjrfp7).

## Example

```python
# import the built-in socket library
import socket

# set the ip address and port
ip_address = '192.168.7.165'
port = 8000

# connect to the Additel device over TCP
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(1)
s.connect((ip_address, port))

# send the command we want to send, in bytes
command = 'MEAS:PRES1?\r\n'
command_in_bytes =  bytes(command, 'utf-8')
s.send(command_in_bytes)

# recieve the response from the device and turn it into a string
data = s.recv(1024)
response_as_str = bytes.decode(data, 'utf-8')
print("recieved data:" + response_as_str)

# close the TCP connection
s.close()
```

Let's go over this example step by step:

1)  First, we get the socket library loaded.

```python
# import the built-in socket library
import socket
```
2) Next, we need to set the IP address and Port of the deice we wish to communicate with.  You can usually find this on your device in Settings -> Communication.  You will need to connect to a network (either through Wifi or Ethernet) for your IP address to show up.  By default, the port used on our devices is 8000 (though you may change it).

```python
# set the ip address and port
ip_address = '192.168.7.165'
port = 8000
```

3) Next, we open the socket.

```python
# connect to the Additel device over TCP
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(1)
s.connect((ip_address, port))
```

4) Once you get the socket set up, you need to write some data to it.  Network Commands will be sent with a command structure called SCPI. SCPI looks like this: `MEAS:PRES1?\r\n`. It consists of several segments separated by colons that describe what an operation does (in this case, `MEAS:PRES1` measures pressure from Sensor 1). Commands asking for information are followed by a `?` indicating they are a query. Paramaters are separarated from the command and other paramaters by a space. Finally, the command terminates with `\r\n`.

```python
# send the command we want to send, in bytes
command = 'MEAS:PRES1?\r\n'
command_in_bytes =  bytes(command, 'utf-8')
s.send(command_in_bytes)
```

5)  Then you can recieve the response from the Additel device through the socket.  the socket works by specifying an amount of characters you'd like to recieve, but other libraries may do this differently.  The data is returned as bytes, and you need to turn it into a string before printing it.  Please note that some commands will not send data as a response, if they are not required to.

```python
# recieve the response from the device and turn it into a string
data = s.recv(1024)
response_as_str = bytes.decode(data, 'utf-8')
print("recieved data:" + response_as_str)
```

6)  Lastly, as cleanup, close the socket.

```python
# close the TCP connection
s.close()
```

And that is pretty much it.  You can now communicate with your Additel devices with Network Communication.

[Jump back to main readme.](../readme.md)
