# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy
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

@register.filter
def public_username(user):
    if user.is_staff or user.is_superuser:
        return ugettext_lazy("Customer support service")
    profile = user.get_profile()
    return "%s %s" % (profile.res_first_name, profile.res_last_name)