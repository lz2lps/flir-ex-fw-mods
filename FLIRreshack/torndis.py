import usb.core
import time

import usb.util

#
# I didn't write this code, I didn't write this code...
#

dev = usb.core.find(idVendor=0x09CB, idProduct=0x1007)

if dev is None:
  raise ValueError('Device not found')

x = 0

while True:
  r = dev.ctrl_transfer(0xA1, 0x85, 0x0200, 0x0600, 2)
  print repr(''.join("%c" % x for x in r if x))
  r = dev.ctrl_transfer(0xA1, 0x81, 0x0200, 0x0600, 0x7C)
  print repr(''.join("%c" % x for x in r if x))
  time.sleep(.1)
  if x == 3:
    cmd = "737461727420636D640D0A000200000000000B00984F8A070C00000000000B00B44F8A070B000000E4270B00CC010B001800000003000000E0270B000000000034EF1D00A86F1477200000000000000074B340611000000000000000A0518A0700000000050000000000000002000000004A80070000000028000000".decode('hex')
    print dev.ctrl_transfer(0x21, 0x01, 0x0200, 0x0600, cmd)
  if x == 6:
    cmds = "usbfn RNDIS\r\n\0"
    cmd = cmds + cmd[len(cmds):]
    print dev.ctrl_transfer(0x21, 0x01, 0x0200, 0x0600, cmd)
  x += 1

print dev.ctrl_transfer(0xA1, 0x86, 0x0600, 0x0100, 1)
