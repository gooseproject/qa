import os, sys
import koji
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

def generate_sorted_rpmlist(file_list):
    '''
    provide a tuple of files to process and return 
    the list of files into a tuple of rpms
    '''

    rpm_list = set()
    for fil in file_list:
        print fil
        f = open(fil, 'r')
        for line in f.readlines():
            l = line.rstrip('\n')
            if l not in rpm_list:
                rpm_list.add(l)

    return sorted(rpm_list)


def generate_upstream_rpms():

    '''
    generate a full list of canonical rpms for all 
    arches (currenty i386 and x86_64)
    '''

    rpms = generate_sorted_rpmlist(FILES)

    print rpms

def generate_goose_rpms(tag, host, base_uri, signed_path, gpg_key_id):

    download_path = '/tmp'
    
    koji_url = '{0}/kojihub'.format(host)
    print 'koji_url {0}'.format(koji_url)
    kojiclient = koji.ClientSession(koji_url, {})
    pkgs = kojiclient.listPackages(tagID=11,inherited=True)
    
    #temporary hack to only include one package for testing
    #pkgs = pkgs[0:4]
    
    rpm_list = set()
    for p in pkgs:
        print p
        # get build package is in
        for build in kojiclient.listBuilds(packageID=p['package_id']):
            print "build['task_id']: {0}".format(build['task_id'])
            if 'gl6' in build['release'] and build['task_id'] is not None:
                children = kojiclient.getTaskChildren(build['task_id'])
                for c in [child['id'] for child in children if child['method'] == 'buildArch']:
                    info = kojiclient.listTaskOutput(c)
                    print "INFO: {0}".format(info)
                    for i in info:
                        if 'rpm' in i and i not in rpm_list:
                            rpm_list.add(i)

    print "rpm_list: {0}".format(rpm_list)

def main():
    generate_upstream_rpms()

    tag = "gl6-beta"
    host = 'http://koji.gooselinux.org'
    base_uri = 'mnt/koji/packages'
    signed_path = 'data/signed'
    gpg_key_id = '1cdbbb39' 

    generate_goose_rpms(tag, host, base_uri, signed_path, gpg_key_id)


if __name__ == "__main__":
    raise SystemExit(main())

