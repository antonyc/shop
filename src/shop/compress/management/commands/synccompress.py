import os
import stat
from django.core.management.base import NoArgsCommand
from optparse import make_option

from django.conf import settings

typical_permission = stat.S_IRGRP + stat.S_IRUSR + stat.S_IWUSR + stat.S_IXUSR + stat.S_IXGRP + stat.S_IROTH + stat.S_IXOTH

class Command(NoArgsCommand):
    option_list = NoArgsCommand.option_list + (
        make_option('--force', action='store_true', default=False, help='Force update of all files, even if the source files are older than the current compressed file.'),
    )
    help = 'Updates and compresses CSS and JavsScript on-demand, without restarting Django'
    args = ''

    def handle_noargs(self, **options):
        
        force = options.get('force', False)
        verbosity = int(options.get('verbosity', 1))

        from compress.utils import needs_update, filter_css, filter_js

        for name, css in settings.COMPRESS_CSS.items():
            u, version = needs_update(css['output_filename'], 
                css['source_filenames'])

            if (force or u) or verbosity >= 2:
                msg = 'CSS Group \'%s\'' % name
                print msg
                print len(msg) * '-'
                print "Version: %s" % version

            if force or u:
                filter_css(css, verbosity)
                os.chmod(os.path.join(settings.STATIC_ROOT,
                                      css['output_filename']),
                         typical_permission)

            if (force or u) or verbosity >= 2:
                print

        for name, js in settings.COMPRESS_JS.items():
            u, version = needs_update(js['output_filename'], 
                js['source_filenames'])

            if (force or u) or verbosity >= 2:
                msg = 'JavaScript Group \'%s\'' % name
                print msg
                print len(msg) * '-'
                print "Version: %s" % version

            if force or u:
                filter_js(js, verbosity)
                os.chmod(os.path.join(settings.STATIC_ROOT,
                                      js['output_filename']),
                         typical_permission)

            if (force or u) or verbosity >= 2:
                print

# Backwards compatibility for Django r9110
if not [opt for opt in Command.option_list if opt.dest=='verbosity']:
    Command.option_list += (
    make_option('--verbosity', '-v', action="store", dest="verbosity",
        default='1', type='choice', choices=['0', '1', '2'],
        help="Verbosity level; 0=minimal output, 1=normal output, 2=all output"),
    )
