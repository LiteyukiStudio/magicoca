import time

from magicoca.chan import Chan
from multiprocessing import Process


class TestChan:
    def test_chan_shift(self):
        ch = Chan[int]()

        def p1f(chan: Chan[int]):
            for i in range(10):
                time.sleep(1)
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

        print("Test Chan Shift")
        p1 = Process(target=p1f, args=(ch,))
        p2 = Process(target=p2f, args=(ch,))
        p1.start()
        p2.start()
        p1.join()
        p2.join()

    def test_chan_sr(self):
        ch = Chan[int]()

        def p1f(chan: Chan[int]):
            for i in range(10):
                time.sleep(1)
                chan.send(i)
            chan.send(-1)

        def p2f(chan: Chan[int]):
            recv_ans = []
            while True:
                a = chan.recv()
                recv_ans.append(a)
                print("Recv2", a)
                if a == -1:
                    break
            if recv_ans != list(range(10)) + [-1]:
                raise ValueError("Chan SR Test Failed")

        print("Test Chan SR")
        p1 = Process(target=p1f, args=(ch,))
        p2 = Process(target=p2f, args=(ch,))
        p1.start()
        p2.start()
        p1.join()
        p2.join()
