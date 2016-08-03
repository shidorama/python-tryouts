class Propertable(object):
    def addprop(inst, name, method):
        cls = type(inst)
        if not hasattr(cls, '_'+cls.__name__+'__perinstance'):
            cls = type(cls.__name__, (cls,), {})
            cls.__perinstance = True
            inst.__class__ = cls
        setattr(cls, name, property(method))