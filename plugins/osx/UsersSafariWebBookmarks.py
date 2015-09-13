__author__ = 'osxripper'
__version__ = '0.1'
__license__ = 'GPLv3'
from riplib.Plugin import Plugin
import codecs
import logging
import os
import ccl_bplist


class UsersSafariWebBookmarks(Plugin):
    """
    Parse information from /Users/username/Library/Caches/Metadata/Safari/Bookmarks/*.webbookmark
    """

    def __init__(self):
        """
        Initialise the class.
        """
        super().__init__()
        self._name = "User Safari Web Bookmarks"
        self._description = "Parse information from /Users/username/Library/Caches/Metadata/Safari/Bookmarks/*.webbookmark plists"
        self._data_file = ""  # None as scanning through multiple files
        self._output_file = ""  # this will have to be defined per user account
        self._type = "bplist"
    
    def parse(self):
        """
        Iterate over /Users directory and find user sub-directories
        """
        users_path = os.path.join(self._input_dir, "Users")
        if os.path.isdir(users_path):
            user_list = os.listdir(users_path)
            for username in user_list:
                if os.path.isdir(os.path.join(users_path, username)) and not username == "Shared":
                    plist_dir = os.path.join(users_path, username, "Library", "Caches", "Metadata", "Safari", "Bookmarks")
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
        Parse /Users/username/Library/Caches/Metadata/Safari/Bookmarks/*.webbookmark
        """
        with codecs.open(os.path.join(self._output_dir, "Users_" + username + "_Safari_Web_Bookmarks.txt"), "a", encoding="utf-8") as of:
            of.write("="*10 + " " + self._name + " " + "="*10 + "\r\n")
            of.write("Source Directory: {}\r\n\r\n".format(file))
            if self._os_version == "yosemite" or self._os_version == "mavericks" or self._os_version == "mountain_lion"\
                    or self._os_version == "lion" or self._os_version == "snow_leopard":
                plist_dir_list = os.listdir(file)
                for wb_file in plist_dir_list:
                    wb_plist = os.path.join(file, wb_file)
                    of.write("Bookmark Plist: {}\r\n".format(wb_plist))
                    if os.path.isfile(wb_plist):
                        bplist = open(wb_plist, "rb")
                        plist = ccl_bplist.load(bplist)
                        bplist.close()
                        try:
                            # Name
                            if "Name" in plist:
                                of.write("Name: {}\r\n".format(plist["Name"]))
                            # URL
                            if "URL" in plist:
                                of.write("URL: {}\r\n".format(plist["URL"]))
                        except KeyError:
                            pass
                        of.write("\r\n")
                    else:
                        logging.warning("File: {} does not exist or cannot be found.".format(file))
                        of.write("[WARNING] File: {} does not exist or cannot be found.\r\n".format(file))
                        print("[WARNING] File: {} does not exist or cannot be found.".format(file))
            else:
                logging.warning("Not a known OSX version.")
                print("[WARNING] Not a known OSX version.")
            of.write("="*40 + "\r\n\r\n")
        of.close()