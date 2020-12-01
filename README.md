# Keyence x Python

Setting up communication with keyence products using python on Linux

Products:
- NU-EP1: Ethernet communication unit
- SR-750: Barcode scanner

# Setting the IP address

Keyence devices can be used via ethernet once the IP has been set. Usually this is done via their Windows software.
However, it can be done fully on linux by setting up a DHCP server. This DHCP server will answer the BOOTP/DHCP requests made by the keyence device.

## Steps

### Install dnsmasq

`sudo vim /etc/dnsmasq.conf`

```
interface=eth0 # interface to which the cable is connected.
dhcp-authoritative
dhcp-range=192.168.1.90,192.168.1.100,12h # .1 is the network on which all the hardware is connected. You reserve a subset of the ips in this network.
dhcp-option=3,192.168.1.24 # IP address of the interface that acts as dhcp server (ip of the computer).
dhcp-host=<MAC_ADDRESS>,192.168.1.91  # set the ip for one keyence device
```

### Configure ip for interface (make it static, just in case) : 

`sudo vim /etc/network/interfaces`

```
auto eth0
iface eth0 inet static
address 192.168.1.24

```

`sudo ifup eth0`

### Restart :

`sudo reboot`

### Communication should work.

If it still doesn't work, these commands should help you debug:

- `sudo tcpdump -i eth0` : examine traffic on the network interface. At the beginning, you should see bootp/dhcp requests coming from the keyence device with its mac address (written somewhere on the device). If you do not see these kinds of requests, the device may already have an ip, albeit a wrong one (e.g : 192.168.100.100), you would need to reset the device ip (ex: SR-750, hold tune button for 5 seconds).

- `ping 192.168.1.91` : if you receive a response, congrats, you can at least detect the device.

- `nmap 192.168.1.91` : check open ports on the device.

- Socket returns `connection refused` : the port maybe closed or not available, if you are sure it's the correct port for communication, then it could be that the device is not setup for ethernet right now (happens with SR-750, defaults to RS-232). You need to either use the windows software :(, or you can use our pre-configured device configuration file (`.ptc`) generated via the software (yet to be tested on other devices). You then need to transmit it using ftp (port 21 should be opened).
