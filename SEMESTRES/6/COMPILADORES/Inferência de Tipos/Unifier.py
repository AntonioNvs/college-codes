from Expression import *
from Visitor import *
import sys

def unify(constraints, sets):
    """
    This function unifies all the type variables in the list of constraints;
    thus, producing a set of unifiers.

    Example:
        >>> sets = unify([('a', type(1))], {})
        >>> integers = sets[type(1)] - {type(1)}
        >>> sorted(integers)
        ['a']

        >>> sets = unify([(type(1), 'b'), ('a', type(1))], {})
        >>> integers = sets[type(1)] - {type(1)}
        >>> sorted(integers)
        ['a', 'b']

        >>> sets = unify([(type(True), 'b'), ('a', type(1))], {})
        >>> booleans = sets[type(True)] - {type(True)}
        >>> sorted(booleans)
        ['b']

        >>> sets = unify([(type(True), 'b'), ('a', type(1))], {})
        >>> integers = sets[type(1)] - {type(1)}
        >>> sorted(integers)
        ['a']

        >>> sets = unify([('a', 'TV_1'), ('b', 'TV_2'), ('TV_2', type(1)), ('TV_1', type(1))], {})
        >>> integers = sets[type(1)] - {type(1)}
        >>> sorted(integers)
        ['TV_1', 'TV_2', 'a', 'b']

    Notice that at this stage, we still allow sets with invalid types. For
    instance, the set associated with 'b' in the example below will contain
    four elements, namely: {<class 'bool'>, <class 'int'>, 'b', 'a'}:
        >>> sets = unify([(type(True), 'b'), ('a', type(1)), ('a', 'b')], {})
        >>> len(sets['b'])
        4
    """
    
    if len(constraints) == 0:
        return sets
    
    el0, el1 = constraints[0]
    rest = constraints[1:]
    if el0 != el1:
        s0 = sets.setdefault(el0, set())
        s1 = sets.setdefault(el1, set())
        new_set = s0 | s1 | {el0, el1}

        for t in new_set:
            sets[t] = new_set
        
    return unify(rest, sets)


def name_sets(sets):
    """
    This method replaces type sets with "canonical type names". A canonical
    type name is the name of a type set. For instance, the type set
    {'a', 'b', type(int)} has the canonical name type(int)

    Notice that this method produces two types of error messages:
    * Polymorphic type: if any canonical type set is empty
    * Ambiguous type: if any canonical type set contains more than one element.
    In both cases, if any of these errors happen, the program should stop with
    the following error message: 'Type error'

    Example:
        >>> sets = name_sets({'a': {'a', 'b', type(1)}, 'b': {'a', 'b', type(1)}})
        >>> [sets['a'], sets['b']]
        [<class 'int'>, <class 'int'>]

        >>> sets = name_sets({'a': {'a', type(1)}, 'b': {'b', type(True)}})
        >>> [sets['a'], sets['b']]
        [<class 'int'>, <class 'bool'>]
    """
    unified = {}
    for name in sets.keys():
        set_ = sets[name]
        
        type_ = None
        for c in set_:
            if c == type(1) and type_ == None: type_ = c
            elif c == type(True) and type_ == None: type_ = c
            elif (c == type(1) or c == type(True)) and type_ != None:
                sys.exit("Type error")
        
        if type_ == None: sys.exit("Type error")
        unified[name] = type_
    
    return unified


def infer_types(expression):
    """
    This method maps all the program variables to type names. We have
    implemented this method for you. This implementation might help you to
    understand how the other two methods, unify and name_sets are meant to
    work.

    # Example:
        >>> e = Let('v', Num(42), Var('v'))
        >>> type_names = infer_types(e)
        >>> type_names['v']
        <class 'int'>

        >>> e = Let('v', Num(1), Let('y', Var('v'), Var('y')))
        >>> type_names = infer_types(e)
        >>> [type_names['v'], type_names['y']]
        [<class 'int'>, <class 'int'>]

        >>> e0 = Let('v', Num(1), Let('y', Var('v'), Var('y')))
        >>> e1 = IfThenElse(Lth(e0, Num(2)), Bln(True), Bln(False))
        >>> e2 = Let('w', e1, And(Var('w'), Var('w')))
        >>> type_names = infer_types(e2)
        >>> [type_names['v'], type_names['w'], type_names['y']]
        [<class 'int'>, <class 'bool'>, <class 'int'>]

        >>> e = Lth(Bln(True), Num(3))
        >>> type_names = infer_types(e)
        >>> type_names
        [""]
     """
    ev = CtrGenVisitor()
    constraints = list(expression.accept(ev, ev.fresh_type_var()))
    type_sets = unify(constraints, {})
    return name_sets(type_sets)


if __name__ == "__main__":
    sets = name_sets({'a': {'a', 'b', type(1)}, 'b': {'a', 'b', type(1)}})
    print([sets['a'], sets['b']])