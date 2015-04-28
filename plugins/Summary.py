__author__ = 'osxripper'
__version__ = '0.1'
__license__ = 'GPLv3'
from riplib.Plugin import Plugin
import binascii
import codecs
import logging
import os
import plistlib
import riplib.ccl_bplist


class Summary(Plugin):
    """
    Plugin to output a summary of the system
    """

    def __init__(self):
        """
        Initialise the class.
        """
        super().__init__()
        self._name = "Summary"
        self._description = "Parse data for system summary"
        self._output_file = "OSXRipper_Summary.txt"
        self._type = "multiple"

    def parse(self):
        self.__hostname()
        self.__ip_mac()
        self.__timezone()
        self.__user_accounts()
        self.__playlists()
        self.__time_machine()
        self.__bluetooth_pairing()
        self.__install_history()

    def __hostname(self):
        """
        Parse /Library/Preferences/SystemConfiguration/com.apple.smb.server.plist
        """
        with codecs.open(os.path.join(self._output_dir, self._output_file), "a", encoding="utf-8") as of:
            of.write("="*10 + " Hostname " + "="*10 + "\r\n")
            plist_file = os.path.join(self._input_dir, "Library", "Preferences", "SystemConfiguration", "com.apple.smb.server.plist")
            of.write("Source File: {}\r\n\r\n".format(plist_file))
            if self._os_version == "yosemite" or self._os_version == "mavericks" or self._os_version == "mountain_lion":
                if os.path.isfile(plist_file):
                    try:
                        with open(plist_file, "rb") as pl:
                            plist = plistlib.load(pl)
                        if "ServerDescription" in plist:
                            of.write("Server Description  : {}\r\n".format(plist["ServerDescription"]))
                        if "NetBIOSName" in plist:
                            of.write("Net BIOS Name       : {}\r\n".format(plist["NetBIOSName"]))
                    except KeyError:
                        pass
                else:
                    logging.warning("File: {} does not exist or cannot be found.\r\n".format(plist_file))
                    of.write("[WARNING] File: {} does not exist or cannot be found.\r\n".format(plist_file))
                    print("[WARNING] File: {} does not exist or cannot be found.".format(plist_file))
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
            of.write("\r\n")
        of.close()

    def __ip_mac(self):
        """
        Parse DHCP Lease files
        """
        working_dir = os.path.join(self._input_dir, "private", "var", "db", "dhcpclient", "leases")
        if os.path.isdir(working_dir):
            file_listing = os.listdir(working_dir)
            if self._os_version == "yosemite" or self._os_version == "mavericks" or self._os_version == "mountain_lion":
                with codecs.open(os.path.join(self._output_dir, self._output_file), "a", encoding="utf-8") as of:
                    of.write("="*10 + " DHCP Leases " + "="*10 + "\r\n")
                    for f in file_listing:
                        of.write("Source File: {}\r\n\r\n".format(f))
                        try:
                            with open(os.path.join(working_dir, f), "rb") as pl:
                                plist = plistlib.load(pl)
                            if "IPAddress" in plist:
                                of.write("IP Address      : {}\r\n".format(plist["IPAddress"]))
                            if "LeaseStartDate" in plist:
                                of.write("Lease Start Date: {}\r\n".format(plist["LeaseStartDate"]))
                        except KeyError:
                            pass
                        of.write("\r\n")
                of.close()
            elif self._os_version == "lion":
                logging.info("This version of OSX is not supported by this plugin.")
                print("[INFO] This version of OSX is not supported by this plugin.")
            elif self._os_version == "snow_leopard":
                logging.info("This version of OSX is not supported by this plugin.")
                print("[INFO] This version of OSX is not supported by this plugin.")
            else:
                logging.warning("Not a known OSX version.")
                print("[WARNING] Not a known OSX version.")
        else:
            with codecs.open(os.path.join(self._output_dir, self._output_file), "a", encoding="utf-8") as of:
                of.write("="*10 + " DHCP Leases " + "="*10 + "\r\n")
                of.write("[WARNING] File: {} does not exist or cannot be found.\r\n".format(working_dir))
            of.close()
            logging.warning("File: {} does not exist or cannot be found.".format(working_dir))
            print("[WARNING] File: {} does not exist or cannot be found.".format(working_dir))

    def __timezone(self):
        """
        Parse timezone related files
        """
        global_plist = os.path.join(self._input_dir, "Library", "Preferences", ".GlobalPreferences.plist")
        auto_tz_plist = os.path.join(self._input_dir, "Library", "Caches", "com.apple.AutoTimeZone.plist")
        if self._os_version == "yosemite" or self._os_version == "mavericks":
            if os.path.isfile(global_plist) and os.path.isfile(auto_tz_plist):
                with codecs.open(os.path.join(self._output_dir, self._output_file), "a", encoding="utf-8") as of:
                    of.write("=" * 10 + " Local Time Zone " + "=" * 10 + "\r\n")
                    of.write("Source File: {}\r\n\r\n".format(global_plist))
                    bplist = open(global_plist, "rb")
                    xml = riplib.ccl_bplist.load(bplist)
                    bplist.close()
                    if "com.apple.preferences.timezone.selected_city" in xml:
                        of.write("Country      : {}\r\n".format(xml["com.apple.preferences.timezone.selected_city"]["CountryCode"]))
                        of.write("Time Zone    : {}\r\n".format(xml["com.apple.preferences.timezone.selected_city"]["TimeZoneName"]))
                        of.write("Selected City: {}\r\n".format(xml["com.apple.preferences.timezone.selected_city"]["Name"]))
                        of.write("Latitude     : {}\r\n".format(xml["com.apple.preferences.timezone.selected_city"]["Latitude"]))
                        of.write("Longitude    : {}\r\n".format(xml["com.apple.preferences.timezone.selected_city"]["Longitude"]))
                        of.write("\r\n")
                        of.write("Source File: {}\r\n\r\n".format(auto_tz_plist))
                        with open(auto_tz_plist, 'rb') as fp:
                            try:
                                pl = plistlib.load(fp).values()
                                for entry in pl:
                                    of.write("Timestamp: {}\r\n".format(entry["timestamp"]))
                                    of.write("Time Zone: {}\r\n".format(entry["timezone"]))
                            except KeyError:
                                pass
                        fp.close()
                    of.write("\r\n")
                of.close()
            else:
                logging.warning("File {} does not exist.".format(global_plist))
                print("[WARNING] File {} does not exist.".format(global_plist))

        elif self._os_version == "mountain_lion":
            if os.path.isfile(global_plist):
                with codecs.open(os.path.join(self._output_dir, self._output_file), "a", encoding="utf-8") as of:
                    of.write("=" * 10 + " Local Time Zone " + "=" * 10 + "\r\n")
                    of.write("Source File: {}\r\n\r\n".format(global_plist))
                    bplist = open(global_plist, "rb")
                    xml = riplib.ccl_bplist.load(bplist)
                    bplist.close()
                    if "com.apple.preferences.timezone.selected_city" in xml:
                        of.write("Country       : {}\r\n".format(xml["com.apple.preferences.timezone.selected_city"]["CountryCode"]))
                        of.write("Time Zone     : {}\r\n".format(xml["com.apple.preferences.timezone.selected_city"]["TimeZoneName"]))
                        of.write("Selected City : {}\r\n".format(xml["com.apple.preferences.timezone.selected_city"]["Name"]))
                        of.write("Latitude      : {}\r\n".format(xml["com.apple.preferences.timezone.selected_city"]["Latitude"]))
                        of.write("Longitude     : {}\r\n".format(xml["com.apple.preferences.timezone.selected_city"]["Longitude"]))
                    of.write("\r\n")
                of.close()
            else:
                logging.warning("File {} does not exist.".format(global_plist))
                print("[WARNING] File {} does not exist.".format(global_plist))
        elif self._os_version == "lion":
            logging.info("This version of OSX is not supported by this plugin.")
            print("[INFO] This version of OSX is not supported by this plugin.")
            # of.write("[INFO] This version of OSX is not supported by this plugin.\r\n")
        elif self._os_version == "snow_lepoard":
            logging.info("This version of OSX is not supported by this plugin.")
            print("[INFO] This version of OSX is not supported by this plugin.")
            # of.write("[INFO] This version of OSX is not supported by this plugin.\r\n")
        else:
            logging.warning("Not a known OSX version.")
            print("[WARNING] Not a known OSX version.")

    def __user_accounts(self):
        """
        Parse a User Account Binary Plist files
        """
        working_dir = os.path.join(self._input_dir, "private", "var", "db", "dslocal", "nodes", "Default", "users")
        file_listing = os.listdir(working_dir)
        with codecs.open(os.path.join(self._output_dir, self._output_file), "a", encoding="utf-8") as of:
            of.write("="*10 + " User Plists " + "="*10 + "\r\n\r\n")
            if self._os_version == "yosemite" or self._os_version == "mavericks" or self._os_version == "mountain_lion":
                for f in file_listing:
                    stat_info = os.stat(working_dir + os.path.sep + f)
                    if f.endswith(".plist") and stat_info.st_size > 0:
                        test_plist = os.path.join(working_dir, f)
                        if os.path.isfile(test_plist):
                            bplist = open(test_plist, "rb")
                            pl = riplib.ccl_bplist.load(bplist)
                            bplist.close()
                            try:
                                if "home" in pl and "/Users" in pl["home"][0]:  # Only /Users
                                    of.write("Source File: {}\r\n\r\n".format(test_plist))
                                    name = None
                                    if "name" in pl:
                                        of.write("Name          : {}\r\n".format(pl["name"][0]))
                                        name = pl["name"][0]
                                    if "realname" in pl:
                                        of.write("Real Name     : {}\r\n".format(pl["realname"][0]))
                                    if "home" in pl:
                                        of.write("Home          : {}\r\n".format(pl["home"][0]))
                                    if "hint" in pl:
                                        of.write("Password Hint : {}\r\n".format(pl["hint"][0]))
                                    if "uid" in pl:
                                        of.write("UID           : {}\r\n".format(pl["uid"][0]))
                                    if "generateduid" in pl:
                                        of.write("Generated UID : {}\r\n".format(pl["generateduid"][0]))
                                    if os.path.isdir(os.path.join("Users", name, "Application Support", "MobileSync", "Backup")):
                                            of.write("Has iOS Backup: Yes\r\n")
                                    else:
                                        of.write("Has iOS Backup: No\r\n")

                                    of.write("\r\n\r\n")
                                else:
                                    return
                            except KeyError:
                                pass
                        else:
                            logging.warning("File: {} does not exist or cannot be found.".format(test_plist))
                            of.write("[WARNING] File: {} does not exist or cannot be found.\r\n".format(test_plist))
                            print("[WARNING] File: {} does not exist or cannot be found.".format(test_plist))
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
                of.write("[INFO] Not a known OSX version.\r\n")
        of.close()

    def __playlists(self):
        """
        List .playlist files under /private/var/db/BootCaches
        """
        with codecs.open(os.path.join(self._output_dir, self._output_file), "a", encoding="utf-8") as of:
            of.write("="*10 + " Playlists " + "="*10 + "\r\n")
            if self._os_version == "yosemite" or self._os_version == "mavericks" or self._os_version == "mountain_lion":
                working_dir = os.path.join(self._input_dir, "private", "var", "db", "BootCaches")
                of.write("Source Directory: {}\r\n\r\n".format(working_dir))
                if os.path.isdir(working_dir):
                    file_listing = os.listdir(working_dir)
                    for f in file_listing:
                        test_file = os.path.join(working_dir, f)
                        if os.path.isdir(test_file):
                            of.write("Generated UID: {}\r\n".format(f))
                            user_playlists = os.listdir(test_file)
                            for user_file in user_playlists:
                                of.write("\t{}\r\n".format(user_file))
                            of.write("\r\n")
                else:
                    logging.warning("Directory: {} does not exist or cannot be found.\r\n".format(working_dir))
                    of.write("[WARNING] Directory: {} does not exist or cannot be found.\r\n".format(working_dir))
                    print("[WARNING] Directory: {} does not exist or cannot be found.\r\n".format(working_dir))
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
        of.close()

    def __time_machine(self):
        """
        Check if /Library/Preferences/com.apple.TimeMachine.plist exists
        """
        with codecs.open(os.path.join(self._output_dir, self._output_file), "a", encoding="utf-8") as of:
            of.write("="*10 + " TimeMachine  " + "="*10 + "\r\n")
            file = os.path.join(self._input_dir, "Library", "Preferences", "com.apple.TimeMachine.plist")
            of.write("Source File: {}\r\n\r\n".format(file))
            if os.path.isfile(file):
                bplist = open(file, "rb")
                plist = riplib.ccl_bplist.load(bplist)
                bplist.close()
                if "Destinations" in plist:
                    of.write("Time Machine Plist Exists: Yes and Destinations key present.\r\n\r\n")
                else:
                    of.write("Time Machine Plist Exists: Yes and no Destinations key present.\r\n\r\n")
            else:
                of.write("Time Machine Plist Exists: No\r\n\r\n")
        of.close()

    def __bluetooth_pairing(self):
        """
        /Library/Preferences/com.apple.Bluetooth.plist
        """
        with codecs.open(os.path.join(self._output_dir, self._output_file), "a", encoding="utf-8") as of:
            of.write("="*10 + " Bluetooth  " + "="*10 + "\r\n")
            file = os.path.join(self._input_dir, "Library", "Preferences", "com.apple.Bluetooth.plist")
            of.write("Source File: {}\r\n\r\n".format(file))
            if self._os_version == "yosemite":
                if os.path.isfile(file):
                    bplist = open(file, "rb")
                    plist = riplib.ccl_bplist.load(bplist)
                    bplist.close()
                    try:
                        # BRPairedDevices ARRAY
                        if "BRPairedDevices" in plist:
                            if len(plist["BRPairedDevices"]) == 0:
                                of.write("BR Paired Devices:\r\n\tNo paired devices listed.\r\n")
                            else:
                                of.write("BR Paired Devices:\r\n")
                                for item in plist["BRPairedDevices"]:
                                    of.write("\tDevice: {}\r\n".format(item))

                        # HIDDevices ARRAY
                        if "HIDDevices" in plist:
                            if len(plist["HIDDevices"]) == 0:
                                of.write("HID Devices:\r\n\tNo paired devices listed.\r\n")
                            else:
                                of.write("HID Devices:\r\n")
                                for item in plist["HIDDevices"]:
                                    of.write("\tDevice: {}\r\n".format(item))

                        # DeviceCache  NESTED DICT
                        if "DeviceCache" in plist:

                            for device in plist["DeviceCache"]:
                                of.write("Device Cache\r\n")
                                of.write("\tDevice: {}\r\n".format(device))

                                # VendorID
                                if "VendorID" in plist["DeviceCache"][device]:
                                    of.write("\t\tVendor ID: {}\r\n".format(plist["DeviceCache"][device]["VendorID"]))

                                # Name
                                if "Name" in plist["DeviceCache"][device]:
                                    of.write("\t\tName: {}\r\n".format(plist["DeviceCache"][device]["Name"]))

                            of.write("\r\n")

                        # D2D MAC Address DATA
                        if "D2D MAC Address" in plist:
                            of.write("D2D MAC Address: {}\r\n".format(binascii.hexlify(plist["D2D MAC Address"])))  # data

                        # PairedDevices ARRAY
                        if "PairedDevices" in plist:
                            if len(plist["PairedDevices"]) == 0:
                                of.write("Paired Devices:\r\n\tNo paired devices listed.\r\n")
                            else:
                                of.write("Paired Devices:\r\n")
                                for item in plist["PairedDevices"]:
                                    of.write("\tDevice: {}\r\n".format(item))
                    except KeyError:
                        pass
                    of.write("\r\n")
                else:
                    logging.warning("File: {} does not exist or cannot be found.".format(file))
                    of.write("[WARNING] File: {} does not exist or cannot be found.\r\n".format(file))
                    print("[WARNING] File: {} does not exist or cannot be found.".format(file))

            elif self._os_version == "mavericks":
                if os.path.isfile(file):
                    bplist = open(file, "rb")
                    plist = riplib.ccl_bplist.load(bplist)
                    bplist.close()
                    try:
                        # PairedDevices ARRAY
                        if "PairedDevices" in plist:
                            if len(plist["PairedDevices"]) == 0:
                                of.write("Paired Devices:\r\n\tNo paired devices listed.\r\n")
                            else:
                                of.write("Paired Devices:\r\n")
                                for paired_device in plist["PairedDevices"]:
                                    of.write("\tDevice: {}\r\n".format(paired_device))

                        # HIDDevices
                        if "HIDDevices" in plist:
                            of.write("HIDDevices\r\n")
                            for hid_device in plist["HIDDevices"]:
                                of.write("\tHID Device: {}\r\n".format(hid_device))

                        # D2D MAC Address
                        if "D2D MAC Address" in plist:
                            of.write("D2D MAC Address :{}\r\n".format(plist["D2D MAC Address"]))
                        # DeviceCache
                        if "DeviceCache" in plist:
                            of.write("Device Cache\r\n")
                            for cached_device in plist["DeviceCache"]:
                                # MAC ADDRESS
                                of.write("\tCached Device: {}\r\n".format(cached_device))
                                for device_data in plist["DeviceCache"][cached_device]:
                                    # VendorID
                                    if "VendorID" in device_data:
                                        of.write("\t\tVendor ID: {}\r\n".format(plist["DeviceCache"][cached_device]["VendorID"]))
                                    # Name
                                    if "Name" in device_data:
                                        of.write("\t\tName: {}\r\n".format(plist["DeviceCache"][cached_device]["Name"]))
                    except KeyError:
                        pass
                    of.write("\r\n")
                else:
                    logging.warning("File: {} does not exist or cannot be found.".format(file))
                    of.write("[WARNING] File: {} does not exist or cannot be found.\r\n".format(file))
                    print("[WARNING] File: {} does not exist or cannot be found.".format(file))

            elif self._os_version == "mountain_lion":
                if os.path.isfile(file):
                    bplist = open(file, "rb")
                    plist = riplib.ccl_bplist.load(bplist)
                    bplist.close()
                    try:
                        # D2D MAC Address
                        if "D2D MAC Address" in plist:
                            of.write("D2D MAC Address :{}\r\n".format(plist["D2D MAC Address"]))

                        # HIDDevices ARRAY
                        if "HIDDevices" in plist:
                            of.write("HIDDevices\r\n")
                            for hid_device in plist["HIDDevices"]:
                                of.write("\tHID Device: {}\r\n".format(hid_device))
                        # DeviceCache
                        if "DeviceCache" in plist:
                            of.write("Device Cache\r\n")
                            for cached_device in plist["DeviceCache"]:
                                # MAC ADDRESS
                                of.write("\tCached Device: {}\r\n".format(cached_device))
                                for device_data in plist["DeviceCache"][cached_device]:
                                    # Name
                                    if "Name" in device_data:
                                        of.write("\t\tName: {}\r\n".format(plist["DeviceCache"][cached_device]["Name"]))
                                    # Manufacturer
                                    if "Manufacturer" in device_data:
                                        of.write("\t\tManufacturer: {}\r\n".format(plist["DeviceCache"][cached_device]["Manufacturer"]))

                    except KeyError:
                        pass
                    of.write("\r\n")
                else:
                    logging.warning("File: {} does not exist or cannot be found.".format(file))
                    of.write("[WARNING] File: {} does not exist or cannot be found.\r\n".format(file))
                    print("[WARNING] File: {} does not exist or cannot be found.".format(file))
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
        of.close()

    def __install_history(self):
        """
        Parse /Library/Receipts/InstallHistory.plist
        """
        with codecs.open(os.path.join(self._output_dir, self._output_file), "a", encoding="utf-8") as of:
            of.write("="*10 + " Install History " + "="*10 + "\r\n")
            plist_file = os.path.join(self._input_dir, "Library", "Receipts", "InstallHistory.plist")
            of.write("Source File: {}\r\n\r\n".format(plist_file))
            if self._os_version == "yosemite" or self._os_version == "mavericks" or self._os_version == "mountain_lion":
                if os.path.isfile(plist_file):
                    try:
                        with open(plist_file, "rb") as pl:
                            plist = plistlib.load(pl)
                        for item in plist:
                            if "contentType" in item:
                                of.write("Content Type       : {}\r\n".format(item["contentType"]))
                            if "displayName" in item:
                                of.write("Display Name       : {}\r\n".format(item["displayName"]))
                            if "displayVersion" in item:
                                of.write("Display Version    : {}\r\n".format(item["displayVersion"]))
                            if "date" in item:
                                of.write("Date               : {}\r\n".format(item["date"]))
                            if "processName" in item:
                                of.write("Process Name       : {}\r\n".format(item["processName"]))
                            if "packageIdentifiers" in item:  # Array
                                of.write("Package Identifiers:\r\n")
                                for packageItem in item["packageIdentifiers"]:
                                    of.write("\t{}\r\n".format(packageItem))
                            of.write("\r\n")
                    except KeyError:
                        pass
                else:
                    logging.warning("File: {} does not exist or cannot be found.\r\n".format(plist_file))
                    of.write("[WARNING] File: {} does not exist or cannot be found.\r\n".format(plist_file))
                    print("[WARNING] File: {} does not exist or cannot be found.".format(plist_file))

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
        of.close()