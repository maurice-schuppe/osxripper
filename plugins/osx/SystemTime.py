__author__ = 'osxripper'
__version__ = '0.1'
__license__ = 'GPLv3'

from riplib.Plugin import Plugin
import codecs
import logging
import os
import plistlib
import ccl_bplist


class SystemTime(Plugin):
    """
    Plugin to derive time information from /Library/Preferences/.GlobalPreferences.plist, /private/etc/localtime, /private/etc/ntp.conf, and /Library/Preferences/com.apple.timezone.auto.plist
    """
    
    def __init__(self):
        """
        Initialise the class.
        """
        super().__init__()
        self._name = "System Time"
        self._description = "List files in /private/var/db/BootCaches"
        self._data_file = ""  # multiple files being accessed
        self._output_file = "SystemTime.txt"
        self._type = "mixed"
    
    def parse(self):
        """
        Read and parse /Library/Preferences/.GlobalPreferences.plist, /private/etc/localtime, /private/etc/ntp.conf, and /Library/Preferences/com.apple.timezone.auto.plist
        """
        if self._os_version == "yosemite" or self._os_version == "mavericks":
            global_plist = os.path.join(self._input_dir, "Library", "Preferences", ".GlobalPreferences.plist")
            auto_tz_plist = os.path.join(self._input_dir, "Library", "Caches", "com.apple.AutoTimeZone.plist")
            tz_auto_plist = os.path.join(self._input_dir, "Library", "Preferences", "com.apple.timezone.auto.plist")
            ntp_conf = os.path.join(self._input_dir, "private", "etc", "ntp.conf")
            if os.path.isfile(global_plist):
                self.__parse_global_plist(global_plist)
            else:
                logging.warning("File {} does not exist.".format(global_plist))
                print("[WARNING] File {} does not exist.".format(global_plist))
            
            if os.path.isfile(auto_tz_plist):
                self.__parse_auto_timezone_plist(auto_tz_plist)
            else:
                logging.warning("File {} does not exist.".format(auto_tz_plist))
                print("[WARNING] File {} does not exist.".format(auto_tz_plist))
                
            if os.path.isfile(tz_auto_plist):
                self.__parse_timezone_auto_plist(tz_auto_plist)
            else:
                logging.warning("File {} does not exist.".format(tz_auto_plist))
                print("[WARNING] File {} does not exist.".format(tz_auto_plist))
            
            if os.path.isfile(ntp_conf):
                self.__read_ntp(ntp_conf)
            else:
                logging.warning("File {} does not exist.".format(ntp_conf))
                print("[WARNING] File {} does not exist.".format(ntp_conf))
        
        elif self._os_version == "mountain_lion" or self._os_version == "lion" or self._os_version == "snow_leopard":
            global_plist = os.path.join(self._input_dir, "Library", "Preferences", ".GlobalPreferences.plist")
            # auto_tz_plist = os.path.join(self._input_dir, "Library", "Caches", "com.apple.AutoTimeZone.plist")
            # tz_auto_plist = os.path.join(self._input_dir, "Library", "Preferences", "com.apple.timezone.auto.plist")
            ntp_conf = os.path.join(self._input_dir, "private", "etc", "ntp.conf")
            if os.path.isfile(global_plist):
                self.__parse_global_plist(global_plist)
            else:
                logging.warning("File {} does not exist.".format(global_plist))
                print("[WARNING] File {} does not exist.".format(global_plist))
            
            # if os.path.isfile(auto_tz_plist):
            #    self.__parse_auto_timezone_plist(auto_tz_plist)
            # else:
            #    print("[WARNING] File {} does not exist.".format(auto_tz_plist))
                
            # if os.path.isfile(tz_auto_plist):
            #    self.__parse_timezone_auto_plist(tz_auto_plist)
            # else:
            #    print("[WARNING] File {} does not exist.".format(tz_auto_plist))
            
            if os.path.isfile(ntp_conf):
                self.__read_ntp(ntp_conf)
            else:
                logging.warning("File {} does not exist.".format(ntp_conf))
                print("[WARNING] File {} does not exist.".format(ntp_conf))
        # elif self._os_version == "lion":
            # logging.info("This version of OSX is not supported by this plugin.")
            # print("[INFO] This version of OSX is not supported by this plugin.")
            # of.write("[INFO] This version of OSX is not supported by this plugin.\r\n")
        # elif self._os_version == "snow_lepoard":
            # logging.info("This version of OSX is not supported by this plugin.")
            # print("[INFO] This version of OSX is not supported by this plugin.")
            # of.write("[INFO] This version of OSX is not supported by this plugin.\r\n")
        else:
            logging.warning("Not a known OSX version.")
            print("[WARNING] Not a known OSX version.")
    
    def __parse_global_plist(self, file):
        """
        Parse a Binary Plist file
        """
        with codecs.open(os.path.join(self._output_dir, self._output_file), "a", encoding="utf-8") as of:
            of.write("=" * 10 + " Local Time Zone " + "=" * 10 + "\r\n")
            of.write("Source File: {}\r\n\r\n".format(file))
            bplist = open(file, "rb")
            xml = ccl_bplist.load(bplist)
            bplist.close()
            if "com.apple.preferences.timezone.selected_city" in xml:
                of.write("Country       : {}\r\n".format(xml["com.apple.preferences.timezone.selected_city"]["CountryCode"]))
                of.write("Time Zone     : {}\r\n".format(xml["com.apple.preferences.timezone.selected_city"]["TimeZoneName"]))
                of.write("Selected City : {}\r\n".format(xml["com.apple.preferences.timezone.selected_city"]["Name"]))
                of.write("Latitude      : {}\r\n".format(xml["com.apple.preferences.timezone.selected_city"]["Latitude"]))
                of.write("Longitude     : {}\r\n".format(xml["com.apple.preferences.timezone.selected_city"]["Longitude"]))
            of.write("=" * 40 + "\r\n\r\n")
        of.close()

    def __read_ntp(self, file):
        with codecs.open(os.path.join(self._output_dir, self._output_file), "a", encoding="utf-8") as of:
            of.write("=" * 10 + " Time Server Setting " + "=" * 10 + "\r\n")
            of.write("Source File: {}\r\n\r\n".format(file))
            # f = open(file, "rb")
            f = open(file, "r")
            of.write("NTP Server: {}\r\n".format(f.read()))
            f.close()
            of.write("=" * 40 + "\r\n\r\n")
        of.close()

