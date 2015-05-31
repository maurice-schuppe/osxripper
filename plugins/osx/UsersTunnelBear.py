__author__ = 'bolodev'
__version__ = '0.1'
__license__ = 'GPLv3'
from riplib.Plugin import Plugin
import ccl_bplist
import codecs
import logging
import os


class UsersTunnelBear(Plugin):
    """
    Parse information from /Users/{username}/Library/Preferences/com.tunnelbear.mac.TunnelBear.plist
    """

    def __init__(self):
        """
        Initialise the class.
        """
        super().__init__()
        self._name = "Tunnelbear VPN Configuration"
        self._description = "Parse information from /Users/{username}/Library/Preferences/com.tunnelbear.mac.TunnelBear.plist file"
        self._data_file = "com.tunnelbear.mac.TunnelBear.plist"
        self._output_file = ""  # this will have to be defined per user account
        self._type = "bplist"
    
    def parse(self):
        """
        Find the xml file
        """
        users_path = os.path.join(self._input_dir, "Users")
        # username = None
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
        with codecs.open(os.path.join(self._output_dir, "Users_" + username + "_VPN_TunnelBear.txt"), "a", encoding="utf-8") as of:
            of.write("="*10 + " " + self._name + " " + "="*10 + "\r\n")
            of.write("Source File: {}\r\n\r\n".format(file))
            if os.path.isfile(file):
                bplist = open(file, "rb")
                pl = ccl_bplist.load(bplist)
                bplist.close()
                try:
                    # username
                    if "username" in pl:
                        of.write("Username                            : {}\r\n".format(pl["username"]))
                    # previousUsername
                    if "previousUsername" in pl:
                        of.write("Previous Username                   : {}\r\n".format(pl["previousUsername"]))
                    # accountVerified
                    if "accountVerified" in pl:
                        of.write("Account Verified                    : {}\r\n".format(pl["accountVerified"]))
                    # paymentStatus
                    if "paymentStatus" in pl:
                        of.write("Payment Status                      : {}\r\n".format(pl["paymentStatus"]))
                    # SULastCheckTime
                    if "SULastCheckTime" in pl:
                        of.write("SU Last Check Time                  : {}\r\n".format(pl["SULastCheckTime"]))
                    # SUEnableAutomaticChecks
                    if "SUEnableAutomaticChecks" in pl:
                        of.write("SU Enable Automatic Checks          : {}\r\n".format(pl["SUEnableAutomaticChecks"]))
                    # uuid
                    if "uuid" in pl:
                        of.write("UUID                                : {}\r\n".format(pl["uuid"]))
                    # vpnToken
                    if "vpnToken" in pl:
                        of.write("VPN Token                           : {}\r\n".format(pl["vpnToken"]))
                    # grizzly
                    if "grizzly" in pl:
                        of.write("Grizzly                             : {}\r\n".format(pl["grizzly"]))
                    # fullRemainingTime
                    if "fullRemainingTime" in pl:
                        of.write("Full Remaining Time                 : {}\r\n".format(pl["fullRemainingTime"]))
                    # currentCountry
                    if "currentCountry" in pl:
                        of.write("Current Country                     : {}\r\n".format(pl["currentCountry"]))
                    # vpnNumSuccessfulTCPConnections
                    if "vpnNumSuccessfulTCPConnections" in pl:
                        of.write("VPN Num. Successful TCP Connections : {}\r\n".format(pl["vpnNumSuccessfulTCPConnections"]))
                    # shouldReconnect
                    if "shouldReconnect" in pl:
                        of.write("Should Reconnect                    : {}\r\n".format(pl["shouldReconnect"]))
                    # vpnServers ARRAY of DICT
                    if "vpnServers" in pl:
                        of.write("VPN Servers:\r\n")
                        vpn_servers = pl["vpnServers"]
                        for vpn_server in vpn_servers:
                            # host
                            of.write("\tHost  : {}\r\n".format(vpn_server["host"]))
                            # port
                            of.write("\tPort  : {}\r\n".format(vpn_server["port"]))
                            # isUdp
                            of.write("\tIs UDP: {}\r\n".format(vpn_server["isUdp"]))
                            of.write("\r\n")
                    # maxBandwidth
                    if "maxBandwidth" in pl:
                        of.write("Max Bandwidth                       : {}\r\n".format(pl["maxBandwidth"]))
                    # bandwidthAvailable
                    if "SUHasLaunchedBefore" in pl:
                        of.write("Has Launched Before                 : {}\r\n".format(pl["SUHasLaunchedBefore"]))
                    # countries ARRAY of DICT
                    if "countries" in pl:
                        of.write("Countries:\r\n")
                        countries = pl["countries"]
                        for country in countries:
                            of.write("\tID  : {}\r\n".format(country["id"]))
                            of.write("\tCode: {}\r\n".format(country["code"]))
                            of.write("\r\n")
                    # lastVersionRun
                    if "lastVersionRun" in pl:
                        of.write("Last Version Run                    : {}\r\n".format(pl["lastVersionRun"]))
                    # fullVersion
                    if "fullVersion" in pl:
                        of.write("Full Version                        : {}\r\n".format(pl["fullVersion"]))
                    # vigilantMode
                    if "vigilantMode" in pl:
                        of.write("Vigilant Mode                       : {}\r\n".format(pl["vigilantMode"]))
                    # privacyEnabled
                    if "privacyEnabled" in pl:
                        of.write("Privacy Enabled                     : {}\r\n".format(pl["privacyEnabled"]))
                    # notificationsEnabled
                    if "notificationsEnabled" in pl:
                        of.write("Notifications Enabled               : {}\r\n".format(pl["notificationsEnabled"]))
                    # dockIconEnabled
                    if "dockIconEnabled" in pl:
                        of.write("Dock Icon Enabled                   : {}\r\n".format(pl["dockIconEnabled"]))
                    # privacyFacebookEnabled
                    if "privacyFacebookEnabled" in pl:
                        of.write("Privacy Facebook Enabled            : {}\r\n".format(pl["privacyFacebookEnabled"]))
                    # privacyLinkedinEnabled
                    if "privacyLinkedinEnabled" in pl:
                        of.write("Privacy Linkedin Enabled            : {}\r\n".format(pl["privacyLinkedinEnabled"]))
                    # privacyTwitterEnabled
                    if "privacyTwitterEnabled" in pl:
                        of.write("Privacy Twitter Enabled             : {}\r\n".format(pl["privacyTwitterEnabled"]))
                except KeyError:
                    pass
            else:
                logging.warning("File: {} does not exist or cannot be found.\r\n".format(file))
                of.write("[WARNING] File: {} does not exist or cannot be found.\r\n".format(file))
                print("[WARNING] File: {} does not exist or cannot be found.\r\n".format(file))
            of.write("="*40 + "\r\n\r\n")
        of.close()
