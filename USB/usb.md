[Jump back to main readme.](../readme.md)

# USB Communication with Additel Calibrators and Devices

Many of the newer Additel devices can communicate over USB cables with USB Communication.  These cables can be USB-A to USB-A or USB-A to USB-B.  This method of communication is a little more complicated than Serial Communication.

Note that not all devices that have a USB cable will use USB communication.  Some of them will use Serial Communication.  You will need to figure out which one your device uses.  As a general rules, if a device uses a USB to USB cable, and has a colored screen, it uses USB Communication.  Otherwise it uses Serial Communication.

## Setup

First, you need to install Additel's USB Driver that is built to specifically communicate with Additel devices.  The easiest way to do this is to install [Additel Land](https://additel.com/product-detail.html/land-pressure-software/) and scan for the device.  The first time you try to interact with the device in Additel Land, it will install the driver.

In this example, we are going to use Python 3 (in this case, version 3.9.1, although newer versions should work fine too), which you can download [here](https://www.python.org/downloads/) or [here](https://www.microsoft.com/en-us/p/python-39/9p7qfqmjrfp7).

You will need a libusb-1.0 dll in order to communicate with a libusb device.  The easiest way to get this it to download it [here](https://github.com/pyusb/pyusb).  Save it to the same directory as the example program.

Lastly, you'll also need to install pyusb, by following the instructions [here](https://github.com/pyusb/pyusb#installing).  pyusb is a 3rd party library that makes communicating with USB devices reasonably easy.

## Example

```python
# import the pyusb library
import usb.core
from usb.backend import libusb1

# download the latest libusb-1.0 dll you can download from here:  https://libusb.info/  - then use the absolute path below as the backend
be = libusb1.get_backend(find_library=lambda x: "C:\\Stick_The_Absolute_Path_To_Lib_USB_1.0_DLL_Here")

# connect to the USB device - you will need to make sure you use the correct vendor and product id (you can ask us for it)
device = usb.core.find(idVendor=0x2E19, idProduct=0x02F8)

# if the usb device exists
if device is not None:

    # set the device configuration, then initialize it
    device.set_configuration()
    configuration = device.get_active_configuration()
    initialization = configuration[(0,0)]

    # get the out endpoint, which we will use to send commands out to the device
    endpoint_out = usb.util.find_descriptor(initialization, custom_match=lambda e: usb.util.endpoint_direction(e.bEndpointAddress) == usb.util.ENDPOINT_OUT)

    # get the in endpoint, which we will use to recieve commands in from the device
    endpoint_in = usb.util.find_descriptor(initialization, custom_match=lambda e: usb.util.endpoint_direction(e.bEndpointAddress) == usb.util.ENDPOINT_IN)

    # if both endpoints exist
    if endpoint_out is not None and endpoint_in is not None:

        # create a command and write it to the USB endpoint
        command = 'MEAS:PRES1?\r\n'
        endpoint_out.write(command)

        # try to read a response
        # note that some commands (like 'SYST:KLOCK ON\r\n') will not have a response, so this action may timeout with an error (which is why we have a try block)
        try:
            response = device.read(endpoint_in.bEndpointAddress, endpoint_in.wMaxPacketSize)
            response_as_str = bytearray(response).decode('utf-8')
            print(response_as_str)
        except Exception:
            pass
```

Let's go over this example step by step:

1)  First, we get the pyusb library loaded.

```python
# import the pyusb library
import usb.core
from usb.backend import libusb1
```

2) Next, we set up the libusb backend.  This will reference the DLL you downloaded in the setup section earlier.  You will need to provide an absolute path to the DLL for this code to work.

```python
# download the latest libusb-1.0 dll you can download from here:  https://libusb.info/  - then use the absolute path below as the backend
be = libusb1.get_backend(find_library=lambda x: "C:\\Stick_The_Absolute_Path_To_Lib_USB_1.0_DLL_Here")
```

3) Next, you need to ask the library to find the USB device.  USB devices are identified by a vendor id and a product id, and you will need both.  This can be found on Windows by going into device manager and looking up the USB device.  If you cannot find these numbers, you can instead [contact us](https://www.additel.com/contactus.html/) and we'll get you the numbers you need (they is one set of numbers for each Additel instrument).  Make sure to check the USB device you asked for exists before proceeding onwards with your program.

```python
# connect to the USB device - you will need to make sure you use the correct vendor and product id (you can ask us for it)
device = usb.core.find(idVendor=0x2E19, idProduct=0x02F8)

# if the usb device exists
if device is not None:
```
4) Next, set the USB device's configuration.  We can just use the default configuration of (0,0).

```python
# set the device configuration, then initialize it
device.set_configuration()
configuration = device.get_active_configuration()
initialization = configuration[(0,0)]
```

5)  Then, we need to get the endpoints.  Endpoints are very much like the programatic concept of 'streams' - you have a data in endpoint, and a data out endpoint, and you will probably need both.  Make sure both endpoints exist before proceeding on with your program.

```python
# get the out endpoint, which we will use to send commands out to the device
endpoint_out = usb.util.find_descriptor(initialization, custom_match=lambda e: usb.util.endpoint_direction(e.bEndpointAddress) == usb.util.ENDPOINT_OUT)

# get the in endpoint, which we will use to recieve commands in from the device
endpoint_in = usb.util.find_descriptor(initialization, custom_match=lambda e: usb.util.endpoint_direction(e.bEndpointAddress) == usb.util.ENDPOINT_IN)

# if both endpoints exist
if endpoint_out is not None and endpoint_in is not None:
```

6)  After the Device and Endpoint are set up, you can start sending USB commands.  USB Commands will be sent with a command structure called SCPI.  SCPI looks like this: `MEAS:PRES1?\r\n.` It consists of several segments separated by colons that describe what an operation does (in this case, `MEAS:PRES1` measures pressure from Sensor 1). Commands asking for information are followed by a `?` indicating they are a query. Paramaters are separarated from the command and other paramaters by a comma. Finally, the command terminates with `\r\n`.

```python
# create a command and write it to the USB endpoint
command = 'MEAS:PRES1?\r\n'
endpoint_out.write(command)
```

7)  Lastly, you can read the response from your unit.  Note that some commands will not have a response, and so you may recieve a timeout.  The best way to deal with this is with a `try` block.  Any responses recieved will have data returned as bytes, and so you will need to turn it into a string before printing it.

```python
# try to read a response
# note that some commands (like 'SYST:KLOCK ON\r\n') will not have a response, so this action may timeout with an error (which is why we have a try block)
try:
  response = device.read(endpoint_in.bEndpointAddress, endpoint_in.wMaxPacketSize)
  response_as_str = bytearray(response).decode('utf-8')
  print(response_as_str)
except Exception:
  pass
```

And that is pretty much it. You can now communicate with your Additel devices with USB Communication.

[Jump back to main readme.](../readme.md)
