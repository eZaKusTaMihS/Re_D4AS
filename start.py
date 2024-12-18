import argparse
import time
import utils
from d4 import GameController, D4ASException


global parser


def __start(_args: argparse.Namespace, crash_cnt: int):
    try:
        controller = GameController(_args, crash_cnt)
        controller.play()
    except KeyboardInterrupt:
        print('KeyboardInterrupt')
        exit(114514)
    except D4ASException:
        import traceback
        print(traceback.format_exc())
        return False


def main(_args: argparse.Namespace):
    cnt = 1
    while not __start(_args, cnt):
        time.sleep(60)
        cnt += 1
        if cnt >= 5:
            break


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--force-update', '-u', type=bool, default=False, required=False)
    parser.add_argument('--config', '-c', type=str, default='usr\\config.json', required=False)
    parser.add_argument('--serial', '-s', type=str, default='', required=False)
    parser.add_argument('--window', '-w', type=str, default='', required=False)
    parser.add_argument('--screen-route', '-S', type=str, default='', required=False)
