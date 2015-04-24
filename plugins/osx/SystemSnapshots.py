__author__ = 'osxripper'
__version__ = '0.1'
__license__ = 'GPLv3'
from riplib.Plugin import Plugin
import codecs
import logging
import os
import sqlite3


class SystemSnapshots(Plugin):
    """
    Parse information from /private/var/db/systemstats/snapshots.db
    """

    def __init__(self):
        """
        Initialise the class.
        """
        super().__init__()
        self._name = "System Snapshots"
        self._description = "Parse information from /private/var/db/systemstats/snapshots.db"
        self._data_file = "snapshots.db"
        self._output_file = "System_Snapshots.txt"
        self._type = "sqlite"
    
    def parse(self):
        """
        Read the /private/var/db/systemstats/snapshots.db SQLite database
        """
        with codecs.open(os.path.join(self._output_dir, self._output_file), "a", encoding="utf-8") as of:
            of.write("="*10 + " " + self._name + " " + "="*10 + "\r\n")
            query = "SELECT datetime(time/1000000, 'unixepoch'), pid, uniqueid, comm FROM snapshots ORDER BY time"
            file = os.path.join(self._input_dir, "private", "var", "db", "systemstats", self._data_file)
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
                                if row[3] is None:
                                    of.write("Comm     :\r\n")
                                else:
                                    of.write("Comm     : {}\r\n".format(row[3]))
                                if row[0] is None:
                                    of.write("Time     :\r\n")
                                else:
                                    of.write("Time     : {}\r\n".format(row[0]))
                                if row[1] is None:
                                    of.write("PID      :\r\n")
                                else:
                                    of.write("PID      : {}\r\n".format(row[1]))
                                if row[2] is None:
                                    of.write("Unique ID:\r\n")
                                else:
                                    of.write("Unique ID: {}\r\n".format(row[2]))
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
                    print("[WARNING] File: {} does not exist or cannot be found.\r\n".format(file))
                    
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