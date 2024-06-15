import scapy.all as scapy
import optparse

IP_RANGE = None

def parse_IP():
    global  IP_RANGE
    parser = optparse.OptionParser()
    parser.add_option("-r","--range",dest = "range", help = "Enter your IP range!")
    args,_ = parser.parse_args()
    IP_RANGE = args.range

def scan():
    arp_pkt = scapy.ARP(pdst = IP_RANGE)
    ether_pkt = scapy.Ether(dst = 'ff:ff:ff:ff:ff:ff')
    pkt = ether_pkt / arp_pkt
    ans,_ = scapy.srp(pkt,timeout = 1, verbose = False)
    print("\tMAC\t\t\tIP")
    cnt = 1
    for i in ans:
        print("----------------------------------------------")
        print(f'{cnt}       {i[1].src}       {i[1].psrc} ')
        cnt+=1

if __name__ == '__main__':
    parse_IP()
    scan()

