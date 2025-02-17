from multiprocessing import set_start_method
from multiprocessing.connection import wait, Connection
from typing import Generator

from magicoca.chan import Chan, T, NoRecvValue

__all__ = [
    "Chan",
    "select"
]

set_start_method("spawn", force=True)

def select(*args: Chan[T]) -> Generator[T, None, None]:
    """
    当其中一个通道接收到数据时，yield 该数据。

    参数:
        args: 多个 Chan 对象
    """
    # 构造管道到通道列表的映射，避免重复的 recv_conn 对象
    pipe_to_chs: dict[Connection, list[Chan[T]]] = {}
    for ch in args:
        if not ch.is_closed:
            pipe: Connection = ch.recv_conn
            pipe_to_chs.setdefault(pipe, []).append(ch)
    pipes: list[Connection] = list(pipe_to_chs.keys())

    while pipes:
        ready_pipes: list[Connection] = wait(pipes) # type: ignore
        for pipe in ready_pipes:
            # 遍历所有使用该管道的通道
            channels: list[Chan[T]] = list(pipe_to_chs.get(pipe, []))
            for ch in channels:
                if not isinstance(value := ch.recv(0), NoRecvValue):
                    yield value
                if ch.is_closed:
                    pipe_to_chs[pipe].remove(ch)
            # 如果该管道已没有活跃的通道，则移除
            if not pipe_to_chs[pipe]:
                pipes.remove(pipe)