# NU-EP1

## Setup

Link the NU-EP1 to jetson via ethernet. The jetson must then act as a DHCP server as the NU-EP1 will ask for an IP.

- Install dnsmasq

`sudo vim /etc/dnsmasq.conf`

```
interface=eth0 # interface to which the cable is connected.
dhcp-authoritative
dhcp-range=192.168.0.50,192.168.0.100,12h
dhcp-option=3,192.168.0.1
dhcp-host=<MAC_ADDRESS>,192.168.0.51  # set the ip for the NU-EP1 mac address
```

- Configure ip for interface : 

`sudo vim /etc/network/interfaces`

```
auto eth0
iface eth0 inet static
address 192.168.0.1

```

`sudo ifup eth0`

- Restart :
`sudo systemctl restart dnsmasq.service`
`sudo systemctl restart networking.service`

- Should work on the ip 

`python poll.py 192.168.0.51`

```
Sat Oct 24 16:53:28 2020: ('@1/0x1/0x7', 'SSTRING') == ['NU-EP1']
Sat Oct 24 16:53:28 2020: ('@0x66/0x1/0x0325', 'UINT') == [5]
Sat Oct 24 16:53:28 2020: ('@1/0x1/0x7', 'SSTRING') == ['NU-EP1']
Sat Oct 24 16:53:28 2020: ('@0x66/0x1/0x0325', 'UINT') == [82]
Sat Oct 24 16:53:28 2020: ('@1/0x1/0x7', 'SSTRING') == ['NU-EP1']
Sat Oct 24 16:53:29 2020: ('@0x66/0x1/0x0325', 'UINT') == [265]
```
