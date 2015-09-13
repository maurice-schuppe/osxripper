__author__ = 'osxripper'
__version__ = '0.1'
__license__ = 'GPLv3'

from riplib.Plugin import Plugin
import codecs
import logging
import os
import plistlib


class CupsPrintersPlist(Plugin):
    """
    Plugin to parse /Library/Preferences/org.cups.printers.plist
    """

    def __init__(self):
        """
        Initialise the class.
        """
        super().__init__()
        self._name = "Cups Printers"
        self._description = "Parse data from org.cups.printers.plist"
        self._data_file = "org.cups.printers.plist"
        self._output_file = "Printers.txt"
        self._type = "plist"
    
    def parse(self):
        """
        Parse /Library/Preferences/org.cups.printers.plist
        """
        with codecs.open(os.path.join(self._output_dir, self._output_file), "a", encoding="utf-8") as of:
            of.write("="*10 + " " + self._name + " " + "="*10 + "\r\n")
            plist_file = os.path.join(self._input_dir, "Library", "Preferences", self._data_file)
            of.write("Source File: {}\r\n\r\n".format(plist_file))
            if self._os_version == "yosemite" or self._os_version == "mavericks" or self._os_version == "mountain_lion"\
                    or self._os_version == "lion" or self._os_version == "snow_leopard":
                if os.path.isfile(plist_file):
                    with open(plist_file, "rb") as pl:
                        plist = plistlib.load(pl)  # ARRAY
                    try:
                        for printer in plist:
                            if "printer-name" in printer:
                                of.write("Printer Name          : {}\r\n".format(printer["printer-name"]))
                            if "printer-info" in printer:
                                of.write("Printer Info          : {}\r\n".format(printer["printer-info"]))
                            if "printer-is-accepting-jobs" in printer:  # BOOLEAN
                                of.write("Printer Accepting Jobs: {}\r\n".format(printer["printer-is-accepting-jobs"])) 
                            if "printer-location" in printer:
                                of.write("Printer Location      : {}\r\n".format(printer["printer-location"]))  # UNICODE STRING
                            if "printer-make-and-model" in printer:
                                of.write("Printer Make & Model  : {}\r\n".format(printer["printer-make-and-model"]))
                            if "printer-state" in printer:
                                of.write("Printer State         : {}\r\n".format(printer["printer-state"]))  # INTEGER
                            if "printer-state-reasons" in printer:  # ARRAY
                                of.write("Printer State Reasons:\r\n")
                                reasons = printer["printer-state-reasons"]
                                for reason in reasons:
                                    of.write("\t{}\r\n".format(reason))
                            if "printer-type" in printer:  # INTEGER
                                of.write("Printer Type          : {}\r\n".format(printer["printer-type"])) 
                            if "device-uri" in printer:
                                of.write("Device URI            : {}\r\n".format(printer["device-uri"]))
                    except KeyError:
                        pass
                else:
                    logging.warning("File: {} does not exist or cannot be found.\r\n".format(plist_file))
                    of.write("[WARNING] File: {} does not exist or cannot be found.\r\n".format(plist_file))
                    print("[WARNING] File: {} does not exist or cannot be found.\r\n".format(plist_file))
            else:
                logging.warning("Not a known OSX version.")
                print("[WARNING] Not a known OSX version.")
            of.write("="*40 + "\r\n\r\n")
        of.close()