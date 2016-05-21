from riplib.Plugin import Plugin
import codecs
import datetime
import logging
import os
import sqlite3

__author__ = 'osxripper'
__version__ = '0.1'
__license__ = 'GPLv3'


class DocumentRevisions(Plugin):
    """
    Parse information from /.DocumentRevisions-V100/db-V1/db.sqlite
    """

    def __init__(self):
        """
        Initialise the class.
        """
        super().__init__()
        self._name = "Document Revisions"
        self._description = "Parse information from /.DocumentRevisions-V100/db-V1/db.sqlite"
        self._data_file = "db.sqlite"
        self._output_file = "DocumentRevisions.txt"  # this will have to be defined per user account
        self._type = "sqlite"
    
    def parse(self):
        """
        Read the db.sqlite SQLite database
        """
        with codecs.open(os.path.join(self._output_dir, self._output_file), "a", encoding="utf-8") as of:
            of.write("="*10 + " " + self._name + " " + "="*10 + "\r\n")
            query = "SELECT * FROM files"
            file = os.path.join(self._input_dir, ".DocumentRevisions-V100", "db-V1", self._data_file)
            of.write("Source File: {}\r\n\r\n".format(file))
            if self._os_version in ["el_capitan", "yosemite"]:
                if os.path.isfile(file):
                    conn = None
                    try:
                        conn = sqlite3.connect(file)
                        with conn:    
                            cur = conn.cursor()
                            cur.execute(query)
                            rows = cur.fetchall()
                            for row in rows:
                                if row[0] is None:
                                    of.write("file_row_id     :\r\n")
                                else:
                                    of.write("file_row_id     : {}\r\n".format(row[0]))
                                if row[1] is None:
                                    of.write("file_name       :\r\n")
                                else:
                                    of.write("file_name       : {}\r\n".format(row[1]))
                                if row[2] is None:
                                    of.write("file_parent_id  :\r\n")
                                else:
                                    of.write("file_parent_id  : {}\r\n".format(row[2]))
                                if row[3] is None:
                                    of.write("file_path       :\r\n")
                                else:
                                    of.write("file_path       : {}\r\n".format(row[3]))
                                if row[4] is None:
                                    of.write("file_inode      :\r\n")
                                else:                            
                                    of.write("file_inode      : {}\r\n".format(row[4]))
                                if row[5] is None:
                                    of.write("file_last_seen  :\r\n")
                                else:
                                    of.write("file_last_seen  : {}\r\n"
                                             .format(datetime.datetime
                                                     .fromtimestamp(int(row[5])).strftime('%Y-%m-%d %H:%M:%S')))
                                if row[6] is None:
                                    of.write("file_status     :\r\n")
                                else:
                                    of.write("file_status     : {}\r\n".format(row[6]))
                                if row[7] is None:
                                    of.write("file_storage_id :\r\n")
                                else:
                                    of.write("file_storage_id : {}\r\n".format(row[7]))
                                if row[8] is None:
                                    of.write("file_document_id:\r\n")
                                else:
                                    of.write("file_document_id: {}\r\n".format(row[8]))
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
                    
            elif self._os_version in ["mavericks", "mountain_lion", "lion"]:
                if os.path.isfile(file):
                    conn = None
                    try:
                        conn = sqlite3.connect(file)
                        with conn:    
                            cur = conn.cursor()
                            cur.execute(query)
                            rows = cur.fetchall()
                            for row in rows:
                                if row[0] is None:
                                    of.write("file_row_id    :\r\n")
                                else:
                                    of.write("file_row_id    : {}\r\n".format(row[0]))
                                if row[1] is None:
                                    of.write("file_name      :\r\n")
                                else:
                                    of.write("file_name      : {}\r\n".format(row[1]))
                                if row[2] is None:
                                    of.write("file_parent_id :\r\n")
                                else:
                                    of.write("file_parent_id : {}\r\n".format(row[2]))
                                if row[3] is None:
                                    of.write("file_path      :\r\n")
                                else:
                                    of.write("file_path      : {}\r\n".format(row[3]))
                                if row[4] is None:
                                    of.write("file_inode     :\r\n")
                                else:                            
                                    of.write("file_inode     : {}\r\n".format(row[4]))
                                if row[5] is None:
                                    of.write("file_last_seen :\r\n")
                                else:
                                    of.write("file_last_seen : {}\r\n"
                                             .format(datetime.datetime
                                                     .fromtimestamp(int(row[5])).strftime('%Y-%m-%d %H:%M:%S')))
                                if row[6] is None:
                                    of.write("file_status    :\r\n")
                                else:
                                    of.write("file_status    : {}\r\n".format(row[6]))
                                if row[7] is None:
                                    of.write("file_storage_id:\r\n")
                                else:
                                    of.write("file_storage_id: {}\r\n".format(row[7]))
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
            elif self._os_version == "snow_leopard":
                logging.info("This version of OSX is not supported by this plugin.")
                print("[INFO] This version of OSX is not supported by this plugin.")
                of.write("[INFO] This version of OSX is not supported by this plugin.\r\n")
            else:
                logging.warning("Not a known OSX version.")
                print("[WARNING] Not a known OSX version.")
            of.write("="*40 + "\r\n\r\n")
        of.close()
