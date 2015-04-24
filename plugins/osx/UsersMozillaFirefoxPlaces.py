__author__ = 'osxripper'
__version__ = '0.1'
__license__ = 'GPLv3'
from riplib.Plugin import Plugin
import codecs
import logging
import os
import sqlite3


class UsersMozillaFirefoxPlaces(Plugin):
    """
    Parse information from /Users/<username>/Library/Application Support/Firefox/Profiles/*.default/places.sqlite
    """

    def __init__(self):
        """
        Initialise the class.
        """
        super().__init__()
        self._name = "User Mozilla Firefox Places"
        self._description = "Parse information from /Users/<username>/Library/Application Support/Firefox/Profiles/*.default/places.sqlite"
        self._data_file = "places.sqlite"
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
        with codecs.open(os.path.join(self._output_dir, "Users_" + username + "_Firefox_Places.txt"), "a", encoding="utf-8") as of:
            of.write("="*10 + " " + self._name + " " + "="*10 + "\r\n")
            if self._os_version == "yosemite" or self._os_version == "mavericks" or self._os_version == "mountain_lion":
                if os.path.isfile(file):
                    of.write("Source File: {}\r\n\r\n".format(file))
                    conn = None
                    try:
                        query = "SELECT url, title, rev_host, visit_count, datetime(last_visit_date / 1000000, 'unixepoch'), hidden, typed FROM moz_places ORDER BY visit_count DESC"
                        conn = sqlite3.connect(file)
                        with conn:    
                            cur = conn.cursor()
                            cur.execute(query)
                            rows = cur.fetchall()
                            for row in rows:
                                if row[0] is None:
                                    of.write("URL            :\r\n")
                                else:
                                    of.write("URL            : {}\r\n".format(row[0]))
                                if row[1] is None:
                                    of.write("Title          :\r\n")
                                else:
                                    of.write("Title          : {}\r\n".format(row[1]))
                                if row[2] is None:
                                    of.write("Rev. Host      :\r\n")
                                else:
                                    of.write("Rev. Host      : {}\r\n".format(row[2]))
                                if row[3] is None:
                                    of.write("Visit Count    :\r\n")
                                else:
                                    of.write("Visit Count    : {}\r\n".format(row[3]))
                                if row[4] is None:
                                    of.write("Last Visit Date:\r\n")
                                else:
                                    of.write("Last Visit Date: {}\r\n".format(row[4]))
                                if row[5] is None:
                                    of.write("Hidden         :\r\n")
                                else:
                                    of.write("Hidden         : {}\r\n".format(row[5]))
                                if row[6] is None:
                                    of.write("Typed          :\r\n")
                                else:
                                    of.write("Typed          : {}\r\n".format(row[6]))
                                of.write("\r\n")
                            
                            of.write("="*10 + " Mozilla Firefox Annotations " + "="*10 + "\r\n")
                            query = "SELECT mp.url,ma.content,maa.name,datetime(ma.dateAdded / 1000000, 'unixepoch')," \
                                    "datetime(ma.lastModified / 1000000, 'unixepoch') FROM moz_annos ma,moz_anno_attributes maa," \
                                    "moz_places mp WHERE ma.anno_attribute_id = maa.id AND mp.id = ma.place_id"
                            cur.execute(query)
                            rows = cur.fetchall()
                            for row in rows:
                                if row[0] is None:
                                    of.write("URL               :\r\n")
                                else:
                                    of.write("URL               : {}\r\n".format(row[0]))
                                if row[1] is None:
                                    of.write("Content           :\r\n")
                                else:
                                    of.write("Content           : {}\r\n".format(row[1]))
                                if row[2] is None:
                                    of.write("Name              :\r\n")
                                else:
                                    of.write("Name              : {}\r\n".format(row[2]))
                                if row[3] is None:
                                    of.write("Date Added        :\r\n")
                                else:
                                    of.write("Date Added        : {}\r\n".format(row[3]))
                                if row[4] is None:
                                    of.write("Date Last Modified:\r\n")
                                else:
                                    of.write("Date Last Modified: {}\r\n".format(row[4]))
                                of.write("\r\n")
                                
                            of.write("="*10 + " Mozilla Firefox Input History " + "="*10 + "\r\n")
                            query = "SELECT mp.url,mi.input,mi.use_count FROM moz_inputhistory mi,moz_places mp WHERE mi.place_id = mp.id ORDER BY use_count DESC"
                            cur.execute(query)
                            rows = cur.fetchall()
                            if len(rows) == 0:
                                of.write("No input history data.\r\n\r\n")
                            else:
                                for row in rows:
                                    if row[0] is None:
                                        of.write("URL      :\r\n")
                                    else:
                                        of.write("URL      : {}\r\n".format(row[0]))
                                    if row[0] is None:
                                        of.write("Input    :\r\n")
                                    else:
                                        of.write("Input    : {}\r\n".format(row[0]))
                                    if row[0] is None:
                                        of.write("Use Count:\r\n")
                                    else:
                                        of.write("Use Count:{}\r\n".format(row[0]))
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