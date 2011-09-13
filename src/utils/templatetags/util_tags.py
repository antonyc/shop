# -*- coding: utf-8 -*-
import os
from django import template
from utils import policy
register = template.Library()

@register.simple_tag
def class_block(block_name):
    """
    Create name of block
    """
    return policy.javascript_block(block_name)

@register.simple_tag
def load_block_file(block_name, filename):
    """
    create path to some block
    """
    return os.path.join('', policy.path_to_block(block_name), filename)
