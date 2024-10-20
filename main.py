import time
from multiprocessing import Process

from magicoca import select, Chan


def send_process(chan: Chan[int], _id: int):
    i = 0
    while True:
        i += 1
        chan << _id
        time.sleep(2)
        if i == 50:
            chan << -1
            break


def recv_process(chan_list: list[Chan[int]]):
    for t in select(*chan_list):
        print(t)
        if t == -1:
            break


def main():
    chan_list = []
    for i in range(10):
        chan = Chan[int]()
        chan_list.append(chan)
        p = Process(target=send_process, args=(chan, i))
        p.start()
    p = Process(target=recv_process, args=(chan_list,))
    p.start()


if __name__ == '__main__':
    main()
