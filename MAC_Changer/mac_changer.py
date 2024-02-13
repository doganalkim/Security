import subprocess
import optparse
import re

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

def get_current_MAC(i):
    ifconfigResultByte = subprocess.check_output(["ifconfig", i])
    ifconfigResultStr = ifconfigResultByte.decode()
    #print("\n" + ifconfigResultStr)

    mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfigResultStr)

    return mac_address_search_result.group(0)
def change_MAC_caller():
    i,m = get_arguments()

    curMac = get_current_MAC(i)

    if curMac:
        print("[+] Your previous MAC address is: " + curMac )
        change_MAC(i, m)
        new_MAC = get_current_MAC(i)
        print("[+] Your new MAC address is: " + new_MAC)
    else:
        print("[-] Your MAC address cannot be changed!")

change_MAC_caller()


