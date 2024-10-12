import time

from magicoca.chan import Chan
from multiprocessing import Process, set_start_method



def p1f(chan: Chan[int]):
    for i in range(10):
        chan << i
    chan << -1

def p2f(chan: Chan[int]):
    recv_ans = []
    while True:
        a = int << chan
        print("Recv", a)
        recv_ans.append(a)
        if a == -1:
            break
    if recv_ans != list(range(10)) + [-1]:
        raise ValueError("Chan Shift Test Failed")

class TestChan:

    def test_test(self):
        print("Test is running")

    def test_chan_shift(self):
        """测试运算符"""
        ch = Chan[int]()
        print("Test Chan Shift")
        p1 = Process(target=p1f, args=(ch,))
        p2 = Process(target=p2f, args=(ch,))
        p1.start()
        p2.start()
        p1.join()
        p2.join()

    def test_chan_sr(self):
        """测试收发"""
        ch = Chan[int]()

        print("Test Chan SR")
        p1 = Process(target=p1f, args=(ch,))
        p2 = Process(target=p2f, args=(ch,))
        p1.start()
        p2.start()
        p1.join()
        p2.join()

    def test_connect(self):
        """测试双通道连接"""
        chan1 = Chan[int]()
        chan2 = Chan[int]()

        chan1 + chan2

        print("Test Chan Connect")
        p1 = Process(target=p1f, args=(chan1,))
        p2 = Process(target=p2f, args=(chan2,))
        p1.start()
        p2.start()
        p1.join()
        p2.join()
