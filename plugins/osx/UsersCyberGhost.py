__author__ = 'bolodev'
__version__ = '0.1'
__license__ = 'GPLv3'
from riplib.Plugin import Plugin
import ccl_bplist
import codecs
import datetime
import logging
import os


class UsersCyberGhost(Plugin):
    """
    Parse information from /Users/{username}/Library/Preferences/com.cyberghostsrl.cyberghostmac.plist
    """

    def __init__(self):
        """
        Initialise the class.
        """
        super().__init__()
        self._name = "User Cyber Ghost VPN Configuration"
        self._description = "Parse information from /Users/{username}/Library/Preferences/com.cyberghostsrl.cyberghostmac.plist"
        self._data_file = "com.cyberghostsrl.cyberghostmac.plist"
        self._output_file = ""  # this will have to be defined per user account
        self._type = "bplist"
    
    def parse(self):
        """
        Scan for the plist
        """
        users_path = os.path.join(self._input_dir, "Users")
        if os.path.isdir(users_path):
            user_list = os.listdir(users_path)
            for username in user_list:
                if os.path.isdir(os.path.join(users_path, username)) and not username == "Shared":
                    config = os.path.join(users_path, username, "Library", "Preferences", self._data_file)
                    if os.path.isfile(config):
                        self.__parse_plist(config, username)
                    else:
                        logging.warning("{} does not exist.".format(config))
                        print("[WARNING] {} does not exist.".format(config))
        else:
            print("[WARNING] {} does not exist.".format(users_path))
            
    def __parse_plist(self, file, username):
        """
        Parse /Users/{username}/Library/Preferences/com.cyberghostsrl.cyberghostmac.plist
        """
        with codecs.open(os.path.join(self._output_dir, "Users_" + username + "_VPN_CyberGhost.txt"), "a", encoding="utf-8") as of:
            of.write("="*10 + " " + self._name + " " + "="*10 + "\r\n")
            of.write("Source File: {}\r\n\r\n".format(file))
            if os.path.isfile(file):
                bplist = open(file, "rb")
                pl = ccl_bplist.load(bplist)
                bplist.close()
                try:
                    # Cyberghost_GUID
                    if "Cyberghost_GUID" in pl:
                        of.write("Cyberghost GUID      : {}\r\n".format(pl["Cyberghost_GUID"]))
                    # startAtSystemStart
                    if "startAtSystemStart" in pl:
                        of.write("Start at System Start: {}\r\n".format(pl["startAtSystemStart"]))
                    # SULastCheckTime
                    if "SULastCheckTime" in pl:
                        of.write("SU Last Check Time   : {}\r\n".format(pl["SULastCheckTime"]))
                    # RandomPort
                    if "RandomPort" in pl:
                        of.write("Random Port          : {}\r\n".format(pl["RandomPort"]))
                    # useOpenVpnOverTcp
                    if "useOpenVpnOverTcp" in pl:
                        of.write("Use OpenVpn Over Tcp : {}\r\n".format(pl["useOpenVpnOverTcp"]))
                    # Cyberghost_RemoteSettings -> DICT
                    if "Cyberghost_RemoteSettings" in pl:
                        of.write("Cyberghost Remote Settings:\r\n")
                        remote_settings = pl["Cyberghost_RemoteSettings"]
                        # instdate -> Unix Millisecond
                        date_foo = remote_settings["instdate"]
                        # print(type(date_foo))
                        date_foo = datetime.datetime.fromtimestamp(date_foo/1000.0)
                        of.write("\tInstall Date           : {}\r\n".format(date_foo))
                        # LastCountry
                        of.write("\tLast Country           : {}\r\n".format(remote_settings["LastCountry"]))
                        # LastServer
                        of.write("\tLast Server            : {}\r\n".format(remote_settings["LastServer"]))
                        # LastLoggedIn
                        of.write("\tLast Logged In         : {}\r\n".format(remote_settings["LastLoggedIn"]))
                        # LastPlanID
                        of.write("\tLas tPlan ID           : {}\r\n".format(remote_settings["LastPlanID"]))
                        # ENC_ConnectedServerID
                        of.write("\tENC Connected Server ID: {}\r\n".format(remote_settings["ENC_ConnectedServerID"]))
                        # LastPlanName
                        of.write("\tLast Plan Name         : {}\r\n".format(remote_settings["LastPlanName"]))
                        # startCounter
                        of.write("\tStart Counter          : {}\r\n".format(remote_settings["startCounter"]))
                except KeyError:
                    pass
            else:
                logging.warning("File: {} does not exist or cannot be found.\r\n".format(file))
                of.write("[WARNING] File: {} does not exist or cannot be found.\r\n".format(file))
                print("[WARNING] File: {} does not exist or cannot be found.\r\n".format(file))
            of.write("="*40 + "\r\n\r\n")
        of.close()
