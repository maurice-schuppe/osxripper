from riplib.Plugin import Plugin
import binascii
import codecs
import logging
import os
import plistlib
import riplib.ccl_bplist

__author__ = 'osxripper'
__version__ = '0.1'
__license__ = 'GPLv3'


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
            plist_file = os.path\
                .join(self._input_dir, "Library", "Preferences", "SystemConfiguration", "com.apple.smb.server.plist")
            of.write("Source File: {0}\r\n\r\n".format(plist_file))
            if self._os_version in ["el_capitan", "yosemite", "mavericks", "mountain_lion", "lion", "snow_leopard"]:
                if os.path.isfile(plist_file):
                    try:
                        with open(plist_file, "rb") as pl:
                            plist = plistlib.load(pl)
                        if "ServerDescription" in plist:
                            of.write("Server Description  : {0}\r\n".format(plist["ServerDescription"]))
                        if "NetBIOSName" in plist:
                            of.write("Net BIOS Name       : {0}\r\n".format(plist["NetBIOSName"]))
                    except KeyError:
                        pass
                else:
                    logging.warning("File: {0} does not exist or cannot be found.\r\n".format(plist_file))
                    of.write("[WARNING] File: {0} does not exist or cannot be found.\r\n".format(plist_file))
                    print("[WARNING] File: {0} does not exist or cannot be found.".format(plist_file))
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
            if self._os_version in ["el_capitan", "yosemite", "mavericks", "mountain_lion", "lion", "snow_leopard"]:
                with codecs.open(os.path.join(self._output_dir, self._output_file), "a", encoding="utf-8") as of:
                    of.write("="*10 + " DHCP Leases " + "="*10 + "\r\n")
                    for f in file_listing:
                        of.write("Source File: {0}\r\n\r\n".format(f))
                        try:
                            with open(os.path.join(working_dir, f), "rb") as pl:
                                plist = plistlib.load(pl)
                            if "IPAddress" in plist:
                                of.write("IP Address      : {0}\r\n".format(plist["IPAddress"]))
                            if "LeaseStartDate" in plist:
                                of.write("Lease Start Date: {0}\r\n".format(plist["LeaseStartDate"]))
                        except KeyError:
                            pass
                        of.write("\r\n")
                of.close()
            else:
                logging.warning("Not a known OSX version.")
                print("[WARNING] Not a known OSX version.")
        else:
            with codecs.open(os.path.join(self._output_dir, self._output_file), "a", encoding="utf-8") as of:
                of.write("="*10 + " DHCP Leases " + "="*10 + "\r\n")
                of.write("[WARNING] File: {0} does not exist or cannot be found.\r\n".format(working_dir))
            of.close()
            logging.warning("File: {0} does not exist or cannot be found.".format(working_dir))
            print("[WARNING] File: {0} does not exist or cannot be found.".format(working_dir))

    def __timezone(self):
        """
        Parse timezone related files
        """
        global_plist = os.path.join(self._input_dir, "Library", "Preferences", ".GlobalPreferences.plist")
        auto_tz_plist = os.path.join(self._input_dir, "Library", "Caches", "com.apple.AutoTimeZone.plist")
        if self._os_version in ["el_capitan", "yosemite", "mavericks"]:
            if os.path.isfile(global_plist) and os.path.isfile(auto_tz_plist):
                with codecs.open(os.path.join(self._output_dir, self._output_file), "a", encoding="utf-8") as of:
                    of.write("=" * 10 + " Local Time Zone " + "=" * 10 + "\r\n")
                    of.write("Source File: {0}\r\n\r\n".format(global_plist))
                    bplist = open(global_plist, "rb")
                    xml = riplib.ccl_bplist.load(bplist)
                    bplist.close()
                    if "com.apple.preferences.timezone.selected_city" in xml:
                        of.write("Country      : {0}\r\n"
                                 .format(xml["com.apple.preferences.timezone.selected_city"]["CountryCode"]))
                        of.write("Time Zone    : {0}\r\n"
                                 .format(xml["com.apple.preferences.timezone.selected_city"]["TimeZoneName"]))
                        of.write("Selected City: {0}\r\n"
                                 .format(xml["com.apple.preferences.timezone.selected_city"]["Name"]))
                        of.write("Latitude     : {0}\r\n"
                                 .format(xml["com.apple.preferences.timezone.selected_city"]["Latitude"]))
                        of.write("Longitude    : {0}\r\n"
                                 .format(xml["com.apple.preferences.timezone.selected_city"]["Longitude"]))
                        of.write("\r\n")
                        of.write("Source File: {0}\r\n\r\n".format(auto_tz_plist))
                        with open(auto_tz_plist, 'rb') as fp:
                            try:
                                pl = plistlib.load(fp).values()
                                for entry in pl:
                                    of.write("Timestamp: {0}\r\n".format(entry["timestamp"]))
                                    of.write("Time Zone: {0}\r\n".format(entry["timezone"]))
                            except KeyError:
                                pass
                        fp.close()
                    of.write("\r\n")
                of.close()
            else:
                logging.warning("File {0} does not exist.".format(global_plist))
                print("[WARNING] File {0} does not exist.".format(global_plist))

        elif self._os_version in ["mountain_lion", "lion", "snow_leopard"]:
            if os.path.isfile(global_plist):
                with codecs.open(os.path.join(self._output_dir, self._output_file), "a", encoding="utf-8") as of:
                    of.write("=" * 10 + " Local Time Zone " + "=" * 10 + "\r\n")
                    of.write("Source File: {0}\r\n\r\n".format(global_plist))
                    bplist = open(global_plist, "rb")
                    xml = riplib.ccl_bplist.load(bplist)
                    bplist.close()
                    if "com.apple.preferences.timezone.selected_city" in xml:
                        of.write("Country       : {0}\r\n"
                                 .format(xml["com.apple.preferences.timezone.selected_city"]["CountryCode"]))
                        of.write("Time Zone     : {0}\r\n"
                                 .format(xml["com.apple.preferences.timezone.selected_city"]["TimeZoneName"]))
                        of.write("Selected City : {0}\r\n"
                                 .format(xml["com.apple.preferences.timezone.selected_city"]["Name"]))
                        of.write("Latitude      : {0}\r\n"
                                 .format(xml["com.apple.preferences.timezone.selected_city"]["Latitude"]))
                        of.write("Longitude     : {0}\r\n"
                                 .format(xml["com.apple.preferences.timezone.selected_city"]["Longitude"]))
                    of.write("\r\n")
                of.close()
            else:
                logging.warning("File {0} does not exist.".format(global_plist))
                print("[WARNING] File {0} does not exist.".format(global_plist))
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
            if self._os_version in ["el_capitan", "yosemite", "mavericks", "mountain_lion", "lion"]:
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
                                    of.write("Source File: {0}\r\n\r\n".format(test_plist))
                                    name = None
                                    if "name" in pl:
                                        of.write("Name          : {0}\r\n".format(pl["name"][0]))
                                        name = pl["name"][0]
                                    if "realname" in pl:
                                        of.write("Real Name     : {0}\r\n".format(pl["realname"][0]))
                                    if "home" in pl:
                                        of.write("Home          : {0}\r\n".format(pl["home"][0]))
                                    if "hint" in pl:
                                        of.write("Password Hint : {0}\r\n".format(pl["hint"][0]))
                                    if "uid" in pl:
                                        of.write("UID           : {0}\r\n".format(pl["uid"][0]))
                                    if "generateduid" in pl:
                                        of.write("Generated UID : {0}\r\n".format(pl["generateduid"][0]))
                                    if os.path.isdir(
                                            os.path.join("Users", name, "Application Support", "MobileSync", "Backup")):
                                            of.write("Has iOS Backup: Yes\r\n")
                                    else:
                                        of.write("Has iOS Backup: No\r\n")

                                    of.write("\r\n\r\n")
                                else:
                                    return
                            except KeyError:
                                pass
                        else:
                            logging.warning("File: {0} does not exist or cannot be found.".format(test_plist))
                            of.write("[WARNING] File: {0} does not exist or cannot be found.\r\n".format(test_plist))
                            print("[WARNING] File: {0} does not exist or cannot be found.".format(test_plist))
            elif self._os_version == "snow_leopard":
                for f in file_listing:
                    stat_info = os.stat(working_dir + os.path.sep + f)
                    if f.endswith(".plist") and stat_info.st_size > 0:
                        test_plist = os.path.join(working_dir, f)
                        if os.path.isfile(test_plist):
                            try:
                                name = None
                                with open(test_plist, "rb") as pl:
                                    plist = plistlib.load(pl)
                                    if "home" in plist and "/Users" in plist["home"][0]:  # Only /Users
                                        of.write("="*10 + " " + self._name + " " + "="*10 + "\r\n")
                                        of.write("Source File: {0}\r\n\r\n".format(f))
                                        if "name" in plist:
                                            of.write("Name          : {0}\r\n".format(plist["name"][0]))
                                            name = plist["name"][0]
                                        if "realname" in plist:
                                            of.write("Real Name     : {0}\r\n".format(plist["realname"][0]))
                                        if "home" in plist:
                                            of.write("Home          : {0}\r\n".format(plist["home"][0]))
                                        if "hint" in plist:
                                            of.write("Password Hint : {0}\r\n".format(plist["hint"][0]))
                                        if "authentication_authority" in plist:
                                            of.write("Authentication: {0}\r\n"
                                                     .format(plist["authentication_authority"]))
                                        if "uid" in plist:
                                            of.write("UID           : {0}\r\n".format(plist["uid"][0]))
                                        if "gid" in plist:
                                            of.write("GID           : {0}\r\n".format(plist["gid"][0]))
                                        if "generateduid" in plist:
                                            of.write("Generated UID : {0}\r\n".format(plist["generateduid"][0]))
                                        if "shell" in plist:
                                            of.write("Shell         : {0}\r\n".format(plist["shell"][0]))
                                        if "picture" in plist:
                                            of.write("Picture       : {0}\r\n".format(plist["picture"][0]))
                                        if "jpegphoto" in plist and name is not None:
                                            jpeg = os.path\
                                                .join(self._output_dir, "UserAccounts-" + name + "-jpgphoto.jpg")
                                            with open(jpeg, "wb") as jof:
                                                jof.write(plist["jpegphoto"][0])
                                                jof.close()
                                                of.write("Logon Picture: {0}\r\n".format(jpeg))
                                    else:
                                        return
                            except KeyError:
                                pass
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
            if self._os_version in ["el_capitan", "yosemite", "mavericks", "mountain_lion", "lion"]:
                working_dir = os.path.join(self._input_dir, "private", "var", "db", "BootCaches")
                of.write("Source Directory: {0}\r\n\r\n".format(working_dir))
                if os.path.isdir(working_dir):
                    file_listing = os.listdir(working_dir)
                    for f in file_listing:
                        test_file = os.path.join(working_dir, f)
                        if os.path.isdir(test_file):
                            of.write("Generated UID: {0}\r\n".format(f))
                            user_playlists = os.listdir(test_file)
                            for user_file in user_playlists:
                                of.write("\t{0}\r\n".format(user_file))
                            of.write("\r\n")
                else:
                    logging.warning("Directory: {0} does not exist or cannot be found.\r\n".format(working_dir))
                    of.write("[WARNING] Directory: {0} does not exist or cannot be found.\r\n".format(working_dir))
                    print("[WARNING] Directory: {0} does not exist or cannot be found.\r\n".format(working_dir))
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
            of.write("Source File: {0}\r\n\r\n".format(file))
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
            of.write("Source File: {0}\r\n\r\n".format(file))
            if self._os_version in ["el_capitan", "yosemite"]:
                if os.path.isfile(file):
                    bplist = open(file, "rb")
                    plist = riplib.ccl_bplist.load(bplist)
                    bplist.close()
                    try:
                        if "BRPairedDevices" in plist:
                            if len(plist["BRPairedDevices"]) == 0:
                                of.write("BR Paired Devices:\r\n\tNo paired devices listed.\r\n")
                            else:
                                of.write("BR Paired Devices:\r\n")
                                for item in plist["BRPairedDevices"]:
                                    of.write("\tDevice: {0}\r\n".format(item))

                        if "HIDDevices" in plist:
                            if len(plist["HIDDevices"]) == 0:
                                of.write("HID Devices:\r\n\tNo paired devices listed.\r\n")
                            else:
                                of.write("HID Devices:\r\n")
                                for item in plist["HIDDevices"]:
                                    of.write("\tDevice: {0}\r\n".format(item))

                        if "DeviceCache" in plist:

                            for device in plist["DeviceCache"]:
                                of.write("Device Cache\r\n")
                                of.write("\tDevice: {0}\r\n".format(device))

                                if "VendorID" in plist["DeviceCache"][device]:
                                    of.write("\t\tVendor ID: {0}\r\n".format(plist["DeviceCache"][device]["VendorID"]))

                                if "Name" in plist["DeviceCache"][device]:
                                    of.write("\t\tName: {0}\r\n".format(plist["DeviceCache"][device]["Name"]))

                            of.write("\r\n")

                        if "D2D MAC Address" in plist:
                            of.write("D2D MAC Address: {0}\r\n".format(binascii.hexlify(plist["D2D MAC Address"])))

                        if "PairedDevices" in plist:
                            if len(plist["PairedDevices"]) == 0:
                                of.write("Paired Devices:\r\n\tNo paired devices listed.\r\n")
                            else:
                                of.write("Paired Devices:\r\n")
                                for item in plist["PairedDevices"]:
                                    of.write("\tDevice: {0}\r\n".format(item))
                    except KeyError:
                        pass
                    of.write("\r\n")
                else:
                    logging.warning("File: {0} does not exist or cannot be found.".format(file))
                    of.write("[WARNING] File: {0} does not exist or cannot be found.\r\n".format(file))
                    print("[WARNING] File: {0} does not exist or cannot be found.".format(file))

            elif self._os_version == "mavericks":
                if os.path.isfile(file):
                    bplist = open(file, "rb")
                    plist = riplib.ccl_bplist.load(bplist)
                    bplist.close()
                    try:
                        if "PairedDevices" in plist:
                            if len(plist["PairedDevices"]) == 0:
                                of.write("Paired Devices:\r\n\tNo paired devices listed.\r\n")
                            else:
                                of.write("Paired Devices:\r\n")
                                for paired_device in plist["PairedDevices"]:
                                    of.write("\tDevice: {0}\r\n".format(paired_device))

                        if "HIDDevices" in plist:
                            of.write("HIDDevices\r\n")
                            for hid_device in plist["HIDDevices"]:
                                of.write("\tHID Device: {0}\r\n".format(hid_device))

                        if "D2D MAC Address" in plist:
                            of.write("D2D MAC Address :{0}\r\n".format(plist["D2D MAC Address"]))
                        if "DeviceCache" in plist:
                            of.write("Device Cache\r\n")
                            for cached_device in plist["DeviceCache"]:
                                of.write("\tCached Device: {0}\r\n".format(cached_device))
                                for device_data in plist["DeviceCache"][cached_device]:
                                    if "VendorID" in device_data:
                                        of.write("\t\tVendor ID: {0}\r\n"
                                                 .format(plist["DeviceCache"][cached_device]["VendorID"]))
                                    if "Name" in device_data:
                                        of.write("\t\tName: {0}\r\n"
                                                 .format(plist["DeviceCache"][cached_device]["Name"]))
                    except KeyError:
                        pass
                    of.write("\r\n")
                else:
                    logging.warning("File: {0} does not exist or cannot be found.".format(file))
                    of.write("[WARNING] File: {0} does not exist or cannot be found.\r\n".format(file))
                    print("[WARNING] File: {0} does not exist or cannot be found.".format(file))

            elif self._os_version == "mountain_lion":
                if os.path.isfile(file):
                    bplist = open(file, "rb")
                    plist = riplib.ccl_bplist.load(bplist)
                    bplist.close()
                    try:
                        if "D2D MAC Address" in plist:
                            of.write("D2D MAC Address :{0}\r\n".format(plist["D2D MAC Address"]))

                        if "HIDDevices" in plist:
                            of.write("HIDDevices\r\n")
                            for hid_device in plist["HIDDevices"]:
                                of.write("\tHID Device: {0}\r\n".format(hid_device))
                        if "DeviceCache" in plist:
                            of.write("Device Cache\r\n")
                            for cached_device in plist["DeviceCache"]:
                                of.write("\tCached Device: {0}\r\n".format(cached_device))
                                for device_data in plist["DeviceCache"][cached_device]:
                                    if "Name" in device_data:
                                        of.write("\t\tName: {0}\r\n"
                                                 .format(plist["DeviceCache"][cached_device]["Name"]))
                                    if "Manufacturer" in device_data:
                                        of.write("\t\tManufacturer: {0}\r\n"
                                                 .format(plist["DeviceCache"][cached_device]["Manufacturer"]))

                    except KeyError:
                        pass
                    of.write("\r\n")
                else:
                    logging.warning("File: {0} does not exist or cannot be found.".format(file))
                    of.write("[WARNING] File: {0} does not exist or cannot be found.\r\n".format(file))
                    print("[WARNING] File: {0} does not exist or cannot be found.".format(file))
            elif self._os_version == "lion":
                if os.path.isfile(file):
                    bplist = open(file, "rb")
                    plist = riplib.ccl_bplist.load(bplist)
                    bplist.close()
                    try:
                        if "DaemonControllersConfigurationKey" in plist:
                            of.write("Daemon Controllers Configuration Key:\r\n")
                            for dmcck_key in plist["DaemonControllersConfigurationKey"]:
                                of.write("\t{0}\r\n".format(dmcck_key))
                                for item in plist["DaemonControllersConfigurationKey"][dmcck_key]:
                                    of.write("\t\t{0}: {1}\r\n"
                                             .format(item, plist["DaemonControllersConfigurationKey"][dmcck_key][item]))
                        if "PANInterfaces" in plist:
                            of.write("PAN Interfaces:\r\n")
                            for pan_interface in plist["PANInterfaces"]:
                                of.write("\tPAN Interface: {0}\r\n".format(pan_interface))
                        if "ControllerPowerState" in plist:
                            of.write("Controller Power State: {0}\r\n".format(plist["ControllerPowerState"]))
                        if "HIDDevices" in plist:
                            of.write("HIDDevices\r\n")
                            for hid_device in plist["HIDDevices"]:
                                of.write("\tHID Device: {0}\r\n".format(hid_device))
                        if "DeviceCache" in plist:
                            of.write("Device Cache\r\n")
                            for cached_device in plist["DeviceCache"]:
                                of.write("\tCached Device: {0}\r\n".format(cached_device))
                                for device_data in plist["DeviceCache"][cached_device]:
                                    if "Name" in device_data:
                                        of.write("\t\tName: {0}\r\n"
                                                 .format(plist["DeviceCache"][cached_device]["Name"]))
                                    if "Manufacturer" in device_data:
                                        of.write("\t\tManufacturer: {0}\r\n"
                                                 .format(plist["DeviceCache"][cached_device]["Manufacturer"]))
                                    if "ClassOfDevice" in device_data:
                                        of.write("\t\tClass Of Device: {0}\r\n"
                                                 .format(plist["DeviceCache"][cached_device]["ClassOfDevice"]))
                                    if "BatteryPercent" in device_data:
                                        of.write("\t\tBattery Percent: {0}\r\n"
                                                 .format(plist["DeviceCache"][cached_device]["BatteryPercent"]))
                                    if "ClockOffset" in device_data:
                                        of.write("\t\tClock Offset: {0}\r\n"
                                                 .format(plist["DeviceCache"][cached_device]["ClockOffset"]))
                                    if "LastNameUpdate" in device_data:
                                        of.write("\t\tLast Name Update: {0}\r\n"
                                                 .format(plist["DeviceCache"][cached_device]["LastNameUpdate"]))
                                    if "LastServicesUpdate" in device_data:
                                        of.write("\t\tLast Services Update: {0}\r\n"
                                                 .format(plist["DeviceCache"][cached_device]["LastServicesUpdate"]))
                                    if "LastInquiryUpdate" in device_data:
                                        of.write("\t\tLast Inquiry Update: {0}\r\n"
                                                 .format(plist["DeviceCache"][cached_device]["LastInquiryUpdate"]))
                                    if "LMPVersion" in device_data:
                                        of.write("\t\tLMP Version: {0}\r\n"
                                                 .format(plist["DeviceCache"][cached_device]["LMPVersion"]))
                                    if "LMPSubversion" in device_data:
                                        of.write("\t\tLMP Subversion: {0}\r\n"
                                                 .format(plist["DeviceCache"][cached_device]["LMPSubversion"]))
                                    if "InquiryRSSI" in device_data:
                                        of.write("\t\tInquiry RSSI: {0}\r\n"
                                                 .format(plist["DeviceCache"][cached_device]["InquiryRSSI"]))
                                    if "PageScanMode" in device_data:
                                        of.write("\t\tPage Scan Mode: {0}\r\n"
                                                 .format(plist["DeviceCache"][cached_device]["PageScanMode"]))
                                    if "PageScanPeriod" in device_data:
                                        of.write("\t\tPage Scan Period: {0}\r\n"
                                                 .format(plist["DeviceCache"][cached_device]["PageScanPeriod"]))
                                    if "PageScanRepetitionMode" in device_data:
                                        of.write("\t\tPage Scan Repetition Mode: {0}\r\n"
                                                 .format(plist["DeviceCache"][cached_device]["PageScanRepetitionMode"]))
                                    # EIRData NOT PARSED
                                    # Services NOT PARSED
                        # PersistentPorts NOT PARSED

                        if "PairedDevices" in plist:
                            if len(plist["PairedDevices"]) == 0:
                                of.write("Paired Devices:\r\n\tNo paired devices listed.\r\n")
                            else:
                                of.write("Paired Devices:\r\n")
                                for paired_device in plist["PairedDevices"]:
                                    of.write("\tDevice: {0}\r\n".format(paired_device))
                    except KeyError:
                        pass
                    of.write("\r\n")
                else:
                    logging.warning("File: {0} does not exist or cannot be found.".format(file))
                    of.write("[WARNING] File: {0} does not exist or cannot be found.\r\n".format(file))
                    print("[WARNING] File: {0} does not exist or cannot be found.".format(file))
            elif self._os_version == "snow_leopard":
                if os.path.isfile(file):
                    bplist = open(file, "rb")
                    plist = riplib.ccl_bplist.load(bplist)
                    bplist.close()
                    try:
                        if "BluetoothAutoSeekHIDDevices" in plist:
                            of.write("Bluetooth Auto Seek HID Devices: {0}\r\n"
                                     .format(plist["BluetoothAutoSeekHIDDevices"]))
                        if "ControllerPowerState" in plist:
                            of.write("Controller Power State         : {0}\r\n".format(plist["ControllerPowerState"]))
                        if "BluetoothVersionNumber" in plist:
                            of.write("Bluetooth Version Number       : {0}\r\n".format(plist["BluetoothVersionNumber"]))
                        if "DaemonControllersConfigurationKey" in plist:
                            of.write("Daemon Controllers Configuration Key:\r\n")
                            for dmcck_key in plist["DaemonControllersConfigurationKey"]:
                                of.write("\t{}\r\n".format(dmcck_key))
                                for item in plist["DaemonControllersConfigurationKey"][dmcck_key]:
                                    of.write("\t\t{0}: {1}\r\n"
                                             .format(item, plist["DaemonControllersConfigurationKey"][dmcck_key][item]))
                        if "HIDDevices" in plist:
                            hid_array = plist["PairedDevices"]
                            of.write("HID Devices: {0}\r\n")
                            for hid_device in hid_array:
                                of.write("\t{0}\r\n".format(hid_device))
                        if "DeviceCache" in plist:
                            of.write("Device Cache\r\n")
                            for cached_device in plist["DeviceCache"]:
                                of.write("\tCached Device: {0}\r\n".format(cached_device))
                                for device_data in plist["DeviceCache"][cached_device]:
                                    if "Name" in device_data:
                                        of.write("\t\tName: {0}\r\n"
                                                 .format(plist["DeviceCache"][cached_device]["Name"]))
                                    if "Manufacturer" in device_data:
                                        of.write("\t\tManufacturer: {0}\r\n"
                                                 .format(plist["DeviceCache"][cached_device]["Manufacturer"]))
                                    if "ClassOfDevice" in device_data:
                                        of.write("\t\tClass Of Device: {0}\r\n"
                                                 .format(plist["DeviceCache"][cached_device]["ClassOfDevice"]))
                                    if "BatteryPercent" in device_data:
                                        of.write("\t\tBattery Percent: {0}\r\n"
                                                 .format(plist["DeviceCache"][cached_device]["BatteryPercent"]))
                                    if "ClockOffset" in device_data:
                                        of.write("\t\tClock Offset: {0}\r\n"
                                                 .format(plist["DeviceCache"][cached_device]["ClockOffset"]))
                                    if "LastNameUpdate" in device_data:
                                        of.write("\t\tLast Name Update: {0}\r\n"
                                                 .format(plist["DeviceCache"][cached_device]["LastNameUpdate"]))
                                    if "LastServicesUpdate" in device_data:
                                        of.write("\t\tLast Services Update: {0}\r\n"
                                                 .format(plist["DeviceCache"][cached_device]["LastServicesUpdate"]))
                                    if "LastInquiryUpdate" in device_data:
                                        of.write("\t\tLast Inquiry Update: {0}\r\n"
                                                 .format(plist["DeviceCache"][cached_device]["LastInquiryUpdate"]))
                                    if "LMPVersion" in device_data:
                                        of.write("\t\tLMP Version: {0}\r\n"
                                                 .format(plist["DeviceCache"][cached_device]["LMPVersion"]))
                                    if "LMPSubversion" in device_data:
                                        of.write("\t\tLMP Subversion: {0}\r\n"
                                                 .format(plist["DeviceCache"][cached_device]["LMPSubversion"]))
                                    if "InquiryRSSI" in device_data:
                                        of.write("\t\tInquiry RSSI: {0}\r\n"
                                                 .format(plist["DeviceCache"][cached_device]["InquiryRSSI"]))
                                    if "PageScanMode" in device_data:
                                        of.write("\t\tPage Scan Mode: {0}\r\n"
                                                 .format(plist["DeviceCache"][cached_device]["PageScanMode"]))
                                    if "PageScanPeriod" in device_data:
                                        of.write("\t\tPage Scan Period: {0}\r\n"
                                                 .format(plist["DeviceCache"][cached_device]["PageScanPeriod"]))
                                    if "PageScanRepetitionMode" in device_data:
                                        of.write("\t\tPage Scan Repetition Mode: {0}\r\n"
                                                 .format(plist["DeviceCache"][cached_device]["PageScanRepetitionMode"]))
                        # PairedDevices
                        if "PairedDevices" in plist:
                            paired_array = plist["PairedDevices"]
                            of.write("Paired Devices:\r\n")
                            for paired_device in paired_array:
                                of.write("\t{0}\r\n".format(paired_device))
                    except KeyError:
                        pass
                    of.write("\r\n")
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
            of.write("Source File: {0}\r\n\r\n".format(plist_file))
            if self._os_version in ["el_capitan", "yosemite", "mavericks", "mountain_lion", "lion", "snow_leopard"]:
                if os.path.isfile(plist_file):
                    try:
                        with open(plist_file, "rb") as pl:
                            plist = plistlib.load(pl)
                        for item in plist:
                            if "contentType" in item:
                                of.write("Content Type       : {0}\r\n".format(item["contentType"]))
                            if "displayName" in item:
                                of.write("Display Name       : {0}\r\n".format(item["displayName"]))
                            if "displayVersion" in item:
                                of.write("Display Version    : {0}\r\n".format(item["displayVersion"]))
                            if "date" in item:
                                of.write("Date               : {0}\r\n".format(item["date"]))
                            if "processName" in item:
                                of.write("Process Name       : {0}\r\n".format(item["processName"]))
                            if "packageIdentifiers" in item:
                                of.write("Package Identifiers:\r\n")
                                for packageItem in item["packageIdentifiers"]:
                                    of.write("\t{0}\r\n".format(packageItem))
                            of.write("\r\n")
                    except KeyError:
                        pass
                else:
                    logging.warning("File: {0} does not exist or cannot be found.\r\n".format(plist_file))
                    of.write("[WARNING] File: {0} does not exist or cannot be found.\r\n".format(plist_file))
                    print("[WARNING] File: {0} does not exist or cannot be found.".format(plist_file))
            else:
                logging.warning("Not a known OSX version.")
                print("[WARNING] Not a known OSX version.")
            of.write("="*10 + "\r\n")
        of.close()
