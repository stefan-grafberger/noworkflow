# Copyright (c) 2013 Universidade Federal Fluminense (UFF), Polytechnic Institute of New York University.
# This file is part of noWorkflow. Please, consult the license terms in the LICENSE file.

import os.path
import hashlib

PROVENANCE_DIRNAME = '.noworkflow'
CONTENT_DIRNAME = 'db'

provenance_dir = ''
content_dir = ''
std_open = open  # This is changed by retrospective provenance collector at runtime

storage = {}  # Logical store

def connect(script_dir):
    global provenance_dir, content_dir
    provenance_dir = os.path.join(script_dir, PROVENANCE_DIRNAME)        
    content_dir = os.path.join(provenance_dir, CONTENT_DIRNAME)
     

def put(content):
    content_hash = hashlib.sha1(content).hexdigest()
    content_dirname = os.path.join(content_dir, content_hash[:2])
    if not os.path.isdir(content_dirname):
        os.makedirs(content_dirname)
    content_filename = os.path.join(content_dirname, content_hash[2:])
    if not os.path.isfile(content_filename):
        with std_open(content_filename, "wb") as content_file:
            content_file.write(content)
    return content_hash


def get(content_hash):
    content_filename = os.path.join(content_dir, content_hash[:2], content_hash[2:])
    with std_open(content_filename, 'rb') as content_file:
        return content_file.read()


def store(name, data):
    global storage
    storage[name] = data
    

def register_file_access(name, mode = 'r', buffering = 'default'):
    'registers an access to a file'
    with std_open(name, 'rb') as f:
        content_hash = put(f.read())
        # TODO: store the content hash together with access type in the current context and its call stack
        

    

        
    