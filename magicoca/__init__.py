from multiprocessing import set_start_method
from typing import Any, Callable, Generator

from magicoca.chan import Chan, T, NoRecvValue

__all__ = [
    "Chan",
    "select"
]

set_start_method("spawn", force=True)

def select(*args: Chan[T]) -> Generator[T, None, None]:
    """
    Return a yield, when a value is received from one of the channels.
    Args:
        args: channels
    """
    while True:
        for ch in args:
            if ch.is_closed:
                continue

            if not isinstance(value := ch.recv(0), NoRecvValue):
                yield value
