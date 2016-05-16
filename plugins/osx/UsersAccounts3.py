from riplib.Plugin import Plugin
import codecs
import logging
import os
import sqlite3
__author__ = 'osxripper'
__version__ = '0.1'
__license__ = 'GPLv3'


class UsersAccounts3(Plugin):
    """
    Parse information from /Users/<username>/Library/Accounts/Accounts3.sqlite
    """

    def __init__(self):
        """
        Initialise the class.
        """
        super().__init__()
        self._name = "Users Accounts"
        self._description = "Parse information from /Users/<username>/Library/Accounts/Accounts3.sqlite"
        self._data_file = "Accounts3.sqlite"
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
                    sqlite_db = os.path.join(users_path, username, "Library", "Accounts", self._data_file)
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
        Read the Accounts3.sqlite SQLite database
        """
        with codecs.open(os.path.join(self._output_dir, "Users_" + username + ".txt"), "a", encoding="utf-8") as of:
            of.write("="*10 + " " + self._name + " " + "="*10 + "\r\n")
            of.write("Source File: {}\r\n\r\n".format(file))
            if self._os_version == "el_capitan" or self._os_version == "yosemite":
                query = "SELECT zusername,zactive,zauthenticated,zvisible,datetime(zdate + 978307200, 'unixepoch')," \
                        "zaccountdescription,zowningbundleid FROM zaccount"
                conn = None
                try:
                    conn = sqlite3.connect(file)
                    with conn:    
                        cur = conn.cursor()
                        cur.execute(query)
                        rows = cur.fetchall()
                        if len(rows) != 0:
                            for row in rows:
                                # zusername
                                if row[0] is None:
                                    of.write("Username           :\r\n")
                                else:
                                    of.write("Username           : {}\r\n".format(row[0]))
                                # zactive
                                if row[1] is None:
                                    of.write("Active             :\r\n")
                                else:
                                    of.write("Active             : {}\r\n".format(row[1]))
                                # zauthenticated
                                if row[2] is None:
                                    of.write("Authenticated      :\r\n")
                                else:
                                    of.write("Authenticated      : {}\r\n".format(row[2]))
                                # zvisible
                                if row[3] is None:
                                    of.write("Visible            :\r\n")
                                else:
                                    of.write("Visible            : {}\r\n".format(row[3]))
                                # zdate
                                if row[4] is None:
                                    of.write("Date               :\r\n")
                                else:
                                    of.write("Date               : {}\r\n".format(row[4]))
                                # zaccountdescription
                                if row[5] is None:
                                    of.write("Account Description:\r\n")
                                else:
                                    of.write("Account Description: {}\r\n".format(row[5]))
                                # zowningbundleid
                                if row[6] is None:
                                    of.write("Owning Bundle ID   :\r\n")
                                else:
                                    of.write("Owning Bundle ID   : {}\r\n".format(row[6]))
                                of.write("\r\n")
                        else:
                            of.write("\r\nNo Account information found\r\n")
                except sqlite3.Error as e:
                    logging.error("{}".format(e.args[0]))
                    print("[ERROR] {}".format(e.args[0]))
                finally:
                    if conn:
                        conn.close()
            elif self._os_version == "mavericks" or self._os_version == "mountain_lion":
                query = "SELECT zusername,zactive,zauthenticated,datetime(zdate + 978307200, 'unixepoch')," \
                        "zaccountdescription,zowningbundleid FROM zaccount"
                conn = None
                try:
                    conn = sqlite3.connect(file)
                    with conn:    
                        cur = conn.cursor()
                        cur.execute(query)
                        rows = cur.fetchall()
                        if len(rows) != 0:
                            for row in rows:
                                # zusername
                                if row[0] is None:
                                    of.write("Username           :\r\n")
                                else:
                                    of.write("Username           : {}\r\n".format(row[0]))
                                # zactive
                                if row[1] is None:
                                    of.write("Active             :\r\n")
                                else:
                                    of.write("Active             : {}\r\n".format(row[1]))
                                # zauthenticated
                                if row[2] is None:
                                    of.write("Authenticated      :\r\n")
                                else:
                                    of.write("Authenticated      : {}\r\n".format(row[2]))
                                # zdate
                                if row[3] is None:
                                    of.write("Date               :\r\n")
                                else:
                                    of.write("Date               : {}\r\n".format(row[3]))
                                # zaccountdescription
                                if row[4] is None:
                                    of.write("Account Description:\r\n")
                                else:
                                    of.write("Account Description: {}\r\n".format(row[4]))
                                # zowningbundleid
                                if row[5] is None:
                                    of.write("Owning Bundle ID   :\r\n")
                                else:
                                    of.write("Owning Bundle ID   : {}\r\n".format(row[5]))
                                of.write("\r\n")
                        else:
                            of.write("\r\nNo Account information found\r\n")
                except sqlite3.Error as e:
                    logging.error("{}".format(e.args[0]))
                    print("[ERROR] {}".format(e.args[0]))
                finally:
                    if conn:
                        conn.close()
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
