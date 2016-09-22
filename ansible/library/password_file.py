#!/usr/bin/python
from   __future__ import print_function
from   errno      import ENOENT
import random
import string
import traceback

def main():
    module = AnsibleModule(
        argument_spec={
            "dest": {"required": True, "type": "path", "aliases": ["path"]},
            "length": {"type": "int", "default": 32},
            "force": {"type": "bool", "default": False},
        },
        add_file_common_args=True,
        supports_check_mode=True,
    )
    dest      = module.params["dest"]
    length    = module.params["length"]
    force     = module.params["force"]
    file_args = module.load_file_common_arguments(module.params)
    try:
        with open(dest) as fp:
            pwd = fp.read.strip()
    except Exception as e:
        if e.errno == ENOENT:
            pwd = None
        else:
            module.fail_json(msg=traceback.format_exc())
    try:
        if pwd is None or pwd == '' or (force and len(pwd) != length):
            pwd = ''.join(random.choice(string.ascii_letters + string.digits)
                          for _ in xrange(length))
            if not module.check_mode:
                #if module.params["backup"]:
                #    module.backup_local(dest)
                with open(dest, 'w') as fp:
                    print(pwd, file=fp)
            changed = True
        else:
            changed = False
        changed = module.set_fs_attributes_if_different(file_args, changed)
    except Exception as e:
        module.fail_json(msg=traceback.format_exc())
    module.exit_json(dest=dest, changed=changed, password=pwd)

from ansible.module_utils.basic import *
main()
