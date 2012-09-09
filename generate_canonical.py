# generate_canonical.py
# - pulls from spacewalk-remote-utils.noarch as a canonical
#   list from upstream, sorts and and writes each to a text file

import os, sys
import koji
import time
import urllib2
from urllib2 import HTTPError, URLError



FILES = (
    '/usr/share/rhn/channel-data/6-gold-client-i386',
    '/usr/share/rhn/channel-data/6-gold-client-i386-Optional', 
    '/usr/share/rhn/channel-data/6-gold-client-i386-Supplementary',
    '/usr/share/rhn/channel-data/6-gold-server-i386',
    '/usr/share/rhn/channel-data/6-gold-server-i386-Optional',
    '/usr/share/rhn/channel-data/6-gold-server-i386-Supplementary',
    '/usr/share/rhn/channel-data/6-gold-workstation-i386',
    '/usr/share/rhn/channel-data/6-gold-workstation-i386-Optional',
    '/usr/share/rhn/channel-data/6-gold-workstation-i386-Supplementary',
    '/usr/share/rhn/channel-data/6-gold-client-x86_64',
    '/usr/share/rhn/channel-data/6-gold-client-x86_64-Optional',
    '/usr/share/rhn/channel-data/6-gold-client-x86_64-Supplementary',
    '/usr/share/rhn/channel-data/6-gold-server-x86_64',
    '/usr/share/rhn/channel-data/6-gold-server-x86_64-Optional',
    '/usr/share/rhn/channel-data/6-gold-server-x86_64-Supplementary',
    '/usr/share/rhn/channel-data/6-gold-workstation-x86_64',
    '/usr/share/rhn/channel-data/6-gold-workstation-x86_64-Optional',
    '/usr/share/rhn/channel-data/6-gold-workstation-x86_64-Supplementary'
)

def generate_upstream_rpms(file_to_write):

    '''
    generate a full list of canonical rpms for all
    arches (currenty i386 and x86_64)
    '''

    print "Generating upstream rpm list"

    rpm_list = set()
    for fil in FILES:
        #print fil
        f = open(fil, 'r')
        for line in f.readlines():
            l = line.rstrip('\n')
            if l not in rpm_list:
                rpm_list.add(l)

    f = open(file_to_write, 'w+')
    for r in sorted(rpm_list):
        f.write('{0}\n'.format(r))
    f.close()

def _get_packages(pkgs, host, slice_size=100):

    slice_start=0

    loops = (len(pkgs) / 100)
    last_loop = (len(pkgs) % 100)
    rpm_list = set()

    for l in range(loops):
        slice_start = 100 * l + 1
        slice_end = 100 * l + 100

        for p in pkgs[slice_start:slice_end]:
            koji_url = '{0}/kojihub'.format(host)
            kojiclient = koji.ClientSession(koji_url, {})

            # get build package is in

            for build in kojiclient.listBuilds(packageID=p['package_id']):
                #print "build['task_id']: {0}".format(build['task_id'])
                if 'gl6' in build['release'] and build['task_id'] is not None:
                    children = kojiclient.getTaskChildren(build['task_id'])
                    for c in [child['id'] for child in children if child['method'] == 'buildArch']:
                        info = kojiclient.listTaskOutput(c)
                        #print "INFO: {0}".format(info) 
                        for i in info:
                            if 'rpm' in i and i not in rpm_list:
                                rpm_list.add(i)

    return rpm_list

def generate_goose_rpms(tag, host, base_uri, signed_path, gpg_key_id, file_to_write):

    print "Generating goose rpm list"
    
    koji_url = '{0}/kojihub'.format(host)
    #print 'koji_url {0}'.format(koji_url)
    kojiclient = koji.ClientSession(koji_url, {})
    pkgs = kojiclient.listPackages(tagID=11,inherited=True)

    #temporary hack to only include one package for testing
    #pkgs = pkgs[0:45]
    
    rpm_list = _get_packages(pkgs, host)


    f = open(file_to_write, 'w+')
    f_count = 0
    for r in sorted(rpm_list):
        f.write('{0}\n'.format(r))
    f.close()

def main():

    upstream_rpm_file = '/tmp/upstream.rpms'
    goose_rpm_file = '/tmp/goose.rpms'

    generate_upstream_rpms(upstream_rpm_file)

    tag = "gl6-beta"
    host = 'http://koji.gooselinux.org'
    base_uri = 'mnt/koji/packages'
    signed_path = 'data/signed'
    gpg_key_id = '1cdbbb39' 

    generate_goose_rpms(tag, host, base_uri, signed_path, gpg_key_id, goose_rpm_file)


if __name__ == "__main__":
    raise SystemExit(main())

