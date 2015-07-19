__author__ = 'osxripper'
__version__ = '0.1'
__license__ = 'GPLv3'

from riplib.Plugin import Plugin
import codecs
import logging
import os
import plistlib


class AirportPreferences(Plugin):
    """
    Plugin to parse /Library/Preferences/SystemConfiguration/com.apple.airport.preferences.plist
    """

    def __init__(self):
        """
        Initialise the class.
        """
        super().__init__()
        self._name = "Airport Preferences"
        self._description = "Parse data from com.apple.airport.preferences.plist"
        self._data_file = "com.apple.airport.preferences.plist"
        self._output_file = "Networking.txt"
        self._type = "plist"
    
    def parse(self):
        """
        Parse /Library/Preferences/SystemConfiguration/com.apple.airport.preferences.plist
        """
        with codecs.open(os.path.join(self._output_dir, self._output_file), "a", encoding="utf-8") as of:
            of.write("="*10 + " " + self._name + " " + "="*10 + "\r\n")
            plist_file = os.path.join(self._input_dir, "Library", "Preferences", "SystemConfiguration", self._data_file)
            of.write("Source File: {}\r\n\r\n".format(plist_file))
            if self._os_version == "yosemite":
                if os.path.isfile(plist_file):
                    with open(plist_file, "rb") as pl:
                        plist = plistlib.load(pl)
                    try:
                        if "Counter" in plist:
                            of.write("Counter                  : {}\r\n".format(plist["Counter"]))
                        if "KnownNetworks" in plist:  # DICT
                            known_networks = plist["KnownNetworks"]
                            for network_key in known_networks:
                                of.write("Network Key              : {}\r\n".format(network_key))
                                of.write("\tAuto Login             : {}\r\n".format(known_networks[network_key]["AutoLogin"]))
                                of.write("\tCaptive                : {}\r\n".format(known_networks[network_key]["Captive"]))
                                of.write("\tClosed                 : {}\r\n".format(known_networks[network_key]["Closed"]))
                                of.write("\tDisabled               : {}\r\n".format(known_networks[network_key]["Disabled"]))
                                of.write("\tLast Connected         : {}\r\n".format(known_networks[network_key]["LastConnected"]))
                                of.write("\tPasspoint              : {}\r\n".format(known_networks[network_key]["Passpoint"]))
                                of.write("\tPossibly Hidden Network: {}\r\n".format(known_networks[network_key]["PossiblyHiddenNetwork"]))
                                of.write("\tRoaming Profile Type   : {}\r\n".format(known_networks[network_key]["RoamingProfileType"]))
                                of.write("\tSP Roaming             : {}\r\n".format(known_networks[network_key]["SPRoaming"]))
                                of.write("\tSSID                   : {}\r\n".format(known_networks[network_key]["SSID"]))
                                of.write("\tSSID String            : {}\r\n".format(known_networks[network_key]["SSIDString"]))
                                of.write("\tSecurity Type          : {}\r\n".format(known_networks[network_key]["SecurityType"]))
                                of.write("\tSystem Mode            : {}\r\n".format(known_networks[network_key]["SystemMode"]))
                                of.write("\tTemporarily Disabled   : {}\r\n".format(known_networks[network_key]["TemporarilyDisabled"]))
                                
                                channel_history = known_networks[network_key]["ChannelHistory"]
                                of.write("\tChannel History\r\n")
                                for channel in channel_history:
                                    if "Timestamp" in channel:
                                        of.write("\t\tTimestamp   : {}\r\n".format(channel["Timestamp"]))
                                    if "Channel" in channel:
                                        of.write("\t\tChannel   : {}\r\n".format(channel["Channel"]))

                        if "PreferredOrder" in plist:  # ARRAY of string
                            of.write("Preferred Order\r\n")
                            orders = plist["PreferredOrder"]
                            for order in orders:
                                of.write("\t{}\r\n".format(order))
                                
                        if "UpdateHistory" in plist:
                            of.write("Update History\r\n")
                            updates = plist["UpdateHistory"]
                            for update in updates:
                                if "Previous" in update:
                                    if len(update["Previous"]) == 0:
                                        of.write("\tNo data in Previous.\r\n")
                                    else:
                                        of.write("\tPrevious: {}\r\n".format(update["Previous"]))
                                if "Timestamp" in update:
                                    of.write("\tTimestamp: {}\r\n".format(update["Timestamp"]))
                                    
                        if "Version" in plist:
                            of.write("Version: {}\r\n".format(plist["Version"]))
                    except KeyError:
                        pass
                else:
                    logging.warning("File: {} does not exist or cannot be found.".format(plist_file))
                    of.write("[WARNING] File: {} does not exist or cannot be found.\r\n".format(plist_file))
                    print("[WARNING] File: {} does not exist or cannot be found.".format(plist_file))
            
            elif self._os_version == "mavericks":
                if os.path.isfile(plist_file):
                    with open(plist_file, "rb") as pl:
                        plist = plistlib.load(pl)
                    try:
                        of.write("Remembered Networks\r\n\r\n")
                        # RememberedNetworks ARRAY of DICT
                        for remembered in plist["RememberedNetworks"]:
                            # AutoLogin
                            if "AutoLogin" in remembered:
                                of.write("\tAuto Login: {}\r\n".format(remembered["AutoLogin"]))
                            # Captive
                            if "Captive" in remembered:
                                of.write("\tCaptive: {}\r\n".format(remembered["Captive"]))
                            # Closed
                            if "Closed" in remembered:
                                of.write("\tClosed: {}\r\n".format(remembered["Closed"]))
                            # Disabled
                            if "Disabled" in remembered:
                                of.write("\tDisabled: {}\r\n".format(remembered["Disabled"]))
                            # LastConnected
                            if "LastConnected" in remembered:
                                of.write("\tLast Connected: {}\r\n".format(remembered["LastConnected"]))
                            # Passpoint
                            if "Passpoint" in remembered:
                                of.write("\tPasspoint: {}\r\n".format(remembered["Passpoint"]))
                            # PossiblyHiddenNetwork
                            if "PossiblyHiddenNetwork" in remembered:
                                of.write("\tPossibly Hidden Network: {}\r\n".format(remembered["PossiblyHiddenNetwork"]))
                            # SPRoaming
                            if "SPRoaming" in remembered:
                                of.write("\tSPRoaming: {}\r\n".format(remembered["SPRoaming"]))
                            # SSID BASE64 DATA
                            if "SSID" in remembered:
                                of.write("\tSSID: {}\r\n".format(remembered["SSID"]))
                            # SSIDString
                            if "SSIDString" in remembered:
                                of.write("\tSSID String: {}\r\n".format(remembered["SSIDString"]))
                            # SecurityType
                            if "SecurityType" in remembered:
                                of.write("\tSecurity Type: {}\r\n".format(remembered["SecurityType"]))
                            # SystemMode
                            if "SystemMode" in remembered:
                                of.write("\tSystem Mode: {}\r\n".format(remembered["SystemMode"]))
                            # TemporarilyDisabled
                            if "TemporarilyDisabled" in remembered:
                                of.write("\tTemporarily Disabled: {}\r\n".format(remembered["TemporarilyDisabled"]))
                            of.write("\r\n")
                            
                        # Version
                        if "Version" in plist:
                            of.write("Version: {}\r\n".format(plist["Version"]))
                        of.write("\r\n")
                    except KeyError:
                        pass
                        
                else:
                    logging.warning("File: {} does not exist or cannot be found.".format(plist_file))
                    of.write("[WARNING] File: {} does not exist or cannot be found.\r\n".format(plist_file))
                    print("[WARNING] File: {} does not exist or cannot be found.".format(plist_file))
            elif self._os_version == "mountain_lion" or self._os_version == "lion":
                if os.path.isfile(plist_file):
                    with open(plist_file, "rb") as pl:
                        plist = plistlib.load(pl)
                    try:
                        of.write("Remembered Networks\r\n\r\n")
                        # RememberedNetworks ARRAY of DICT
                        remembered = None
                        for remembered in plist["RememberedNetworks"]:
                            # AutoLogin
                            if "AutoLogin" in remembered:
                                of.write("\tAuto Login: {}\r\n".format(remembered["AutoLogin"]))
                            # CachedScanRecord
                            if "CachedScanRecord" in remembered:
                                of.write("\tCached Scan Record\r\n")
                                # BSSID
                                of.write("\t\tChannel: {}\r\n".format(remembered["CachedScanRecord"]["BSSID"]))
                                # CHANNEL
                                of.write("\t\tChannel: {}\r\n".format(remembered["CachedScanRecord"]["CHANNEL"]))
                                # SSID
                                of.write("\t\tSSID: {}\r\n".format(remembered["CachedScanRecord"]["SSID"]))
                                # SSID_STR
                                of.write("\t\tSSID String: {}\r\n".format(remembered["CachedScanRecord"]["SSID_STR"]))
                        # Captive
                        if "Captive" in remembered:
                            of.write("\tCaptive: {}\r\n".format(remembered["Captive"]))
                        # Closed
                        if "Closed" in remembered:
                            of.write("\tClosed: {}\r\n".format(remembered["Closed"]))
                        # Disabled
                        if "Disabled" in remembered:
                            of.write("\tDisabled: {}\r\n".format(remembered["Disabled"]))
                        # LastConnected
                        if "LastConnected" in remembered:
                            of.write("\tLast Connected: {}\r\n".format(remembered["LastConnected"]))
                        # SSID
                        if "SSID" in remembered:
                            of.write("\tSSID: {}\r\n".format(remembered["SSID"]))
                        # SSIDString
                        if "SSIDString" in remembered:
                            of.write("\tSSID String: {}\r\n".format(remembered["SSIDString"]))
                        # SecurityType
                        if "SecurityType" in remembered:
                            of.write("\tSecurity Type: {}\r\n".format(remembered["SecurityType"]))
                        # SystemMode
                        if "SystemMode" in remembered:
                            of.write("\tSystem Mode: {}\r\n".format(remembered["SystemMode"]))
                        # TemporarilyDisabled
                        if "TemporarilyDisabled" in remembered:
                            of.write("\tTemporarily Disabled: {}\r\n".format(remembered["TemporarilyDisabled"]))
                        of.write("\r\n")
                        # Version
                        if "Version" in plist:
                            of.write("Version: {}\r\n".format(plist["Version"]))
                        of.write("\r\n")
                    except KeyError:
                            pass
                else:
                    logging.warning("File: {} does not exist or cannot be found.".format(plist_file))
                    of.write("[WARNING] File: {} does not exist or cannot be found.\r\n".format(plist_file))
                    print("[WARNING] File: {} does not exist or cannot be found.".format(plist_file))
                    
            # elif self._os_version == "lion":
                # logging.info("This version of OSX is not supported by this plugin.")
                # print("[INFO] This version of OSX is not supported by this plugin.")
                # of.write("[INFO] This version of OSX is not supported by this plugin.\r\n")
            elif self._os_version == "snow_leopard":
                if os.path.isfile(plist_file):
                    with open(plist_file, "rb") as pl:
                        plist = plistlib.load(pl)
                    try:
                        if "KnownNetworks" in plist:
                            # print(plist["KnownNetworks"])
                            for known_network in plist["KnownNetworks"]:
                                of.write("Known Network: {}\r\n".format(known_network))  # str
                                for channel in plist["KnownNetworks"][known_network]["Remembered channels"]:
                                    of.write("\tChannel           : {}\r\n".format(channel))  # dict
                                of.write("\tSSID              : {}\r\n".format(plist["KnownNetworks"][known_network]["SSID_STR"]))
                                of.write("\tSecurity Type     : {}\r\n".format(plist["KnownNetworks"][known_network]["SecurityType"]))
                                if "Unique Password ID" in plist["KnownNetworks"][known_network]:
                                    of.write("\tUnique Password ID: {}\r\n".format(plist["KnownNetworks"][known_network]["Unique Password ID"]))
                                of.write("\tTimestamp         : {}\r\n".format(plist["KnownNetworks"][known_network]["_timeStamp"]))
                                of.write("\r\n")

                        if "en1" in plist:
                            of.write("en1\r\n")
                            if "RecentNetworks" in plist["en1"]:
                                recent_networks = plist["en1"]["RecentNetworks"]
                                of.write("Recent Networks:\r\n\r\n")
                                for recent_network in recent_networks:
                                    if "SSID_STR" in recent_network:
                                        of.write("\tSSID              : {}\r\n".format(recent_network["SSID_STR"]))
                                    if "SecurityType" in recent_network:
                                        of.write("\tSecurity Type     : {}\r\n".format(recent_network["SecurityType"]))
                                    if "Unique Network ID" in recent_network:
                                        of.write("\tUnique Network ID : {}\r\n".format(recent_network["Unique Network ID"]))
                                    if "Unique Password ID" in recent_network:
                                        of.write("\tUnique Password ID: {}\r\n".format(recent_network["Unique Password ID"]))
                                    of.write("\r\n")
                            else:
                                of.write("\tNo Recent Networks\r\n")
                    except KeyError as e:
                        # print("[ERROR] {}".format(e))
                        pass
            else:
                logging.warning("[WARNING] Not a known OSX version.")
                print("[WARNING] Not a known OSX version.")
            of.write("="*40 + "\r\n\r\n")
        of.close()