__author__ = 'chapson'
import os
import re

def list_of_files(root_dir, extension='js'):
    regexp = re.compile(r'.*\.%s$' % extension)
    result = []
    dirs = os.walk(root_dir)
    for dir in dirs:
        if not dir[1]:
            for file in dir[2]:
                full_path = os.path.join(dir[0], file)
                if full_path.endswith('jquery.gallerific.js'):
                    continue
                match = regexp.match(full_path)
                if match is not None:
                    result.append(full_path)
    result.reverse()
    return result
