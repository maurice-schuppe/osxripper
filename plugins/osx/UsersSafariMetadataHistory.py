__author__ = 'osxripper'
__version__ = '0.1'
__license__ = 'GPLv3'
from riplib.Plugin import Plugin
import codecs
import logging
import os
import ccl_bplist


class UsersSafariMetadataHistory(Plugin):
    """
    Parse information from /Users/username/Library/Caches/Metadata/Safari/History/.tracked filenames.plist and list the *.webhistory files
    """

    def __init__(self):
        """
        Initialise the class.
        """
        super().__init__()
        self._name = "User Safari Web Bookmarks"
        self._description = "Parse information from /Users/username/Library/Caches/Metadata/Safari/History/.tracked filenames.plist and list the *.webhistory files"
        self._data_file = ""  # None as scanning through multiple files
        self._output_file = ""  # this will have to be defined per user account
        self._type = "multi"
    
    def parse(self):
        """
        Iterate over /Users directory and find user sub-directories
        """
        users_path = os.path.join(self._input_dir, "Users")
        # username = None
        if os.path.isdir(users_path):
            user_list = os.listdir(users_path)
            for username in user_list:
                if os.path.isdir(os.path.join(users_path, username)) and not username == "Shared":
                    plist_dir = os.path.join(users_path, username, "Library", "Caches", "Metadata", "Safari", "History")
                    if os.path.isdir(plist_dir):
                        self.__parse_bplist(plist_dir, username)
                    else:
                        logging.warning("{} does not exist.".format(plist_dir))
                        print("[WARNING] {} does not exist.".format(plist_dir))
        else:
            logging.warning("{} does not exist.".format(users_path))
            print("[WARNING] {} does not exist.".format(users_path))
            
    def __parse_bplist(self, file, username):
        """
        Parse /Users/username/Library/Caches/Metadata/Safari/History/.tracked filenames.plist and list the *.webhistory files
        """
        with codecs.open(os.path.join(self._output_dir, "Users_" + username + "_Safari_Metadata_History.txt"), "a", encoding="utf-8") as of:
            of.write("="*10 + " " + self._name + " " + "="*10 + "\r\n")
            of.write("Source Directory: {}\r\n\r\n".format(file))
            if self._os_version == "yosemite" or self._os_version == "mavericks" or self._os_version == "mountain_lion":
                plist_dir_list = os.listdir(file)
                if ".tracked filenames.plist" in plist_dir_list:
                    bplist = open(os.path.join(file, ".tracked filenames.plist"), "rb")
                    plist = ccl_bplist.load(bplist)
                    bplist.close()
                    try:
                        for key in plist:
                            of.write("Tracked URL    : {}\r\n".format(key))
                            of.write("Web Hitory File: {}\r\n".format(plist[key]))
                    except KeyError:
                        pass
                    of.write("\r\n")
                else:
                    logging.warning("File: .tracked filenames.plist does not exist or cannot be found.")
                    of.write("[WARNING] File: .tracked filenames.plist does not exist or cannot be found.\r\n")
                    print("[WARNING] File: .tracked filenames.plist does not exist or cannot be found.")    
                
                of.write("Web History Files:\r\n\r\n")
                for wh_file in plist_dir_list:
                    if wh_file.endswith(".webhistory"):
                        of.write("{}\r\n".format(wh_file))
            
            elif self._os_version == "lion":
                plist_dir_list = os.listdir(file)
                of.write("Web History Files:\r\n\r\n")
                for wh_file in plist_dir_list:
                    if wh_file.endswith(".webhistory"):
                        of.write("{}\r\n".format(wh_file))
                # logging.info("This version of OSX is not supported by this plugin.")
                # print("[INFO] This version of OSX is not supported by this plugin.")
                # of.write("[INFO] This version of OSX is not supported by this plugin.\r\n")
            elif self._os_version == "snow_leopard":
                logging.info("This version of OSX is not supported by this plugin.")
                print("[INFO] This version of OSX is not supported by this plugin.")
                of.write("[INFO] This version of OSX is not supported by this plugin.\r\n")
            else:
                logging.warning("Not a known OSX version.")
                print("[WARNING] Not a known OSX version.")
            of.write("="*40 + "\r\n\r\n")
        of.close()
