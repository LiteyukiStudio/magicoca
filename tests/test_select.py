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


class TestSelect:
    def test_select(self):
        chan1 = Chan[int]()
        chan2 = Chan[int]()

        print("Test Chan Select")

        p1 = Process(target=sp1, args=(chan1,))
        p2 = Process(target=sp2, args=(chan2,))
        p3 = Process(target=rp, args=([chan1, chan2],))
        p3.start()
        p1.start()
        p2.start()

        p1.join()
        p2.join()
        p3.join()
