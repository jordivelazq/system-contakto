import time

class Timer(object):
    def __init__(self, verbose=False):
        self.verbose = verbose

    def __enter__(self):
        self.start = time.time()
        return self

    def __exit__(self, *args):
        self.end = time.time()
        self.secs = self.end - self.start
        self.msecs = self.secs * 1000  # millisecs
        if self.verbose:
            print 'elapsed time: %f ms' % self.msecs

def timethis(func):
    def func_wrapper(*args, **kwargs):
        with Timer() as t:
	    ret_val = func(*args, **kwargs)
        print "Time to Execute %s: %0.6f" % (func.__name__, t.secs)
        return ret_val
    return func_wrapper
