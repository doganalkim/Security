
You need to install netfilterqueue if not installed. This can be done by 
typing "pip3 install netfliterqueue".

IMPORTANT: type terminal "iptables -I FORWARD -j NFQUEUE --queue-num 0"
This command traps the packets into the queue. You can change the queue number.

This usually requires becoming MITM, which can be achieved by using ARP python3 script
that is also available in this repository. However, if you want to test it on your local machine
instead of a virtual machine, then you should type "iptables -I INPUT -j NFQUEUE --queue-num 0 && iptables -I OUTPUT -j NFQUEUE --queue-num 0"
