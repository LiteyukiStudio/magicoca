"""
Chan is a simple channel implementation using multiprocessing.Pipe.
"""
from multiprocessing import Pipe
from typing import TypeVar, Generic, Any

T = TypeVar("T")

class NoRecvValue(Exception):
    """
    Exception raised when there is no value to receive.
    """
    pass


class Chan(Generic[T]):
    """
    Chan is a simple channel implementation using multiprocessing.Pipe.

    Attributes:
        send_conn: The sending end of the pipe.
        recv_conn: The receiving end of the pipe.

    Methods:
        send: Send a value to the channel.
        recv: Receive a value from the channel.
        close: Close the channel.
        __iter__: Return the channel object.
        __next__: Receive a value from the channel.
        __lshift__: Send a value to the channel.
        __rlshift__: Receive a value from the channel.
    """

    def __init__(self):
        """
        Initialize the channel.
        """
        self.send_conn, self.recv_conn = Pipe()

        self.is_closed = False

    def send(self, value: T):
        """
        Send a value to the channel.
        Args:
            value: The value to send.
        """
        self.send_conn.send(value)

    def recv(self, timeout: float | None = None) -> T | None | NoRecvValue:
        """Receive a value from the channel.
        If the timeout is None, it will block until a value is received.
        If the timeout is a positive number, it will wait for the specified time, and if no value is received, it will return None.
        接收通道中的值。
        如果超时为None，则它将阻塞，直到接收到值。
        如果超时是正数，则它将等待指定的时间，如果没有接收到值，则返回None。
        Args:
            timeout:
                The maximum time to wait for a value.
                等待值的最长时间。
        Returns:
            T: The value received from the channel.
            从通道接收的值。
        """
        if timeout is not None:
            if not self.recv_conn.poll(timeout):
                return NoRecvValue("No value to receive.")
        return self.recv_conn.recv()


    def close(self):
        """
        Close the channel. destructor
        """
        self.send_conn.close()
        self.recv_conn.close()
        self.is_closed = True

    def __iter__(self) -> "Chan[T]":
        """
        Returns: The channel object.
        """
        return self

    def __next__(self) -> T:
        return self.recv()

    def __lshift__(self, other: T):
        """
        chan << obj
        Args:
            other: The object to send.
        Returns: self
        """
        self.send(other)
        return self

    def __rlshift__(self, other: Any) -> T:
        """
        << chan
        Returns: The value received from the channel.
        """
        return self.recv(None)

    def __add__(self, other: "Chan[T]"):
        """
        Connect 1 channel.send to another channel.recv.
        Args:
            other:
        Returns:
        """
        self.recv_conn, other.recv_conn = other.recv_conn, self.recv_conn

    def __del__(self):
        """
        Close the channel when the object is deleted.
        """
        self.close()
