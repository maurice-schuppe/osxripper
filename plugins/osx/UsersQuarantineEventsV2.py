__author__ = 'osxripper'
__version__ = '0.1'
__license__ = 'GPLv3'
from riplib.Plugin import Plugin
import codecs
import datetime
import logging
import os
import sqlite3


class UsersQuarantineEventsV2(Plugin):
    """
    Parse information from /Users/<username>/Library/Preferences/com.apple.LaunchServices.QuarantineEventsV2
    """

    def __init__(self):
        """
        Initialise the class.
        """
        super().__init__()
        self._name = "User LaunchServices.QuarantineEventsV2"
        self._description = "Parse information from /Users/<username>/Library/Preferences/com.apple.LaunchServices.QuarantineEventsV2"
        self._data_file = "com.apple.LaunchServices.QuarantineEventsV2"
        self._output_file = ""  # this will have to be defined per user account
        self._type = "sqlite"
    
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
                    sqlite_db = os.path.join(users_path, username, "Library", "Preferences", self._data_file)
                    if os.path.isfile(sqlite_db):
                        self.__parse_sqlite_db(sqlite_db, username)
                    else:
                        logging.warning("{} does not exist.".format(sqlite_db))
                        print("[WARNING] {} does not exist.".format(sqlite_db))
        else:
            logging.warning("{} does not exist.".format(users_path))
            print("[WARNING] {} does not exist.".format(users_path))
    
    def __parse_sqlite_db(self, file, username):
        """
        Read the com.apple.LaunchServices.QuarantineEventsV2 SQLite database
        """
        with codecs.open(os.path.join(self._output_dir, "Users_" + username + "_Quarantine_Events.txt"), "a", encoding="utf-8") as of:
            of.write("="*10 + " " + self._name + " " + "="*10 + "\r\n")
            if self._os_version == "yosemite" or self._os_version == "mavericks" or self._os_version == "mountain_lion"\
                    or self._os_version == "lion":
                query = "SELECT * FROM LSQuarantineEvent"
                if os.path.isfile(file):
                    of.write("Source File: {}\r\n\r\n".format(file))
                    conn = None
                    try:
                        conn = sqlite3.connect(file)
                        with conn:    
                            cur = conn.cursor()
                            cur.execute(query)
                            rows = cur.fetchall()
                            for row in rows:
                                if row[0] is None:
                                    of.write("Event Identifier      :\r\n")
                                else:
                                    of.write("Event Identifier      : {}\r\n".format(row[0]))
                                if row[1] is None:
                                    of.write("Timestamp             :\r\n")
                                else:
                                    of.write("Timestamp             : {}\r\n".format(datetime.datetime.fromtimestamp(row[1] + 978307200)))
                                if row[2] is None:
                                    of.write("AgentBundle Identifier:\r\n")
                                else:
                                    of.write("AgentBundle Identifier: {}\r\n".format(row[2]))
                                if row[3] is None:
                                    of.write("Agent Name            :\r\n")
                                else:
                                    of.write("Agent Name            : {}\r\n".format(row[3]))
                                if row[4] is None:
                                    of.write("Data URL String       :\r\n")
                                else:                            
                                    of.write("Data URL String       : {}\r\n".format(row[4]))
                                if row[5] is None:
                                    of.write("Sender Name           :\r\n")
                                else:
                                    of.write("Sender Name           : {}\r\n".format(row[5]))
                                if row[6] is None:
                                    of.write("Sender Address        :\r\n")
                                else:
                                    of.write("Sender Address        : {}\r\n".format(row[6]))
                                if row[7] is None:
                                    of.write("Type Number           :\r\n")
                                else:
                                    of.write("Type Number           : {}\r\n".format(row[7]))
                                if row[8] is None:
                                    of.write("Origin Title          :\r\n")
                                else:
                                    of.write("Origin Title          : {}\r\n".format(row[8]))
                                if row[9] is None:
                                    of.write("Origin URL String     : \r\n")
                                else:
                                    of.write("Origin URL String     : {}\r\n".format(row[9]))
                                if row[10] is None:
                                    of.write("Origin Alias          :\r\n")
                                else:    
                                    of.write("Origin Alias          : {}\r\n".format(row[10]))
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
            
            # elif self._os_version == "lion":
            #     logging.info("This version of OSX is not supported by this plugin.")
            #     print("[INFO] This version of OSX is not supported by this plugin.")
            #     of.write("[INFO] This version of OSX is not supported by this plugin.\r\n")
            elif self._os_version == "snow_leopard":
                logging.info("This version of OSX is not supported by this plugin.")
                print("[INFO] This version of OSX is not supported by this plugin.")
                of.write("[INFO] This version of OSX is not supported by this plugin.\r\n")
            else:
                logging.warning("Not a known OSX version.")
                print("[WARNING] Not a known OSX version.")
            of.write("="*40 + "\r\n\r\n")
        of.close()