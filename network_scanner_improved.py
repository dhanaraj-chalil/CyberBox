#! python_prgms/network_scanner_improved

import scapy.all as scapy
#import optparse as op #Depricated
import argparse as ap


def get_arguments():
    parser = ap.ArgumentParser()
    parser.add_argument("-i", "--ip", dest="ip", help="IP address of target whose MAC to be retrieved")
    options = parser.parse_args()
    return options

def scan(ip_addr):
    if not ip_addr:
        print("Please specify IP address of target client")
        return None
    else:
        arp_request = scapy.ARP(pdst=ip_addr)
        broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
        arp_request_broadcast = broadcast/arp_request
        answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

        client_list = []
        for element in answered_list:
            client_dict = {"ip": element[1].psrc, "mac": element[1].hwsrc}
            client_list.append(client_dict)

    return client_list


def print_result(results_list):
    print("IP Address \t\tMAC Address\n----------------------------------------")
    for client in results_list:
        print(client["ip"] + "\t\t" + client["mac"])

command = get_arguments()
scan_result = scan(command.ip)
if scan_result:
    print_result(scan_result)