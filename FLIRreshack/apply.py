import hashlib, sys, os, time, telnetlib, argparse

files = [
	("common_dll.dll", [("75b37c3c755409cc355d2875eadfa128f8e6e27a1b2adf92273656a20ceb5037", "30e8fe5891fc3268bd834451ff054f184db1b4cbf49fb941b15efd3199a60cad", "common_dll.dll.delta")], "/FlashBFS/system/"),
	("conf.cfc", [(6608, None, "conf.cfc.delta.e4"), (6336, None, "conf.cfc.delta.e5")], "/FlashFS/system/appcore.d/config.d/"),
]

# step 0: output stupid disclaimer

print """

E4HACK-2 v0.4

            **** DISCLAIMER ****

- You do this on your own risk.
- By using this tool, you agree that you will
  remove the hack before selling the device.
- TO REPEAT: UNDER NO CIRCUMSTANCES you are allowed
  to sell a device that has this hack installed.
- Please also uninstall the hack before attempting
  to do any firmware upgrade.
- This was only tested with a factory 2.3.0 E4.


IF ANY OF THIS FAILS AND YOU NEED TO RESTORE THE ORIGINAL
CONTENTS MANUALLY: (which you shouldn't need to, but just
in case...)

A backup directory of relevant files is created for each "apply".
Simply upload the files manually using FTP. You may have to run
"stopapp" before you can overwrite common_dll.dll.

Make sure you keep a good backup of your .CFC files. They are 
strong-signed so if you lose all your backups and the on-device 
files, _THEY ARE GONE_.

(This script backs them up when you "apply", though.)
"""

# step 1: download, verify and backup files

from ftplib import FTP

if len(sys.argv) != 3:
	print "usage: %s {apply,revert} <IP-of-cam>" % sys.argv[0]
	sys.exit()

command = sys.argv[1]
ip_address = sys.argv[2]

assert command in ["apply", "revert"]

print " = CONNECT TO FTP"
ftp = FTP(ip_address)
ftp.login()

files_found = []

if command == "apply":
	backupdir = time.strftime("backup-%Y%m%d%H%M%S")
	print " = CREATING BACKUP DIR %s" % backupdir
	os.mkdir(backupdir)

	for name, digests, ftppath in files:
		print " = RETR %s%s" % (ftppath, name)
		ftp.cwd(ftppath)
		assert not os.path.exists(name), "%s already exists, please run from clean directory" % name
		with open(name, "wb") as tmpfile:
			ftp.retrbinary("RETR " + name, tmpfile.write)

		with open(name, "rb") as tmpfile:
			contents = tmpfile.read()

		found = False
		found_new = False
		for digest, digest_new, delta in digests:
			if type(digest) is str:
				h = hashlib.sha256(contents).hexdigest()
			else:
				h = len(contents)
		
			if h == digest_new:
				found_new = True
			if h == digest:
				found = True
				files_found.append((name, digest, digest_new, delta, ftppath))

		assert not found_new, "ALREADY PATCHED; to restore, use backed-up files."
		assert found, "UNKNOWN %s: digest/len is %s" % (name, h)

		with open(os.path.join(backupdir, name), "wb") as backup:
			backup.write(contents)

	# step 2: produce patched files

	for name, digests, digest_new, delta,ftpfile in files_found:
		with open(name, "rb+") as f:
			deltas = eval(open(delta).read())

			for offset, delta in deltas:
				print "Applying %d bytes of delta at %08x" % (len(delta), offset)
				f.seek(offset)
				d = f.read(len(delta))
				assert len(d) == len(delta)
				delta = ''.join(chr(ord(a)^ord(b)) for a, b in zip(d, delta))
				f.seek(offset)
				f.write(delta)
elif command == "revert":
	for name, digests, ftppath in files:
		with open(name, "rb") as tmpfile:
			contents = tmpfile.read()

		found = False
		for digest, digest_new, delta in digests:
			if type(digest) is str:
				h = hashlib.sha256(contents).hexdigest()
			else:
				h = len(contents)
			if h == digest:
				found = True
				files_found.append((name, digest, digest_new, delta, ftppath))
		assert found, "LOCAL FILE ALREADY PATCHED; please run from backup directory."

# step 3: stop app

print " * stopping application..."

tn = telnetlib.Telnet(ip_address)
tn.expect(["FLIR Command Line Interpreter"])
assert tn.expect(['>'])[0] == 0
tn.write("stopapp\n")
assert tn.expect(['>'])[0] == 0
tn.write("exit\n")
tn.read_all()

# step 4: upload patched file (well, instruct the user to do so.)

for name, digest, digest_new, delta, ftppath in files_found:
	ftp.cwd(ftppath)

	print " *  uploading %s to %s" % (name, ftppath)

	for retry in range(10):
		if retry:
			print " * attempt %d" % (retry+1)
			time.sleep(3)
		try:
			ftp.delete(name)
			break
		except Exception, r:
			print " * failed (%s)." % repr(r)
	with open(name, "rb") as tmpfile:
		ftp.storbinary("STORE %s" % name, tmpfile)
		
	if command == "apply":
		os.remove(name)

print " * PLEASE HARD-REBOOT DEVICE."
