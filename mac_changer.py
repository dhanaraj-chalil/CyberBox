#!ethical hacking with python

import subprocess as sp
import optparse as op

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

def change_mac(interface, new_mac):
    print("Changing MAC address for " + interface + " to " + new_mac)
    sp.call(["ifconfig", interface, "down"])
    sp.call(["ifconfig", interface, "hw", "ether", new_mac])
    sp.call(["ifconfig", interface, "up"])

options = get_arguments()
change_mac(options.interface, options.new_mac)


