from multiprocessing import Pipe
from typing import TypeVar, Generic, Any

T = TypeVar("T")


class Chan(Generic[T]):
    def __init__(self, buffer: int = 0):
        self._buffer = buffer
        self._send_conn, self._recv_conn = Pipe()

    def send(self, value: T):
        self._send_conn.send(value)

    def recv(self) -> T:
        return self._recv_conn.recv()

    def close(self):
        self._send_conn.close()
        self._recv_conn.close()

    def __iter__(self):
        """

        Returns:
        """
        return self

    def __next__(self) -> T:
        return self.recv()

    def __lshift__(self, other: T):
        """
        chan << obj
        Args:
            other:
        Returns:

        """
        self.send(other)
        return self

    def __rlshift__(self, other: Any) -> T:
        """
        << chan
        Returns:

        """
        return self.recv()
