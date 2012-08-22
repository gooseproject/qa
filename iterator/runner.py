#!/usr/bin/env python

import os  
import subprocess
import rpm
import yaml

TESTDIR='tests/'
RPMDIR='rpms'

def readRpmHeader(ts, filename):
    """ Read an rpm header. """
    fd = os.open(filename, os.O_RDONLY)
    h = None
    try:
        h = ts.hdrFromFdno(fd)
    except rpm.error, e:
        if str(e) == "public key not available":
            print str(e)
        if str(e) == "public key not trusted":
            print str(e)
        if str(e) == "error reading package header":
            print str(e)
        h = None
    finally:
        os.close(fd)
    return h


def is_exe(fpath):
    return(os.path.isfile(fpath) and os.access(fpath, os.X_OK))

def main():
    results={}
    # init chroot
    for myrpm in os.listdir(RPMDIR):
        results[myrpm] = {}
        rpmpath = os.path.join(RPMDIR, myrpm)
  
        # install rpm into the mock chroot (don't clean, will take too long)

        # get rpm name (not package name)
        ts = rpm.TransactionSet()
        h = readRpmHeader( ts, rpmpath )
        rpmname = h['name']
       
        # iterate over the tests
        for testfile in os.listdir(TESTDIR):
            testpath = os.path.join(TESTDIR, testfile)
            if is_exe(testpath):
                results[myrpm][testfile] = ['']
                # copyin the test file
                # run the testfile in chroot
                cmd = subprocess.Popen([testpath, rpmname],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
                (results[myrpm][testfile][0],err) = cmd.communicate()
  
    #destroy chroot
    return(results)

if __name__ == '__main__':
    print(yaml.dump(main()))
