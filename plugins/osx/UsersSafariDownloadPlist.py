__author__ = 'osxripper'
__version__ = '0.1'
__license__ = 'GPLv3'
from riplib.Plugin import Plugin
import codecs
import logging
import os
import ccl_bplist


class UsersSafariDownloadPlist(Plugin):
    """
    Parse information from /Users/username/Library/Safari/Downloads.plist
    """

    def __init__(self):
        """
        Initialise the class.
        """
        super().__init__()
        self._name = "User Safari Download Plist"
        self._description = "Parse information from /Users/username/Library/Safari/Downloads.plist"
        self._data_file = "Downloads.plist"
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
                    plist = os.path.join(users_path, username, "Library", "Safari", self._data_file)
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
        Parse /Users/username/Library/Safari/Downloads.plist
        """
        with codecs.open(os.path.join(self._output_dir, "Users_" + username + "_Safari_Downloads.txt"), "a", encoding="utf-8") as of:
            of.write("="*10 + " " + self._name + " " + "="*10 + "\r\n")
            of.write("Source File: {}\r\n\r\n".format(file))
            if self._os_version == "yosemite":
                if os.path.isfile(file):
                    bplist = open(file, "rb")
                    plist = ccl_bplist.load(bplist)
                    try:
                        # DownloadHistory ARRAY of DICT
                        if "DownloadHistory" in plist:
                            of.write("Download History:\r\n")
                            for item in plist["DownloadHistory"]:
                                # DownloadEntryProgressBytesSoFar
                                of.write("\tProgress Bytes So Far : {}\r\n".format(item["DownloadEntryProgressBytesSoFar"]))
                                # DownloadEntryProgressTotalToLoad
                                of.write("\tProgress Total To Load: {}\r\n".format(item["DownloadEntryProgressTotalToLoad"]))
                                # DownloadEntryDateAddedKey
                                of.write("\tDate Added Key        : {}\r\n".format(item["DownloadEntryDateAddedKey"]))
                                # DownloadEntryDateFinishedKey
                                of.write("\tDate Finished Key     : {}\r\n".format(item["DownloadEntryDateFinishedKey"]))
                                # DownloadEntryIdentifier
                                of.write("\tIdentifier            : {}\r\n".format(item["DownloadEntryIdentifier"]))
                                # DownloadEntryURL
                                of.write("\tURL                   : {}\r\n".format(item["DownloadEntryURL"]))
                                # DownloadEntryRemoveWhenDoneKey
                                of.write("\tRemove When Done Key  : {}\r\n".format(item["DownloadEntryRemoveWhenDoneKey"]))
                                # DownloadEntryPath
                                of.write("\tPath                  : {}\r\n".format(item["DownloadEntryPath"]))
                                of.write("\r\n")
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
                        # DownloadHistory
                        if "DownloadHistory" in plist:
                            of.write("Download History:\r\n")
                            for item in plist["DownloadHistory"]:
                                # DownloadEntryIdentifier
                                of.write("\tIdentifier            : {}\r\n".format(item["DownloadEntryIdentifier"]))
                                # DownloadEntryURL
                                of.write("\tURL                   : {}\r\n".format(item["DownloadEntryURL"]))
                                # DownloadEntryProgressTotalToLoad
                                of.write("\tProgress Total To Load: {}\r\n".format(item["DownloadEntryProgressTotalToLoad"]))
                                # DownloadEntryProgressBytesSoFar
                                of.write("\tProgress Bytes So Far : {}\r\n".format(item["DownloadEntryProgressBytesSoFar"]))
                                # DownloadEntryPath
                                of.write("\tPath                  : {}\r\n".format(item["DownloadEntryPath"]))
                                of.write("\r\n")
                    except KeyError:
                        pass
                    bplist.close()
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