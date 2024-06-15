import optparse
import scapy.all as scapy


def command_input():
    parser = optparse.OptionParser()                                                    # Initialize parser
    parser.add_option("-r","--range",dest = "iprange",help = "Enter your IP range")     # Add range as a command line arguement
    (o,a) = parser.parse_args()
    return o.iprange

def scan(ip):
    arp_request = scapy.ARP(pdst = ip)
    broadcast = scapy.Ether(dst = "ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    ansed, unansed = scapy.srp(arp_request_broadcast,timeout = 1,verbose = False)

    print("IP\t\tMAC ADRESS")
    client_list = []
    for i in ansed:
        client = {"ip":i[1].psrc, "MAC":i[1].hwsrc}
        client_list.append(client)
        print(i[1].psrc, end = "\t")
        print(i[1].hwsrc)
        print("--------------")


ip = command_input()
scan(ip)

