from Result import Result

class BaseException(Exception):
    """A Base Exception that all other Exceptions derive from."""

    def __init__(self, code, desc):
        self.code = code
        self.desc = desc

    def __str__(self):
        return '{} {}'.format(str(self.code), str(self.desc))

    def to_result(self):
        return Result(self.code, False, self.desc)
