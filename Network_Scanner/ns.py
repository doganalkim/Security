import optparse
import scapy.all as scapy


def command_input():
    parser = optparse.OptionParser()                                                    # Initialize parser
    parser.add_option("-r","--range",dest = "iprange",help = "Enter your IP range")     # Add range as a command line arguement
    (o,a) = parser.parse_args()
    return o.iprange
def scan(ip):
    #scapy.arping(ip) # We will implement it manually
    arp_request = scapy.ARP(pdst = ip)
    #arp_request.show()
    #print(arp_request.summary()) # prints the summary
    #scapy.ls(scapy.ARP()) # prints the variables to set
    broadcast = scapy.Ether(dst = "ff:ff:ff:ff:ff:ff")
    #scapy.ls(scapy.Ether())
    #print(broadcast.summary())
    #broadcast.show()
    arp_request_broadcast = broadcast/arp_request
    #print(arp_request_broadcast.summary())
    #arp_request_broadcast.show()
    ansed, unansed = scapy.srp(arp_request_broadcast,timeout = 1,verbose = False)
    #print(ansed.summary())
    #print(unansed.summary())

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

