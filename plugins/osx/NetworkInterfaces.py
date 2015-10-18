__author__ = 'osxripper'
__version__ = '0.1'
__license__ = 'GPLv3'

from riplib.Plugin import Plugin
import binascii
import codecs
import logging
import os
import plistlib


class NetworkInterfaces(Plugin):
    """
    Plugin to parse /Library/Preferences/SystemConfiguration/NetworkInterfaces.plist
    """

    def __init__(self):
        """
        Initialise the class.
        """
        super().__init__()
        self._name = "Network Interfaces"
        self._description = "Parse data from NetworkInterfaces.plist"
        self._data_file = "NetworkInterfaces.plist"
        self._output_file = "Networking.txt"
        self._type = "plist"
    
    def parse(self):
        """
        Parse /Library/Preferences/SystemConfiguration/NetworkInterfaces.plist
        """
        with codecs.open(os.path.join(self._output_dir, self._output_file), "a", encoding="utf-8") as of:
            of.write("="*10 + " " + self._name + " " + "="*10 + "\r\n")
            plist_file = os.path.join(self._input_dir, "Library", "Preferences", "SystemConfiguration", self._data_file)
            of.write("Source File: {}\r\n\r\n".format(plist_file))
            if self._os_version == "el_capitan" or self._os_version == "yosemite" or self._os_version == "mavericks":
                if os.path.isfile(plist_file):
                    with open(plist_file, "rb") as pl:
                        plist = plistlib.load(pl)
                    try:
                        if "Interfaces" in plist:
                            network_interfaces = plist["Interfaces"]
                            for network_interface in network_interfaces:
                                if "Active" in network_interface:
                                    of.write("Active                   : {}\r\n".format(network_interface["Active"]))
                                if "BSD Name" in network_interface:
                                    of.write("BSD Name                 : {}\r\n".format(network_interface["BSD Name"]))
                                if "IOBuiltin" in network_interface:
                                    of.write("IOBuiltin                : {}\r\n".format(network_interface["IOBuiltin"]))
                                if "IOInterfaceNamePrefix" in network_interface:
                                    of.write("IO Interface Name Prefix : {}\r\n".format(network_interface["IOInterfaceNamePrefix"]))
                                if "IOInterfaceType" in network_interface:
                                    of.write("IO Interface Type        : {}\r\n".format(network_interface["IOInterfaceType"]))
                                if "IOInterfaceUnit" in network_interface:
                                    of.write("IO Interface Unit        : {}\r\n".format(network_interface["IOInterfaceUnit"]))
                                if "IOMACAddress" in network_interface:
                                    # data = plistlib.Data.asBase64(network_interface["IOMACAddress"])
                                    # of.write("IO MAC Address           : {}\r\n".format(binascii.hexlify(base64.b64decode(data))))
                                    of.write("IO MAC Address           : {}\r\n".format(binascii.hexlify(network_interface["IOMACAddress"])))
                                if "SCNetworkInterfaceInfo" in network_interface:
                                    of.write("SC Network Interface Info: {}\r\n".format(network_interface["SCNetworkInterfaceInfo"]["UserDefinedName"]))
                                if "SCNetworkInterfaceType" in network_interface:
                                    of.write("SC Network Interface Type: {}\r\n".format(network_interface["SCNetworkInterfaceType"]))
                                of.write("\r\n")
################################
# Move to own Plugin?
                        if "Model" in plist:
                            of.write("Model: {}\r\n".format(plist["Model"]))
################################
                    except KeyError:
                        pass
                else:
                    logging.warning("File: {} does not exist or cannot be found.\r\n".format(plist_file))
                    of.write("[WARNING] File: {} does not exist or cannot be found.\r\n".format(plist_file))
                    print("[WARNING] File: {} does not exist or cannot be found.".format(plist_file))
            elif self._os_version == "mountain_lion" or self._os_version == "lion" or self._os_version == "snow_leopard":
                if os.path.isfile(plist_file):
                    with open(plist_file, "rb") as pl:
                        plist = plistlib.load(pl)
                    try:
                        if "Interfaces" in plist:
                            network_interfaces = plist["Interfaces"]
                            for network_interface in network_interfaces:
                                if "Active" in network_interface:
                                    of.write("Active                   : {}\r\n".format(network_interface["Active"]))
                                if "BSD Name" in network_interface:
                                    of.write("BSD Name                 : {}\r\n".format(network_interface["BSD Name"]))
                                if "IOBuiltin" in network_interface:
                                    of.write("IOBuiltin                : {}\r\n".format(network_interface["IOBuiltin"]))
                                if "IOInterfaceType" in network_interface:
                                    of.write("IO Interface Type        : {}\r\n".format(network_interface["IOInterfaceType"]))
                                if "IOInterfaceUnit" in network_interface:
                                    of.write("IO Interface Unit        : {}\r\n".format(network_interface["IOInterfaceUnit"]))
                                if "IOMACAddress" in network_interface:
                                    # data = plistlib.Data.asBase64(network_interface["IOMACAddress"])
                                    # of.write("IO MAC Address           : {}\r\n".format(binascii.hexlify(base64.b64decode(data))))
                                    of.write("IO MAC Address           : {}\r\n".format(binascii.hexlify(network_interface["IOMACAddress"])))
                                if "SCNetworkInterfaceInfo" in network_interface:
                                    of.write("SC Network Interface Info: {}\r\n".format(network_interface["SCNetworkInterfaceInfo"]["UserDefinedName"]))
                                if "SCNetworkInterfaceType" in network_interface:
                                    of.write("SC Network Interface Type: {}\r\n".format(network_interface["SCNetworkInterfaceType"]))
                                of.write("\r\n")
################################
# Move to own Plugin?
                        if "Model" in plist:
                            of.write("Model: {}\r\n".format(plist["Model"]))
################################
                    except KeyError:
                        pass
                    # except Error as e:
                    #     logging.error("{}".format(e.args[0]))
                    #     print("[ERROR] {}".format(e.args[0]))
                else:
                    logging.warning("File: {} does not exist or cannot be found.\r\n".format(plist_file))
                    of.write("[WARNING] File: {} does not exist or cannot be found.\r\n".format(plist_file))
                    print("[WARNING] File: {} does not exist or cannot be found.".format(plist_file))
            else:
                logging.warning("Not a known OSX version.")
                print("[WARNING] Not a known OSX version.")
            of.write("="*40 + "\r\n\r\n")
        of.close()