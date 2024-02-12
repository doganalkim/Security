import subprocess
import optparse


def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i","--interface",dest = "interface",help = "Interface to change its MAC address")
    parser.add_option("-m","--mac",dest = "newMac",help = "The destination MAC address")

    (opts,args) = parser.parse_args()

    if not opts.interface:
        parser.error("[-] Please indicate the interface")
    if not opts.newMac:
        parser.error("[-] Please indicate the MAC address")
        
    return opts.interface,opts.newMac

def change_MAC(interface,newMac):

    print(f"[+] Changing MAC address for {interface} to {newMac}")

    #subprocess.call(f"ifconfig  {interface} down",shell = True)
    #subprocess.call(f"ifconfig {interface} hw ether {newMac}",shell = True)
    #subprocess.call(f"ifconfig {interface} up",shell = True)

    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", newMac])
    subprocess.call(["ifconfig", interface, "up"])


i,m = get_arguments()
change_MAC(i,m)
