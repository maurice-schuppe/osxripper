__author__ = 'osxripper'
__version__ = '0.1'
__license__ = 'GPLv3'

from riplib.Plugin import Plugin
import codecs
import logging
import os


class Autoruns(Plugin):
    """
    Plugin to list autoruns
    """
    def __init__(self):
        """
        Initialise the class.
        """
        super().__init__()
        self._name = "Autoruns"
        self._description = "List files in System amd Library Launch* directories "
        self._data_file = ""  # listing directories so this is not needed
        self._output_file = "Autoruns.txt"
        self._type = "dir_list"
    
    def parse(self):
        """
        List contents of known Launch* directories
        """
        with codecs.open(os.path.join(self._output_dir, self._output_file), "a", encoding="utf-8") as of:
            if self._os_version == "yosemite" or self._os_version == "mavericks" or self._os_version == "mountain_lion":
                sys_lib_launch_agents = os.path.join(self._input_dir, "System", "Library", "LaunchAgents")
                sys_lib_launch_daemons = os.path.join(self._input_dir, "System", "Library", "LaunchDaemons")
                sys_lib_startup_items = os.path.join(self._input_dir, "System", "Library", "StartupItems")
                lib_launch_agents = os.path.join(self._input_dir, "Library", "LaunchAgents")
                lib_launch_daemons = os.path.join(self._input_dir, "Library", "LaunchDaemons")
                lib_startup_items = os.path.join(self._input_dir, "Library", "StartupItems")
                collected_directories = [sys_lib_launch_agents, sys_lib_launch_daemons, sys_lib_startup_items,
                                         lib_launch_agents, lib_launch_daemons, lib_startup_items]
                for doi in collected_directories:
                    if os.path.isdir(doi):
                        of.write("="*10 + " Autoruns: " + doi.replace(self._input_dir, "") + "="*10 + "\r\n")
                        of.write("Source Directory: {}\r\n\r\n".format(doi))
                        file_listing = os.listdir(doi)
                        for f in file_listing:
                            of.write("\t{}\r\n".format(f))
                    else:
                        logging.warning("Directory {} does not exist.".format(doi))
                        of.write("[WARNING] Directory {} does not exist or cannot be found.\r\n".format(doi))
                        print("[WARNING] Directory {} does not exist.".format(doi))

            elif self._os_version == "lion":
                logging.info("This version of OSX is not supported by this plugin.")
                print("[INFO] This version of OSX is not supported by this plugin.")
                of.write("[INFO] This version of OSX is not supported by this plugin.\r\n")
            elif self._os_version == "snow_leopard":
                logging.info("This version of OSX is not supported by this plugin.")
                print("[INFO] This version of OSX is not supported by this plugin.")
                of.write("[INFO] This version of OSX is not supported by this plugin.\r\n")
            else:
                logging.warning("[WARNING] Not a known OSX version.")
                print("[WARNING] Not a known OSX version.")
            of.write("="*40 + "\r\n\r\n")
        of.close()