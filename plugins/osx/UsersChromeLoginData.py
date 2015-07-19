__author__ = 'osxripper'
__version__ = '0.1'
__license__ = 'GPLv3'
from riplib.Plugin import Plugin
import codecs
import logging
import os
import sqlite3


class UsersChromeLoginData(Plugin):
    """
    Parse information from /Users/<username>/Library/Application Support/Google/Chrome/Default/Login Data
    """

    def __init__(self):
        """
        Initialise the class.
        """
        super().__init__()
        self._name = "User Chrome Browser Login Data"
        self._description = "Parse information from /Users/<username>/Library/Application Support/Google/Chrome/Default/Login Data"
        self._data_file = "Login Data"
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
                    history_path = os.path.join(users_path, username, "Library", "Application Support", "Google", "Chrome", "Default")
                    if os.path.isdir(history_path):
                        self.__parse_sqlite_db(history_path, username)
                    else:
                        logging.warning("{} does not exist.".format(history_path))
                        print("[WARNING] {} does not exist.".format(history_path))
        else:
            logging.warning("{} does not exist.".format(users_path))
            print("[WARNING] {} does not exist.".format(users_path))
    
    def __parse_sqlite_db(self, file, username):
        """
        Read the Login Data SQLite database
        """
        with codecs.open(os.path.join(self._output_dir, "Users_" + username + "_Chrome_Login_Data.txt"), "a", encoding="utf-8") as of:
            of.write("="*10 + " " + self._name + " " + "="*10 + "\r\n")
            history_db = os.path.join(file, self._data_file)
            query = "SELECT username_value,display_name,origin_url,action_url,datetime((date_created / 1000000)-11644473600, 'unixepoch')," \
                    "datetime((date_synced / 1000000)-11644473600, 'unixepoch'),signon_realm,ssl_valid,preferred,times_used,blacklisted_by_user," \
                    "scheme,password_type,avatar_url,federation_url FROM logins ORDER BY username_value"
#  "scheme,password_type,avatar_url,federation_url,is_zero_click FROM logins ORDER BY username_value"

            if os.path.isfile(history_db):
                of.write("Source File: {}\r\n\r\n".format(history_db))
                of.write("N.B. Creds are stored as BLOBS, not retrieved by this plugin\r\n\r\n")
                conn = None
                try:
                    conn = sqlite3.connect(history_db)
                    with conn:    
                        cur = conn.cursor()
                        cur.execute(query)
                        rows = cur.fetchall()
                        if len(rows) == 0:
                            of.write("No data found in this database.\r\n\r\n")
                        else:
                            for row in rows:
                                # username_value
                                if row[0] is None:
                                    of.write("Username           :\r\n")
                                else:
                                    of.write("Username           : {}\r\n".format(row[0]))
                                # display_name
                                if row[1] is None:
                                    of.write("Display Name       :\r\n")
                                else:
                                    of.write("Display Name       : {}\r\n".format(row[1]))
                                # origin_url
                                if row[2] is None:
                                    of.write("Origin URL         :\r\n")
                                else:
                                    of.write("Origin URL         : {}\r\n".format(row[2]))
                                # action_url
                                if row[3] is None:
                                    of.write("Action URL         :\r\n")
                                else:
                                    of.write("Action URL         : {}\r\n".format(row[3]))
                                # datetime((date_created / 1000000)-11644473600, 'unixepoch')
                                if row[4] is None:
                                    of.write("Date Created       :\r\n")
                                else:
                                    of.write("Date Created       : {}\r\n".format(row[4]))
                                # datetime((date_synced / 1000000)-11644473600, 'unixepoch')
                                if row[5] is None:
                                    of.write("Date Synced:       :\r\n")
                                else:
                                    of.write("Date Synced        : {}\r\n".format(row[5]))
                                # signon_realm
                                if row[6] is None:
                                    of.write("Signon Realm       :\r\n")
                                else:
                                    of.write("Signon Realm       : {}\r\n".format(row[6]))
                                # ssl_valid
                                if row[7] is None:
                                    of.write("SSL Valid          :\r\n")
                                else:
                                    of.write("SSL Valid          : {}\r\n".format(row[7]))
                                # preferred
                                if row[8] is None:
                                    of.write("Preferred          :\r\n")
                                else:
                                    of.write("Preferred          : {}\r\n".format(row[8]))
                                # times_used
                                if row[9] is None:
                                    of.write("Times Used         :\r\n")
                                else:
                                    of.write("Times Used         : {}\r\n".format(row[9]))
                                # blacklisted_by_user
                                if row[10] is None:
                                    of.write("Blacklisted by User:\r\n")
                                else:
                                    of.write("Blacklisted by User: {}\r\n".format(row[10]))
                                # scheme
                                if row[11] is None:
                                    of.write("Scheme             :\r\n")
                                else:
                                    of.write("Scheme             : {}\r\n".format(row[11]))
                                # password_type
                                if row[12] is None:
                                    of.write("Password Type      :\r\n")
                                else:
                                    of.write("Password Type      : {}\r\n".format(row[12]))
                                # avatar_url
                                if row[13] is None:
                                    of.write("Avatar URL         :\r\n")
                                else:
                                    of.write("Avatar URL         : {}\r\n".format(row[13]))
                                # federation_url
                                if row[14] is None:
                                    of.write("Federation URL     :\r\n")
                                else:
                                    of.write("Federation URL     : {}\r\n".format(row[14]))
                                # is_zero_click
                                # if row[15] is None:
                                #     of.write("Is Zero Click      :\r\n")
                                # else:
                                #     of.write("Is Zero Click      : {}\r\n".format(row[15]))
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
            of.write("="*40 + "\r\n\r\n")
        of.close()