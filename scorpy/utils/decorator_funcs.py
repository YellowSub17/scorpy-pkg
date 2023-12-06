


import os


import contextlib

def verbose_dec(fn):

    def wrapper(*args, **kwargs):
        if 'verbose' in kwargs.keys() and kwargs['verbose']>0:
            result = fn(*args, **kwargs)
        else:
            with open(os.devnull, "w") as f, contextlib.redirect_stdout(f):
                result = fn(*args, **kwargs)
        return result
    return wrapper



