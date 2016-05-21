from riplib.Plugin import Plugin
import codecs
import logging
import os
import osxripper_time
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
                if not os.path.isfile(database_file):
                    logging.warning("File: {0} does not exist or cannot be found.\r\n".format(self._data_file))
                    of.write("[WARNING] File: {0} does not exist or cannot be found.\r\n".format(self._data_file))
                    print("[WARNING] File: {0} does not exist or cannot be found.".format(self._data_file))
                else:
                    of.write("Source Database: {0}\r\n\r\n".format(database_file))
                    conn = None
                    try:
                        conn = sqlite3.connect(database_file)
                        conn.row_factory = sqlite3.Row
                        # cocoa time 2001/1/1 00:00
                        query = "SELECT zpk.z_name,zc.zdisplayname,zc.zidentifier," \
                                "zc.zcreationdate," \
                                "zc.zfirstincomingrecipientdate," \
                                "zc.zfirstincomingsenderdate," \
                                "zc.zfirstoutgoingrecipientdate," \
                                "zc.zlastincomingrecipientdate," \
                                "zc.zlastincomingsenderdate," \
                                "zc.zlastoutgoingrecipientdate" \
                                " FROM z_primarykey zpk,zcontacts zc WHERE zpk.z_ent = zc.z_ent"
                        with conn:
                            cur = conn.cursor()
                            cur.execute(query)
                            rows = cur.fetchall()
                            if len(rows) > 0:
                                for row in rows:
                                    creationdate = \
                                        osxripper_time.get_cocoa_seconds(row["zcreationdate"])
                                    firstincomingrecipientdate = \
                                        osxripper_time.get_cocoa_seconds(row["zfirstincomingrecipientdate"])
                                    firstincomingsenderdate = \
                                        osxripper_time.get_cocoa_seconds(row["zfirstincomingsenderdate"])
                                    firstoutgoingrecipientdate = \
                                        osxripper_time.get_cocoa_seconds(row["zfirstoutgoingrecipientdate"])
                                    lastincomingrecipientdate = \
                                        osxripper_time.get_cocoa_seconds(row["zlastincomingrecipientdate"])
                                    lastincomingsenderdate = \
                                        osxripper_time.get_cocoa_seconds(row["zlastincomingsenderdate"])
                                    lastoutgoingrecipientdate = \
                                        osxripper_time.get_cocoa_seconds(row["zlastincomingsenderdate"])

                                    of.write("Name                         : {0}\r\n".format(row["z_name"]))
                                    of.write("Display Name                 : {0}\r\n".format(row["zdisplayname"]))
                                    of.write("Identifier                   : {0}\r\n".format(row["zidentifier"]))
                                    of.write("Creation Date                : {0}\r\n".format(creationdate))
                                    of.write("First Incoming Recipient Date: {0}\r\n"
                                             .format(firstincomingrecipientdate))
                                    of.write("First Incoming Sender Date   : {0}\r\n"
                                             .format(firstincomingsenderdate))
                                    of.write("First Outgoing Recipient Date: {0}\r\n"
                                             .format(firstoutgoingrecipientdate))
                                    of.write("Last Incoming Recipient Date : {0}\r\n"
                                             .format(lastincomingrecipientdate))
                                    of.write("Last Incoming Sender Date    : {0}\r\n"
                                             .format(lastincomingsenderdate))
                                    of.write("Last Outgoing Recipient Date : {0}\r\n"
                                             .format(lastoutgoingrecipientdate))
                                    of.write("\r\n")
                            else:
                                of.write("No data in database.\r\n")
                        of.write("\r\n")
                    except sqlite3.Error as e:
                        logging.error("{0}".format(e.args[0]))
                        print("[ERROR] {0}".format(e.args[0]))
                    finally:
                        if conn:
                            conn.close()
                    of.write("="*50 + "\r\n")

            elif self._os_version in ["yosemite", "mavericks", "mountain_lion", "lion", "snow_leopard"]:
                logging.info("This version of OSX is not supported this plugin.")
                print("[INFO] This version of OSX is not supported this plugin.")
                of.write("[INFO] This version of OSX is not supported this plugin.\r\n")
            else:
                logging.warning("Not a known OSX version.")
                print("[WARNING] Not a known OSX version.")
        of.close()
