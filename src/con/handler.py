from ruleset.ruleset import RuleSet
from ruleset.action import Action

from web.request import HttpRequest

class Handler:
    def __init__(self, ruleset: RuleSet, allow, size, action, logger):
        self.ruleset = ruleset
        self.allow = allow
        self.size = size
        self.action = action
        self.logger = logger

    def handler(self, data: bytes, ip):
        http = HttpRequest(data, ip)

        if len(http.body) > self.size:
            assert self.action != Action.COUNT
            if self.action == Action.BLOCK:
                return False
            http.body = ""
            self.json_body = None

        if self.allow(
            ip,
            http.ipv4,
            http.ipv6,
            http.header["user-agent"]
            ):
            return True

        rule, detected = self.ruleset.detect(http)
        if detected:
            self.logger(http, rule, detected)
        return rule.action != Action.BLOCK
