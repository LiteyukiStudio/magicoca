"""
Chan is a simple channel implementation using multiprocessing.Pipe.

Chan 是一个简单的通道实现，使用 multiprocessing.Pipe。
"""
from multiprocessing import Pipe
from typing import TypeVar, Generic, Any

T = TypeVar("T")

class NoRecvValue(Exception):
    """
    Exception raised when there is no value to receive.

    当没有值可以接收时引发的异常。
    """
    pass


class Chan(Generic[T]):
    """
    Chan is a simple channel implementation using multiprocessing.Pipe.

    Chan 是一个简单的通道实现，使用 multiprocessing.Pipe。

    Attributes:
        send_conn: The sending end of the pipe.
                   管道的发送端。
        recv_conn: The receiving end of the pipe.
                   管道的接收端。
    """

    def __init__(self):
        """
        Initialize the channel.

        初始化通道。
        """
        self.send_conn, self.recv_conn = Pipe()
        self.is_closed = False

    def send(self, value: T):
        """
        Send a value to the channel.

        发送一个值到通道。

        Args:
            value: The value to send.
                  要发送的值。
        """
        self.send_conn.send(value)

    def recv(self, timeout: float | None = None) -> T | NoRecvValue:
        """
        Receive a value from the channel.

        从通道接收一个值。

        Args:
            timeout: The maximum time to wait for a value.
                    等待值的最长时间。
                    If None, it will block until a value is received.
                    如果为 None，则阻塞直到接收到值。

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
        Close the channel.

        关闭通道。
        """
        self.send_conn.close()
        self.recv_conn.close()
        self.is_closed = True

    def __iter__(self) -> "Chan[T]":
        """
        Return the channel object.

        返回通道对象。
        """
        return self

    def __next__(self) -> T | NoRecvValue:
        """
        Receive a value from the channel.

        从通道接收一个值。
        """
        return self.recv()

    def __lshift__(self, other: T):
        """
        Send an object to the channel.

        发送一个对象到通道。

        Args:
            other: The object to send.
                   要发送的对象。

        Returns:
            self: The channel object.
                  通道对象。
        """
        self.send(other)
        return self

    def __rlshift__(self, other: Any) -> T | NoRecvValue:
        """
        Receive a value from the channel.

        从通道接收一个值。

        Returns:
            T: The value received from the channel.
               从通道接收的值。
        """
        return self.recv(None)

    def __add__(self, other: "Chan[T]"):
        """
        Connect one channel's send to another channel's recv.

        将一个通道的发送端连接到另一个通道的接收端。

        Args:
            other: The other channel to connect.
                   要连接的另一个通道。
        """
        self.recv_conn, other.recv_conn = other.recv_conn, self.recv_conn

    def __del__(self):
        """
        Close the channel when the object is deleted.

        当对象被删除时关闭通道。
        """
        self.close()

