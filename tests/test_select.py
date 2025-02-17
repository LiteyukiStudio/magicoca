import time
from multiprocessing import Process

from magicoca import Chan, select


def send_process(chan: Chan[int], _id: int):
    for i in range(10):
        chan << i
        time.sleep(0.1 * _id)

def recv_process(chan_list: list[Chan[int]]):
    c = []
    for t in select(*chan_list):
        c.append(t)
        print("Select", t)
        if len(c) == 30:
            break
class TestSelect:
    def test_select(self):
        ch1 = Chan[int]()
        ch2 = Chan[int]()
        ch3 = Chan[int]()

        p1 = Process(target=send_process, args=(ch1, 1))
        p2 = Process(target=send_process, args=(ch2, 2))
        p3 = Process(target=send_process, args=(ch3, 3))
        p4 = Process(target=recv_process, args=([ch1, ch2, ch3],))

        p1.start()
        p2.start()
        p3.start()
        p4.start()

        p1.join()
        p2.join()
        p3.join()
        p4.join()
