#!/usr/bin/env python

import json
import os
import re
import sys

content=dict()

device_tree_dir = '/proc/device-tree'
model_file = device_tree_dir  + '/model'

hardware_version_re = re.compile('^Hardware[:\s]+(?P<version>[^ ]+)')
revision_version_re = re.compile('^Revision[:\s]+(?P<version>[^ ]+)')

stripped = lambda s: "".join(i for i in s if 31 < ord(i) < 127)

try:
    # CPU informations
    hdl = open('/proc/cpuinfo', 'r')
    for line in hdl.readlines():
        line = line.strip()
        # HARDWARE
        match = hardware_version_re.search(line)
        if match:
            content['hardware'] = match.group('version')
        # REVISION
        match = revision_version_re.search(line)
        if match:
            content['hardware_revision'] = match.group('version')
    # Device informations
    if os.path.isfile(model_file):
        hdl = open(model_file, 'r')
        content['model_string'] = stripped(hdl.read())
except subprocess.CalledProcessError as e:
    content['error'] = str(e)

if len(content) == 0:
    content = None

print(json.dumps(content))
sys.exit(0)
