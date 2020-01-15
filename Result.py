import json

class Result:
    """
    A class to store all results of target interrogation.
    """
    def __init__(self, code, outcome, desc):
        self.code = code
        self.outcome = outcome
        self.desc = desc

    def __str__(self):
        return "'code': '{}', 'outcome': {}, 'desc': '{}'".format(str(self.code), str(self.outcome), str(self.desc))

    def __repr__(self):
        return str(self)

class CustomEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Result):
            return {'code': o.code, 'outcome': o.outcome, 'desc': o.desc}

