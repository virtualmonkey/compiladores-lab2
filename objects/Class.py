class Class:
    def __init__(
        self,
        name,
        inheritsFrom = "Object"
    ):
        self.name = name
        self.inheritsFrom = inheritsFrom

    def __str__(self):
        return '[CLASS] -> Identifier: %s, inheritsFrom: %s' % (self.name, self.inheritsFrom)