#!/usr/bin/env python

import scapy.all as scapy #doesnt come preinstalled with python3. Need to install it using pip. Install scapy-python3
import optparse #argparse is the python 3 version, import argparse

def scan(ip):
    arp_request = scapy.ARP(pdst=ip) # getting an arp request ready for the broadcast ip address
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff") # getting the arp request ready for the broadcast mac address
    arp_request_broadcast = broadcast/arp_request # combining the 2 things above to get the packet ready.
    answeredlist= scapy.srp(arp_request_broadcast,timeout= 1,verbose = False)[0] #b roadcasting the arp packet, timeout = 1 neccessary, verbose gets rid of an unneeded part out of output and [0] prints out whats needed from the list



    clients_list=[]

    for i in answeredlist:
        client_dict = {"IP": i[1].psrc, "MAC": i[1].hwsrc}
        clients_list.append(client_dict) #appending the client to the list

    return clients_list # returning the list of the needed information


def getinfo():
    parser = optparse.OptionParser() #defining the parser. For argparse, parser = argparse.ArgumentParser()
    parser.add_option("-t", "--targetrange", dest="iprange") #getting the ip range. For argparse: parser.add_argument
    options,arguments = parser.parse_args() #defining the 2 variables. Argparse doesn't return arguments, only options.
    return options

def printresult(results_list):
    print("IP\t\t\tMAC Address\n---------------------------------------------")  # the \t gives a tab space, \n goes down a line
    for i in results_list:
        print(i["IP"] + "\t\t" + i["MAC"])

options = getinfo() #getting the information from the command line
scan_result = scan(options.iprange) #using the scan function with the command line options
printresult(scan_result) # calling the function to print the result from the scan_result function

