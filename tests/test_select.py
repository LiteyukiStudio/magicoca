import time
from multiprocessing import Process

from magicoca import Chan, select


def sp1(chan: Chan[int]):
    for i in range(10):
        chan << i << i * 2


def sp2(chan: Chan[int]):
    for i in range(10):
        chan << i << i * 3


def rp(chans: list[Chan[int]]):
    rl = []
    for t in select(*chans):
        rl.append(t)
        if len(rl) == 40:
            break
    print(rl)

def send_process(chan: Chan[int], _id: int):
    while True:
        chan << _id
        time.sleep(2)

def recv_process(chan_list: list[Chan[int]]):
    for t in select(*chan_list):
        print(t)


class TestSelect:
    def test_select(self):
        chan_list = []
        for i in range(10):
            chan = Chan[int]()
            chan_list.append(chan)
            p = Process(target=send_process, args=(chan, i))
            p.start()
        p = Process(target=recv_process, args=(chan_list,))
        p.start()
