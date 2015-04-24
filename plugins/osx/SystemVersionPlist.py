__author__ = 'osxripper'
__version__ = '0.1'
__license__ = 'GPLv3'

from riplib.Plugin import Plugin
import codecs
import logging
import os
import plistlib


class SystemVersionPlist(Plugin):
    """
    Plugin to retrieve OSX version information
    """
    def __init__(self):
        """
        Initialise the class.
        """
        super().__init__()
        self._name = "System Version"
        self._description = "Get the OSX version from /System/Library/CoreServices/SystemVersion.plist"
        self._data_file = "SystemVersion.plist"
        self._output_file = "SystemVersion.txt"
        self._type = "plist"
        
    def parse(self): 
        """
        Parse SystemVersion.plist and write version information to file
        """
        with codecs.open(os.path.join(self._output_dir, self._output_file), "a", encoding="utf-8") as of:
            of.write("="*10 + " " + self._name + " " + "="*10 + "\r\n")
            plist_file = os.path.join(self._input_dir, "System", "Library", "CoreServices", self._data_file)
            of.write("Source File: {}\r\n\r\n".format(plist_file))
            if self._os_version == "yosemite" or self._os_version == "mavericks" or self._os_version == "mountain_lion":
                if os.path.isfile(plist_file):
                    try:
                        with open(plist_file, "rb") as pl:
                            plist = plistlib.load(pl)
                        if "ProductBuildVersion" in plist:
                            of.write("Product Build Version       : {}\r\n".format(plist["ProductBuildVersion"]))
                        if "ProductCopyright" in plist:
                            of.write("Product Copyright           : {}\r\n".format(plist["ProductCopyright"]))
                        if "ProductName" in plist:
                            of.write("Product Name                : {}\r\n".format(plist["ProductName"]))
                        if "ProductUserVisibleVersion" in plist:
                            of.write("Product User Visible Version: {}\r\n".format(plist["ProductUserVisibleVersion"]))
                        if "ProductVersion" in plist:
                            of.write("Product Version             : {}\r\n".format(plist["ProductVersion"]))
                    except KeyError:
                        pass
                else:
                    logging.warning("File: {} does not exist or cannot be found.\r\n".format(plist_file))
                    of.write("[WARNING] File: {} does not exist or cannot be found.\r\n".format(plist_file))
                    print("[WARNING] File: {} does not exist or cannot be found.".format(plist_file))
            
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