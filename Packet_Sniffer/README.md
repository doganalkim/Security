This is a packet sniffer where you can sniff the packet of the target once you become MITM.

To become MITM, you can use ARP Spoof either with bettercap caplet or python3 script in my github.

This basic python3 scripts only prints the login info (username & password) and sniffed links. Also,
script only sniffs HTTP protocols.

IMPORTANT: You should type "echo 1 > /proc/sys/net/ipv4/ip_forward" in terminal to activate port forwarding for IPv4.

Usage is "python3 packet_sniffer.py -i eth0"

To get help just type "python3 packet_sniffer.py --help"
