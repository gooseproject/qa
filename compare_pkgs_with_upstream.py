# compare_pkgs_with_upstream.py
# - opens existing upstream rpm list
# - verify matching RPMs exist

import os, sys
import koji
import time
import urllib2
from urllib2 import HTTPError, URLError

def find_missing_pkgs(tag, host, base_uri, signed_path, gpg_key_id, file_to_read):

    print "looping through upstream rpm list"

    missing_pkgs = []
    
    koji_url = '{0}/kojihub'.format(host)
    kojiclient = koji.ClientSession(koji_url, {})

    fr = open(file_to_read, 'r')
    lines = fr.readlines()
    fr.close()

#    lines = lines[:30]

    for line in lines:
        l = line.replace('el6', 'gl6')
        l = l.replace('\n', '')

        # try to find packages matching l
        rpm = kojiclient.getRPM(l)
#        print "RPM: {0}".format(l)
#        print "Data: {0}".format(rpm)

        if rpm is None:
            #print "RPM missing: {0}".format(l)
            new_l = l.replace('gl6', 'gl6.goose.1')

            # try to find packages matching new_l
            rpm = kojiclient.getRPM(new_l)

            if rpm is None:
                #print "RPM missing: {0}".format(new_l)
                new_l = new_l.replace('gl6.goose.1', 'gl6.goose.2')
                # try to find packages matching new_l
                rpm = kojiclient.getRPM(new_l)

                # finally, if the package still doesn't exist, log it
                if rpm is None:
                    print ""
                    print "Missing RPM: {0}".format(l)
                    print "PLEASE VERIFY ALL MISSING RPMS BY HAND"
                    print ""
                    missing_pkgs.append(l)




def main():

    upstream_rpm_file = '/tmp/upstream.rpms'

    tag = "gl6-beta"
    host = 'http://koji.gooselinux.org'
    base_uri = 'mnt/koji/packages'
    signed_path = 'data/signed'
    gpg_key_id = '1cdbbb39' 

    find_missing_pkgs(tag, host, base_uri, signed_path, gpg_key_id, upstream_rpm_file)


if __name__ == "__main__":
    raise SystemExit(main())
