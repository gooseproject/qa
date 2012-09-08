Breakdown of scripts
--------------------

generate_canonical.py
=====================

pulls from spacewalk-remote-utils.noarch as a canonical 
list from upstream, sorts and and writes to a text file

compare_pkgs_with_upstream.py
=============================

 - loops through above file and attempts to match a built rpm 
   in the following order::

   - checks for same rpm with gl6 instead of el6
   - checks for same rpm with goose.X where X is 1,2,3
   - checks for release version +1 

 - if rpm doesn't exist, it will be written to missing.rpms file

generate_rpm_data.py
====================

 - generates a page for each existing RPM with the following::

   - name, summary and sha256sum of the rpm itself
   - the equivalent of rpm -qp --dump RPM - which generates a 
     list of each file and its useful values
   - for each binary in the rpm, perform an ldd dump


download and install rpm

name
summary
requires
files
 paths
 md5/sha
 type
 abi on binaries
  ldd
  symbols?


