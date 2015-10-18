__author__ = 'osxripper'
__version__ = '0.1'
__license__ = 'GPLv3'
from riplib.Plugin import Plugin
import codecs
import datetime
import logging
import os
import sqlite3
import ccl_bplist


class UsersSafariHistory(Plugin):
    """
    Parse information from /Users/<username>/Library/Safari/History.db or /Users/<username>/Library/Safari/History.plist
    """

    def __init__(self):
        """
        Initialise the class.
        """
        super().__init__()
        self._name = "User Safari History"
        self._description = "Parse information from /Users/<username>/Library/Preferences/com.apple.LaunchServices.QuarantineEventsV2"
        self._data_file = ""  # multiple files, Yosemite is a SQLite DB and others are Plists
        self._output_file = ""  # this will have to be defined per user account
        self._type = "multi"
    
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
                    history_path = os.path.join(users_path, username, "Library", "Safari")
                    if os.path.isdir(history_path):
                        if self._os_version == "el_capitan" or self._os_version == "yosemite":
                            self.__parse_sqlite_db(history_path, username)
                        elif self._os_version == "mavericks":
                            self.__parse_history_plist(history_path, username)
                        elif self._os_version == "mountain_lion":
                            self.__parse_history_plist(history_path, username)
                        elif self._os_version == "lion":
                            self.__parse_history_plist(history_path, username)
                        elif self._os_version == "snow_leopard":
                            self.__parse_history_plist(history_path, username)
                        else:
                            logging.warning("Not a known OSX version.")
                            print("[WARNING] Not a known OSX version.")
                    else:
                        logging.warning("{} does not exist.".format(history_path))
                        print("[WARNING] {} does not exist.".format(history_path))
        else:
            logging.warning("{} does not exist.".format(users_path))
            print("[WARNING] {} does not exist.".format(users_path))
    
    def __parse_sqlite_db(self, file, username):
        """
        Read the History.db SQLite database
        """
        with codecs.open(os.path.join(self._output_dir, "Users_" + username + "_Safari_History.txt"), "a", encoding="utf-8") as of:
            of.write("="*10 + " " + self._name + " " + "="*10 + "\r\n")
            history_db = os.path.join(file, "History.db")
            query = "SELECT hi.id,hi.url,hi.visit_count,datetime(hv.visit_time + 978307200, 'unixepoch'),hv.title,hv.redirect_source," \
                    "hv.redirect_destination FROM history_items hi,history_visits hv WHERE hi.id = hv.id"
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
                                of.write("ID               :\r\n")
                            else:
                                of.write("ID               : {}\r\n".format(row[0]))
                            if row[1] is None:
                                of.write("URL              :\r\n")
                            else:
                                of.write("URL              : {}\r\n".format(row[1]))
                            if row[2] is None:
                                of.write("Visit Count      :\r\n")
                            else:
                                of.write("Visit Count      : {}\r\n".format(row[2]))
                            if row[3] is None:
                                of.write("Visit Time       :\r\n")
                            else:
                                of.write("Visit Time       : {}\r\n".format(row[3]))
                            if row[4] is None:
                                of.write("Title            :\r\n")
                            else:
                                of.write("Title            : {}\r\n".format(row[4]))
                            if row[5] is None:
                                of.write("Redirect ID      :\r\n")
                            else:
                                of.write("Redirect ID      : {}\r\n".format(row[5]))
                            if row[6] is None:
                                of.write("Redirect Dest. ID:\r\n")
                            else:
                                of.write("Redirect Dest. ID: {}\r\n".format(row[6]))
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
        
    def __parse_history_plist(self, file, username):
        """
        Read the History.plist
        """
        mac_absolute = datetime.datetime(2001, 1, 1, 0, 0, 0)
        with codecs.open(os.path.join(self._output_dir, "Users_" + username + "_Safari_History.txt"), "a", encoding="utf-8") as of:
            of.write("="*10 + " " + self._name + " " + "="*10 + "\r\n")
            history_plist = os.path.join(file, "History.plist")
            if os.path.isfile(history_plist):
                of.write("Source File: {}\r\n\r\n".format(history_plist))
                bplist = open(history_plist, "rb")
                plist = ccl_bplist.load(bplist)
                try:
                    # WebHistoryFileVersion
                    if "WebHistoryFileVersion" in plist:
                        of.write("Web History File Version: {}\r\n".format(plist["WebHistoryFileVersion"]))
                    # WebHistoryDates ARRAY of DICT
                    if "WebHistoryDates" in plist:
                        of.write("Web History:\r\n")
                        for whd in plist["WebHistoryDates"]:
                            # EMPTY KEY with URL value
                            of.write("\tURL: {}\r\n".format(whd[""]))
                            # title
                            if "title" in whd:
                                of.write("\tTitle: {}\r\n".format(whd["title"]))
                            # lastVisitedDate FLOAT DATE
                            if "lastVisitedDate" in whd:
                                of.write("\tLast Visited Date: {}\r\n".format(mac_absolute + datetime.timedelta(0, float(whd["lastVisitedDate"]))))
                            # visitCount
                            if "visitCount" in whd:
                                of.write("\tVisit Count: {}\r\n".format(whd["visitCount"]))
                            # redirectURLs ARRAY of STRING
                            if "redirectURLs" in whd:
                                for redirect in whd["redirectURLs"]:
                                    of.write("\tRedirect URL: {}\r\n".format(redirect))
                            of.write("\r\n")
                    # WebHistoryDomains.v2 MAVERICKS? ARRAY of DICT
                    if "WebHistoryDomains.v2" in plist:
                        of.write("Web History Domains v2:\r\n")
                        
                    of.write("\r\n")
                except KeyError:
                    pass
            else:
                logging.warning("File: {} does not exist or cannot be found.\r\n".format(file))
                of.write("[WARNING] File: {} does not exist or cannot be found.\r\n".format(file))
                print("[WARNING] File: {} does not exist or cannot be found.\r\n".format(file))
            of.write("="*40 + "\r\n\r\n")
        of.close()