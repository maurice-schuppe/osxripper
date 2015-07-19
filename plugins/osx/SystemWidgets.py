__author__ = 'osxripper'
__version__ = '0.1'
__license__ = 'GPLv3'

from riplib.Plugin import Plugin
import codecs
import logging
import os


class SystemWidgets(Plugin):
    """
    Plugin to list .wdgt directories in /Library/Widgets"
    """
    
    def __init__(self):
        """
        Initialise the class.
        """
        super().__init__()
        self._name = "System Widgets"
        self._description = "List .wdgt directories in /Library/Widgets"
        self._data_file = ""  # listing directories so this is not needed
        self._output_file = "SystemWidgets.txt"
        self._type = "dir_list"
    
    def parse(self):
        """
        List .wdgt files under /Library/Widgets
        """
        with codecs.open(os.path.join(self._output_dir, self._output_file), "a", encoding="utf-8") as of:
            of.write("="*10 + " " + self._name + " " + "="*10 + "\r\n")
            working_dir = os.path.join(self._input_dir, "Library", "Widgets")
            of.write("Source Directory: {}\r\n\r\n".format(working_dir))
            if self._os_version == "yosemite" or self._os_version == "mavericks" or self._os_version == "mountain_lion"\
                    or self._os_version == "lion" or self._os_version == "snow_leopard":
                if os.path.isdir(working_dir):
                    file_listing = os.listdir(working_dir)
                    for f in file_listing:
                        if f.endswith(".wdgt"):
                            of.write(f + "\r\n")
                    of.write("\r\n")
                else:
                    logging.warning("Directory: {} does not exist or cannot be found.\r\n".format(working_dir))
                    of.write("[WARNING] Directory: {} does not exist or cannot be found.\r\n".format(working_dir))
                    print("[WARNING] Directory: {} does not exist or cannot be found.\r\n".format(working_dir))
            
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