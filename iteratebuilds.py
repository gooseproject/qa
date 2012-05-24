#!/usr/bin/python
from __future__ import print_function
import koji
from operator import itemgetter
kojiclient = koji.ClientSession('http://koji.gooselinux.org/kojihub', {})

tag = "gl6-beta"

pkgs = kojiclient.listPackages(tagID=11,inherited=True)

# PSEUDOCODE STARTS HERE
#for i in pkgs:
    # get build package is in
    #kojiclient.listBuilds(packageID=foo['package_id'])
    # need to do some magic to determine if right build (using release?)
    #build = kojiclient.listBuilds(packageID=foo['package_id'])[0]
    # get rpms from build
    #buildrpms = kojiclient.listRPMs(buildID=build['build_id'])
    #for i in buildrpms:
        # get rpm 
        #rpm = kojiclient.getRPM(400)
        # magic handwavy turn info from rpm into download link
        # download rpm 
        # rpm2cpio rpm
        # cpio extract rpm into tmpdir
        # find binary files from tmpdir
        #pythonic way of (find tmpdir | xargs file | grep linked | cut -d ':' -f 1 | xargs ldd) # for linked files
        # TODO need a way to get info for non-linked files
        
# store abi data in repo for pkg
# do we want a github fork and pull request from this tool?
#git clone 
#git co -b ... # do we want a seperate branch
#append to abi-info.yaml
#git add abi-info.yaml
#git ci -m "abi info added"
#git push
# do we want pull request?

""" EXAMPLE abi-info.yaml
bc-1.06.95-1.gl6:
  bc-1.06.95-1.gl6.i686.rpm:
    /usr/bin/bc: [linux-gate.so.1 =>  (0xf77a0000), libreadline.so.6 => /lib/libreadline.so.6
        (0xf7760000), libncurses.so.5 => /lib/libncurses.so.5 (0xf773b000), libc.so.6
        => /lib/libc.so.6 (0xf758d000), libtinfo.so.5 => /lib/libtinfo.so.5 (0xf756d000),
      libdl.so.2 => /lib/libdl.so.2 (0xf7567000), /lib/ld-linux.so.2 (0xf77a1000)]
    /usr/bin/dc: [linux-gate.so.1 =>  (0xf76f4000), libc.so.6 => /lib/libc.so.6 (0xf7541000),
      /lib/ld-linux.so.2 (0xf76f5000)]
"""