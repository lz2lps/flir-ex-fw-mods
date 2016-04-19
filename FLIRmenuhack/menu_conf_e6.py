import sys, os, shutil
files = [
         ("common_dll.dll", "common_dll.dll.e6", "common_dll_ori.dll"),
         ("conf.cfc", "conf.cfc.menu.e6", "conf_ori.cfc"),
]

for name, delta, backup in files:
   with open(name,'rb+') as f:
      shutil.copy(name, backup)
      deltas = eval(open(delta).read())
      for offset, delta in deltas:
	  print "Applying %d bytes of delta at %08x" % (len(delta), offset)
	  f.seek(offset)
	  d = f.read(len(delta))
	  assert len(d) == len(delta)
	  delta = ''.join(chr(ord(a)^ord(b)) for a, b in zip(d, delta))
	  f.seek(offset)
	  f.write(delta)


print " * copy new conf and common_dll to camera *"
