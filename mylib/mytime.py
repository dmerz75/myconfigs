import time

def mytime(f):
    def wrap(*args):
        time1 = time.time()
        ret = f(*args)
        time2 = time.time()
        print '%s function took %0.3f ms' % (f.func_name, (time2-time1)*1000.0)
        timef = (time2 - time1) * 1000.0
        return ret,timef
    return wrap


class myTimer(object):

    def __init__(self,f):
        self.f = f
        self.total_time = 0.0


    def __call__(self,*args):

        print "Entered: ",self.f.__name__

        time1 = time.time()
        ret = self.f(*args)
        time2 = time.time()

        # self.total_time = "%0.3f" % ((time2-time1)*1000.0)
        self.total_time = (time2-time1)

        print "Exited: ",self.f.__name__
        print '%s function took %0.3f ms' % (self.f.__name__,self.total_time * 1000.0)
        print '%s function took %0.3f s' % (self.f.__name__,self.total_time)
        # print '%s function took %0.3f ms' % (self.f.__name__, (time2-time1)*1000.0)


        return self.total_time


    def print_time(self):

        for attr in attr(self):
            print attr

    def __print_time__(self,*args):

        print self.total_time
        # print '%s function took %0.3f ms' % (self.f.__name__, (time2-time1)*1000.0)








class entryExit(object):

    def __init__(self, f):
        self.f = f

    def __call__(self):
        print "Entering", self.f.__name__
        self.f()
        print "Exited", self.f.__name__



@entryExit
def func1():
    print "inside func1()"

@entryExit
def func2():
    print "inside func2()"


@myTimer
def func3():
    print "running..begin"

@myTimer
def func4():
    print "running..stop"

@myTimer
def func5(f):
    f()
