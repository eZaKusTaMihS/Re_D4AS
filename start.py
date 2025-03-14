import argparse
import pickle
from d4 import GameController, D4ASException


def start(crash_cnt: int) -> bool:
    try:
        controller = GameController(args, crash_cnt)
        controller.play()
    except KeyboardInterrupt:
        exit()
    except D4ASException:
        import traceback
        print(traceback.format_exc())
        return False


def mian():
    cnt = 1
    while not start(cnt):
        cnt += 1
        if cnt > 5:
            break


if __name__ == '__main__':
    args = pickle.load(open('temp\\args', 'rb'))
    mian()
