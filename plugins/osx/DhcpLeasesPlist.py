__author__ = 'osxripper'
__version__ = '0.1'
__license__ = 'GPLv3'
from riplib.Plugin import Plugin
# import base64
import binascii
import codecs
import logging
import os
import plistlib


class DhcpLeasesPlist(Plugin):
    """
    Plugin to parse DHCP plists in /private/var/db/dhcpclient/leases/en
    """
    
    def __init__(self):
        """
        Initialise plugins
        """
        super().__init__()
        self._name = "DHCP Leases"
        self._description = "Parse DHCP Lease plists from /private/var/db/dhcpclient/leases/en"
        self._data_file = ""  # Empty as parsing multiple files
        self._output_file = "Networking.txt"
        self._type = "plist"
        
    def parse(self):
        """
        Parse DHCP plists in /private/var/db/dhcpclient/leases/en
        """
        working_dir = os.path.join(self._input_dir, "private", "var", "db", "dhcpclient", "leases")
        if os.path.isdir(working_dir):
            file_listing = os.listdir(working_dir)
            for f in file_listing:
                self.__parse_plist(os.path.join(working_dir, f))
        else:
            with codecs.open(os.path.join(self._output_dir, self._output_file), "a", encoding="utf-8") as of:
                of.write("="*10 + " " + self._name + " " + "="*10 + "\r\n")
                of.write("[WARNING] File: {} does not exist or cannot be found.\r\n".format(working_dir))
                of.write("="*40 + " " + "\r\n\r\n")
            of.close()
            logging.warning("File: {} does not exist or cannot be found.".format(working_dir))
            print("[WARNING] File: {} does not exist or cannot be found.".format(working_dir))
    
    def __parse_plist(self, file):
        """
        Parse the plist
        """
        with codecs.open(os.path.join(self._output_dir, self._output_file), "a", encoding="utf-8") as of:
            of.write("="*10 + " " + self._name + " " + "="*10 + "\r\n")
            of.write("Source File: {}\r\n\r\n".format(file))
            if self._os_version == "yosemite" or self._os_version == "mavericks" or self._os_version == "mountain_lion":
                try:
                    with open(file, "rb") as pl:
                        plist = plistlib.load(pl)
                    if "IPAddress" in plist:
                        of.write("IP Address: {}\r\n".format(plist["IPAddress"]))
                    if "LeaseLength" in plist:
                        of.write("Lease Length: {}\r\n".format(plist["LeaseLength"]))
                    if "LeaseStartDate" in plist:
                        of.write("Lease Start Date: {}\r\n".format(plist["LeaseStartDate"]))
                    if "RouterHardwareAddress" in plist:
                        # TODO sort out binary string output into MAC address format
                        of.write("Router Hardware Address: {}\r\n".format(binascii.hexlify(plist["RouterHardwareAddress"])))
                    if "RouterIPAddress" in plist:
                        of.write("Router IP Address: {}\r\n".format(plist["RouterIPAddress"]))
                except KeyError:
                    pass

            elif self._os_version == "lion":
                logging.info("This version of OSX is not supported by this plugin.")
                print("[INFO] This version of OSX is not supported by this plugin.")
                of.write("[INFO] This version of OSX is not supported by this plugin.\r\n")
            elif self._os_version == "snow_leopard":
                logging.info("This version of OSX is not supported by this plugin.")
                print("[INFO] This version of OSX is not supported by this plugin.")
                of.write("[INFO] This version of OSX is not supported by this plugin.\r\n")
            else:
                logging.warning("Not a known OSX version.")
                print("[WARNING] Not a known OSX version.")
            of.write("="*40 + "\r\n\r\n")
        of.close()