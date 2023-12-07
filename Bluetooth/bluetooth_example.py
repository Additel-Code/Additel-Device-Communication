# the framework we use for Bluetooth Communication requires asynchronous functions, so we use asyncio for this
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
                command = "*idn?\r\n"
                command_in_bytes =  bytes(command, 'utf-8')
                await client.write_gatt_char(write_characteristic_UUID, command_in_bytes)

                # This is just here so we wait for the responses to the callback from earlier
                await asyncio.sleep(1)


# Have asyncio run the main function (asynchronously)
asyncio.run(main())