__author__ = 'osxripper'
__version__ = '0.1'
__license__ = 'GPLv3'
from riplib.Plugin import Plugin
import codecs
import logging
import os
import plistlib


class SmbServer(Plugin):
    """
    Plugin to parse /Library/Preferences/SystemConfiguration/com.apple.smb.server.plist
    """
    
    def __init__(self):
        """
        Initialise the class.
        """
        super().__init__()
        self._name = "SMB Server"
        self._description = "Parse data from com.apple.smb.server.plist"
        self._data_file = "com.apple.smb.server.plist"
        self._output_file = "Networking.txt"
        self._type = "plist"
        
    def parse(self):
        """
        Parse /Library/Preferences/SystemConfiguration/com.apple.smb.server.plist
        """
        with codecs.open(os.path.join(self._output_dir, self._output_file), "a", encoding="utf-8") as of:
            of.write("="*10 + " " + self._name + " " + "="*10 + "\r\n")
            plist_file = os.path.join(self._input_dir, "Library", "Preferences", "SystemConfiguration", self._data_file)
            of.write("Source File: {}\r\n\r\n".format(plist_file))
            if self._os_version == "yosemite" or self._os_version == "mavericks" or self._os_version == "mountain_lion" \
                    or self._os_version == "lion" or self._os_version == "snow_leopard":
                if os.path.isfile(plist_file):
                    try:
                        with open(plist_file, "rb") as pl:
                            plist = plistlib.load(pl)
                        if "ServerDescription" in plist:
                            of.write("Server Description  : {}\r\n".format(plist["ServerDescription"]))
                        if "NetBIOSName" in plist:
                            of.write("Net BIOS Name       : {}\r\n".format(plist["NetBIOSName"]))
                        if "DOSCodePage" in plist:
                            of.write("DOS Code Page       : {}\r\n".format(plist["DOSCodePage"]))
                        if "LocalKerberosRealm" in plist:
                            of.write("Local Kerberos Realm: {}\r\n".format(plist["LocalKerberosRealm"]))
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