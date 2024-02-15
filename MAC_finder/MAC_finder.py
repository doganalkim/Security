from subprocess import *
from optparse import *
from re import *

def get_opts():
    parser = OptionParser()
    parser.add_option("-i","--iface", dest = "iface", help = "The interface whose MAC you want to change")
    (opts,args) = parser.parse_args()
    #print(f"{opts.iface} {opts.newMac}")
    return opts.iface

def  get_MAC(i):
    try:
        output = check_output(["ifconfig",i]).decode()
        result = search("\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", output)
        if result and result.group(0):
            print(f"[+] Your MAC address for the interface {i} is {result.group(0)}")
        else:
            print(f"[-] Your MAC address for the interface {i} cannot be found!")
    except:
        print(f"[-] There is no such an interface called {i} on your PC!")

def main():
    i = get_opts()
    if not i:
        print("[-] Make sure your interface is valid!")
    else:
        get_MAC(i)

main()

