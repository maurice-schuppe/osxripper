__author__ = 'osxripper'
__version__ = '0.1'
__license__ = 'GPLv3'

from riplib.Plugin import Plugin
import codecs
import logging
import os


class Playlists(Plugin):
    """
    Plugin to list playlist files under /private/var/db/BootCaches
    """
    
    def __init__(self):
        """
        Initialise the class.
        """
        super().__init__()
        self._name = "Playlists"
        self._description = "List files in /private/var/db/BootCaches"
        self._data_file = ""  # listing directories so this is not needed
        self._output_file = "Playlists.txt"
        self._type = "dir_list"
    
    def parse(self):
        """
        List .playlist files under /private/var/db/BootCaches
        """
        with codecs.open(os.path.join(self._output_dir, self._output_file), "a", encoding="utf-8") as of:
            of.write("="*10 + " " + self._name + " " + "="*10 + "\r\n")
            if self._os_version == "yosemite" or self._os_version == "mavericks" or self._os_version == "mountain_lion":
                working_dir = os.path.join(self._input_dir, "private", "var", "db", "BootCaches")
                of.write("Source Directory: {}\r\n\r\n".format(working_dir))
                if os.path.isdir(working_dir):
                    file_listing = os.listdir(working_dir)
                    for f in file_listing:
                        test_file = os.path.join(working_dir, f)
                        if os.path.isdir(test_file):
                            of.write("Generated User ID: {}\r\n".format(f))
                            user_playlists = os.listdir(test_file)
                            for user_file in user_playlists:
                                of.write("\t{}\r\n".format(user_file))
                            of.write("\r\n")
                else:
                    logging.warning("Directory: {} does not exist or cannot be found.\r\n".format(working_dir))
                    of.write("[WARNING] Directory: {} does not exist or cannot be found.\r\n".format(working_dir))
                    print("[WARNING] Directory: {} does not exist or cannot be found.\r\n".format(working_dir))
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