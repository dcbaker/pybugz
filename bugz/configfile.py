import configparser
import glob
import os
import sys

from bugz.log import log_error


def load_config(UserConfig=None):
    parser = configparser.ConfigParser(default_section='default')
    DefaultConfigs = sorted(glob.glob(sys.prefix + '/share/pybugz.d/*.conf'))
    SystemConfigs = sorted(glob.glob('/etc/pybugz.d/*.conf'))
    if UserConfig is not None:
        UserConfig = os.path.expanduser(UserConfig)
    else:
        # Try to load the user config. Start with the
        # $XDG_CONFIG_HOME/bugz/bugzrc, then move to the fallback
        # XDG_CONFIG_HOME path of ~/.config/bugz/bugzrc, and finally ~/.bugzrc.
        # If none of those are found, set the config to an empty list.
        for each in [os.path.expandvars('$XDG_CONFIG_HOME/bugz/bugzrc'),
                     os.path.expanduser('~/.config/bugz/bugzrc'),
                     os.path.expanduser('~/.bugzrc')]:
            if os.path.exists(each):
                UserConfig = [each]
                break
        else:
            UserConfig = []

    try:
        parser.read(DefaultConfigs + SystemConfigs + UserConfig)

    except configparser.DuplicateOptionError as error:
        log_error(error)
        sys.exit(1)
    except configparser.DuplicateSectionError as error:
        log_error(error)
        sys.exit(1)
    except configparser.MissingSectionHeaderError as error:
        log_error(error)
        sys.exit(1)
    except configparser.ParsingError as error:
        log_error(error)
        sys.exit(1)

    return parser


def get_config_option(get, section, option):
    try:
        value = get(section, option)

    except configparser.InterpolationSyntaxError as error:
        log_error('Syntax Error in configuration file: {0}'.format(error))
        sys.exit(1)

    except ValueError as error:
        log_error('{0} is not in the right format: {1}'.format(option,
                  str(error)))
        sys.exit(1)

    if value == '':
        log_error('{0} is not set'.format(option))
        sys.exit(1)

    return value
