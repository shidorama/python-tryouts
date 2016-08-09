test = {'interests': ['Action games', 'Taylor Swift'],
        'behaviors': ['Crossover', 'Luxury SUV', 'Farmers', 'Expats (All)'], 'countries': ['US'],
        'friends_of_connections': ['My Favorit Product'], 'location_types': ['home', 'recent'],
        'user_adclusters': ['Fast Food'], 'life_events': ['New job'],
        'regions': ['Connecticut', 'Hawaii', 'Massachusetts', 'New York'], 'user_os': ['Android_ver_5.1_and_above'],
        'age_min': [18], 'age_max': [45], 'cities': ['Barcelona'], 'locales': [23, 44, 9]}


# y = [x[1] for x in test]
# print y


class Tstttts(object):
    def __init__(self, add = None):
        props = ['a', 'b', 'c']
        self._targeting = {'a': 1, 'b': 2, 'c': None}
        if isinstance(add, dict):
            for prp in add:
                props.append(prp)
                self._targeting[prp] = add[prp]
        for propname in props:
            self.addprop(propname, lambda self: self._targeting.get(propname))

    def addprop(inst, name, method):
        cls = type(inst)
        if not hasattr(cls, '_'+cls.__name__+'__perinstance'):
            cls = type(cls.__name__, (cls,), {})
            cls.__perinstance = True
            inst.__class__ = cls
        setattr(cls, name, property(method))

y = Tstttts({'eee': 12321})
print y.eee

x= Tstttts()
print x.a
print x.c
#
print isinstance(x, Tstttts)
print isinstance(y, Tstttts)
print type(x) == Tstttts
#
# from random import choice
# class Ttt(object):
#     __slots__ = ['a', 'b', 'c']
    # def __init__(self):
    #     pool = ['a', 'b', 'c']
    #     self.__setattr__(choice(pool), choice(pool))
#
# x = Ttt()
# y = Ttt()
# z = Ttt()
# print x.a + x.b + x.c
