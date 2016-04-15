#!/usr/bin/python
# Why is this not a module already?

def main():
    module = AnsibleModule(
        argument_spec={
            "command": {
                "type": "str",
                "required": True,
                "aliases": ["binary", "bin", "cmd", "program"],
            },
            "required": {"type": "bool", "default": False}
            "opt_dirs": {"type": "list", "default": []}
        },
        supports_check_mode=True,
    )
    path = module.get_bin_path(module.params["command"],
                               required=module.params["required"],
                               opt_dirs=module.params["opt_dirs"])
    module.exit_json(changed=False, path=path)

from ansible.module_utils.basic import *
main()
