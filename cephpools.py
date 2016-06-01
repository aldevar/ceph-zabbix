#!/usr/bin/python

import subprocess
import json
import sys

if len(sys.argv) < 2:
    sys.exit("Missing argument")

if len(sys.argv) > 2:
    sys.exit("Too many arguments")

arg = sys.argv[1]

if arg == "pooldiscovery":
    poolList = subprocess.Popen("/usr/bin/rados lspools |grep -v ^'\.' | grep  -v ^rbd$", shell=True, stdout=subprocess.PIPE).communicate()[0]
    poolDiscovery = []
    imageDiscovery = []
    for pool in poolList.splitlines():
        imageList = subprocess.Popen('rbd ls "%s"'%pool, shell=True, stdout=subprocess.PIPE).communicate()[0]
        for image in imageList.splitlines():
            imageInfo = subprocess.Popen('rbd --format json info "%s/%s"'% (pool, image), shell=True, stdout=subprocess.   PIPE).communicate()[0]
            jsonImageInfo = json.loads(imageInfo)
            imageDiscovery.append({'{#POOL}':pool, '{#IMAGE}':image,'{#IMGSIZE}':jsonImageInfo["size"] })
        #    imageList = subprocess.Popen('rbd ls "%s"'%pool, shell=True, stdout=subprocess.PIPE).communicate()[0]
        #    for image in imageList.splitlines():
        #        print (image + " est dans " + pool)
    print json.dumps({"data": imageDiscovery})
    sys.exit()
else:
    sys.exit("Unknown argument " + arg)


