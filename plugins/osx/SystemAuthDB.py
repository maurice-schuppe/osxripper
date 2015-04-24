__author__ = 'osxripper'
__version__ = '0.1'
__license__ = 'GPLv3'
from riplib.Plugin import Plugin
import codecs
import logging
import os
import sqlite3


class SystemAuthDB(Plugin):
    """
    Parse information from /private/var/db/auth.db
    """

    def __init__(self):
        """
        Initialise the class.
        """
        super().__init__()
        self._name = "System Auth DB"
        self._description = "Parse information from /private/var/db/auth.db"
        self._data_file = "auth.db"
        self._output_file = "System_Auth.txt"
        self._type = "sqlite"
    
    def parse(self):
        """
        Read the /private/var/db/auth.db SQLite database
        """
        with codecs.open(os.path.join(self._output_dir, self._output_file), "a", encoding="utf-8") as of:
            of.write("="*10 + " " + self._name + " " + "="*10 + "\r\n")
            query = "SELECT name, rules.'group', type, class, tries, version, kofn, datetime(created + 978307200, 'unixepoch'), " \
                    "datetime(modified + 978307200, 'unixepoch'), identifier, comment FROM rules ORDER BY name"
            file = os.path.join(self._input_dir, "private", "var", "db", self._data_file)
            of.write("Source File: {}\r\n\r\n".format(file))
            if self._os_version == "yosemite" or self._os_version == "mavericks":
                if os.path.isfile(file):
                    conn = None
                    try:
                        conn = sqlite3.connect(file)
                        with conn:    
                            cur = conn.cursor()
                            cur.execute(query)
                            rows = cur.fetchall()
                            for row in rows:
                                if row[0] is None:
                                    of.write("Name      :\r\n")
                                else:
                                    of.write("Name      : {}\r\n".format(row[0]))
                                if row[1] is None:
                                    of.write("Group     :\r\n")
                                else:
                                    of.write("Group     : {}\r\n".format(row[1]))
                                if row[2] is None:
                                    of.write("Type      :\r\n")
                                else:
                                    of.write("Type      : {}\r\n".format(row[2]))
                                if row[3] is None:
                                    of.write("Class     :\r\n")
                                else:
                                    of.write("Class     : {}\r\n".format(row[3]))
                                if row[4] is None:
                                    of.write("Tries     :\r\n")
                                else:
                                    of.write("Tries     : {}\r\n".format(row[4]))
                                if row[5] is None:
                                    of.write("Version   :\r\n")
                                else:
                                    of.write("Version   : {}\r\n".format(row[5]))
                                if row[6] is None:
                                    of.write("K-OF-N    :\r\n")
                                else:
                                    of.write("K-OF-N    : {}\r\n".format(row[6]))
                                if row[7] is None:
                                    of.write("Created   :\r\n")
                                else:
                                    of.write("Created   : {}\r\n".format(row[7]))
                                if row[8] is None:
                                    of.write("Modified  :\r\n")
                                else:
                                    of.write("Modified  : {}\r\n".format(row[8]))
                                if row[9] is None:
                                    of.write("Identifier:\r\n")
                                else:
                                    of.write("Identifier: {}\r\n".format(row[9]))
                                if row[10] is None:
                                    of.write("Comment   :\r\n")
                                else:
                                    of.write("Comment   : {}\r\n".format(row[10]))
                                of.write("\r\n")
                    except sqlite3.Error as e:
                        logging.error("{}".format(e.args[0]))
                        print("[ERROR] {}".format(e.args[0]))
                    finally:
                        if conn:
                            conn.close()
                else:
                    logging.warning("File: {} does not exist or cannot be found.\r\n".format(file))
                    of.write("[WARNING] File: {} does not exist or cannot be found.\r\n".format(file))
                    print("[WARNING] File: {} does not exist or cannot be found.".format(file))
                    
            elif self._os_version == "mountain_lion":
                logging.info("This version of OSX is not supported by this plugin.")
                print("[INFO] This version of OSX is not supported by this plugin.")
                of.write("[INFO] This version of OSX is not supported by this plugin.\r\n")
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