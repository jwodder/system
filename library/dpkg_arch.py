#!/usr/bin/python
# Like `command: dpkg --print-architecture`, except it works in check mode
import subprocess
import traceback
from ansible.module_utils.basic import AnsibleModule


def main() -> None:
    module = AnsibleModule(argument_spec={}, supports_check_mode=True)
    try:
        r = subprocess.run(
            ["dpkg", "--print-architecture"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
            encoding="utf-8",
        )
        arch = r.stdout.strip()
        module.exit_json(changed=False, arch=arch)
    except Exception:
        module.fail_json(msg=traceback.format_exc())


if __name__ == "__main__":
    main()