######################################################################################
# Issue when running on a live machine in that the file appears to be a binary file, 
# this deos not appear to be the case when addressing an extracted copy from an image
########################################################################################
#    def __read_localtime(self, file):
#        with codecs.open(os.path.join(self._output_dir, self._output_file), "a", encoding="utf-8") as of:
#            of.write("=" * 10 + " Local Timezone " + "=" * 10 + "\r\n")
#            of.write("Source File: {}".format(file))
#            of.write("N.B. On a live system this may look like a binary dump, check the string at the end for Timezone information\r\n\r\n")
#            f = open(file, "rb")
#            of.write("Local Timezone: " + f.read() + "\r\n")
#            f.close()
#            of.write("=" * 40 + "\r\n\r\n")
#        of.close()
        
    def __parse_auto_timezone_plist(self, file):
        """
        Parse a plain XML Plist file
        """
        with codecs.open(os.path.join(self._output_dir, self._output_file), "a", encoding="utf-8") as of:
            of.write("="*10 + " Auto Timezone " + "="*10 + "\r\n")
            of.write("Source File: {}\r\n\r\n".format(file))
            with open(file, 'rb') as fp:
                try:
                    pl = plistlib.load(fp).values()
                    for entry in pl:
                        of.write("Timestamp: {}\r\n".format(entry["timestamp"]))
                        of.write("Time Zone: {}\r\n".format(entry["timezone"]))
                except KeyError:
                    pass
                fp.close()
            of.write("="*40 + "\r\n\r\n")
        of.close()
        
    def __parse_timezone_auto_plist(self, file):
        """
        Parse a plain XML Plist file
        """
        with codecs.open(os.path.join(self._output_dir, self._output_file), "a", encoding="utf-8") as of:
            of.write("="*10 + " Timezone Auto " + "="*10 + "\r\n")
            of.write("Source File: {}\r\n\r\n".format(file))
            with open(file, 'rb') as fp:
                try:
                    pl = plistlib.load(fp)
                    of.write("Active: {}\r\n".format(pl["Active"]))
                except KeyError:
                    pass
                fp.close()
            of.write("="*40 + "\r\n\r\n")
        of.close()