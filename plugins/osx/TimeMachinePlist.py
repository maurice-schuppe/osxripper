__author__ = 'osxripper'
__version__ = '0.1'
__license__ = 'GPLv3'
from riplib.Plugin import Plugin
import codecs
import logging
import os
import ccl_bplist


class TimeMachinePlist(Plugin):
    """
    Plugin to parse /Library/Preferences/com.apple.TimeMachine.plist
    """
    
    def __init__(self):
        """
        Initialise the class.
        """
        super().__init__()
        self._name = "TimeMachine"
        self._description = "Parse data from /Library/Preferences/com.apple.TimeMachine.plist"
        self._data_file = "com.apple.TimeMachine.plist"
        self._output_file = "TimeMachine.txt"
        self._type = "bplist"
        
    def parse(self):
        """
        Parse /Library/Preferences/com.apple.TimeMachine.plist
        """
        with codecs.open(os.path.join(self._output_dir, self._output_file), "a", encoding="utf-8") as of:
            of.write("="*10 + " " + self._name + " " + "="*10 + "\r\n")
            file = os.path.join(self._input_dir, "Library", "Preferences", self._data_file)
            of.write("Source File: {}\r\n\r\n".format(file))
            if self._os_version == "yosemite" or self._os_version == "mavericks" or self._os_version == "mountain_lion"\
                    or self._os_version == "lion" or self._os_version == "snow_leopard":
                if os.path.isfile(file):
                    try:
                        bplist = open(file, "rb")
                        pl = ccl_bplist.load(bplist)
                        if "MobileBackups" in pl:
                            of.write("MobileBackups                      : {}\r\n".format(pl["MobileBackups"]))
                        if "SkipSystemFiles" in pl:
                            of.write("Skip System Files                  : {}\r\n".format(pl["SkipSystemFiles"]))
                        if "PreferencesVersion" in pl:
                            of.write("Preferences Version                : {}\r\n".format(pl["PreferencesVersion"]))
                        if "AutoBackup" in pl:
                            of.write("AutoBackup                         : {}\r\n".format(pl["AutoBackup"]))
                        if "RequiresACPower" in pl:
                            of.write("Requires AC Power                  : {}\r\n".format(pl["RequiresACPower"]))
                        if "AlwaysShowDeletedBackupsWarning" in pl:
                            of.write("Always Show Deleted Backups Warning: {}\r\n".format(pl["AlwaysShowDeletedBackupsWarning"]))
                        if "RootVolumeUUID" in pl:
                            of.write("Root Volume UUID                   : {}\r\n".format(pl["RootVolumeUUID"]))
                        if "LastDestinationID" in pl:
                            of.write("Last Destination ID                : {}\r\n".format(pl["LastDestinationID"]))
                        if "LocalizedDiskImageVolumeName" in pl:
                            of.write("Localized DiskImag eVolume Name    : {}\r\n".format(pl["LocalizedDiskImageVolumeName"]))
                        if "HostUUIDs" in pl:  # ARRAY of STRING
                            of.write("Host UUIDs:\r\n")
                            for host_uuid in pl["HostUUIDs"]:
                                of.write("\t{}\r\n".format(host_uuid))
                        if "SkipPaths" in pl:  # ARRAY of STRING
                            of.write("Skip Paths:\r\n")
                            for skip_path in pl["SkipPaths"]:
                                of.write("\t{}\r\n".format(skip_path))
                        if "ExcludedVolumeUUIDs" in pl:  # ARRAY of STRING
                            of.write("Excluded Volume UUIDs:\r\n")
                            for exc_vol_uuid in pl["ExcludedVolumeUUIDs"]:
                                of.write("\t{}\r\n".format(exc_vol_uuid))
                        if "IncludeByPath" in pl:  # ARRAY of STRING
                            of.write("Include By Path:\r\n")
                            for inc_path in pl["IncludeByPath"]:
                                of.write("\t{}\r\n".format(inc_path))
                        if "Destinations" in pl:  # ARRAY of DICT
                            of.write("Destinations:\r\n")
                            for destination in pl["Destinations"]:
                                if "RESULT" in destination:
                                    of.write("\tRESULT         : {}\r\n".format(destination["RESULT"]))
                                if "BytesUsed" in destination:
                                    of.write("\tBytes Used     : {}\r\n".format(destination["BytesUsed"]))
                                if "BytesAvailable" in destination:
                                    of.write("\tBytes Available: {}\r\n".format(destination["BytesAvailable"]))
                                if "DestinationID" in destination:
                                    of.write("\tDestination ID : {}\r\n".format(destination["DestinationID"]))
                                if "SnapshotCount" in destination:
                                    of.write("\tSnapshot Count : {}\r\n".format(destination["SnapshotCount"]))
                                if "DestinationUUIDs" in destination:  # ARRAY of STRING
                                    of.write("Destination UUIDs:\r\n")
                                    for dest_uuid in destination["DestinationUUIDs"]:
                                        of.write("\t\t{}\r\n".format(dest_uuid))
                                if "SnapshotDates" in destination:  # ARRAY of DATE
                                    of.write("Snapshot Dates:\r\n")
                                    for snap_date in destination["SnapshotDates"]:
                                        of.write("\t\t{}\r\n".format(snap_date))
                                of.write("\r\n")
                        bplist.close()
                    except KeyError:
                        pass
                else:
                    logging.warning("File: {} does not exist or cannot be found.\r\n".format(file))
                    of.write("[WARNING] File: {} does not exist or cannot be found.\r\n".format(file))
                    print("[WARNING] File: {} does not exist or cannot be found.".format(file))
            
            # elif self._os_version == "lion":
            #     logging.info("This version of OSX is not supported by this plugin.")
            #     print("[INFO] This version of OSX is not supported by this plugin.")
            #     of.write("[INFO] This version of OSX is not supported by this plugin.\r\n")
            # elif self._os_version == "snow_leopard":
            #     logging.info("This version of OSX is not supported by this plugin.")
            #     print("[INFO] This version of OSX is not supported by this plugin.")
            #     of.write("[INFO] This version of OSX is not supported by this plugin.\r\n")
            else:
                logging.warning("Not a known OSX version.")
                print("[WARNING] Not a known OSX version.")
            of.write("="*40 + "\r\n\r\n")
        of.close()