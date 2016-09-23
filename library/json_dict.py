#!/usr/bin/python
import traceback

def main():
    module = AnsibleModule(
        argument_spec={
            "dest": {"required": True, "type": "path", "aliases": ["path"]},
            "update": {"type": "dict", "default": {}},
            "delete": {"type": "list", "default": []},
        },
        add_file_common_args=True,
        supports_check_mode=True,
    )
    dest      = module.params["dest"]
    file_args = module.load_file_common_arguments(module.params)
    try:
        with open(dest) as fp:
            data = module.from_json(fp.read())
    except Exception:
        module.fail_json(msg=traceback.format_exc())
    if not isinstance(data, dict):
        module.fail_json(msg='File must contain a JSON object/dictionary')
    for k,v in module.params["update"].iteritems():
        if k not in data or data[k] != v:
            data[k] = v
            changed = True
    for k in module.params["delete"]:
        if k in data:
            del data[k]
            changed = True
    try:
        if changed and not module.check_mode:
            if module.params["backup"]:
                module.backup_local(dest)
            with open(dest, 'w') as fp:
                fp.write(module.jsonify(data))
        changed = module.set_fs_attributes_if_different(file_args, changed)
    except Exception:
        module.fail_json(msg=traceback.format_exc())
    module.exit_json(dest=dest, changed=changed)

from ansible.module_utils.basic import *
main()
