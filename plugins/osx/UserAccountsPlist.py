__author__ = 'osxripper'
__version__ = '0.1'
__license__ = 'GPLv3'

from riplib.Plugin import Plugin
import codecs
import logging
import os
import ccl_bplist


class UserAccountsPlist(Plugin):
    """
    Plugin class to parse /private/var/db/dslocal/nodes/Default/users/<username>.plist
    """
    def __init__(self):
        """
        Initialise the class. N.B. in a full implementation of a class deriving from Plugin the self.* values should be changed.
        """
        super().__init__()
        self._name = "User Accounts"
        self._description = "Base class for plugins"
        self._output_file = "UserAccounts.txt"
        self._data_file = ""  # In this case multiple files are being searched for across different directories
        self._type = "bplist"
        
    def parse(self): 
        """
        Public function called to parse the data file set in __init__
        """
        working_dir = os.path.join(self._input_dir, "private", "var", "db", "dslocal", "nodes", "Default", "users")
        file_listing = os.listdir(working_dir)
        for f in file_listing:
            stat_info = os.stat(working_dir + os.path.sep + f)
            if f.endswith(".plist") and stat_info.st_size > 0:
                test_plist = os.path.join(working_dir, f)
                self.__parse_bplist(test_plist)

    def __parse_bplist(self, file):
        """
        Parse a User Account Binary Plist files
        """
        with codecs.open(os.path.join(self._output_dir, self._output_file), "a", encoding="utf-8") as of:
            if self._os_version == "yosemite" or self._os_version == "mavericks" or self._os_version == "mountain_lion":
                if os.path.isfile(file):
                    bplist = open(file, "rb")
                    pl = ccl_bplist.load(bplist)
                    bplist.close()
                    try:
                        if "home" in pl and "/Users" in pl["home"][0]:  # Only /Users
                            of.write("="*10 + " " + self._name + " " + "="*10 + "\r\n")
                            of.write("Source File: {}\r\n\r\n".format(file))
                            if "name" in pl:
                                of.write("Name          : {}\r\n".format(pl["name"][0]))
                            if "realname" in pl:
                                of.write("Real Name     : {}\r\n".format(pl["realname"][0]))
                            if "home" in pl:
                                of.write("Home          : {}\r\n".format(pl["home"][0]))
                            if "hint" in pl:
                                of.write("Password Hint : {}\r\n".format(pl["hint"][0]))
                            if "authentication_authority" in pl:
                                of.write("Authentication: {}\r\n".format(pl["authentication_authority"]))
                            if "uid" in pl:
                                of.write("UID           : {}\r\n".format(pl["uid"][0]))
                            if "gid" in pl:
                                of.write("GID           : {}\r\n".format(pl["gid"][0]))
                            if "generateduid" in pl:
                                of.write("Generated UID : {}\r\n".format(pl["generateduid"][0]))
                            if "shell" in pl:
                                of.write("Shell         : {}\r\n".format(pl["shell"][0]))
                            if "picture" in pl:
                                of.write("Picture       : {}\r\n".format(pl["picture"][0]))
                        else:
                            return
                    except KeyError:
                        pass
                else:
                    logging.warning("File: {} does not exist or cannot be found.".format(file))
                    of.write("[WARNING] File: {} does not exist or cannot be found.\r\n".format(file))
                    print("[WARNING] File: {} does not exist or cannot be found.".format(file))
            
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