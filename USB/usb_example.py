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