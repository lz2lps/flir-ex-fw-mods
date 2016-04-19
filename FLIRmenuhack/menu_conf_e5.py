import sys, os, shutil
input1 = "conf.cfc.menu.e5"
input2 = "conf.cfc"
backup = "conf_reso_only.cfc"
f = open(input2,'rb+')
shutil.copy(input2, backup)
deltas = eval(open(input1).read())
for offset, delta in deltas:
	print "Applying %d bytes of delta at %08x" % (len(delta), offset)
	f.seek(offset)
	d = f.read(len(delta))
	assert len(d) == len(delta)
	delta = ''.join(chr(ord(a)^ord(b)) for a, b in zip(d, delta))
	f.seek(offset)
	f.write(delta)
print " * copy new conf to camera *"
