def coroutine(func):
    def start(*args,**kwargs):
        cr = func(*args,**kwargs)
        cr.next()
        return cr
    return start


def pipeline(func):
    def loop(target=None):
        while True:
            payload = func((yield))
            if target:
                target.send(payload)
    return loop


@coroutine
@pipeline
def primer(payload):
    return [payload]


@coroutine
@pipeline
def printer(payload):
    print reduce(lambda x, y: x + ' ' + y, map(str, payload))
    return payload


def fizzbuzz_factory(interval, text):
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
    for i in range(30):
        cr.send(i)
