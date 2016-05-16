from riplib.Plugin import Plugin
import codecs
import logging
import os
import sqlite3
__author__ = 'osxripper'
__version__ = '0.1'
__license__ = 'GPLv3'


class UsersChromeHistory(Plugin):
    """
    Parse information from /Users/<username>/Library/Application Support/Google/Chrome/Default/History 
    """

    def __init__(self):
        """
        Initialise the class.
        """
        super().__init__()
        self._name = "User Chrome Browser History"
        self._description = "Parse information from /Users/<username>/Library/Application Support/Google/Chrome/Default/History "
        self._data_file = "History"
        self._output_file = ""  # this will have to be defined per user account
        self._type = "sqlite"
    
    def parse(self):
        """
        Iterate over /Users directory and find user sub-directories
        """
        users_path = os.path.join(self._input_dir, "Users")
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
        with codecs.open(os.path.join(self._output_dir, "Users_" + username + "_Chrome_History.txt"), "a", encoding="utf-8") as of:
            of.write("="*10 + " " + self._name + " " + "="*10 + "\r\n")
            history_db = os.path.join(file, "History")
            query = "SELECT id, url,title,term,visit_count,datetime(last_visit_time / 1000000 + (strftime('%s', '1601-01-01')), 'unixepoch'),typed_count,hidden FROM urls, keyword_search_terms WHERE keyword_search_terms.url_id=urls.id"
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
                                of.write("ID         :\r\n")
                            else:
                                of.write("ID         : {}\r\n".format(row[0]))
                            if row[1] is None:
                                of.write("URL        :\r\n")
                            else:
                                of.write("URL        : {}\r\n".format(row[1]))
                            if row[2] is None:
                                of.write("Title      :\r\n")
                            else:
                                of.write("Title      : {}\r\n".format(row[2]))
                            if row[3] is None:
                                of.write("Search Term:\r\n")
                            else:
                                of.write("Search Term: {}\r\n".format(row[3]))
                            if row[3] is None:
                                of.write("Visit Count:\r\n")
                            else:
                                of.write("Visit Count: {}\r\n".format(row[4]))
                            if row[4] is None:
                                of.write("Last Visit :\r\n")
                            else:
                                of.write("Last Visit : {}\r\n".format(row[5]))
                            if row[5] is None:
                                of.write("Typed Count:\r\n")
                            else:
                                of.write("Typed Count: {}\r\n".format(row[6]))
                            if row[6] is None:
                                of.write("Hidden     :\r\n")
                            else:
                                of.write("Hidden     : {}\r\n".format(row[7]))
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
