# This method does not bypass https. NO HSTS hijack
# It implements a man in the middle attack within the subnet by ARP SPOOF
# Bettercap should be installed to run the caplet.
# The IP address parameter sent to target must be changed according to your victim. In my case, the victim is 192.168.139.130 (private IP address)
# To run, you should type "bettercap -iface eth0 -caplet caplet.cap" in the terminal/terminator on Kali Linux.
# I run these commands on Kali linux
