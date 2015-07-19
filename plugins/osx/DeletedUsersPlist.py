__author__ = 'osxripper'
__version__ = '0.1'
__license__ = 'GPLv3'
from riplib.Plugin import Plugin
import codecs
import logging
import os
import ccl_bplist


class DeletedUsersPlist(Plugin):
    """
    Plugin to parse /Library/Preferences/com.apple.preferences.accounts.plist
    """
    
    def __init__(self):
        """
        Initialise plugins
        """
        super().__init__()
        self._name = "Deleted Users"
        self._description = "List deleted users"
        self._data_file = "com.apple.preferences.accounts.plist"
        self._output_file = "DeletedUsers.txt"
        self._type = "bplist"
        
    def parse(self):
        """
        Parse bplist com.apple.preferences.accounts.plist
        """
        with codecs.open(os.path.join(self._output_dir, self._output_file), "a", encoding="utf-8") as of:
            of.write("="*10 + " " + self._name + " " + "="*10 + "\r\n")
            file = os.path.join(self._input_dir, "Library", "Preferences", self._data_file)
            of.write("Source File: {}\r\n\r\n".format(file))
            if self._os_version == "yosemite" or self._os_version == "mavericks" or self._os_version == "mountain_lion"\
                    or self._os_version == "lion" or self._os_version == "snow_leopard":
                if os.path.isfile(file):
                    bplist = open(file, "rb")
                    pl = ccl_bplist.load(bplist)
                    try:
                        if "deletedUsers" in pl:
                            user_array = pl["deletedUsers"]
                            for user in user_array:
                                of.write("Real Name: {}\r\n".format(user["dsAttrTypeStandard:RealName"]))
                                of.write("Name     : {}\r\n".format(user["name"]))
                                of.write("Date     : {}\r\n".format(user["date"]))
                                of.write("UID      : {}\r\n".format(user["dsAttrTypeStandard:UniqueID"]))
                                of.write("\r\n")
                    except KeyError:
                        pass
                    bplist.close()
                else:
                    logging.warning("File: {} does not exist or cannot be found.".format(file))
                    of.write("[WARNING] File: {} does not exist or cannot be found.\r\n".format(file))
                    print("[WARNING] File: {} does not exist or cannot be found.".format(file))

            # elif self._os_version == "lion":
            #     logging.info("This version of OSX is not supported by this plugin.")
            #     print("[INFO] This version of OSX is not supported by this plugin.")
            #     of.write("[INFO] This version of OSX is not supported by this plugin.\r\n")
            # elif self._os_version == "snow_leopard":
            #     logging.info("This version of OSX is not supported by this plugin.")
            #     print("[INFO] This version of OSX is not supported by this plugin.")
            #     of.write("[INFO] This version of OSX is not supported by this plugin.\r\n")
            else:
                logging.warning("Not a known OSX version.")
                print("[WARNING] Not a known OSX version.")
            of.write("="*40 + "\r\n\r\n")
        of.close()