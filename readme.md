# How to Communicate with Additel Calibrators and Devices

Additel has some fantastic calibration devices - and most of the time you can get what you want out of them with [Additel Land](https://www.additel.com/product-detail.html/land-pressure-software/), [Additel Log II](https://www.additel.com/product-detail.html/9502-log-II-pressure-software/), [Additel ACal](https://www.additel.com/product-detail.html/9530-acal-automatic-pressure-software/), or [Additel Link](https://www.additel.com/product-detail.html/additel-link-mobile-application/).  Sometimes that isn't enough to do what you want, however, especially if you want to integrate the units into your own software.  This guide will teach you how to communciate with your Additel devices, hopefully helping you avoid some of the problems you might face trying to figure out how to do this from scratch.

Most of the examples in this guide will be in the Python 3 programming langauge.  We chose Python 3 for two reasons:

* Python 3 is very clean and easy to understand.  This means as long as you have some programming experience, you don't need to have experience with Python 3 to understand the examples that will be given.  You can spend that time writing your software instead.
   
* Python 3 has access to a lot of really good 3rd party libraries and tools.  Much of the communication we do with the Additel devices will be through these 3rd party libraries, as they make our work much easier.  Naturally, that means if you aren't using Python 3, you may need to spend some time finding libraries in your programming language which do similar things.  We think this is an okay tradeoff for the guide as it allows us to simplify things alot.

If you have any questions, please feel free to [contact us](https://www.additel.com/contactus.html/).  Most of the time for simple problems, we will respond during the same day if it's within business hours.  For more complex problems, it may take a day or two for us to get back to you.

## Communication Types

Different Additel devices use different communication types.  Not every communication type is available for every device.  You'll need to see which types your device supports.  Click on the links below to jump to the guide section for the specific type of communication you want to support.

1) **[Serial Communication](/Serial/serial.md)** - Communication over a RS232 cable.  (We also have a few devices that can optionally communicate over an RS485 cable)
   - ADT220/221/222/223/226Ex/227Ex
   - ADT672/681/685
   - ADT673/686 (ordered optionally)
   - ADT761/780
2) **[USB Communication](/USB/usb.md)** - Communication over a USB type A, type B, or type C cable.
    - ADT226/227/260/273
    - ADT673/686
    - ADT760/761A/762/762W/780
3) **[Network Communication (TCP/IP)](/Network/network.md)** - Communication over Wifi or through an Ethernet (RJ-45) Cable.
    - ADT673/686
    - ADT760/761A/762/762W
    - ADT780
4) **[Bluetooth Low Energy Communication](/Bluetooth/bluetooth.md)** - Communicate over Bluetooth Low Energy.  **Please note that this guide is a work in progress, and not fully complete yet.**
    - ADT226/227/226Ex/227Ex/260/273/282/286
    - ADT673/685/686
    - ADT761A/762/762W
    - ADT850/875/878
5) **No Communciation Method Available** - Unfortunately, some of our devices don't have ways to communicate with 3rd party software, and have to be paired up with special hardware or other Additel devices.
    - ADT158
    - ADT160/161
    - ADT680
    
Note 1:  Some Additel devices also can communicate with HART protocol, but that mainly refers to device-to-device communication (which isn't described in this guide).

Note 2:  There are a few other advanced communication methods not talked about in this guide (in addition to bluetooth).  This is mainly because they are difficult, and can feel incomplete at times.  We don't have any plans to write guides for them in the future though.
