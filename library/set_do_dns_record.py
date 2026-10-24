#!/usr/bin/python
# Set a DNS record in DigitalOcean to a given value, deleting any conflicting
# records of the same domain, name, & type
# cf. <https://github.com/ansible/ansible/pull/31765>
from __future__ import annotations
from dataclasses import dataclass
import json
import traceback
from typing import Any
from urllib.error import HTTPError
from urllib.request import Request, urlopen
from ansible.module_utils.basic import AnsibleModule

USER_AGENT = "set_do_dns_record.py/0.0.0"


@dataclass
class JsonClient:
    token: str

    def headers(self) -> dict[str, str]:
        return {
            "User-Agent": USER_AGENT,
            "Authorization": f"Bearer {self.token}",
        }

    def dorequest(self, req: Request) -> Any:
        try:
            with urlopen(req) as r:
                if r.status == 204 or r.headers.get("Content-Length", None) == "0":
                    return None
                else:
                    return json.load(r)
        except HTTPError as e:
            with e:
                bodybytes = e.fp.read()
                try:
                    data = json.loads(bodybytes)
                except ValueError:
                    body = bodybytes.decode("utf-8", "surrogateescape")
                else:
                    body = json.dumps(data, sort_keys=True, indent=4)
                raise PrettyHTTPError(
                    method=req.get_method(),
                    code=e.code,
                    reason=e.reason,
                    url=e.url,
                    body=body,
                )

    def get(self, url: str) -> Any:
        return self.dorequest(Request(url, headers=self.headers()))

    def post(self, url: str, data: Any) -> None:
        self.dorequest(
            Request(
                url,
                data=json.dumps(data).encode("utf-8"),
                headers={**self.headers(), "Content-Type": "application/json"},
            )
        )

    def delete(self, url: str) -> None:
        self.dorequest(Request(url, method="DELETE", headers=self.headers()))


@dataclass
class PrettyHTTPError(Exception):
    method: str
    code: int
    reason: str
    url: str
    body: str

    def __str__(self) -> str:
        if 400 <= self.code < 500:
            errtype = "Client"
        elif 500 <= self.code < 600:
            errtype = "Server"
        else:
            errtype = "Unknown"
        return (
            f"{self.code} {errtype} Error: {self.reason} for"
            f" {self.method} {self.url}\n{self.body}"
        )


def main() -> None:
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
    client = JsonClient(token=module.params["oauth_token"].strip())
    recurl = (
        "https://api.digitalocean.com/v2/domains/"
        + module.params["domain"]
        + "/records"
    )
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
            data = client.get(url)
            for rec in data["domain_records"]:
                if rec["name"] == recname and rec["type"] == rectype:
                    records.append(rec)
            try:
                url = data["links"]["pages"]["next"]
            except KeyError:
                break
        matching = {
            rec["id"]
            for rec in records
            if rec["data"] == recdata
            and rec["priority"] == recpriority
            and rec["port"] == recport
            and rec["weight"] == recweight
        }
        if not matching:
            if not module.check_mode:
                client.post(
                    recurl,
                    data={
                        "type": rectype,
                        "name": recname,
                        "data": recdata,
                        "priority": recpriority,
                        "port": recport,
                        "weight": recweight,
                    },
                )
            changed = True
        for rec in records:
            if rec["id"] not in matching:
                if not module.check_mode:
                    client.delete(recurl + "/" + str(rec["id"]))
                changed = True
    except PrettyHTTPError as e:
        module.fail_json(msg=traceback.format_exc() + "\n\n" + str(e))
    except Exception:
        module.fail_json(msg=traceback.format_exc())
    module.exit_json(changed=changed)


if __name__ == "__main__":
    main()
