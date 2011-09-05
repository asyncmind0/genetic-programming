import numpy as np

current_config  = dict(
        integer_low=-10,
        integer_high=10,
        float_low=-1,
        float_high=1,
        random_integer_low=-10,
        random_integer_high=10,
        random_float_low=-1,
        random_float_high=1,
        )

class Primitive:
    def is_callable(self):
        return hasattr(self, '__call__')

class Function(Primitive):
    def __call__():
        pass
    @property
    def arity(self):
        return self._arity if self._arity else 0

class Terminal(Primitive):
    pass


class RandomInteger(Terminal):
    def __call__(self):
        return np.random.random_integers(
            current_config['random_integer_low'],
            current_config['random_integer_high'])

class RandomFloat(Terminal):
    def __call__(self):
        integer =  np.random.random_integers(
            current_config['random_float_low'],
            current_config['random_float_high'])
        return np.random.random_sample(1)[0]+integer

class ConstRandomInteger(int, Primitive):
    def __new__(cls, *args, **kwargs):
        value =  np.random.random_integers(
            current_config['integer_low'],
            current_config['integer_high'])
        return  super(ConstRandomInteger, cls).__new__(cls, value)

class ConstRandomFloat(float, Primitive):
    def __new__(cls, *args, **kwargs):
        integer =  np.random.random_integers(
            current_config['float_low'],
            current_config['float_high'])
        float =  np.random.random_sample(1)[0]+integer
        return  super(ConstRandomFloat, cls).__new__(cls, float)

class Add(Function):
    _arity=2
    def __call__(self,x,y):
        return np.add(x,y)

class Subtract(Function):
    _arity=2
    def __call__(self,x,y):
        return np.subtract(x,y)

class Multiply(Function):
    _arity=2
    def __call__(self,x,y):
        return np.multiply(x,y)

class Divide(Function):
    _arity=2
    def __call__(self,x,y):
        return np.divide(x,y)

base_functions = [Add, Subtract, Multiply, Divide]
base_terminals = [RandomInteger, RandomFloat, ConstRandomInteger, ConstRandomFloat]

def get_random_function(arity=2):
    index = np.random.random_integers(0,len(base_functions)-1)
    return base_functions[index]


def get_random_terminal():
    index = np.random.random_integers(0,len(base_terminals)-1)
    return base_terminals[index]()

