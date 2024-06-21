To run type "python3 arp_spoof_detector -r 192.168.2.1" where the parameter must be your routers ip address.

To find out your router ip address, just type command "arp -a" or use tool similar to netdiscover.

This program aims to detect ARP spoof attack by monitoring ARP packets sent on behalf of router. And only detects
ongoing attack where the attaacker repeatedly sends ARP packets to change ARP table.

Default interface is hard coded as "eth0". You should change it for your purpose if your interface is different than "eth0".
But mostly it is mostly either "eth0" or "en0".
