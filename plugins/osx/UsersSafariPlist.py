__author__ = 'osxripper'
__version__ = '0.1'
__license__ = 'GPLv3'
from riplib.Plugin import Plugin
import codecs
import logging
import os
import ccl_bplist


class UsersSafariPlist(Plugin):
    """
    Parse information from /Users/username/Library/Preferences/com.apple.Safari.plist
    """

    def __init__(self):
        """
        Initialise the class.
        """
        super().__init__()
        self._name = "User Safari Plist"
        self._description = "Parse information from /Users/username/Library/Preferences/com.apple.Safari.plist"
        self._data_file = "com.apple.Safari.plist"
        self._output_file = ""  # this will have to be defined per user account
        self._type = "bplist"
    
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
                    plist = os.path.join(users_path, username, "Library", "Preferences", self._data_file)
                    if os.path.isfile(plist):
                        self.__parse_bplist(plist, username)
                    else:
                        logging.warning("{} does not exist.".format(plist))
                        print("[WARNING] {} does not exist.".format(plist))
        else:
            logging.warning("{} does not exist.".format(users_path))
            print("[WARNING] {} does not exist.".format(users_path))
            
    def __parse_bplist(self, file, username):
        """
        Parse /Users/username/Library/Preferences/com.apple.finder.plist
        """
        with codecs.open(os.path.join(self._output_dir, "Users_" + username + "_Safari.txt"), "a", encoding="utf-8") as of:
            of.write("="*10 + " " + self._name + " " + "="*10 + "\r\n")
            of.write("Source File: {}\r\n\r\n".format(file))
            if self._os_version == "yosemite":
                if os.path.isfile(file):
                    bplist = open(file, "rb")
                    plist = ccl_bplist.load(bplist)
                    try:
                        # RecentWebSearches ARRAY of DICT
                        if "RecentWebSearches" in plist:
                            of.write("Recent Web Searches:\r\n")
                            for rws in plist["RecentWebSearches"]:
                                of.write("\tSearch String: {}\r\n".format(rws["SearchString"]))
                                of.write("\tSearch Date  : {}\r\n\r\n".format(rws["Date"]))
                                
                        # LocalFileRestrictionsEnabled
                        if "LocalFileRestrictionsEnabled" in plist:
                            of.write("Local File Restrictions Enabled: {}\r\n".format(plist["LocalFileRestrictionsEnabled"]))
                        # CachedBookmarksFileSize
                        if "CachedBookmarksFileSize" in plist:
                            of.write("Cached Bookmarks File Size     : {}\r\n".format(plist["CachedBookmarksFileSize"]))
                        # ExtensionsEnabled
                        if "ExtensionsEnabled" in plist:
                            of.write("Extensions Enabled             : {}\r\n".format(plist["ExtensionsEnabled"]))
                        # DownloadsPath
                        if "DownloadsPath" in plist:
                            of.write("Downloads Path                 : {}\r\n".format(plist["DownloadsPath"]))
                    except KeyError:
                        pass
                    bplist.close()
                else:
                    logging.warning("File: {} does not exist or cannot be found.".format(file))
                    of.write("[WARNING] File: {} does not exist or cannot be found.\r\n".format(file))
                    print("[WARNING] File: {} does not exist or cannot be found.".format(file))
            elif self._os_version == "mavericks" or self._os_version == "mountain_lion":
                if os.path.isfile(file):
                    bplist = open(file, "rb")
                    plist = ccl_bplist.load(bplist)
                    try:
                        # RecentSearchStrings ARRAY of STRING
                        if "RecentSearchStrings" in plist:
                            of.write("Recent Search Strings:\r\n")
                            for search_string in plist["RecentSearchStrings"]:
                                of.write("\t{}\r\n".format(search_string))
                            of.write("\r\n")
                        # DownloadsPath
                        if "DownloadsPath" in plist:
                            of.write("Downloads Path                 : {}\r\n".format(plist["DownloadsPath"]))
                        # LocalFileRestrictionsEnabled
                        if "LocalFileRestrictionsEnabled" in plist:
                            of.write("Local File Restrictions Enabled: {}\r\n".format(plist["LocalFileRestrictionsEnabled"]))
                        # CachedBookmarksFileSize
                        if "CachedBookmarksFileSize" in plist:
                            of.write("Cached Bookmarks File Size     : {}\r\n".format(plist["CachedBookmarksFileSize"]))
                    except KeyError:
                        pass
                    bplist.close()
                else:
                    logging.warning("File: {} does not exist or cannot be found.".format(file))
                    of.write("[WARNING] File: {} does not exist or cannot be found.\r\n".format(file))
                    print("[WARNING] File: {} does not exist or cannot be found.".format(file))

            elif self._os_version == "lion":
                if os.path.isfile(file):
                    bplist = open(file, "rb")
                    plist = ccl_bplist.load(bplist)
                    try:
                        # RecentSearchStrings ARRAY of STRING
                        if "RecentSearchStrings" in plist:
                            of.write("Recent Search Strings:\r\n")
                            for search_string in plist["RecentSearchStrings"]:
                                of.write("\t{}\r\n".format(search_string))
                            of.write("\r\n")
                        # DownloadsPath
                        if "DownloadsPath" in plist:
                            of.write("Downloads Path                 : {}\r\n".format(plist["DownloadsPath"]))
                        # LocalFileRestrictionsEnabled
                        # if "LocalFileRestrictionsEnabled" in plist:
                        #     of.write("Local File Restrictions Enabled: {}\r\n".format(plist["LocalFileRestrictionsEnabled"]))
                        # CachedBookmarksFileSize
                        if "CachedBookmarksFileSize" in plist:
                            of.write("Cached Bookmarks File Size     : {}\r\n".format(plist["CachedBookmarksFileSize"]))
                    except KeyError:
                        pass
                    bplist.close()
                else:
                    logging.warning("File: {} does not exist or cannot be found.".format(file))
                    of.write("[WARNING] File: {} does not exist or cannot be found.\r\n".format(file))
                    print("[WARNING] File: {} does not exist or cannot be found.".format(file))
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