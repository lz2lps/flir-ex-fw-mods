DISCLAIMER: 
YOU DO THIS AT YOUR OWN RISK. THERE IS RISK TO BRICK YOUR CAMERA.
ALWAYS MAKE BACKUP COPIES BEFORE CHANGING OR REPLACING ORIGINAL FILES.

**********************************************************************

All this was done by people from EEVblog Electronics Community Forum.

Be careful. Only if you know what to do, then you can patch the
E4 2.3.0 high resolution enhanced conf.cfc file to use the enhanced
menu files that are in the \FlashBFS folder.

If you changed conf.cfc previously, find that first file (conf.cfc
highres only for E4 or E5 patch).
  Copy this conf.cfc,
  conf.cfc.menu.e(your camera nr [4, 5]) and
  menu_conf_e(your camera nr [4, 5]).py
to the Python27 directory and run
  "python.exe menu_conf_e(your camera nr [4, 5]).py"

After that you have a new conf and a backup copy of the old conf.
Replace it in \FlashFS\system\appcore.d\config.d\
and store the backup copy for recovery.

To have new menu files add them to camera with
FLIRInstallNet - browse 2.3.0_Menu.fif file then run fif file.
Reboot if not done.


For E6 patch copy from camera or backup factory 
  conf.cfc and
  common_dll.dll
to the Python27 directory.
From update copy
  conf.cfc.menu.e6,
  menu_conf_e6.py and
  common_dll.dll.e6
to the same Python27 directory and run
  "python.exe menu_conf_e6.py"

After that you have a new conf and dll and a backup copy of the
old conf and dll. Replace conf in \FlashFS\system\appcore.d\config.d\
and dll in \FlashBFS\system\ and store the backup copyes for recovery.

To have new menu files add them to camera with
FLIRInstallNet - browse 2.3.0_Menu.fif file then run fif file.
Reboot if not done.


AND REMEMBER, THIS DOES NOT ADD ANY MONETARY VALUE TO THIS CAMERA.
YOU CAN'T SELL IT AND ASK FOR MONEY FOR WHAT OTHERS HAVE ACHIEVED
AND DONE. THIS IS A FREE ENHANCEMENT PACK FOR PERSONAL USE ONLY.
AFTER ENHANCEMENT IT CAN'T BE SOLD OR USED FOR PROFESSIONAL WORK
FOR PROFIT. AND ALL OTHER CASES THIS ENHANCEMENT MUST NOT ADD
EXTRA FINANCIAL VALUE FOR THE HELP THAT YOU PROVIDE WITH THIS TOOL.

BEWARE THAT THE MANUFACTURER MAY TAKE LEGAL ACTIONS AGAINST YOU

WE WILL KEEP AN EYE ON YOU.