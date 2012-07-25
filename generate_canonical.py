ARCHES_FILES = {
    'i386': ('/usr/share/rhn/channel-data/6-gold-client-i386',
    '/usr/share/rhn/channel-data/6-gold-client-i386-Optional', 
    '/usr/share/rhn/channel-data/6-gold-client-i386-Supplementary',
    '/usr/share/rhn/channel-data/6-gold-server-i386',
    '/usr/share/rhn/channel-data/6-gold-server-i386-Optional',
    '/usr/share/rhn/channel-data/6-gold-server-i386-Supplementary',
    '/usr/share/rhn/channel-data/6-gold-workstation-i386',
    '/usr/share/rhn/channel-data/6-gold-workstation-i386-Optional',
    '/usr/share/rhn/channel-data/6-gold-workstation-i386-Supplementary'),
    
    'x86_64': ('/usr/share/rhn/channel-data/6-gold-client-x86_64',
    '/usr/share/rhn/channel-data/6-gold-client-x86_64-Optional',
    '/usr/share/rhn/channel-data/6-gold-client-x86_64-Supplementary',
    '/usr/share/rhn/channel-data/6-gold-server-x86_64',
    '/usr/share/rhn/channel-data/6-gold-server-x86_64-Optional',
    '/usr/share/rhn/channel-data/6-gold-server-x86_64-Supplementary',
    '/usr/share/rhn/channel-data/6-gold-workstation-x86_64',
    '/usr/share/rhn/channel-data/6-gold-workstation-x86_64-Optional',
    '/usr/share/rhn/channel-data/6-gold-workstation-x86_64-Supplementary')
}

def generate_rpmlist(file_list):
    '''
    provide a tuple of files to process and return 
    the list of files into a tuple of rpms
    '''

    rpm_list = []
    for fil in file_list:
        print fil
        f = open(fil, 'r')
        for line in f.readlines():
            rpm_list.append(line.rstrip('\n'))

    return rpm_list


def generate_canonical_rpms():

    '''
    generate a full list of canonical rpms for all 
    arches (currenty i386 and x86_64)
    '''

    arches_rpms = {}

    for arch in ARCHES_FILES.keys():
        print "ARCH: {0}".format(arch)
        arches_rpms[arch] = generate_rpmlist(ARCHES_FILES[arch])

    print arches_rpms


def main():
    generate_canonical_rpms()


if __name__ == "__main__":
    raise SystemExit(main())


