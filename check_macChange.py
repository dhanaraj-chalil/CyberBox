#!ethical hacking with python

import subprocess as sp
import optparse as op
import re


# Function to get arguments for changing MAC
def get_arguments():
    parser = op.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change its mac address")
    parser.add_option("-m", "--mac", dest="new_mac", help="new mac address")
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("Please specify an interface, use --help for more info.")
    elif not options.new_mac:
        parser.error("Please enter a new MAC address, use --help for more info.")
    else:
        return options


# Function to change MAC address
def change_mac(interface, new_mac):

    print("Changing MAC address for " + interface + " to " + new_mac)
    sp.call(["ifconfig", interface, "down"])
    sp.call(["ifconfig", interface, "hw", "ether", new_mac])
    sp.call(["ifconfig", interface, "up"])


# Function to get the current MAC address
def get_current_mac(interface):

    ifconfig_result = sp.check_output(["ifconfig", interface])
    curr_mac_addr = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)

    if curr_mac_addr:
        return curr_mac_addr.group(0)
    else:
        print("Could not read MAC address")
        return str(curr_mac_addr)


command_args = get_arguments()
current_mac = get_current_mac(command_args.interface)
print("Current MAC address is "+current_mac)


change_mac(command_args.interface, command_args.new_mac)


current_mac = get_current_mac(command_args.interface)


if current_mac == command_args.new_mac:

    print("MAC address for interface "+command_args.interface+" was successfully changed to "+current_mac)
else:

    print("MAC address for interface "+command_args.interface+" did not get changed.")

