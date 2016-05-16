from riplib.Plugin import Plugin
import codecs
import logging
import os
import sqlite3
__author__ = 'osxripper'
__version__ = '0.1'
__license__ = 'GPLv3'


class UsersMozillaFirefoxCookies(Plugin):
    """
    Parse information from /Users/<username>/Library/Application Support/Firefox/Profiles/*.default/cookies.sqlite
    """

    def __init__(self):
        """
        Initialise the class.
        """
        super().__init__()
        self._name = "User Mozilla Firefox Cookies"
        self._description = "Parse information from /Users/<username>/Library/Application Support/Firefox/Profiles/*.default/cookies.sqlite"
        self._data_file = "cookies.sqlite"
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
                    profile_search_path = os.path.join(users_path, username, "Library", "Application Support", "Firefox", "Profiles")
                    if os.path.isdir(profile_search_path):
                        profiles_list = os.listdir(profile_search_path)
                        for profile in profiles_list:
                            if profile.endswith(".default"):
                                sqlite_db = os.path.join(profile_search_path, profile, self._data_file)
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
        Read the places.sqlite SQLite database
        """
        with codecs.open(os.path.join(self._output_dir, "Users_" + username + "_Firefox_Cookies.txt"), "a", encoding="utf-8") as of:
            of.write("="*10 + " " + self._name + " " + "="*10 + "\r\n")
            if os.path.isfile(file):
                of.write("Source File: {}\r\n\r\n".format(file))
                conn = None
                try:
                    query = "SELECT baseDomain,name,value,host,path,datetime(creationTime/1000000, 'unixepoch'),datetime(lastAccessed/1000000, 'unixepoch')," \
                            "datetime(expiry/1000000, 'unixepoch'),isSecure,isHttpOnly FROM moz_cookies ORDER BY creationTime"
                    conn = sqlite3.connect(file)
                    with conn:
                        cur = conn.cursor()
                        cur.execute(query)
                        rows = cur.fetchall()
                        for row in rows:
                            if row[0] is None:
                                of.write("Base Domain  :\r\n")
                            else:
                                of.write("Base Domain  : {}\r\n".format(row[0]))
                            if row[1] is None:
                                of.write("Name         :\r\n")
                            else:
                                of.write("Name         : {}\r\n".format(row[1]))
                            if row[2] is None:
                                of.write("Value        :\r\n")
                            else:
                                of.write("Value        : {}\r\n".format(row[2]))
                            if row[3] is None:
                                of.write("Host         :\r\n")
                            else:
                                of.write("Host         : {}\r\n".format(row[3]))
                            if row[4] is None:
                                of.write("Path         :\r\n")
                            else:
                                of.write("Path         : {}\r\n".format(row[4]))
                            if row[5] is None:
                                of.write("Creation Time:\r\n")
                            else:
                                of.write("Creation Time: {}\r\n".format(row[5]))
                            if row[6] is None:
                                of.write("Last Accessed:\r\n")
                            else:
                                of.write("Last Accessed: {}\r\n".format(row[6]))
                            if row[7] is None:
                                of.write("Expiry       :\r\n")
                            else:
                                of.write("Expiry       : {}\r\n".format(row[7]))
                            if row[8] is None:
                                of.write("Is Secure    :\r\n")
                            else:
                                of.write("Is Secure    : {}\r\n".format(row[8]))
                            if row[9] is None:
                                of.write("Is HTTP Only :\r\n")
                            else:
                                of.write("Is HTTP Only : {}\r\n".format(row[9]))

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
            of.write("="*40 + "\r\n\r\n")
        of.close()
