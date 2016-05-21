from riplib.Plugin import Plugin
import codecs
import logging
import os
import ccl_bplist

__author__ = 'osxripper'
__version__ = '0.1'
__license__ = 'GPLv3'


class SystemGlobalPreferences(Plugin):
    """
    Plugin to derive time information from /Library/Preferences/.GlobalPreferences.plist
    """
    
    def __init__(self):
        """
        Initialise the class.
        """
        super().__init__()
        self._name = "System Settings"
        self._description = "Parse /Library/Preferences/.GlobalPreferences.plist"
        self._data_file = ".GlobalPreferences.plist"
        self._output_file = "System.txt"
        self._type = "bplist"
    
    def parse(self):
        """
        Parse /Library/Preferences/.GlobalPreferences.plist
        """
        with codecs.open(os.path.join(self._output_dir, self._output_file), "a", encoding="utf-8") as of:
            of.write("="*10 + " " + self._name + " " + "="*10 + "\r\n")
            global_plist = os.path.join(self._input_dir, "Library", "Preferences", self._data_file)
            of.write("Source File: {}\r\n\r\n".format(global_plist))
            if self._os_version in ["el_capitan", "yosemite", "mavericks", "mountain_lion", "lion"]:
                if os.path.isfile(global_plist):
                    bplist = open(global_plist, "rb")
                    plist = ccl_bplist.load(bplist)
                    bplist.close()
                    if "MultipleSessionEnabled" in plist:
                        of.write("Multiple Session Enabled       : {}\r\n".format(plist["MultipleSessionEnabled"]))
                    if "com.apple.updatesettings_did_disable_ftp" in plist:
                        of.write("Update Settings Did Disable FTP: {}\r\n"
                                 .format(plist["com.apple.updatesettings_did_disable_ftp"]))
                    if "com.apple.AppleModemSettingTool.LastCountryCode" in plist:
                        of.write("Modem Last Country Code        : {}\r\n"
                                 .format(plist["com.apple.AppleModemSettingTool.LastCountryCode"]))
                    if "Country" in plist:
                        of.write("Country                        : {}\r\n".format(plist["Country"]))
                    if "AppleLocale" in plist:
                        of.write("Apple Locale                   : {}\r\n".format(plist["AppleLocale"]))
                    if "AppleLanguages" in plist:
                        apple_languages = plist["AppleLanguages"]
                        of.write("Languages:\r\n")
                        for apple_language in apple_languages:
                            of.write("\tLanguage: {}\r\n".format(apple_language))
                else:
                    logging.warning("File {} does not exist.".format(global_plist))
                    print("[WARNING] File {} does not exist.".format(global_plist))
            elif self._os_version == "snow_leopard":
                if os.path.isfile(global_plist):
                    bplist = open(global_plist, "rb")
                    plist = ccl_bplist.load(bplist)
                    bplist.close()
                    if "com.apple.AppleModemSettingTool.LastCountryCode" in plist:
                        of.write("Last Country Code: {}\r\n"
                                 .format(plist["com.apple.AppleModemSettingTool.LastCountryCode"]))
                    if "com.apple.preferences.timezone.selected_city" in plist:
                        of.write("Selected City: {}\r\n")
                        selected_city = plist["com.apple.preferences.timezone.selected_city"]
                        if "RegionalCode" in selected_city:
                            of.write("\tRegional Code : {}\r\n".format(selected_city["RegionalCode"]))
                        if "Version" in selected_city:
                            of.write("\tVersion       : {}\r\n".format(selected_city["Version"]))
                        if "TimeZoneName" in selected_city:
                            of.write("\tTime Zone Name: {}\r\n".format(selected_city["TimeZoneName"]))
                        if "Latitude" in selected_city:
                            of.write("\tLatitude      : {}\r\n".format(selected_city["Latitude"]))
                        if "Longitude" in selected_city:
                            of.write("\tLongitude     : {}\r\n".format(selected_city["Longitude"]))
                        if "GeonameID" in selected_city:
                            of.write("\tGeoname ID    : {}\r\n".format(selected_city["GeonameID"]))
                        if "CountryCode" in selected_city:
                            of.write("\tCountry Code  : {}\r\n".format(selected_city["CountryCode"]))
                        if "Name" in selected_city:
                            of.write("\tName          : {}\r\n".format(selected_city["Name"]))

                    if "Country" in plist:
                        of.write("Country: {}\r\n".format(plist["Country"]))
                    if "AppleLocale" in plist:
                        of.write("Apple Locale: {}\r\n".format(plist["AppleLocale"]))
                    if "AppleLanguages" in plist:
                        of.write("Apple Languages:\r\n")
                        for apple_language in plist["AppleLanguages"]:
                            of.write("\t{}\r\n".format(apple_language))
                    if "com.apple.TimeZonePref.Last_Selected_City" in plist:
                        of.write("Last Selected City:\r\n")
                        for item in plist["com.apple.TimeZonePref.Last_Selected_City"]:
                            of.write("\t{}\r\n".format(item))
            else:
                logging.warning("Not a known OSX version.")
                of.write("[WARNING] Not a known OSX version.\r\n")
                print("[WARNING] Not a known OSX version.")
            of.write("="*40 + "\r\n\r\n")
        of.close()
