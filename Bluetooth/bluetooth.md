[Jump back to main readme.](../readme.md)

# Bluetooth Low Energy Communication with Additel Calibrators and Devices

**Please note that this guide is a work in progress, and is not fully complete  yet.**

Many of the newer Additel devices can communicate with 3rd party programs over Bluetooth Low Energy.  This method of communication is a little complicated, as not all Bluetooth devices are the same, and not all devices Bluetooth scanning capabilities are the same.  However, this guide should get you going in the correct direction if you want to connect to our devices with your programs using Bluetooth.

## Setup

In this example, we are going to use Python 3 (in this case, version 3.9.1, although newer versions should work fine too), which you can download [here](https://www.python.org/downloads/) or [here](https://www.microsoft.com/en-us/p/python-39/9p7qfqmjrfp7).

You'll also need to install Bleak, by following the instructions [here](https://bleak.readthedocs.io/en/latest/installation.html).  Bleak is a 3rd party library that makes communicating with bluetooth devices really easy.

## Example

```python
# the framework we use for Bluetooth Communication requires asynchronous functions ,so we use asyncio for htis
import asyncio

# Bleak has a Bluetooth Scanner and a Bluetooth Client class (and we will need both)
from bleak import BleakScanner
from bleak import BleakClient

# The main function, which has all of our logic
async def main():

    # First we defined three UUIDs we may need to connect to the ADT685Ex (these may differ if you have a different instrument)
    communication_service_UUID = "AF661820-D14A-4B21-90F8-54D58F8614F0"
    notification_characteristic_UUID = "1B6B9415-FF0D-47C2-9444-A5032F727B2D"
    write_characteristic_UUID = "1B6B9415-FF0D-47C2-9444-A5032F727B2D"

    # Then, we ge scan for a list of nearby Bluetooth Devices
    scanned_bluetooth_devices = await BleakScanner.discover()

    # We loop through each device, checking to see if it advertises itself as an ADT685Ex
    for device in scanned_bluetooth_devices:
        if device.name == "ADT685":

            # If it does, we crate a Client Connection with the device
            async with BleakClient(device) as client:

                # While this code doesn't use it, sometimes we will need access to the 'Communication Service' of the Bluetooth device
                # This is how we gain access to it
                communication_service = client.services.get_service(communication_service_UUID)

                # In order to listen to responses form the device, we will need to listen on the 'Notification Characteristic' of the Bluetooth Device
                # We recieve all responses in the callback as a bytearray, and print them out
                async def callback(sender, data_as_bytearray):
                    print(data_as_bytearray.decode())
                
                await client.start_notify(notification_characteristic_UUID, callback)

                # We can send commands thorugh the 'Write Characteristic' of the Bluetooth Device
                # We must send the commands as a bytearray
                command = "@*idn?\r\n"
                command_in_bytes =  bytes(command, 'utf-8')
                await client.write_gatt_char(write_characteristic_UUID, command_in_bytes)

                # This is just here so we wait for the responses to the callback from earlier
                await asyncio.sleep(1)


# Have asyncio run the main function (asynchronously)
asyncio.run(main())
```

Let's go over this example step by step:

1) First, we get the asyncio library.  This library allows us to write what are called 'async' methods in Python.  This allows much more efficient code when it comes to doing Networking (like Bluetooth).

```python
# the framework we use for Bluetooth Communication requires asynchronous functions ,so we use asyncio for htis
import asyncio
```

2) Next, we import two classes from Bleak, the Scanner class (which will allow us to search for Bluetooth Devices) and the Client class (which will allow us to connect to Bluetooth Devices)
```python
# Bleak has a Bluetooth Scanner and a Bluetooth Client class (and we will need both)
from bleak import BleakScanner
from bleak import BleakClient
```

3) Then, we have the main 'async' function.  In this example, all of our logic is included inside of this, but in your proram, there's a good chance it will be split up into other 'async' subfunctions.

```python
# The main function, which has all of our logic
async def main():
```

4) After that, we establish three UUID constants, that we will use to connect to our Bluetooth device.  These constants differ for each type of device we sell.  In this case, the UUIDs are for the ADT685/685Ex.
```python
# First we defined three UUIDs we may need to connect to the ADT685Ex (these may differ if you have a different instrument)
communication_service_UUID = "AF661820-D14A-4B21-90F8-54D58F8614F0"
notification_characteristic_UUID = "1B6B9415-FF0D-47C2-9444-A5032F727B2D"
write_characteristic_UUID = "1B6B9415-FF0D-47C2-9444-A5032F727B2D"
```

5) Next, we scan for Bluetooth devices our computer can see.
```python
# Then, we ge scan for a list of nearby Bluetooth Devices
scanned_bluetooth_devices = await BleakScanner.discover()
```

6) Then, we loop through our scanned devices.  In this case, we only care about the ones that say their name is 'ADT685'.  You can probably also use other method to filter out the Bluetooth devices you do not care about (there's also a way to do this in the BleakScanner.discover() method that makes scanning faster)
```python
# We loop through each device, checking to see if it advertises itself as an ADT685Ex
for device in scanned_bluetooth_devices:
    if device.name == "ADT685":
```

7) Once we have our device, we create a BleakClient connection to it (or if there are multiple devices we want to connect to, to them).
```python
# If it does, we crate a Client Connection with the device
async with BleakClient(device) as client:
```

8) Each of our Bluetooth devices has a 'Communication Service'.  This is how you access it (though we won't use it in this example).
```python
# While this code doesn't use it, sometimes we will need access to the 'Communication Service' of the Bluetooth device
# This is how we gain access to it
communication_service = client.services.get_service(communication_service_UUID)
```

9) Each of our Bluetooth devices also has a 'Notification Characteristic', which allows us to listen to responses back form the device.  Before we send any commands to the device, we need to listen for responses it gives.  Any responses we get are recieved by the callback method, and printed out to the screen.  The first response we receive will always be `CODE?`, and recieving it means we can start sending commands and getting responses back (we don't wait in this example though for the sake of simplicity).
```python
# In order to listen to responses form the device, we will need to listen on the 'Notification Characteristic' of the Bluetooth Device
# We recieve all responses in the callback as a bytearray, and print them out
async def callback(sender, data_as_bytearray):
    print(data_as_bytearray.decode())

await client.start_notify(notification_characteristic_UUID, callback)
```

1)  Each of our Bluetooth devices in addition has a 'Write Characteristic', which allows us to send commands to the device.  Responses will be recieved by the callback talked about in Step 9.
```python
# We can send commands thorugh the 'Write Characteristic' of the Bluetooth Device
# We must send the commands as a bytearray
command = "*idn?\r\n"
command_in_bytes =  bytes(command, 'utf-8')
await client.write_gatt_char(write_characteristic_UUID, command_in_bytes)
```

1)  Last of all, in order to wait for the response from Step 10, we sleep this thread for a bit.  this gives time for the callback talked about in Step 9 to recieve and print the response to the command we sent in Step 10.
```python
# This is just here so we wait for the responses to the callback from earlier
await asyncio.sleep(1)
```

And that is pretty much it.  You can now communicate with your Additel devices with Bluetooth Low Energy.

[Jump back to main readme.](../readme.md)
