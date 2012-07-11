#!/usr/bin/python

#URLS look like this for an individual rpm
#http://koji.gooselinux.org/mnt/koji/packages/goose-logos/60.0.15/3.gl6/data/signed/1cdbbb39/noarch/goose-logos-60.0.15-3.gl6.noarch.rpm
#we should be able to grab the rpm from this url reliably below

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

#temporary hack to only include one package for testing
pkgs = pkgs[0:4]

for p in pkgs:
    print p
    # get build package is in
    for build in kojiclient.listBuilds(packageID=p['package_id']):
        if 'gl6' in build['release']:
            print 'downloading {0}'.format(p['package_name'])
            rpms = kojiclient.listRPMs(buildID=build['build_id'])
#            print 'RPMS: {0}'.format(rpms)
            for rpm in rpms:
                 print 'downloading {0}-{1}-{2}.{3}'.format(p['package_name'], rpm['version'], rpm['release'], rpm['arch'])
                if 'src' not in rpm['arch']:
#
                    full_rpm = '{0}-{1}-{2}.{3}.rpm'.format(rpm['name'], rpm['version'], rpm['release'], rpm['arch'])
                    full_url = '{0}/{1}/{2}/{3}/{4}/{5}/{6}/{7}/{8}'.format(host, base_uri, p['package_name'], rpm['version'], 
                                                                    rpm['release'], signed_path, gpg_key_id, rpm['arch'],
                                                                    full_rpm)
#
#                    print 'full rpm: {0}'.format(full_rpm)
#                    print 'full url: {0}'.format(full_url)

                    print 'downloading {0}-{1}-{2}.{3}'.format(p['package_name'], rpm['version'], rpm['release'], rpm['arch'])
                    try:
                        f = urllib2.urlopen(full_url)
                    
                        # Open our local file for writing
                        file_path = '{0}/{1}'.format(download_path, full_rpm)
                        local_file = open(file_path, 'wb', 0644)
                        #Write to our local file
                        local_file.write(f.read())
                        local_file.close()
                    
                    #handle errors
                    except HTTPError, e:
                        print "HTTP Error:",e.code , full_url
                    except URLError, e:
                        print "URL Error:",e.reason , full_url


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
