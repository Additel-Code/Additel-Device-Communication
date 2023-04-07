# import the pyserial library
import serial

# open a serial port
port = serial.Serial(   port='COM2',
                        baudrate=9600,
                        bytesize=serial.EIGHTBITS,
                        parity=serial.PARITY_NONE,
                        stopbits=serial.STOPBITS_TWO,
                        timeout=1   )


# encode the command to get the device SN in bytes, and write it to the device
command = "255:R:MRMD:1\r\n"
command_in_bytes = bytes(command, 'utf-8')
port.write(command_in_bytes)

# read the first 500 characters (or less if it times out), convert it to a string, and print it
response = port.read(size=500)
response_as_str = bytes.decode(response, 'utf-8')
print(response_as_str)