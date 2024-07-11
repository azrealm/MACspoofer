'''
Program Description: Change MAC address of desired interface, for LINUX ONLY.
IDE: Visual Studio Code
DEV: A D E V
Python: Python 3.11.7
'''


import subprocess
import re
import os
import random
from platform import system

msft_macs = ["9C:AA:1B:4D:BB:DC", "F0:6E:0B:74:11:D2", "EC:59:E7:FD:9C:C8"]
aapl_macs = ["FC:FC:48:51:75:02", "FC:25:3F:0A:76:B5", "FC:18:3C:E3:CD:45"]
cisc_macs = ["FC:FB:FB:0A:2F:FE", "F4:4E:05:3B:AF:A8", "F4:1F:C2:9D:2A:2E"]
goog_macs = ["F8:0F:F9:7A:6C:2F", "F0:EF:86:AE:48:28", "20:DF:B9:84:19:2C"]

def list_interfaces():
    interfaces_dir = "/sys/class/net"
    interfaces = os.listdir(interfaces_dir)
    interfaces.remove("lo") 
    print("[+] Interface List:\n-----------------")

    for index, item in enumerate(interfaces):
        with open(interfaces_dir + "/" + str(item) + '/operstate') as f:
            status = f.readline().strip()

            if (status == "up"):
                print(f"{index}: {item} (online)")
            elif (status == "down"):
                print(f"{index}: {item}")

    select_item = input("\nSelect> ")

    for index, item in enumerate(interfaces):
        if (select_item == str(index)):
            return item


def get_permanent_mac(interface):
    ethtool_result = subprocess.check_output(["ethtool", "-P", interface])
    current_mac = re.search(
        r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(ethtool_result))

    if (current_mac):
        return current_mac.group(0).upper()
    else:
        print("[-] Could not read MAC address.")


def get_current_mac(interface):

    ethtool_result = subprocess.check_output(["ifconfig", interface])
    current_mac = re.search(
        r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(ethtool_result))

    if (current_mac):
        return current_mac.group(0).upper()
    else:
        print("[-] Could not read MAC address.")

def print_mac_list():

    print(f"\nMicrosoft:")
    for i in msft_macs:
        print(f"{i}")

    print(f"\nApple:")
    for i in aapl_macs:
        print(f"{i}")

    print(f"\nCisco:")
    for i in cisc_macs:
        print(f"{i}")

    print(f"\nGoogle:")
    for i in goog_macs:
        print(f"{i}")

    print("\n-----------------\nCopy and paste a MAC address from list\nType 'random' for a random MAC address\nType 'reset' to reset to permanent MAC address")

    mac_selection = input("\nSelect> ")

    return mac_selection

def change_mac(selected_interface, mac_address):
    if (mac_address.lower() == "random"):

        all_macs = msft_macs + aapl_macs + cisc_macs + goog_macs

        print("\n[+] Selecting random MAC address...")

        random_mac = random.choice(all_macs)

        subprocess.call(["ifconfig", selected_interface, "down"])
        subprocess.call(["ifconfig", selected_interface,
                         "hw", 'ether', random_mac])
        subprocess.call(["ifconfig", selected_interface, "up"])

        print(
            f"\nPermanent MAC address for [{selected_interface}]: {get_permanent_mac(selected_interface)}")

        print(
            f"New MAC address for [{selected_interface}]: {get_current_mac(selected_interface)}")

    elif (mac_address.lower() == "reset"):
        print("\n[+] Resetting MAC address...")

        subprocess.call(["ifconfig", selected_interface, "down"])
        subprocess.call(["ifconfig", selected_interface,
                         "hw", 'ether', get_permanent_mac(selected_interface)])
        subprocess.call(["ifconfig", selected_interface, "up"])

        print(
            f"\nPermanent MAC address for [{selected_interface}]: {get_permanent_mac(selected_interface)}")

        print(
            f"New MAC address for [{selected_interface}]: {get_current_mac(selected_interface)}")

    elif (re.match(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", mac_address)):
        print("\n[+] Changing MAC address...")

        subprocess.call(["ifconfig", selected_interface, "down"])
        subprocess.call(
            ["ifconfig", selected_interface, "hw", 'ether', mac_address])
        subprocess.call(["ifconfig", selected_interface, "up"])

        print(
            f"\nPermanent MAC address for [{selected_interface}]: {get_permanent_mac(selected_interface)}")

        print(
            f"New MAC address for [{selected_interface}]: {get_current_mac(selected_interface)}")

    else:
        print("[-] Invalid Input!")
        raise SystemExit


def main():
    if (system().lower() == "windows" or system().lower() == "darwin"):
        print("[-] This script is for Linux systems only.")
        raise SystemExit
    if (os.getuid() != 0):
        print("[-] You must run as root.")
        raise SystemExit
    try:
        subprocess.call(["ifconfig"], stdout=subprocess.PIPE,
                        stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    except FileNotFoundError:
        print(
            "\nPackage 'net-tools' is required for this script to work, please install using: \n\nsudo apt install net-tools\n")
        raise SystemExit

    try:
        subprocess.call(["ethtool"], stdout=subprocess.PIPE,
                        stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    except FileNotFoundError:
        print(
            "\nPackage 'ethtool' is required for this script to work, please install using: \n\nsudo apt install ethtool\n")
        raise SystemExit

    # Get selected interface from input()
    selected_interface = list_interfaces()

    if (selected_interface == None):
        print("[-] Invalid Selection!")
        raise SystemExit
    else:
        permanent_mac = get_permanent_mac(selected_interface)
        current_mac = get_current_mac(selected_interface)
        print(
            f"\nPermanent MAC address for [{selected_interface}]: {permanent_mac}")

        print(
            f"Current MAC address for [{selected_interface}]: {current_mac}\n-----------------")
    mac_selection = print_mac_list()
    change_mac(selected_interface, mac_selection)


if __name__ == "__main__":
    main()
