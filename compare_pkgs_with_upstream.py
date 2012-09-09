# compare_pkgs_with_upstream.py
# - opens existing upstream rpm list
# - verify matching RPMs exist

import os, sys
import koji
import time
import urllib2
from urllib2 import HTTPError, URLError

def find_missing_pkgs(tag, host, base_uri, signed_path, gpg_key_id, file_to_read, missing_rpms_file):

    print "looping through upstream rpm list"

    f = open(missing_rpms_file, 'w+')
    f.close()

    koji_url = '{0}/kojihub'.format(host)
    kojiclient = koji.ClientSession(koji_url, {})

    fr = open(file_to_read, 'r')
    rpms = fr.readlines()
    fr.close()

#    lines = lines[:30]

    loop_size = 75

    loops = (len(rpms) / loop_size)
    last_loop = (len(rpms) % loop_size)

    for l in range(loops):

        missing_pkgs = []

        slice_start = loop_size * l
        if l < loops - 1:
            print "loop {0} of {1}".format(l, loops)
            slice_end = loop_size * l + loop_size - 1
        else:
            print "LAST LOOP: {0} of {1}".format(l, loops)
            slice_end = loop_size * l + last_loop

        kojiclient.logout()
        time.sleep(1)
        koji_url = '{0}/kojihub'.format(host)
        kojiclient = koji.ClientSession(koji_url, {})

        print "rpms[{0}:{1}]".format(slice_start + 1,slice_end + 1)

        for rpm in rpms[slice_start:slice_end]:

            r = rpm.replace('el6', 'gl6')
            r = r.replace('\n', '')

            # try to find packages matching r
            pkg = kojiclient.getRPM(r)
    #        print "RPM: {0}".format(r)
    #        print "Data: {0}".format(pkg)

            if pkg is None:
                #print "RPM missing: {0}".format(l)
                new_r = r.replace('gl6', 'gl6.goose.1')

                # try to find packages matching new_r
                pkg = kojiclient.getRPM(new_r)

                if pkg is None:
                    #print "RPM missing: {0}".format(new_r)
                    new_r = new_r.replace('gl6.goose.1', 'gl6.goose.2')
                    # try to find packages matching new_r
                    pkg = kojiclient.getRPM(new_r)

                    # finally, if the package still doesn't exist, log it
                    if pkg is None:
                        print ""
                        print "Missing RPM: {0}".format(r)
                        print "PLEASE VERIFY ALL MISSING RPMS BY HAND"
                        print ""
                        missing_pkgs.append(r)

        if missing_pkgs:
            with open(missing_rpms_file, 'a+') as f:
                for pkg in missing_pkgs:
                    f.write('{0}\n'.format(pkg))




def main():

    upstream_rpms_file = '/tmp/upstream.rpms'
    missing_rpms_file = '/tmp/missing.goose.rpms'

    tag = "gl6-beta"
    host = 'http://koji.gooselinux.org'
    base_uri = 'mnt/koji/packages'
    signed_path = 'data/signed'
    gpg_key_id = '1cdbbb39' 

    find_missing_pkgs(tag, host, base_uri, signed_path, gpg_key_id, upstream_rpms_file, missing_rpms_file)


if __name__ == "__main__":
    raise SystemExit(main())
