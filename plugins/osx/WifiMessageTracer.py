__author__ = 'osxripper'
__version__ = '0.1'
__license__ = 'GPLv3'

from riplib.Plugin import Plugin
import codecs
import logging
import os
import plistlib


class WifiMessageTracer(Plugin):
    """
    Plugin to parse /Library/Preferences/SystemConfiguration/com.apple.wifi.message-tracer.plist
    """

    def __init__(self):
        """
        Initialise the class.
        """
        super().__init__()
        self._name = "Wifi Message Tracer"
        self._description = "Parse data from com.apple.wifi.message-tracer.plist"
        self._data_file = "com.apple.wifi.message-tracer.plist"
        self._output_file = "Networking.txt"
        self._type = "plist"
    
    def parse(self):
        """
        Parse /Library/Preferences/SystemConfiguration/com.apple.wifi.message-tracer.plist
        """
        with codecs.open(os.path.join(self._output_dir, self._output_file), "a", encoding="utf-8") as of:
            of.write("="*10 + " " + self._name + " " + "="*10 + "\r\n")
            plist_file = os.path.join(self._input_dir, "Library", "Preferences", "SystemConfiguration", self._data_file)
            of.write("Source File: {}\r\n\r\n".format(plist_file))
            if self._os_version == "yosemite":
                if os.path.isfile(plist_file):
                    with open(plist_file, "rb") as pl:
                        plist = plistlib.load(pl)
                    try:
                        # AssociationSSIDMap
                        if "AssociationSSIDMap" in plist:
                            of.write("AssociationSSIDMap:\r\n")
                            for asm_key in plist["AssociationSSIDMap"]:
                                of.write("\t{}: {}\r\n".format(asm_key, plist["AssociationSSIDMap"][asm_key]))
                            of.write("\r\n")
                        # InternalAssociationSSIDMap
                        if "InternalAssociationSSIDMap" in plist:
                            of.write("InternalAssociationSSIDMap:\r\n")
                            for iasm_key in plist["InternalAssociationSSIDMap"]:
                                of.write("\t{}: {}\r\n".format(iasm_key, plist["InternalAssociationSSIDMap"][iasm_key]))
                            of.write("\r\n")
                        # LastSubmissionTimestamp
                        if "LastSubmissionTimestamp" in plist:
                            of.write("Last Submission Timestamp: {}\r\n".format(plist["LastSubmissionTimestamp"]))
                            of.write("\r\n")
                        # PendingList
                        if "PendingList" in plist:
                            of.write("Pending List:\r\n")
                            pending_list = plist["PendingList"]  # list
                            # print len(pending_list)
                            for pending_list_item in pending_list:
                                for item_key in pending_list_item:
                                    # print type(pending_list_item[item_key])
                                    if isinstance(pending_list_item[item_key], str):
                                        of.write("\t{}: {}\r\n".format(item_key, pending_list_item[item_key]))
                                    else:
                                        of.write("\t{}: {}\r\n".format(item_key, pending_list_item[item_key]))
                                of.write("\r\n")
                        of.write("\r\n")
                    except KeyError:
                        pass
                else:
                    logging.warning("File: {} does not exist or cannot be found.\r\n".format(plist_file))
                    of.write("[WARNING] File: {} does not exist or cannot be found.\r\n".format(plist_file))
                    print("[WARNING] File: {} does not exist or cannot be found.".format(plist_file))
            elif self._os_version == "mavericks":
                if os.path.isfile(plist_file):
                    with open(plist_file, "rb") as pl:
                        plist = plistlib.load(pl)
                    try:
                        # LastSubmissionTimestamp
                        if "LastSubmissionTimestamp" in plist:
                            of.write("Last Submission Timestamp: {}\r\n".format(plist["LastSubmissionTimestamp"]))
                            of.write("\r\n")
                        # PendingList
                        if "PendingList" in plist:
                            of.write("Pending List:\r\n")
                            pending_list = plist["PendingList"]  # list
                            # print len(pending_list)
                            for pending_list_item in pending_list:
                                for item_key in pending_list_item:
                                    # print type(pending_list_item[item_key])
                                    if isinstance(pending_list_item[item_key], str):
                                        of.write("\t{}: {}\r\n".format(item_key, pending_list_item[item_key]))
                                    else:
                                        of.write("\t{}: {}\r\n".format(item_key, pending_list_item[item_key]))
                                of.write("\r\n")
                        of.write("\r\n")
                    except KeyError:
                        pass
                else:
                    logging.warning("File: {} does not exist or cannot be found.\r\n".format(plist_file))
                    of.write("[WARNING] File: {} does not exist or cannot be found.\r\n".format(plist_file))
                    print("[WARNING] File: {} does not exist or cannot be found.".format(plist_file))
            elif self._os_version == "mountain_lion":
                logging.info("This version of OSX is not supported by this plugin.")
                print("[INFO] This version of OSX is not supported by this plugin.")
                of.write("[INFO] This version of OSX is not supported by this plugin.\r\n")
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