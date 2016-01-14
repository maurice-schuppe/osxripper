from riplib.Plugin import Plugin
import codecs
import logging
import os
import sqlite3
__author__ = 'osxripper'
__version__ = '0.1'
__license__ = 'GPLv3'


class CacheEncryptedDatabase(Plugin):
    """
    Parse information from /private/var/folders/.../cache_encryptedA.db
    """

    def __init__(self):
        """
        Initialise the class.
        """
        super().__init__()
        self._name = "Wifi Locations - cache_encryptedA.db"
        self._description = "Parse information from /private/var/folders/.../cache_encryptedA.db"
        self._data_file = "cache_encryptedA.db"
        self._output_file = "Wifi_Cache_Encrypted.txt"
        self._type = "sqlite"

    def parse(self):
        """
        Read the /private/var/folders/.../cache_encryptedA.db
        """
        with codecs.open(os.path.join(self._output_dir, self._output_file), "a", encoding="utf-8") as of:
            of.write("="*10 + " " + self._name + " " + "="*10 + "\r\n")

            start_folder = os.path.join(self._input_dir, "private", "var", "folders")
            file_list = []

            if self._os_version == "el_capitan" or self._os_version == "yosemite" or self._os_version == "mavericks":
                # search for cache_encryptedA.db
                for root, subdirs, files in os.walk(start_folder):
                    if self._data_file in files:
                        file_list.append(os.path.join(root, self._data_file))
                if len(file_list) > 0:
                    for database_file in file_list:
                        if os.path.isfile(database_file):
                            of.write("Source Database: {}\r\n\r\n".format(database_file))
                            conn = None
                            try:
                                conn = sqlite3.connect(database_file)
                                query = "SELECT mac,channel,datetime(timestamp + 978307200, 'unixepoch'),latitude," \
                                        "longitude,horizontalaccuracy,altitude,verticalaccuracy,speed,course," \
                                        "confidence,score,reach FROM wifilocation ORDER BY timestamp, mac"
                                with conn:
                                    cur = conn.cursor()
                                    cur.execute(query)
                                    rows = cur.fetchall()
                                    if len(rows) > 0:
                                        for row in rows:
                                            if row[0] is None:
                                                of.write("MAC Address        :\r\n")
                                            else:
                                                of.write("MAC Address        : {}\r\n".format(row[0]))
                                            if row[1] is None:
                                                of.write("Channel            :\r\n")
                                            else:
                                                of.write("Channel            : {}\r\n".format(row[1]))
                                            if row[2] is None:
                                                of.write("Timestamp          :\r\n")
                                            else:
                                                of.write("Timestamp          : {}\r\n".format(row[2]))
                                            if row[3] is None:
                                                of.write("Latitude           :\r\n")
                                            else:
                                                of.write("Latitude           : {}\r\n".format(row[3]))
                                            if row[4] is None:
                                                of.write("Longitude          :\r\n")
                                            else:
                                                of.write("Longitude          : {}\r\n".format(row[4]))
                                            if row[5] is None:
                                                of.write("Horizontal Accuracy:\r\n")
                                            else:
                                                of.write("Horizontal Accuracy: {}\r\n".format(row[5]))
                                            if row[6] is None:
                                                of.write("Altitude           :\r\n")
                                            else:
                                                of.write("Altitude           : {}\r\n".format(row[6]))
                                            if row[7] is None:
                                                of.write("Vertical Accuracy  :\r\n")
                                            else:
                                                of.write("Vertical Accuracy  : {}\r\n".format(row[7]))
                                            if row[8] is None:
                                                of.write("Speed              :\r\n")
                                            else:
                                                of.write("Speed              : {}\r\n".format(row[8]))
                                            if row[9] is None:
                                                of.write("Course             :\r\n")
                                            else:
                                                of.write("Course             : {}\r\n".format(row[9]))
                                            if row[10] is None:
                                                of.write("Confidence         :\r\n")
                                            else:
                                                of.write("Confidence         : {}\r\n".format(row[10]))
                                            if row[11] is None:
                                                of.write("Score              :\r\n")
                                            else:
                                                of.write("Score              : {}\r\n".format(row[11]))
                                            if row[12] is None:
                                                of.write("Reach              :\r\n")
                                            else:
                                                of.write("Reach              : {}\r\n".format(row[12]))
                                            of.write("\r\n")
                                    else:
                                        of.write("No data in database.\r\n")
                                of.write("\r\n")
                            except sqlite3.Error as e:
                                logging.error("{}".format(e.args[0]))
                                print("[ERROR] {}".format(e.args[0]))
                            finally:
                                if conn:
                                    conn.close()
                        of.write("="*50 + "\r\n")
                else:
                    logging.warning("File: index.sqlite does not exist or cannot be found.\r\n")
                    of.write("[WARNING] File: index.sqlite does not exist or cannot be found.\r\n")
                    print("[WARNING] File: index.sqlite does not exist or cannot be found.")
            elif self._os_version == "mountain_lion":
                # search for cache_encryptedA.db
                for root, subdirs, files in os.walk(start_folder):
                    if self._data_file in files:
                        file_list.append(os.path.join(root, self._data_file))
                if len(file_list) > 0:
                    for database_file in file_list:
                        if os.path.isfile(database_file):
                            of.write("Source Database: {}\r\n\r\n".format(database_file))
                            conn = None
                            try:
                                conn = sqlite3.connect(database_file)
                                query = "SELECT mac,channel,datetime(timestamp + 978307200, 'unixepoch'),latitude," \
                                        "longitude,horizontalaccuracy,altitude,verticalaccuracy,speed,course," \
                                        "confidence,score FROM wifilocation ORDER BY timestamp, mac"
                                with conn:
                                    cur = conn.cursor()
                                    cur.execute(query)
                                    rows = cur.fetchall()
                                    if len(rows) > 0:
                                        for row in rows:
                                            if row[0] is None:
                                                of.write("MAC Address        :\r\n")
                                            else:
                                                of.write("MAC Address        : {}\r\n".format(row[0]))
                                            if row[1] is None:
                                                of.write("Channel            :\r\n")
                                            else:
                                                of.write("Channel            : {}\r\n".format(row[1]))
                                            if row[2] is None:
                                                of.write("Timestamp          :\r\n")
                                            else:
                                                of.write("Timestamp          : {}\r\n".format(row[2]))
                                            if row[3] is None:
                                                of.write("Latitude           :\r\n")
                                            else:
                                                of.write("Latitude           : {}\r\n".format(row[3]))
                                            if row[4] is None:
                                                of.write("Longitude          :\r\n")
                                            else:
                                                of.write("Longitude          : {}\r\n".format(row[4]))
                                            if row[5] is None:
                                                of.write("Horizontal Accuracy:\r\n")
                                            else:
                                                of.write("Horizontal Accuracy: {}\r\n".format(row[5]))
                                            if row[6] is None:
                                                of.write("Altitude           :\r\n")
                                            else:
                                                of.write("Altitude           : {}\r\n".format(row[6]))
                                            if row[7] is None:
                                                of.write("Vertical Accuracy  :\r\n")
                                            else:
                                                of.write("Vertical Accuracy  : {}\r\n".format(row[7]))
                                            if row[8] is None:
                                                of.write("Speed              :\r\n")
                                            else:
                                                of.write("Speed              : {}\r\n".format(row[8]))
                                            if row[9] is None:
                                                of.write("Course             :\r\n")
                                            else:
                                                of.write("Course             : {}\r\n".format(row[9]))
                                            if row[10] is None:
                                                of.write("Confidence         :\r\n")
                                            else:
                                                of.write("Confidence         : {}\r\n".format(row[10]))
                                            if row[11] is None:
                                                of.write("Score              :\r\n")
                                            else:
                                                of.write("Score              : {}\r\n".format(row[11]))
                                            of.write("\r\n")
                                    else:
                                        of.write("No data in database.\r\n")
                                of.write("\r\n")
                            except sqlite3.Error as e:
                                logging.error("{}".format(e.args[0]))
                                print("[ERROR] {}".format(e.args[0]))
                            finally:
                                if conn:
                                    conn.close()
                        of.write("="*50 + "\r\n")
                else:
                    logging.warning("File: index.sqlite does not exist or cannot be found.\r\n")
                    of.write("[WARNING] File: index.sqlite does not exist or cannot be found.\r\n")
                    print("[WARNING] File: index.sqlite does not exist or cannot be found.")
            elif self._os_version == "lion" or self._os_version == "snow_leopard":
                logging.info("This version of OSX is not supported this plugin.")
                print("[INFO] This version of OSX is not supported this plugin.")
                of.write("[INFO] This version of OSX is not supported this plugin.\r\n")
            else:
                logging.warning("Not a known OSX version.")
                print("[WARNING] Not a known OSX version.")
        of.close()
