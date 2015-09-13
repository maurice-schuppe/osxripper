__author__ = 'osxripper'
__version__ = '0.1'
__license__ = 'GPLv3'

from riplib.Plugin import Plugin
import codecs
import logging
import os
import plistlib


class InstallHistory(Plugin):
    """
    Plugin to list installed software from /Library/Receipts/InstallHistory.plist
    """
    
    def __init__(self):
        """
        Initialise the class.
        """
        super().__init__()
        self._name = "Install History"
        self._description = "Parse data from /Library/Receipts/InstallHistory.plist"
        self._data_file = "InstallHistory.plist"
        self._output_file = "InstallHistory.txt"
        self._type = "plist"

    def parse(self):
        """
        Parse /Library/Receipts/InstallHistory.plist
        """
        with codecs.open(os.path.join(self._output_dir, self._output_file), "a", encoding="utf-8") as of:
            of.write("="*10 + " " + self._name + " " + "="*10 + "\r\n")
            plist_file = os.path.join(self._input_dir, "Library", "Receipts", self._data_file)
            of.write("Source File: {}\r\n\r\n".format(plist_file))
            if self._os_version == "yosemite" or self._os_version == "mavericks" or self._os_version == "mountain_lion"\
                    or self._os_version == "lion" or self._os_version == "snow_leopard":
                if os.path.isfile(plist_file):
                    try:
                        with open(plist_file, "rb") as pl:
                            plist = plistlib.load(pl)
                        for item in plist:
                            if "contentType" in item:
                                of.write("Content Type       : {}\r\n".format(item["contentType"]))
                            if "displayName" in item:
                                of.write("Display Name       : {}\r\n".format(item["displayName"]))
                            if "displayVersion" in item:
                                of.write("Display Version    : {}\r\n".format(item["displayVersion"]))
                            if "date" in item:
                                of.write("Date               : {}\r\n".format(item["date"]))
                            if "processName" in item:
                                of.write("Process Name       : {}\r\n".format(item["processName"]))
                            if "packageIdentifiers" in item:  # Array
                                of.write("Package Identifiers:\r\n")
                                for packageItem in item["packageIdentifiers"]:
                                    of.write("\t{}\r\n".format(packageItem))
                            of.write("\r\n")
                    except KeyError:
                        pass
                else:
                    logging.warning("File: {} does not exist or cannot be found.\r\n".format(plist_file))
                    of.write("[WARNING] File: {} does not exist or cannot be found.\r\n".format(plist_file))
                    print("[WARNING] File: {} does not exist or cannot be found.".format(plist_file))
            else:
                logging.warning("Not a known OSX version.")
                print("[WARNING] Not a known OSX version.")
            of.write("="*40 + "\r\n\r\n")
        of.close()