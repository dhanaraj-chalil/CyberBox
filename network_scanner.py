#! python_prgms/network_scanner

import scapy.all as scapy


def scan(ip):
    #scapy.arping(ip) #Buildin function to scan network/subnet to get IP and MAC addresses

    #scapy.ls(scapy.ARP()) #'ls' function will display all fields in ARP (or other protocol) packet
    arp_request = scapy.ARP(pdst=ip) #Creating an ARP object, 'pdst' variable set IP address of destination device
    #print("ARP request IP summary : "+arp_request.summary()) #'Summary()' will display ARP request packet (or respective packet) summary
    #arp_request.show()

    #scapy.ls(scapy.Ether()) #'ls' function to display all fields in Ether object
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    #print("ARP request Ether summary : "+broadcast.summary())
    #broadcast.show()

    #Combining Ether and IP objects togather to frame ARP request packet
    arp_request_broadcast = broadcast/arp_request
    #print("ARP request summary : "+arp_request_broadcast.summary())
    arp_request_broadcast.show() #show() will display all details about the packet

    #Sending packet using SRP()
    #answered_list, unanswered_list = scapy.srp(arp_request_broadcast, timeout=1)

    #answered_list.show()
    #unanswered_list.show()

    #Fetching only answered list
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    #Fetching each element in answered_list
    print("IP Address \t\tMAC Address\n----------------------------------------") #Formating output
    for element in answered_list:
        #print(element)

        #Each element has 2 parts - first for request and second for reply
        #Fetching only ARP reply part
        #print(element[1].show())

        #Fetching only target IP and MAC addresses
        print(element[1].psrc + "\t\t" + element[1].hwsrc)

scan("10.0.2.1/24")