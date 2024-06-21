import scapy.all as scapy
import optparse

IFACE = 'eth0'

ROUTER_IP = None
ROUTER_MAC = None

def parse_router_ip():
    global ROUTER_IP
    parser = optparse.OptionParser()
    parser.add_option("-r","--router-ip",dest = "ipaddr",
                      help = "Enter your router's ip address which can be seen using the command arp -a")
    opts,_ = parser.parse_args()
    ROUTER_IP = opts.ipaddr

def get_router_mac():
    global ROUTER_MAC
    try:
        scapy_pkt = scapy.ARP( pdst = ROUTER_IP)
        ether_pkt = scapy.Ether( dst = 'ff:ff:ff:ff:ff:ff')
        pkt = ether_pkt / scapy_pkt
        ans,_ = scapy.srp(pkt, timeout = 1, verbose = False)
        ROUTER_MAC = ans[0][1].hwsrc
    except Exception as E:
        pass

def process_pkt(pkt):
    try:
        if pkt.haslayer(scapy.ARP) and pkt[scapy.ARP].op == 2 and \
                pkt[scapy.ARP].psrc == ROUTER_IP and pkt[scapy.ARP].hwsrc != ROUTER_MAC:
            print("[+] You are under ARP spoof attack!")
    except Exception as E:
        pass

def sniff():
    scapy.sniff(store = False, prn = process_pkt, iface = IFACE )

if __name__ == '__main__':
    parse_router_ip()
    get_router_mac()
    try:
        sniff()
    except KeyboardInterrupt:
        print('\n[-] Ctrl-C detected! Quiting the program ...')

