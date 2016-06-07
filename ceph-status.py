#!/usr/bin/python

import subprocess
import json
import sys

req = sys.argv[1]
ceph_bin = "/usr/bin/ceph"
rados_bin = "/usr/bin/rados"

# Initialising variables
# See: http://ceph.com/docs/master/rados/operations/pg-states/
creating=0
active=0
clean=0
down=0
replay=0
splitting=0
scrubbing=0
degraded=0
inconsistent=0
peering=0
repair=0
recovering=0
backfill=0
waitBackfill=0
incomplete=0
stale=0
remapped=0
pgstates = ['creating', 'active', 'clean', 'down', 'replay', 'splitting', 'scrubbing', 'degraded', 'inconsistent', 'peering', 'repair', 'recovering', 'backfill', 'waitBackfill', 'incomplete', 'stale', 'remapped']
iops = {'wbps' : 'write_bytes_sec', 'rbps': 'read_bytes_sec', 'ops': 'op_per_sec'}

def pgcount(pgtype):
    "Count the number of pgs that are in the given argument state"
    pgTypeCount = 0
    pginfo = json.loads(subprocess.Popen('"%s" pg stat --format json' %ceph_bin, shell=True, stdout=subprocess.PIPE).communicate()[0])['num_pg_by_state']
    for pgDict in pginfo:
        if pgtype in pgDict['name']:
            pgTypeCount += pgDict['num']
    return pgTypeCount

def iopsCount(iotype):
    "Number of operations per seconds (read, write, ops)"
    try:
        pgmap = json.loads(subprocess.Popen('"%s" status --format json' %ceph_bin, shell=True, stdout=subprocess.PIPE).communicate()[0])['pgmap']
        return pgmap[iotype]
    except:
        return 0

if req == "health":
    clusterStatus = json.loads(subprocess.Popen('"%s" health --format json' %ceph_bin, shell=True, stdout=subprocess.PIPE).communicate()[0])['overall_status']
    if clusterStatus == "HEALTH_OK":
        print "1"
    elif clusterStatus == "HEALTH_WARN":
        print "2"
    elif clusterStatus == "HEALTH_ERR":
        print "3"
    sys.exit()

if req == "rados_total":
    print json.loads(subprocess.Popen('"%s" df --format json' %rados_bin, shell=True, stdout=subprocess.PIPE).communicate()[0])['total_space']
    sys.exit()

if req == "rados_used":
    print json.loads(subprocess.Popen('"%s" df --format json' %rados_bin, shell=True,  stdout=subprocess.PIPE).communicate()[0])['total_used']
    sys.exit()

if req == "rados_free":
    print json.loads(subprocess.Popen('"%s" df --format json' %rados_bin, shell=True,  stdout=subprocess.PIPE).communicate()[0])['total_avail']
    sys.exit()

if req == "mon":
    print len(json.loads(subprocess.Popen('"%s" mon_status --format json' %ceph_bin,   shell=True, stdout=subprocess.PIPE).communicate()[0])['monmap']['mons'])
    sys.exit()

if req == "count":
    print len(json.loads(subprocess.Popen('"%s" osd dump --format json' %ceph_bin,     shell=True,  stdout=subprocess.PIPE).communicate()[0])['osds'])
    sys.exit()

if req in ['up', 'in']:
    upCount = 0
    inCount = 0
    osdCount = len(json.loads(subprocess.Popen('"%s" osd dump --format json' %ceph_bin, shell=True, stdout=subprocess.PIPE).communicate()[0])['osds'])
    osdData = json.loads(subprocess.Popen('"%s" osd dump --format json' %ceph_bin,        shell=True, stdout=subprocess.PIPE).communicate()[0])['osds']
    for osdDict in osdData:
        if osdDict['up'] == 1:
            upCount += 1
        if osdDict['in'] == 1:
            inCount += 1
    if req == "up":
        print (upCount*100/osdCount)
    if req == "in":
        print (inCount*100/osdCount)
    sys.exit()

if req == "degraded_percent":
    try:
        degradpc = json.loads(subprocess.Popen('"%s" pg stat --format json' %ceph_bin, shell=True, stdout=subprocess.PIPE).communicate()[0])['degraded_ratio']
        print (degradpc*100)
    except:
        print "0"
    sys.exit()

if req == "pgtotal":
    print json.loads(subprocess.Popen('"%s" pg stat --format json' %ceph_bin, shell=True, stdout=subprocess.PIPE).communicate()[0])['num_pgs']
    sys.exit()

if req in pgstates:
    print pgcount(req)
    sys.exit()

if req in iops.keys():
    print iopsCount(iops[req])
    sys.exit

