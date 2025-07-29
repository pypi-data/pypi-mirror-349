# Small useful functions

# str

def replacer(inp='', changes=None):
    '''
    Uses the replace() function for strings on param inp for multiple changes
        param changes has to be iterable that contains iterables of length 2 that contain 2 strings
    Changes will be applied in the order of param changes
        Ex: replacer('abcdef', [('abc', 'cba'), ('def', 'fed'), ('bafe', 'x')]) = 'cxd'
            replacer('abcdef', [('abc', 'cba'), ('bafe', 'x'), ('def', 'fed')]) = 'cbafed'
    :param inp: str     string to apply changes to
    :param changes: iter    iter of iters of 2 str
    :return: str    inp with all replacings applied
    '''
    # checks for parameters
    if type(inp) != str:    # inp not str?
        raise TypeError('inp not str')
    iter(changes)           # is changes iterable?
    # Apply all changes
    res = str(inp)  # copy inp
    for change in changes:              # For each change
        res = res.replace(*change)      # Apply the change
    return res  # return changed str


def remover(inp='', to_remove=None):
    '''
    Removes substrings in to_remove from inp and returns changed string
        Does not change the parameter
        to_remove can be str (remove one substring) or iterable of str (remove all those substrings)
            substrings are removed in order of param to_remove
    :param inp: str     input string
    :param to_remove: str or iter   substring(s) that should be removed from inp
    :return: str
    '''
    # checks for parameters
    if type(inp) != str:    # inp not str?
        raise TypeError('inp not str')
    if to_remove is None:   # to_remove is None?
        return inp  # nothing has to be removed
    elif type(to_remove) == str:    # to_remove is str?
        to_remove = [to_remove]     # put it in a list
    iter(to_remove)     # Is to_remove iterable?
    # Remove all strings in iterable to_remove
    res = str(inp)      # copy param inp
    for item in to_remove:      # for item in to_remove
        res = res.replace(item, '')     # replace item with empty string
    return res  # return str with applied removes


def str_len(s=None, l=None, char=None, cut=False):
    '''
    Makes str 's' have the length 'l' by adding 'char' until the length matches
        cut:    if True and len(s) > l: the last len(s)-l chars of s will be cut off
    :param s:   str : input string      default: empty string
    :param l:   int : desired length    default: len(s)
    :param char:    str : char to lengthen  default: ' '
    :param cut: bool : should s be trimmed to length l if l < len(s)?   default: False
    :return: str
    '''
    # checks and default values for parameters
    if s is None:
        s = ''
    if type(s) != str:
        raise TypeError(f's needs to be type str but is {type(s)}')
    if l is None:
        l = len(s)
    if type(l) != int:
        l = int(l)
    if char is None:
        char = ' '
    if type(char) != str:
        raise TypeError(f'char needs to be type str but is {type(char)}')
    # actual code starts here
    s += (char * (l - len(s)))[:l - len(s)] # make s longer
    if cut:
        s = s[:l]   # cut s to length l if it is too long
    return s
