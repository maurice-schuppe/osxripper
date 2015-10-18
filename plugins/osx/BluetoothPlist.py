__author__ = 'osxripper'
__version__ = '0.1'
__license__ = 'GPLv3'

from riplib.Plugin import Plugin
import binascii
import codecs
import logging
import os
import ccl_bplist


class BluetoothPlist(Plugin):
    """
    Plugin class to parse /Library/Preferences/com.apple.Bluetooth.plist
    """
    def __init__(self):
        """
        Initialise the class.
        """
        super().__init__()
        self._name = "Bluetooth Settings"
        self._description = "Parse bluetooth connection data."
        self._output_file = "Networking.txt"
        self._data_file = "com.apple.Bluetooth.plist"
        self._type = "bplist"
        
    def parse(self): 
        """
        /Library/Preferences/com.apple.Bluetooth.plist
        """
        with codecs.open(os.path.join(self._output_dir, self._output_file), "a", encoding="utf-8") as of:
            of.write("="*10 + " " + self._name + " " + "="*10 + "\r\n")
            file = os.path.join(self._input_dir, "Library", "Preferences", self._data_file)
            of.write("Source File: {}\r\n\r\n".format(file))
            if self._os_version == "el_capitan" or self._os_version == "yosemite":
                if os.path.isfile(file):
                    bplist = open(file, "rb")
                    plist = ccl_bplist.load(bplist)
                    bplist.close()
                    try:
                        # BluetoothVersionNumber
                        if "BluetoothVersionNumber" in plist:
                            of.write("Bluetooth Version Number: {}\r\n".format(plist["BluetoothVersionNumber"]))
                        
                        # IgnoredDevices ARRAY
                        if "IgnoredDevices" in plist:
                            if len(plist["IgnoredDevices"]) == 0:
                                of.write("Ignored Devices:\r\n\tNo ignored devices listed.\r\n")
                            else:
                                of.write("Ignored Devices:\r\n")
                                for item in plist["IgnoredDevices"]:
                                    of.write("\tDevice: {}\r\n".format(item))
                        
                        # BRPairedDevices ARRAY
                        if "BRPairedDevices" in plist:
                            if len(plist["BRPairedDevices"]) == 0:
                                of.write("BR Paired Devices:\r\n\tNo paired devices listed.\r\n")
                            else:
                                of.write("BR Paired Devices:\r\n")
                                for item in plist["BRPairedDevices"]:
                                    of.write("\tDevice: {}\r\n".format(item))
                        
                        # ControllerPowerState INTEGER
                        if "ControllerPowerState" in plist:
                            of.write("Controller Power State: {}\r\n".format(plist["BluetoothVersionNumber"]))
                        
                        # HIDDevices ARRAY
                        if "HIDDevices" in plist:
                            if len(plist["HIDDevices"]) == 0:
                                of.write("HID Devices:\r\n\tNo paired devices listed.\r\n")
                            else:
                                of.write("HID Devices:\r\n")
                                for item in plist["HIDDevices"]:
                                    of.write("\tDevice: {}\r\n".format(item))
                        
                        # PersistentPorts NOTHING OF INTEREST?????
                        
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
                                
                                # LMPSubversion
                                if "LMPSubversion" in plist["DeviceCache"][device]:
                                    of.write("\t\tLMP Subversion: {}\r\n".format(plist["DeviceCache"][device]["LMPSubversion"]))
                                
                                # PageScanPeriod
                                if "PageScanPeriod" in plist["DeviceCache"][device]:
                                    of.write("\t\tPage Scan Period: {}\r\n".format(plist["DeviceCache"][device]["PageScanPeriod"]))
                                
                                # LastNameUpdate
                                if "LastNameUpdate" in plist["DeviceCache"][device]:
                                    of.write("\t\tLast Name Update: {}\r\n".format(plist["DeviceCache"][device]["LastNameUpdate"]))
                                
                                # SupportedFeatures
                                if "SupportedFeatures" in plist["DeviceCache"][device]:
                                    of.write("\t\tSupported Features: {}\r\n".format(binascii.hexlify(plist["DeviceCache"][device]["SupportedFeatures"])))  # data
                                
                                # ProductID
                                if "ProductID" in plist["DeviceCache"][device]:
                                    of.write("\t\tProduct ID: {}\r\n".format(plist["DeviceCache"][device]["ProductID"]))
                                
                                # LMPVersion
                                if "LMPVersion" in plist["DeviceCache"][device]:
                                    of.write("\t\tLMP Version: {}\r\n".format(plist["DeviceCache"][device]["LMPVersion"]))
                                
                                # PageScanRepetitionMode
                                if "PageScanRepetitionMode" in plist["DeviceCache"][device]:
                                    of.write("\t\tPage Scan Repetition Mode: {}\r\n".format(plist["DeviceCache"][device]["PageScanRepetitionMode"]))
                                
                                # LastInquiryUpdate
                                if "LastInquiryUpdate" in plist["DeviceCache"][device]:
                                    of.write("\t\tLast Inquiry Update: {}\r\n".format(plist["DeviceCache"][device]["LastInquiryUpdate"]))
                                    
                                # Manufacturer
                                if "Manufacturer" in plist["DeviceCache"][device]:
                                    of.write("\t\tManufacturer: {}\r\n".format(plist["DeviceCache"][device]["Manufacturer"]))
                                
                                # ClockOffset
                                if "ClockOffset" in plist["DeviceCache"][device]:
                                    of.write("\t\tClock Offset: {}\r\n".format(plist["DeviceCache"][device]["ClockOffset"]))
                                
                                # PageScanMode
                                if "PageScanMode" in plist["DeviceCache"][device]:
                                    of.write("\t\tPage Scan Mode: {}\r\n".format(plist["DeviceCache"][device]["PageScanMode"]))
                                
                                # ClassOfDevice
                                if "ClassOfDevice" in plist["DeviceCache"][device]:
                                    of.write("\t\tClass Of Device: {}\r\n".format(plist["DeviceCache"][device]["ClassOfDevice"]))
                            of.write("\r\n")
                            
                        # D2D MAC Address DATA
                        if "D2D MAC Address" in plist:
                            of.write("D2D MAC Address: {}\r\n".format(binascii.hexlify(plist["D2D MAC Address"])))  # data
                        
                        # PersistentPortsServices  NOTHING OF INTEREST?????
                        
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
                    plist = ccl_bplist.load(bplist)
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
                                    
                        # DaemonControllersConfigurationKey
                        if "DaemonControllersConfigurationKey" in plist:
                            if "DaemonControllersConfigurationKey" in plist:
                                of.write("Daemon Controllers Configuration Key:\r\n")
                                for dmcck_key in plist["DaemonControllersConfigurationKey"]:
                                    # INNER DICT
                                    of.write("\t{}\r\n".format(dmcck_key))
                                    for item in plist["DaemonControllersConfigurationKey"][dmcck_key]:
                                        of.write("\t\t{}: {}\r\n".format(item, plist["DaemonControllersConfigurationKey"][dmcck_key][item]))
                        # ControllerPowerState
                        if "ControllerPowerState" in plist:
                            of.write("Controller Power State: {}\r\n".format(plist["ControllerPowerState"]))
                        # HIDDevices
                        if "HIDDevices" in plist:
                            of.write("HIDDevices\r\n")
                            for hid_device in plist["HIDDevices"]:
                                of.write("\tHID Device: {}\r\n".format(hid_device))
                        # BluetoothVersionNumber
                        if "BluetoothVersionNumber" in plist:
                            of.write("Bluetooth Version Number: {}\r\n".format(plist["BluetoothVersionNumber"]))
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
                                    # LMPSubversion
                                    if "LMPSubversion" in device_data:
                                        of.write("\t\tLMP Subversion: {}\r\n".format(plist["DeviceCache"][cached_device]["LMPSubversion"]))
                                    # LastNameUpdate
                                    if "LastNameUpdate" in device_data:
                                        of.write("\t\tLast Name Update: {}\r\n".format(plist["DeviceCache"][cached_device]["LastNameUpdate"]))
                                    # ProductID
                                    if "ProductID" in device_data:
                                        of.write("\t\tProduct ID: {}\r\n".format(plist["DeviceCache"][cached_device]["ProductID"]))
                                    # LMPVersion
                                    if "LMPVersion" in device_data:
                                        of.write("\t\tLMP Version: {}\r\n".format(plist["DeviceCache"][cached_device]["LMPVersion"]))
                                    # BatteryPercent
                                    if "BatteryPercent" in device_data:
                                        of.write("\t\tBattery Percent: {}\r\n".format(plist["DeviceCache"][cached_device]["BatteryPercent"]))
                                    # Manufacturer
                                    if "Manufacturer" in device_data:
                                        of.write("\t\tManufacturer: {}\r\n".format(plist["DeviceCache"][cached_device]["Manufacturer"]))
                                    # ClassOfDevice
                                    if "ClassOfDevice" in device_data:
                                        of.write("\t\tClass Of Device: {}\r\n".format(plist["DeviceCache"][cached_device]["ClassOfDevice"]))
                                    # LastServicesUpdate
                                    if "LastServicesUpdate" in device_data:
                                        of.write("\t\tLast Services Update: {}\r\n".format(plist["DeviceCache"][cached_device]["LastServicesUpdate"]))

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
                    plist = ccl_bplist.load(bplist)
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
                        # D2D MAC Address
                        if "D2D MAC Address" in plist:
                            of.write("D2D MAC Address :{}\r\n".format(plist["D2D MAC Address"]))
                        # DaemonControllersConfigurationKey
                        if "DaemonControllersConfigurationKey" in plist:
                            of.write("Daemon Controllers Configuration Key:\r\n")
                            for dmcck_key in plist["DaemonControllersConfigurationKey"]:
                                # INNER DICT
                                of.write("\t{}\r\n".format(dmcck_key))
                                for item in plist["DaemonControllersConfigurationKey"][dmcck_key]:
                                    of.write("\t\t{}: {}\r\n".format(item, plist["DaemonControllersConfigurationKey"][dmcck_key][item]))
                        # PANInterfaces ARRAY
                        if "PANInterfaces" in plist:
                            of.write("PAN Interfaces:\r\n")
                            for pan_interface in plist["PANInterfaces"]:
                                of.write("\tPAN Interface: {}\r\n".format(pan_interface))
                        # ControllerPowerState
                        if "ControllerPowerState" in plist:
                            of.write("Controller Power State: {}\r\n".format(plist["ControllerPowerState"]))
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
                                    # ClassOfDevice
                                    if "ClassOfDevice" in device_data:
                                        of.write("\t\tClass Of Device: {}\r\n".format(plist["DeviceCache"][cached_device]["ClassOfDevice"]))
                                    # BatteryPercent
                                    if "BatteryPercent" in device_data:
                                        of.write("\t\tBattery Percent: {}\r\n".format(plist["DeviceCache"][cached_device]["BatteryPercent"]))
                                    # ClockOffset
                                    if "ClockOffset" in device_data:
                                        of.write("\t\tClock Offset: {}\r\n".format(plist["DeviceCache"][cached_device]["ClockOffset"]))
                                    # LastNameUpdate
                                    if "LastNameUpdate" in device_data:
                                        of.write("\t\tLast Name Update: {}\r\n".format(plist["DeviceCache"][cached_device]["LastNameUpdate"]))
                                    # LastServicesUpdate
                                    if "LastServicesUpdate" in device_data:
                                        of.write("\t\tLast Services Update: {}\r\n".format(plist["DeviceCache"][cached_device]["LastServicesUpdate"]))
                                    # LastInquiryUpdate
                                    if "LastInquiryUpdate" in device_data:
                                        of.write("\t\tLast Inquiry Update: {}\r\n".format(plist["DeviceCache"][cached_device]["LastInquiryUpdate"]))
                                    # LMPVersion
                                    if "LMPVersion" in device_data:
                                        of.write("\t\tLMP Version: {}\r\n".format(plist["DeviceCache"][cached_device]["LMPVersion"]))
                                    # LMPSubversion
                                    if "LMPSubversion" in device_data:
                                        of.write("\t\tLMP Subversion: {}\r\n".format(plist["DeviceCache"][cached_device]["LMPSubversion"]))
                                    # InquiryRSSI
                                    if "InquiryRSSI" in device_data:
                                        of.write("\t\tInquiry RSSI: {}\r\n".format(plist["DeviceCache"][cached_device]["InquiryRSSI"]))
                                    # PageScanMode
                                    if "PageScanMode" in device_data:
                                        of.write("\t\tPage Scan Mode: {}\r\n".format(plist["DeviceCache"][cached_device]["PageScanMode"]))
                                    # PageScanPeriod
                                    if "PageScanPeriod" in device_data:
                                        of.write("\t\tPage Scan Period: {}\r\n".format(plist["DeviceCache"][cached_device]["PageScanPeriod"]))
                                    # PageScanRepetitionMode
                                    if "PageScanRepetitionMode" in device_data:
                                        of.write("\t\tPage Scan Repetition Mode: {}\r\n".format(plist["DeviceCache"][cached_device]["PageScanRepetitionMode"]))
                                    # EIRData NOT PARSED
                                    # Services NOT PARSED
                        # PersistentPorts NOT PARSED
                                
                    except KeyError:
                        pass
                    of.write("\r\n")
                else:
                    logging.warning("File: {} does not exist or cannot be found.".format(file))
                    of.write("[WARNING] File: {} does not exist or cannot be found.\r\n".format(file))
                    print("[WARNING] File: {} does not exist or cannot be found.".format(file))    
            elif self._os_version == "lion":
                if os.path.isfile(file):
                    bplist = open(file, "rb")
                    plist = ccl_bplist.load(bplist)
                    bplist.close()
                    try:
                        # D2D MAC Address
                        # if "D2D MAC Address" in plist:
                        #     of.write("D2D MAC Address :{}\r\n".format(plist["D2D MAC Address"]))

                        # DaemonControllersConfigurationKey
                        if "DaemonControllersConfigurationKey" in plist:
                            of.write("Daemon Controllers Configuration Key:\r\n")
                            for dmcck_key in plist["DaemonControllersConfigurationKey"]:
                                # INNER DICT
                                of.write("\t{}\r\n".format(dmcck_key))
                                for item in plist["DaemonControllersConfigurationKey"][dmcck_key]:
                                    of.write("\t\t{}: {}\r\n".format(item, plist["DaemonControllersConfigurationKey"][dmcck_key][item]))
                        # PANInterfaces ARRAY
                        if "PANInterfaces" in plist:
                            of.write("PAN Interfaces:\r\n")
                            for pan_interface in plist["PANInterfaces"]:
                                of.write("\tPAN Interface: {}\r\n".format(pan_interface))
                        # ControllerPowerState
                        if "ControllerPowerState" in plist:
                            of.write("Controller Power State: {}\r\n".format(plist["ControllerPowerState"]))
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
                                    # ClassOfDevice
                                    if "ClassOfDevice" in device_data:
                                        of.write("\t\tClass Of Device: {}\r\n".format(plist["DeviceCache"][cached_device]["ClassOfDevice"]))
                                    # BatteryPercent
                                    if "BatteryPercent" in device_data:
                                        of.write("\t\tBattery Percent: {}\r\n".format(plist["DeviceCache"][cached_device]["BatteryPercent"]))
                                    # ClockOffset
                                    if "ClockOffset" in device_data:
                                        of.write("\t\tClock Offset: {}\r\n".format(plist["DeviceCache"][cached_device]["ClockOffset"]))
                                    # LastNameUpdate
                                    if "LastNameUpdate" in device_data:
                                        of.write("\t\tLast Name Update: {}\r\n".format(plist["DeviceCache"][cached_device]["LastNameUpdate"]))
                                    # LastServicesUpdate
                                    if "LastServicesUpdate" in device_data:
                                        of.write("\t\tLast Services Update: {}\r\n".format(plist["DeviceCache"][cached_device]["LastServicesUpdate"]))
                                    # LastInquiryUpdate
                                    if "LastInquiryUpdate" in device_data:
                                        of.write("\t\tLast Inquiry Update: {}\r\n".format(plist["DeviceCache"][cached_device]["LastInquiryUpdate"]))
                                    # LMPVersion
                                    if "LMPVersion" in device_data:
                                        of.write("\t\tLMP Version: {}\r\n".format(plist["DeviceCache"][cached_device]["LMPVersion"]))
                                    # LMPSubversion
                                    if "LMPSubversion" in device_data:
                                        of.write("\t\tLMP Subversion: {}\r\n".format(plist["DeviceCache"][cached_device]["LMPSubversion"]))
                                    # InquiryRSSI
                                    if "InquiryRSSI" in device_data:
                                        of.write("\t\tInquiry RSSI: {}\r\n".format(plist["DeviceCache"][cached_device]["InquiryRSSI"]))
                                    # PageScanMode
                                    if "PageScanMode" in device_data:
                                        of.write("\t\tPage Scan Mode: {}\r\n".format(plist["DeviceCache"][cached_device]["PageScanMode"]))
                                    # PageScanPeriod
                                    if "PageScanPeriod" in device_data:
                                        of.write("\t\tPage Scan Period: {}\r\n".format(plist["DeviceCache"][cached_device]["PageScanPeriod"]))
                                    # PageScanRepetitionMode
                                    if "PageScanRepetitionMode" in device_data:
                                        of.write("\t\tPage Scan Repetition Mode: {}\r\n".format(plist["DeviceCache"][cached_device]["PageScanRepetitionMode"]))
                                    # EIRData NOT PARSED
                                    # Services NOT PARSED
                        # PersistentPorts NOT PARSED
                        # PairedDevices ARRAY
                        if "PairedDevices" in plist:
                            if len(plist["PairedDevices"]) == 0:
                                of.write("Paired Devices:\r\n\tNo paired devices listed.\r\n")
                            else:
                                of.write("Paired Devices:\r\n")
                                for paired_device in plist["PairedDevices"]:
                                    of.write("\tDevice: {}\r\n".format(paired_device))
                    except KeyError:
                        pass
                    of.write("\r\n")
                else:
                    logging.warning("File: {} does not exist or cannot be found.".format(file))
                    of.write("[WARNING] File: {} does not exist or cannot be found.\r\n".format(file))
                    print("[WARNING] File: {} does not exist or cannot be found.".format(file))
            elif self._os_version == "snow_leopard":
                if os.path.isfile(file):
                    bplist = open(file, "rb")
                    plist = ccl_bplist.load(bplist)
                    bplist.close()
                    try:
                        # BluetoothAutoSeekHIDDevices
                        if "BluetoothAutoSeekHIDDevices" in plist:
                            of.write("Bluetooth Auto Seek HID Devices: {}\r\n".format(plist["BluetoothAutoSeekHIDDevices"]))
                        # ControllerPowerState
                        if "ControllerPowerState" in plist:
                            of.write("Controller Power State         : {}\r\n".format(plist["ControllerPowerState"]))
                        # BluetoothVersionNumber
                        if "BluetoothVersionNumber" in plist:
                            of.write("Bluetooth Version Number       : {}\r\n".format(plist["BluetoothVersionNumber"]))
                        # DaemonControllersConfigurationKey
                        if "DaemonControllersConfigurationKey" in plist:
                            of.write("Daemon Controllers Configuration Key:\r\n")
                            for dmcck_key in plist["DaemonControllersConfigurationKey"]:
                                # INNER DICT
                                of.write("\t{}\r\n".format(dmcck_key))
                                for item in plist["DaemonControllersConfigurationKey"][dmcck_key]:
                                    of.write("\t\t{}: {}\r\n".format(item, plist["DaemonControllersConfigurationKey"][dmcck_key][item]))
                        # HIDDevices
                        if "HIDDevices" in plist:
                            hid_array = plist["PairedDevices"]
                            of.write("HID Devices: {}\r\n")
                            for hid_device in hid_array:
                                of.write("\t{}\r\n".format(hid_device))
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
                                    # ClassOfDevice
                                    if "ClassOfDevice" in device_data:
                                        of.write("\t\tClass Of Device: {}\r\n".format(plist["DeviceCache"][cached_device]["ClassOfDevice"]))
                                    # BatteryPercent
                                    if "BatteryPercent" in device_data:
                                        of.write("\t\tBattery Percent: {}\r\n".format(plist["DeviceCache"][cached_device]["BatteryPercent"]))
                                    # ClockOffset
                                    if "ClockOffset" in device_data:
                                        of.write("\t\tClock Offset: {}\r\n".format(plist["DeviceCache"][cached_device]["ClockOffset"]))
                                    # LastNameUpdate
                                    if "LastNameUpdate" in device_data:
                                        of.write("\t\tLast Name Update: {}\r\n".format(plist["DeviceCache"][cached_device]["LastNameUpdate"]))
                                    # LastServicesUpdate
                                    if "LastServicesUpdate" in device_data:
                                        of.write("\t\tLast Services Update: {}\r\n".format(plist["DeviceCache"][cached_device]["LastServicesUpdate"]))
                                    # LastInquiryUpdate
                                    if "LastInquiryUpdate" in device_data:
                                        of.write("\t\tLast Inquiry Update: {}\r\n".format(plist["DeviceCache"][cached_device]["LastInquiryUpdate"]))
                                    # LMPVersion
                                    if "LMPVersion" in device_data:
                                        of.write("\t\tLMP Version: {}\r\n".format(plist["DeviceCache"][cached_device]["LMPVersion"]))
                                    # LMPSubversion
                                    if "LMPSubversion" in device_data:
                                        of.write("\t\tLMP Subversion: {}\r\n".format(plist["DeviceCache"][cached_device]["LMPSubversion"]))
                                    # InquiryRSSI
                                    if "InquiryRSSI" in device_data:
                                        of.write("\t\tInquiry RSSI: {}\r\n".format(plist["DeviceCache"][cached_device]["InquiryRSSI"]))
                                    # PageScanMode
                                    if "PageScanMode" in device_data:
                                        of.write("\t\tPage Scan Mode: {}\r\n".format(plist["DeviceCache"][cached_device]["PageScanMode"]))
                                    # PageScanPeriod
                                    if "PageScanPeriod" in device_data:
                                        of.write("\t\tPage Scan Period: {}\r\n".format(plist["DeviceCache"][cached_device]["PageScanPeriod"]))
                                    # PageScanRepetitionMode
                                    if "PageScanRepetitionMode" in device_data:
                                        of.write("\t\tPage Scan Repetition Mode: {}\r\n".format(plist["DeviceCache"][cached_device]["PageScanRepetitionMode"]))
                        # PairedDevices
                        if "PairedDevices" in plist:
                            paired_array = plist["PairedDevices"]
                            of.write("Paired Devices:\r\n")
                            for paired_device in paired_array:
                                of.write("\t{}\r\n".format(paired_device))
                    except KeyError:
                        pass
                    of.write("\r\n")
            else:
                logging.warning("Not a known OSX version.")
                print("[WARNING] Not a known OSX version.")
            of.write("="*40 + "\r\n\r\n")
        of.close()