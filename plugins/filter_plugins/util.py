class FilterModule(object):
    def filters(self):
        return {
            # Just `str.splitlines` doesn't support unicode arguments
            "splitlines": lambda s: s.splitlines(),
        }
