__author__ = 'osxripper'
__version__ = '0.1'
__license__ = 'GPLv3'

from riplib.Plugin import Plugin
import codecs
import logging
import os
import ccl_bplist


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
            if self._os_version == "yosemite" or self._os_version == "mavericks" or self._os_version == "mountain_lion"\
                    or self._os_version == "lion":
                if os.path.isfile(global_plist):
                    bplist = open(global_plist, "rb")
                    plist = ccl_bplist.load(bplist)
                    bplist.close()
                    # MultipleSessionEnabled
                    if "MultipleSessionEnabled" in plist:
                        of.write("Multiple Session Enabled       : {}\r\n".format(plist["MultipleSessionEnabled"]))
                        
                    # com.apple.updatesettings_did_disable_ftp
                    if "com.apple.updatesettings_did_disable_ftp" in plist:
                        of.write("Update Settings Did Disable FTP: {}\r\n".format(plist["com.apple.updatesettings_did_disable_ftp"]))
                    
                    # com.apple.AppleModemSettingTool.LastCountryCode
                    if "com.apple.AppleModemSettingTool.LastCountryCode" in plist:
                        of.write("Modem Last Country Code        : {}\r\n".format(plist["com.apple.AppleModemSettingTool.LastCountryCode"]))
                    
                    # Country
                    if "Country" in plist:
                        of.write("Country                        : {}\r\n".format(plist["Country"]))
                    
                    # AppleLocale
                    if "AppleLocale" in plist:
                        of.write("Apple Locale                   : {}\r\n".format(plist["AppleLocale"]))
                    
                    # AppleLanguages
                    if "AppleLanguages" in plist:
                        apple_languages = plist["AppleLanguages"]
                        of.write("Languages:\r\n")
                        for apple_language in apple_languages:
                            of.write("\tLanguage: {}\r\n".format(apple_language))
                else:
                    logging.warning("File {} does not exist.".format(global_plist))
                    print("[WARNING] File {} does not exist.".format(global_plist))
            
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
                of.write("[WARNING] Not a known OSX version.\r\n")
                print("[WARNING] Not a known OSX version.")
            of.write("="*40 + "\r\n\r\n")
        of.close()