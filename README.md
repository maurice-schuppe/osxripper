# OSXRipper
OSXRipper is a tool to gather system and user information from OSX file systems

__Prereqs__<br />
Assumes at least Python 3.4.3 is installed

####Uses the CCL Forensics BPlist parser
https://code.google.com/p/ccl-bplist/

####Usage

python3 osxripper.py --help

__Options__<br />
-h, --help                       Show help message and exit<br />
-i DIRECTORY, --input=DIRECTORY  input directory<br />
-o DIRECTORY, --output=DIRECTORY output directory<br />
-s, --summary                    Run Summary plugin only<br />

__Notes__<br />
N.B. if run on Linux and OSX systems user may have to escalate privileges to root<br />
N.B. the output directory must exist

__On OSX:__<br />
sudo python3 osxripper.py -i /Volumes/my_mounted_volume -o /Users/username/Desktop/my_analysis<br />

__On Linux:__<br />
sudo python3 osxripper.py -i /mnt/hfs_mount -o /home/username/my_analysis<br />
N.B. if kpartx used to mount the image the input path may be /media/...<br />

__On Windows:__<br />
python.exe osxripper.py -i X:\extracted_files_root -o C:\Users\username\Desktop\my_analysis<br />
