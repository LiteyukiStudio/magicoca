from multiprocessing import set_start_method
from multiprocessing.connection import wait
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
    pipes = [ch.recv_conn for ch in args if not ch.is_closed]

    while pipes:
        ready_pipes = wait(pipes)
        for pipe in ready_pipes:
            for ch in args:
                if ch.recv_conn == pipe:
                    if not isinstance(value := ch.recv(0), NoRecvValue):
                        yield value
                    if ch.is_closed:
                        pipes.remove(pipe)