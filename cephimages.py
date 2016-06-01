#!/usr/bin/python

import subprocess
import json
import sys

if len(sys.argv) < 2:
    sys.exit("Missing argument")

if len(sys.argv) > 3:
    sys.exit("Too many arguments")
imagesSize = 0
poolSize = 0

if len(sys.argv) == 2 and sys.argv[1] == 'sum':
    poolList = subprocess.Popen("/usr/bin/rados lspools |grep -v ^'\.' | grep  -v ^rbd$", shell=True, stdout=subprocess.PIPE).communicate()[0]
    poolDiscovery = []
    imageDiscovery = []
    for pool in poolList.splitlines():
        imageList = subprocess.Popen('rbd ls "%s"'%pool, shell=True, stdout=subprocess.PIPE).communicate()[0]
        for image in imageList.splitlines():
            imageInfo = subprocess.Popen('rbd --format json info "%s/%s"'% (pool, image), shell=True,stdout=subprocess.PIPE).communicate()[0]
            jsonImageInfo = json.loads(imageInfo)
            imagesSize += jsonImageInfo['size']
    print  imagesSize
    sys.exit()

if len(sys.argv) == 3:
    pool = sys.argv[1]
    image = sys.argv[2]
    imageInfo = subprocess.Popen('rbd --format json info "%s/%s"'% (pool, image), shell=True, stdout=subprocess.PIPE).communicate()[0]
    jsonImageInfo = json.loads(imageInfo)
    print jsonImageInfo['size']
    sys.exit()


