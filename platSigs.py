#!/usr/bin/env python
#
# Copyright (C) 2018 Joe Maples <joe@maples.dev>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import base64
import sys
import os
import zipfile

tmpDir = "/tmp/platCerts/"

def getSig(certFileName):
    certFile = open(certFileName, "r")
    cert = certFile.read()
    sig = base64.b16encode(cert)
    return sig

def findRSAFiles(workingDir):
    fileList = list()
    for path, subdirs, files in os.walk(workingDir):
        for name in files:
            if name.endswith(".RSA"):
                file = os.path.join(path, name)
                fileList.append(file)
    return fileList

def getSignatures(certFiles):
    signatures = list()
    for file in range(len(certFiles)):
        signatures.append(getSig(certFiles[file - 1]))
    return signatures

def findJavaBinaries(vendorRootPath):
    pathList = list()
    fileList = list()
    for path, subdirs, files in os.walk(vendorRootPath):
        for name in files:
            if name.endswith(".apk") or name.endswith(".jar"):
                pathList.append(os.path.abspath(path))
                fileList.append(name)
    return (pathList, fileList)

def processJavaBinaries(javaBinaries):
    if not os.path.isdir(tmpDir):
        os.mkdir(tmpDir)
    for file in range(len(javaBinaries)):
        name, ext = os.path.splitext(javaBinaries[1][file - 1])
        if not os.path.isdir(tmpDir + name):
            os.mkdir(tmpDir + name)
            zip_ref = zipfile.ZipFile((javaBinaries[0][file - 1] + "/" + javaBinaries[1][file - 1]), 'r')
            zip_ref.extractall(tmpDir + name)
            zip_ref.close()

def removeDuplicates(signatures):
  return list(dict.fromkeys(signatures))

def printSignatures(signatures):
    for sig in range(len(signatures)):
        print "Signature " + str(sig + 1) + ": " + signatures[sig - 1] + "\n"

if len(sys.argv) != 2:
	sys.exit("usage: " + sys.argv[0] + " /path/to/vendor/root")

apksAndJars = findJavaBinaries(sys.argv[1])
processJavaBinaries(apksAndJars)
certs = findRSAFiles(tmpDir)
sigs = removeDuplicates(getSignatures(certs))
print "Signatures Found:\n"
printSignatures(sigs)
