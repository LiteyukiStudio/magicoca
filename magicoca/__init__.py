from magicoca.chan import Chan, T


def select(*args: Chan[T]) -> T:
    return Chan.select(*args)