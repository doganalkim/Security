This code applies ARP spoof attack in Python3. It makes use of basic Scapy framework functions for this purpose.

Once you run it, you become Man in the Middle ( MITM ). 

IMPORTANT: You should type "echo 1 > /proc/sys/net/ipv4/ip_forward" in terminal to activate port forwarding for IPv4.

Example usage is "python3 ARP.py -t 192.168.64.132 -r  192.168.64.76"

You can write "python3 ARP.py --help" to get help.
