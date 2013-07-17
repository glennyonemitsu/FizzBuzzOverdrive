def coroutine(func):
    '''
    Taken from the one and only David Beazley 
    http://www.dabeaz.com/coroutines/index.html
    '''
    def start(*args,**kwargs):
        cr = func(*args,**kwargs)
        cr.next()
        return cr
    return start


def pipeline(func):
    '''
    Decorator to remove the "while True:" and "target.send()" boilerplate.
    DRYer than talcum powder!
    '''
    def loop(target=None):
        while True:
            payload = func((yield))
            if target:
                target.send(payload)
    return loop


@coroutine
@pipeline
def primer(payload):
    '''
    Initial integer sends are to become lists so metadata can be sent along
    the pipeline
    '''
    return [payload]


@coroutine
@pipeline
def printer(payload):
    '''
    Map/Reduce/lambda this payload to construct the final fizzbuzz string per
    iteration. No list comprehensions like some n00b Pythonista.
    '''
    print reduce(lambda x, y: x + ' ' + y, map(str, payload))
    return payload


def fizzbuzz_factory(interval, text):
    '''
    What's that, Jeff Atwood? Now it's Fizz Buzz Woof? I got you covered!
    '''
    @coroutine
    @pipeline
    def fizzbuzz(payload):
        if payload[0] % interval == 0:
            payload.append(text)
        return payload
    return fizzbuzz


if __name__ == '__main__':
    fizzer = fizzbuzz_factory(3, 'fizz')
    buzzer = fizzbuzz_factory(5, 'buzz')

    cr = primer(fizzer(buzzer(printer())))

    # if you want to crank your CPU to 11 and run fizz buzz woof
    #woofer = fizzbuzz_factory(7, 'woof')
    #cr = primer(fizzer(buzzer(woofer(printer()))))

    for i in range(30):
        cr.send(i)
