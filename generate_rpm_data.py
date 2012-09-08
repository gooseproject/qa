#!/usr/bin/python

#URLS look like this for an individual rpm
#http://koji.gooselinux.org/mnt/koji/packages/goose-logos/60.0.15/3.gl6/data/signed/1cdbbb39/noarch/goose-logos-60.0.15-3.gl6.noarch.rpm
#we should be able to grab the rpm from this url reliably below

import os, sys
import koji
import urllib2
from urllib2 import HTTPError, URLError

tag = "gl6-beta"
host = 'http://koji.gooselinux.org'
base_uri = 'mnt/koji/packages'
signed_path = 'data/signed'
gpg_key_id = '1cdbbb39' 
download_path = '/tmp'

kojiclient = koji.ClientSession('http://koji.gooselinux.org/kojihub', {})
pkgs = kojiclient.listPackages(tagID=11,inherited=True)

template_dir = '6.x'
release = '6.0'

docs_basedir = '/home/clints/Projects/gooseproject/qa'
docs_index = 'index.rst'

#temporary hack to only include one package for testing
pkgs = pkgs[0:4]

dest_dir = '{0}/GoOSe/{1}'.format(docs_basedir, release)

if not os.path.exists(dest_dir):
    os.makedirs(dest_dir, 0755)

index_src = open('{0}/{1}/{2}'.format(docs_basedir, template_dir, docs_index), 'r')
index_dst = open('{0}/{1}'.format(dest_dir, docs_index), 'w')
index_dst.write(index_src.read() % {'release': release})


for p in pkgs:
    print p
    # get build package is in
    for build in kojiclient.listBuilds(packageID=p['package_id']):
        if 'gl6' in build['release']:
            children = kojiclient.getTaskChildren(build['task_id'])
            for c in [child['id'] for child in children if child['method'] == 'buildArch']:
                info = kojiclient.listTaskOutput(c)
                print 'downloading {0}'.format(info[0])
                x = kojiclient.downloadTaskOutput(c, info[0])
                # ^^ gives you the entire RPM in a string, scary!

                file_path = '{0}/{1}'.format(download_path, info[0])
                local_file = open(file_path, 'wb', 0644)
                #Write to our local file
                local_file.write(x)
                local_file.close()




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
