#!/usr/bin/env bash
rm *.db
rm *.dat

python2 super_xml_parser.py ./databaseFiles0/items-*.xml

cat user.dat | sort -u -t'|' -k1,1 > user2.dat
