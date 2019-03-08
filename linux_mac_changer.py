#!/usr/bin/env python

import subprocess
import optparse
import re

def get_arguments():
    parser = optparse.OptionParser() #defining the parser
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change its MAC") #adding an option for command line arguments
    parser.add_option("-m", "--mac", dest="new_mac", help="New MAC address")#adding an option for command line arguments
    (options, arguments) = parser.parse_args() #defining 2 variables based on the options give. Options is all we need, args is the list of left over arguments, for example if -i is defined but -m isnt
    if not options.interface:
        #code to handle error
        parser.error("Please specify an interface, use --help for more info")
    elif not options.new_mac:
        #code to handle error
        parser.error("Please specify a new MAC, use --help for more info")
    return options


def change_mac(interface,new_mac):
    print("Changing MAC address for " + interface + "to " + new_mac)
    subprocess.call(["ifconfig", interface, "down"]) #issuing commands to take the interface down to change mac
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac]) #changing the mac
    subprocess.call(["ifconfig", interface, "up"]) #putting the interface up

def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface]) #checking if the MAC actually changed, comparing the inputted mac with the new mac

    mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(ifconfig_result)) #searching for the mac in the ifconfig output

    if mac_address_search_result:
        return mac_address_search_result.group(0) #returning the mac it found in the inteface output
    else:
        print("Could not find a MAC address in this interface") #error handling


options=get_arguments() #getting the command line arguments
current_mac= get_current_mac(options.interface)#setting a global variable to the new mac
change_mac(options.interface,options.new_mac)#chaning the mac address
check_new_mac= get_current_mac(options.interface) #checking if it changed

if check_new_mac == options.new_mac: #if it changed print this
    print("Your MAC was changed successfully")
else: print("Your MAC was not changed successfully.")
