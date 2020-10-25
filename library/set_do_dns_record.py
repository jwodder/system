#!/usr/bin/python3
# Set a DNS record in DigitalOcean to a given value, deleting any conflicting
# records of the same domain, name, & type
# cf. <https://github.com/ansible/ansible/pull/31765>
import traceback
import requests

### TODO: Use Ansible's utility functions in place of `requests`

def main():
    module = AnsibleModule(
        argument_spec={
            "oauth_token": {"required": True},
            "domain": {"required": True},
            "type": {"required": True},
            "name": {"required": True},
            "data": {"required": True},
            "priority": {"type": "int", "default": None},
            "port": {"type": "int", "default": None},
            "weight": {"type": "int", "default": None},
        },
        supports_check_mode=True,
    )
    s = requests.Session()
    s.headers["Authorization"] = "Bearer " + module.params["oauth_token"].strip()

    recurl = 'https://api.digitalocean.com/v2/domains/' \
            + module.params["domain"] + '/records'

    recname = module.params["name"]
    rectype = module.params["type"]
    recdata = module.params["data"]
    recpriority = module.params["priority"]
    recport = module.params["port"]
    recweight = module.params["weight"]

    changed = False
    try:
        records = []
        url = recurl
        while True:
            r = s.get(url)
            r.raise_for_status()
            data = r.json()
            for rec in data["domain_records"]:
                if rec["name"] == recname and rec["type"] == rectype:
                    records.append(rec)
            try:
                url = data["links"]["pages"]["next"]
            except KeyError:
                break

        matching = {
            rec["id"] for rec in records
                      if rec["data"] == recdata
                          and rec["priority"] == recpriority
                          and rec["port"] == recport
                          and rec["weight"] == recweight
        }
        if not matching:
            if not module.check_mode:
                s.post(recurl, json={
                    "type": rectype,
                    "name": recname,
                    "data": recdata,
                    "priority": recpriority,
                    "port": recport,
                    "weight": recweight,
                }).raise_for_status()
            changed = True

        for rec in records:
            if rec["id"] not in matching:
                if not module.check_mode:
                    s.delete(recurl + '/' + str(rec["id"])).raise_for_status()
                changed = True
    except requests.HTTPError as e:
        if 400 <= e.response.status_code < 500:
            msg = '{0.status_code} Client Error: {0.reason} for URL: {0.url}\n'
        elif 500 <= e.response.status_code < 600:
            msg = '{0.status_code} Server Error: {0.reason} for URL: {0.url}\n'
        else:
            msg = '{0.status_code} Unknown Error: {0.reason} for URL: {0.url}\n'
        msg = msg.format(e.response)
        try:
            resp = e.response.json()
        except ValueError:
            msg += e.response.text
        else:
            msg += json.dumps(resp, sort_keys=True, indent=4)
        module.fail_json(msg=traceback.format_exc() + '\n\n' + msg)
    except Exception:
        module.fail_json(msg=traceback.format_exc())
    module.exit_json(changed=changed)

from ansible.module_utils.basic import *
main()
