import gevent

def ifilter(func, iterable):
    for item in iterable:
        if func(item):
            yield item
        gevent.sleep(0)

def imap(func, iterable):
    for item in iterable:
        yield func(item)
        gevent.sleep(0)

