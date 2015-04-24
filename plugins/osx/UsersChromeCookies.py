__author__ = 'osxripper'
__version__ = '0.1'
__license__ = 'GPLv3'
from riplib.Plugin import Plugin
import codecs
import logging
import os
import sqlite3


class UsersChromeCookies(Plugin):
    """
    Parse information from /Users/<username>/Library/Application Support/Google/Chrome/Default/Cookies
    """

    def __init__(self):
        """
        Initialise the class.
        """
        super().__init__()
        self._name = "User Chrome Browser Cookies"
        self._description = "Parse information from /Users/<username>/Library/Application Support/Google/Chrome/Default/Cookies"
        self._data_file = "Cookies"
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
        Read the History SQLite database
        """
        with codecs.open(os.path.join(self._output_dir, "Users_" + username + "_Chrome_Cookies.txt"), "a", encoding="utf-8") as of:
            of.write("="*10 + " " + self._name + " " + "="*10 + "\r\n")
            history_db = os.path.join(file, self._data_file)
            # SQL from http://www.forensicswiki.org/wiki/Google_Chrome
            query = "SELECT host_key,name,value,path,datetime(((creation_utc/1000000)-11644473600), 'unixepoch'),datetime(((last_access_utc/1000000)-11644473600), 'unixepoch')," \
                    "datetime(((expires_utc/1000000)-11644473600), 'unixepoch'),secure,httponly,has_expires,persistent,priority FROM cookies ORDER BY creation_utc;"
            if os.path.isfile(history_db):
                of.write("Source File: {}\r\n\r\n".format(history_db))
                conn = None
                try:
                    conn = sqlite3.connect(history_db)
                    with conn:    
                        cur = conn.cursor()
                        cur.execute(query)
                        rows = cur.fetchall()
                        for row in rows:
                            if row[0] is None:
                                of.write("Host Key       :\r\n")
                            else:
                                of.write("Host Key       : {}\r\n".format(row[0]))
                            if row[1] is None:
                                of.write("Name           :\r\n")
                            else:
                                of.write("Name           : {}\r\n".format(row[1]))
                            if row[2] is None:
                                of.write("Value          :\r\n")
                            else:
                                of.write("Value          : {}\r\n".format(row[2]))
                            if row[3] is None:
                                of.write("Path           :\r\n")
                            else:
                                of.write("Path           : {}\r\n".format(row[3]))
                            if row[4] is None:
                                of.write("Creation UTC   :\r\n")
                            else:
                                of.write("Creation UTC   : {}\r\n".format(row[4]))
                            if row[5] is None:
                                of.write("Last Access UTC:\r\n")
                            else:
                                of.write("Last Access UTC: {}\r\n".format(row[5]))
                            if row[6] is None:
                                of.write("Expires UTC    :\r\n")
                            else:
                                of.write("Expires UTC    : {}\r\n".format(row[6]))
                            if row[7] is None:
                                of.write("Secure         :\r\n")
                            else:
                                of.write("Secure         : {}\r\n".format(row[7]))
                            if row[8] is None:
                                of.write("HTTP Only      :\r\n")
                            else:
                                of.write("HTTP Only      : {}\r\n".format(row[8]))
                            if row[9] is None:
                                of.write("Has Expires    :\r\n")
                            else:
                                of.write("Has Expires    : {}\r\n".format(row[9]))
                            if row[10] is None:
                                of.write("Persistent     :\r\n")
                            else:
                                of.write("Persistent     : {}\r\n".format(row[10]))
                            if row[11] is None:
                                of.write("Priority       :\r\n")
                            else:
                                of.write("Priority       : {}\r\n".format(row[11]))
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