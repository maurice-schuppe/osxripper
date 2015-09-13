__author__ = 'osxripper'
__version__ = '0.1'
__license__ = 'GPLv3'
from riplib.Plugin import Plugin
import codecs
import logging
import os
import ccl_bplist


class DiagnosticReportingNetworksNew(Plugin):
    """
    Plugin to parse /Library/Caches/com.apple.DiagnosticReporting.Networks.New.plist
    """
    def __init__(self):
        """
        Initialise plugins
        """
        super().__init__()
        self._name = "DiagnosticReporting.Networks.New"
        self._description = "Parse DHCP Lease plists from /Library/Caches/com.apple.DiagnosticReporting.Networks.New.plist"
        self._data_file = "com.apple.DiagnosticReporting.Networks.New.plist"
        self._output_file = "Networking.txt"
        self._type = "bplist"
        
    def parse(self):
        with codecs.open(os.path.join(self._output_dir, self._output_file), "a", encoding="utf-8") as of:
            of.write("="*10 + " " + self._name + " " + "="*10 + "\r\n")
            if self._os_version == "yosemite":
                file = os.path.join(self._input_dir, "Library", "Caches", self._data_file)
                of.write("Source File: {}\r\n\r\n".format(file))
                if os.path.isfile(file):
                    bplist = open(file, "rb")
                    pl = ccl_bplist.load(bplist)
                    try:
                        if "ExternalSignatures" in pl:
                            for ext_sig in pl["ExternalSignatures"]:
                                of.write("Network Data: {}\r\n".format(ext_sig))
                                of.write("Timestamp: {}\r\n".format(pl["ExternalSignatures"][ext_sig]))
                    except KeyError:
                        pass
                    bplist.close()
                else:
                    logging.warning("File: {} does not exist or cannot be found.\r\n".format(file))
                    of.write("[WARNING] File: {} does not exist or cannot be found.\r\n".format(file))
                    print("[WARNING] File: {} does not exist or cannot be found.\r\n".format(file))
            elif self._os_version == "mavericks":
                logging.info("This version of OSX is not supported by this plugin.")
                print("[INFO] This version of OSX is not supported by this plugin.")
                of.write("[INFO] This version of OSX is not supported this plugin.\r\n")
            elif self._os_version == "mountain_lion":
                logging.info("This version of OSX is not supported this plugin.")
                print("[INFO] This version of OSX is not supported this plugin.")
                of.write("[INFO] This version of OSX is not supported this plugin.\r\n")
            elif self._os_version == "lion":
                logging.info("This version of OSX is not supported this plugin.")
                print("[INFO] This version of OSX is not supported this plugin.")
                of.write("[INFO] This version of OSX is not supported this plugin.\r\n")
            elif self._os_version == "snow_leopard":
                logging.info("This version of OSX is not supported this plugin.")
                print("[INFO] This version of OSX is not supported this plugin.")
                of.write("[INFO] This version of OSX is not supported this plugin.\r\n")
            else:
                logging.warning("Not a known OSX version.")
                print("[WARNING] Not a known OSX version.")
            of.write("="*40 + "\r\n\r\n")
        of.close()