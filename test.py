def simple_gen():

    a = 0

    while True:
        if a == 0:
            yield "Black"
            a = 1
        else:
            yield "White"
            a = 0

a = simple_gen()


