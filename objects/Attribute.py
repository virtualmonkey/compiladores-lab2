class Attribute:
    def __init__(
        self,
        name,
        type,
        scope = None,
        insideClass = None,
        insideMethod = None,
        isParameterOfFunction = False,
        size = 1,
        displacement = 0,
    ):
        self.name = name
        self.type = type
        self.scope = scope
        self.insideClass = insideClass
        self.insideMethod = insideMethod
        self.isParameterOfFunction = isParameterOfFunction
        self.size = size
        self.displacement = displacement
    def __str__(self):
        return '[ATTRIBUTE] -> identifier: %s, type: %s, scope: %s, insideClass: %s, insideMethod: %s, isParameterOfFunction: %s, size = %s bytes, displacement = %s' % (self.name, self.type, self.scope, self.insideClass, self.insideMethod, self.isParameterOfFunction, self.size, self.displacement)