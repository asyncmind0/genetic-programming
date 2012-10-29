import numpy as np
import random

current_config = dict(
    integer_low=-10,
    integer_high=10,
    float_low=-1,
    float_high=1,
    random_integer_low=-10,
    random_integer_high=10,
    random_float_low=-1,
    random_float_high=1,
    organism_max_node_length=6
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

    def __repr__(self):
        return "RanInt"


class RandomFloat(Terminal):
    def __call__(self):
        integer = np.random.random_integers(
            current_config['random_float_low'],
            current_config['random_float_high'])
        return np.random.random_sample(1)[0] + integer

    def __repr__(self):
        return "RanFloat"


class ConstRandomInteger(int, Terminal):
    def __new__(cls, *args, **kwargs):
        value = np.random.random_integers(
            current_config['integer_low'],
            current_config['integer_high'])
        return  super(ConstRandomInteger, cls).__new__(cls, value)

    def __call__(self):
        return self


class ConstRandomFloat(float, Terminal):
    def __new__(cls, *args, **kwargs):
        integer = np.random.random_integers(
            current_config['float_low'],
            current_config['float_high'])
        float = np.random.random_sample(1)[0] + integer
        return  super(ConstRandomFloat, cls).__new__(cls, float)

    def __call__(self):
        return self


class Add(Function):
    _arity = 2

    def __call__(self, x, y):
        return np.add(x, y)

    def __repr__(self):
        return "+"

class Subtract(Function):
    _arity = 2

    def __call__(self, x, y):
        return np.subtract(x, y)

    def __repr__(self):
        return "-"


class Multiply(Function):
    _arity = 2

    def __call__(self, x, y):
        return np.multiply(x, y)

    def __repr__(self):
        return "*"

class Divide(Function):
    _arity = 2

    def __call__(self, x, y):
        return np.divide(x, y)

    def __repr__(self):
        return "/"

base_functions = [Add, Subtract, Multiply, Divide]
base_terminals = [RandomInteger, RandomFloat, ConstRandomInteger,
                  ConstRandomFloat]


def get_random_function(arity=2):
    index = np.random.random_integers(0, len(base_functions) - 1)
    return base_functions[index]()


def get_random_terminal():
    index = np.random.random_integers(0, len(base_terminals) - 1)
    return base_terminals[index]()


def get_random_node():
    return (get_random_terminal() if bool(random.getrandbits(1))
            else get_random_function())


def nodelen(nodelist):
    if not nodelist:
        return True
    return len(filter(lambda x: isinstance(x, Function), nodelist))


def grow(node, select_function=True):
    segment = []
    #print node
    segment.insert(0, node)
    if isinstance(node, Terminal):
        pass
    else:
        for n in range(node.arity):
            select_function = nodelen(segment) < current_config['organism_max_node_length']
            newnode = (get_random_node() if select_function
                       else get_random_terminal())
            if isinstance(node, Function):
                newsegment = grow(newnode, select_function)
                newsegment.extend(segment)
                segment = newsegment
            else:
                segment.insert(0, newnode)
    return segment


def eval_progranism(proganism):
    evalstack = []
    while len(proganism) >= 1:
        node = proganism.pop()
        if isinstance(node, Terminal):
            evalstack.insert(0, node())
        else:
            args = []
            for n in range(node.arity):
                args.append(evalstack.pop())
            try:
                res = apply(node, args)
                evalstack.insert(0, res)
            except Exception as e:
                print e
    return evalstack.pop()


if __name__ == '__main__':
    import sys
    population = []
    fitness = float(sys.argv[2])
    selected = []
    for n in range(int(sys.argv[1])):
        proganism = grow(get_random_function())
        proganism.reverse()
        population.append(proganism)
    for proganism in population:
        if abs(eval_progranism(list(proganism)) - fitness) <= 5:
            selected.append(proganism)

    print len(selected)
