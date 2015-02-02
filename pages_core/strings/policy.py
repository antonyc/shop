# -*- coding: utf-8 -*-
import os
BLOCK_PREFIX = 'block'
BLOCK_FOLDER = BLOCK_PREFIX

def javascript_block(block_name):
    return 'block-'+block_name

def path_to_block(block_name):
    return os.path.join(BLOCK_FOLDER, block_name) 