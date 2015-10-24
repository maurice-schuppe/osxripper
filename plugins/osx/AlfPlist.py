__author__ = 'osxripper'
__version__ = '0.1'
__license__ = 'GPLv3'
from riplib.Plugin import Plugin
import codecs
import logging
import os
import ccl_bplist


class AlfPlist(Plugin):
    """
    Plugin to parse /Library/Preferences/com.apple.alf.plist
    """
    def __init__(self):
        """
        Initialise plugins
        """
        super().__init__()
        self._name = "Firewall Settings"
        self._description = "Parse Firewall settings from /Library/Preferences/com.apple.alf.plist"
        self._data_file = "com.apple.alf.plist"
        self._output_file = "Networking.txt"
        self._type = "bplist"
        
    def parse(self):
        with codecs.open(os.path.join(self._output_dir, self._output_file), "a", encoding="utf-8") as of:
            of.write("="*10 + " " + self._name + " " + "="*10 + "\r\n")
            file = os.path.join(self._input_dir, "Library", "Preferences", self._data_file)
            of.write("Source File: {}\r\n\r\n".format(file))
            if self._os_version == "el_capitan" or self._os_version == "yosemite" or self._os_version == "mavericks":
                if os.path.isfile(file):
                    bplist = open(file, "rb")
                    plist = ccl_bplist.load(bplist)
                    try:
                        # allowsignedenabled
                        if "allowsignedenabled" in plist:
                            of.write("Allow Signed: {}\r\n".format(plist["allowsignedenabled"]))
                        # globalstate
                        if "globalstate" in plist:
                            of.write("Global State: {}\r\n".format(plist["globalstate"]))
                        # loggingoption
                        if "loggingoption" in plist:
                            of.write("Global State: {}\r\n".format(plist["loggingoption"]))
                        # stealthenabled
                        if "stealthenabled" in plist:
                            of.write("Stealth Enabled: {}\r\n".format(plist["stealthenabled"]))
                        # version
                        if "version" in plist:
                            of.write("Version: {}\r\n".format(plist["version"]))
                        # loggingenabled
                        if "loggingenabled" in plist:
                            of.write("Logging Enabled: {}\r\n".format(plist["loggingenabled"]))
                        # firewallunload
                        if "firewallunload" in plist:
                            of.write("Firewall Unload: {}\r\n".format(plist["firewallunload"]))
                            
                        # exceptions ARRAY of DICT
                        if "exceptions" in plist:
                            of.write("Exceptions:\r\n")
                            exps = plist["exceptions"]
                            for exp in exps:
                                # path
                                of.write("\tPath: {}\r\n".format(exp["path"]))
                                # state
                                of.write("\tState: {}\r\n".format(exp["state"]))

                        # firewall DICT of DICTs
                        if "firewall" in plist:
                            firewall_dict = plist["firewall"]
                            of.write("Firewall:\r\n")
                            for fw_dict in firewall_dict:
                                of.write("\t{}:\r\n".format(fw_dict))
                                # state
                                of.write("\t\tState: {}\r\n".format(firewall_dict[fw_dict]["state"]))
                                # proc
                                of.write("\t\tProc: {}\r\n".format(firewall_dict[fw_dict]["proc"]))

                        # explicitauths ARRAY
                        if "explicitauths" in plist:
                            explicit_auths = plist["explicitauths"]
                            of.write("Explicit Auths:\r\n")
                            for explicit_auth in explicit_auths:
                                of.write("\t{}\r\n".format(explicit_auth["id"]))
                            
                    except KeyError:
                        pass
                    bplist.close()
                else:
                    logging.warning("File: {} does not exist or cannot be found.".format(file))
                    of.write("[WARNING] File: {} does not exist or cannot be found.\r\n".format(file))
                    print("[WARNING] File: {} does not exist or cannot be found.".format(file))
                    
            elif self._os_version == "mountain_lion" or self._os_version == "lion":
                if os.path.isfile(file):
                    bplist = open(file, "rb")
                    plist = ccl_bplist.load(bplist)
                    try:
                        # allowsignedenabled
                        if "allowsignedenabled" in plist:
                            of.write("Allow Signed: {}\r\n".format(plist["allowsignedenabled"]))
                        # globalstate
                        if "globalstate" in plist:
                            of.write("Global State: {}\r\n".format(plist["globalstate"]))
                        # loggingoption
                        if "loggingoption" in plist:
                            of.write("Global State: {}\r\n".format(plist["loggingoption"]))
                        # stealthenabled
                        if "stealthenabled" in plist:
                            of.write("Stealth Enabled: {}\r\n".format(plist["stealthenabled"]))
                        # version
                        if "version" in plist:
                            of.write("Version: {}\r\n".format(plist["version"]))
                        # loggingenabled
                        if "loggingenabled" in plist:
                            of.write("Logging Enabled: {}\r\n".format(plist["loggingenabled"]))
                        # firewallunload
                        if "firewallunload" in plist:
                            of.write("Firewall Unload: {}\r\n".format(plist["firewallunload"]))
                        # previousonstate
                        if "previousonstate" in plist:
                            of.write("Previous On State: {}\r\n".format(plist["previousonstate"]))
                            
                        # exceptions ARRAY of DICT
                        if "exceptions" in plist:
                            of.write("Exceptions:\r\n")
                            exps = plist["exceptions"]
                            for exp in exps:
                                # path
                                of.write("\tPath: {}\r\n".format(exp["path"]))
                                # state
                                of.write("\tState: {}\r\n".format(exp["state"]))

                        # firewall DICT of DICTs
                        if "firewall" in plist:
                            firewall_dict = plist["firewall"]
                            of.write("Firewall:\r\n")
                            for fw_dict in firewall_dict:
                                of.write("\t{}:\r\n".format(fw_dict))
                                # state
                                of.write("\t\tState: {}\r\n".format(firewall_dict[fw_dict]["state"]))
                                # proc
                                of.write("\t\tProc: {}\r\n".format(firewall_dict[fw_dict]["proc"]))

                        # explicitauths ARRAY
                        if "explicitauths" in plist:
                            explicit_auths = plist["explicitauths"]
                            of.write("Explicit Auths:\r\n")
                            for explicit_auth in explicit_auths:
                                of.write("\t{}\r\n".format(explicit_auth["id"]))
                            
                    except KeyError:
                        pass
                    bplist.close()
                else:
                    logging.warning("File: {} does not exist or cannot be found.".format(file))
                    of.write("[WARNING] File: {} does not exist or cannot be found.\r\n".format(file))
                    print("[WARNING] File: {} does not exist or cannot be found.".format(file))
            elif self._os_version == "snow_leopard":
                if os.path.isfile(file) and os.path.getsize(file) != 0:
                    bplist = open(file, "rb")
                    plist = ccl_bplist.load(bplist)
                    try:
                        if "allowsignedenabled" in plist:
                            of.write("Allow Signed: {}\r\n".format(plist["allowsignedenabled"]))
                        if "globalstate" in plist:
                            of.write("Global State: {}\r\n".format(plist["globalstate"]))
                        if "loggingoption" in plist:
                            of.write("Global State: {}\r\n".format(plist["loggingoption"]))
                        if "stealthenabled" in plist:
                            of.write("Stealth Enabled: {}\r\n".format(plist["stealthenabled"]))
                        if "version" in plist:
                            of.write("Version: {}\r\n".format(plist["version"]))
                        if "loggingenabled" in plist:
                            of.write("Logging Enabled: {}\r\n".format(plist["loggingenabled"]))
                        if "firewallunload" in plist:
                            of.write("Firewall Unload: {}\r\n".format(plist["firewallunload"]))

                        if "exceptions" in plist:
                            of.write("Exceptions:\r\n")
                            exps = plist["exceptions"]
                            for exp in exps:
                                of.write("\tPath: {}\r\n".format(exp["path"]))
                                of.write("\tState: {}\r\n".format(exp["state"]))

                        if "firewall" in plist:
                            firewall_dict = plist["firewall"]
                            of.write("Firewall:\r\n")
                            for fw_dict in firewall_dict:
                                of.write("\t{}:\r\n".format(fw_dict))
                                of.write("\t\tState: {}\r\n".format(firewall_dict[fw_dict]["state"]))
                                of.write("\t\tProc: {}\r\n".format(firewall_dict[fw_dict]["proc"]))

                        if "explicitauths" in plist:
                            explicit_auths = plist["explicitauths"]
                            of.write("Explicit Auths:\r\n")
                            for explicit_auth in explicit_auths:
                                of.write("\t{}\r\n".format(explicit_auth["path"]))

                        if "signexceptions" in plist:
                            signed_exceptions = plist["signexceptions"]
                            of.write("Signed Exceptions:\r\n")
                            for signed_exception in signed_exceptions:
                                proc_name = signed_exception["procname"]
                                if proc_name == "":
                                    proc_name = "NO_PROC_NAME"
                                of.write("\tProc Name: {}\r\n".format(proc_name))
                                if "bundleid" in signed_exception:
                                    of.write("\tBundle ID : {}\r\n".format(signed_exception["bundleid"]))
                                if "creator" in signed_exception:
                                    of.write("\tCreator   : {}\r\n".format(signed_exception["creator"]))

                        if "applications" in plist:
                            applications = plist["applications"]
                            of.write("Applications:\r\n")
                            for application in applications:
                                of.write("\tBundle ID: {}\r\n".format(application["bundleid"]))
                                of.write("\tState    : {}\r\n".format(application["state"]))

                    except KeyError as e:
                        pass
                    bplist.close()
                pass
            else:
                logging.warning("Not a known OSX version.")
                print("[WARNING] Not a known OSX version.")
            of.write("="*40 + "\r\n\r\n")
        of.close()