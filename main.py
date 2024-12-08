import json
import argparse
from d4 import GameController, ControllerCrashException


crash_cnt = 0


def mian(args: argparse.Namespace):
    global crash_cnt
    config = json.load(open('config.json'))
    controller = GameController(config, args)
    try:
        controller.play()
    except ControllerCrashException:
        if crash_cnt >= 3:
            return
        crash_cnt += 1
        mian(args)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--serial', '-s', type=str, default='', required=False)
    parser.add_argument('--window', '-w', type=str, default='', required=False)
    parser.add_argument('--screen-route', '-S', type=str, default='', required=False)
    mian(parser.parse_args())
