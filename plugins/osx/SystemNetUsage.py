from riplib.Plugin import Plugin
import codecs
import logging
import os
import sqlite3
__author__ = 'osxripper'
__version__ = '0.1'
__license__ = 'GPLv3'


class SystemNetUsage(Plugin):
    """
    Parse information from /private/var/networkd/netusage.sqlite
    """

    def __init__(self):
        """
        Initialise the class.
        """
        super().__init__()
        self._name = "System Net Usage"
        self._description = "Parse information from /private/var/networkd/netusage.sqlite"
        self._data_file = "netusage.sqlite"
        self._output_file = "System_NetUsage.txt"
        self._type = "sqlite"

    def parse(self):
        """
        Read the /private/var/networkd/netusage.sqlite SQLite database
        """
        with codecs.open(os.path.join(self._output_dir, self._output_file), "a", encoding="utf-8") as of:
            of.write("="*10 + " " + self._name + " " + "="*10 + "\r\n")
            file = os.path.join(self._input_dir, "private", "var", "networkd", self._data_file)
            of.write("Source File: {}\r\n\r\n".format(file))
            if self._os_version == "el_capitan":
                if os.path.isfile(file):
                    pass
                    conn = None
                    try:
                        conn = sqlite3.connect(file)
                        of.write("="*10 + " Network Attachments " + "="*10 + "\r\n")
                        run_network_attachment_query(conn, of)
                        of.write("="*10 + " Networked Processes " + "="*10 + "\r\n")
                        run_process_query(conn, of)
                        of.write("="*10 + " Network Process Usage " + "="*10 + "\r\n")
                        run_live_usage_query(conn, of)
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

            elif self._os_version in ["yosemite", "mavericks", "mountain_lion", "lion", "snow_leopard"]:
                logging.info("This version of OSX is not supported by this plugin.")
                print("[INFO] This version of OSX is not supported by this plugin.")
                of.write("[INFO] This version of OSX is not supported by this plugin.\r\n")
            else:
                logging.warning("Not a known OSX version.")
                print("[WARNING] Not a known OSX version.")
            of.write("="*40 + "\r\n\r\n")
        of.close()


def run_process_query(sqlite_connection, output_file):
    query = "SELECT zpk.z_name,zp.zprocname,datetime(zp.zfirsttimestamp + 978307200, 'unixepoch')," \
            "datetime(zp.ztimestamp + 978307200, 'unixepoch') FROM zprocess zp,z_primarykey zpk " \
            "WHERE zp.z_ent = zpk.z_ent ORDER BY zpk.z_name"
    with sqlite_connection:
        cur = sqlite_connection.cursor()
        cur.execute(query)
        rows = cur.fetchall()
        for row in rows:
            if row[0] is None:
                output_file.write("Name           :\r\n")
            else:
                output_file.write("Name           : {}\r\n".format(row[0]))
            if row[1] is None:
                output_file.write("Process        :\r\n")
            else:
                output_file.write("Process        : {}\r\n".format(row[1]))
            if row[2] is None:
                output_file.write("First Timestamp:\r\n")
            else:
                output_file.write("First Timestamp: {}\r\n".format(row[2]))
            if row[3] is None:
                output_file.write("Timestamp      :\r\n")
            else:
                output_file.write("Timestamp      : {}\r\n".format(row[3]))
            output_file.write("\r\n")


def run_live_usage_query(sqlite_connection, output_file):
    query = "SELECT zpk.z_name,zp.zprocname,datetime(zlu.ztimestamp + 978307200, 'unixepoch') AS ts,zlu.zwifiin," \
            "zlu.zwifiout,zlu.zwiredin,zlu.zwiredout,zlu.zwwanin,zlu.zwwanout FROM zprocess zp,zliveusage zlu," \
            "z_primarykey zpk WHERE zp.z_ent = zpk.z_ent AND zp.z_pk = zlu.zhasprocess ORDER BY zpk.z_name"
    with sqlite_connection:
        cur = sqlite_connection.cursor()
        cur.execute(query)
        rows = cur.fetchall()
        for row in rows:
            if row[0] is None:
                output_file.write("Name     :\r\n")
            else:
                output_file.write("Name     : {}\r\n".format(row[0]))
            if row[1] is None:
                output_file.write("Process  :\r\n")
            else:
                output_file.write("Process  : {}\r\n".format(row[1]))
            if row[2] is None:
                output_file.write("Timestamp:\r\n")
            else:
                output_file.write("Timestamp: {}\r\n".format(row[2]))
            if row[3] is None:
                output_file.write("WiFi In  :\r\n")
            else:
                output_file.write("WiFi In  : {}\r\n".format(row[3]))
            if row[4] is None:
                output_file.write("WiFi Out :\r\n")
            else:
                output_file.write("WiFi Out : {}\r\n".format(row[4]))
            if row[5] is None:
                output_file.write("Wired In :\r\n")
            else:
                output_file.write("Wired In : {}\r\n".format(row[5]))
            if row[6] is None:
                output_file.write("Wired Out:\r\n")
            else:
                output_file.write("Wired Out: {}\r\n".format(row[6]))
            if row[7] is None:
                output_file.write("WAN In   :\r\n")
            else:
                output_file.write("WAN In   : {}\r\n".format(row[7]))
            if row[8] is None:
                output_file.write("WAN Out  :\r\n")
            else:
                output_file.write("WAN Out  : {}\r\n".format(row[8]))
            output_file.write("\r\n")


def run_network_attachment_query(sqlite_connection, output_file):
    query = "SELECT zpk.z_name,zna.zidentifier,datetime(zna.zfirsttimestamp + 978307200, 'unixepoch')," \
            "datetime(zna.ztimestamp + 978307200, 'unixepoch') FROM znetworkattachment zna,z_primarykey zpk " \
            "WHERE zna.z_ent = zpk.z_ent ORDER BY zpk.z_name"
    with sqlite_connection:
            cur = sqlite_connection.cursor()
            cur.execute(query)
            rows = cur.fetchall()
            for row in rows:
                if row[0] is None:
                    output_file.write("Name           :\r\n")
                else:
                    output_file.write("Name           : {}\r\n".format(row[0]))
                if row[1] is None:
                    output_file.write("Network        :\r\n")
                    output_file.write("MAC Address    :\r\n")
                else:
                    ident = row[1]
                    dash_index = ident.rfind("-")
                    network_name = ident[0:dash_index]
                    network_mac = ident[dash_index+1:len(ident)]
                    output_file.write("Network        : {}\r\n".format(network_name))
                    output_file.write("MAC Address    : {}\r\n".format(network_mac))
                if row[2] is None:
                    output_file.write("First Timestamp:\r\n")
                else:
                    output_file.write("First Timestamp: {}\r\n".format(row[2]))
                if row[3] is None:
                    output_file.write("Timestamp      :\r\n")
                else:
                    output_file.write("Timestamp      : {}\r\n".format(row[3]))
                output_file.write("\r\n")
