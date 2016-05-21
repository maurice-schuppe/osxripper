from riplib.Plugin import Plugin
import codecs
import logging
import os
import sqlite3

__author__ = 'osxripper'
__version__ = '0.1'
__license__ = 'GPLv3'


class InteractionDatabase(Plugin):
    """
    Parse information from /private/var/db/CoreDuet/People/interactionC.db
    """

    def __init__(self):
        """
        Initialise the class.
        """
        super().__init__()
        self._name = "Interaction Database"
        self._description = "Parse information from /private/var/db/CoreDuet/People/interactionC.db"
        self._data_file = "interactionC.db"
        self._output_file = "Interaction_Database.txt"
        self._type = "sqlite"

    def parse(self):
        """
        Read the /private/var/db/CoreDuet/People/interactionC.db SQLite database
        """
        with codecs.open(os.path.join(self._output_dir, self._output_file), "a", encoding="utf-8") as of:
            of.write("="*10 + " " + self._name + " " + "="*10 + "\r\n")
            database_file = os.path.join(self._input_dir, "private", "var", "db", "CoreDuet", "People", self._data_file)
            if self._os_version == "el_capitan":
                if os.path.isfile(database_file):
                    of.write("Source Database: {0}\r\n\r\n".format(database_file))
                    conn = None
                    try:
                        conn = sqlite3.connect(database_file)
                        query = "SELECT zpk.z_name,zc.zdisplayname,zc.zidentifier," \
                                "datetime(zc.zcreationdate + 978307200, 'unixepoch')," \
                                "datetime(zc.zfirstincomingrecipientdate + 978307200, 'unixepoch')," \
                                "datetime(zc.zfirstincomingsenderdate + 978307200, 'unixepoch')," \
                                "datetime(zc.zfirstoutgoingrecipientdate + 978307200, 'unixepoch')," \
                                "datetime(zc.zlastincomingrecipientdate + 978307200, 'unixepoch')," \
                                "datetime(zc.zlastincomingsenderdate + 978307200, 'unixepoch')," \
                                "datetime(zc.zlastoutgoingrecipientdate + 978307200, 'unixepoch')" \
                                " FROM z_primarykey zpk,zcontacts zc WHERE zpk.z_ent = zc.z_ent"
                        with conn:
                            cur = conn.cursor()
                            cur.execute(query)
                            rows = cur.fetchall()
                            if len(rows) > 0:
                                for row in rows:
                                    if row[0] is None:
                                        of.write("Name                         :\r\n")
                                    else:
                                        of.write("Name                         : {0}\r\n".format(row[0]))
                                    if row[1] is None:
                                        of.write("Display Name                 :\r\n")
                                    else:
                                        of.write("Display Name                 : {0}\r\n".format(row[1]))
                                    if row[2] is None:
                                        of.write("Identifier                   :\r\n")
                                    else:
                                        of.write("Identifier                   : {0}\r\n".format(row[2]))
                                    if row[3] is None:
                                        of.write("Creation Date                :\r\n")
                                    else:
                                        of.write("Creation Date                : {0}\r\n".format(row[3]))
                                    if row[4] is None:
                                        of.write("First Incoming Recipient Date:\r\n")
                                    else:
                                        of.write("First Incoming Recipient Date: {0}\r\n".format(row[4]))
                                    if row[5] is None:
                                        of.write("First Incoming Sender Date   :\r\n")
                                    else:
                                        of.write("First Incoming Sender Date   : {0}\r\n".format(row[5]))
                                    if row[6] is None:
                                        of.write("First Outgoing Recipient Date:\r\n")
                                    else:
                                        of.write("First Outgoing Recipient Date: {0}\r\n".format(row[6]))
                                    if row[7] is None:
                                        of.write("Last Incoming Recipient Date :\r\n")
                                    else:
                                        of.write("Last Incoming Recipient Date : {0}\r\n".format(row[7]))
                                    if row[8] is None:
                                        of.write("Last Incoming Sender Date    :\r\n")
                                    else:
                                        of.write("Last Incoming Sender Date    : {0}\r\n".format(row[8]))
                                    if row[9] is None:
                                        of.write("Last Outgoing Recipient Date :\r\n")
                                    else:
                                        of.write("Last Outgoing Recipient Date : {0}\r\n".format(row[9]))
                                    of.write("\r\n")
                            else:
                                of.write("No data in dtabase.\r\n")
                        of.write("\r\n")
                    except sqlite3.Error as e:
                        logging.error("{0}".format(e.args[0]))
                        print("[ERROR] {0}".format(e.args[0]))
                    finally:
                        if conn:
                            conn.close()
                    of.write("="*50 + "\r\n")
                else:
                    logging.warning("File: index.sqlite does not exist or cannot be found.\r\n")
                    of.write("[WARNING] File: index.sqlite does not exist or cannot be found.\r\n")
                    print("[WARNING] File: index.sqlite does not exist or cannot be found.")
            elif self._os_version in ["yosemite", "mavericks", "mountain_lion", "lion", "snow_leopard"]:
                logging.info("This version of OSX is not supported this plugin.")
                print("[INFO] This version of OSX is not supported this plugin.")
                of.write("[INFO] This version of OSX is not supported this plugin.\r\n")
            else:
                logging.warning("Not a known OSX version.")
                print("[WARNING] Not a known OSX version.")
            # of.write("="*40 + "\r\n\r\n")
        of.close()
