import re
from iob_variables import iob_tag

def command(text, cmd):
    if re.match(r"^/{}({})*$".format(cmd, iob_tag), text):
        return True
    else:
        return False

def command_with_args(text, cmd):
    if re.match(r"^/{0}({1})*$|^/{0}({1})*\s+.*".format(cmd, iob_tag), text):
        return True
    else:
        return False
