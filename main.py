import json
import argparse
import subprocess
from d4 import GameController, ControllerCrashException


crash_cnt = 0


def mian(_args: argparse.Namespace):
    global crash_cnt
    config = json.load(open('config.json'))
    controller = GameController(config, _args)
    try:
        controller.play()
    except ControllerCrashException:
        if crash_cnt >= 3:
            return
        crash_cnt += 1
        mian(_args)


def update():
    with open('pull.bat', 'r', encoding='utf-8') as f:
        subprocess.run(f.readline().strip())


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--force-update', '-u', type=bool, default=False, required=False)
    parser.add_argument('--serial', '-s', type=str, default='', required=False)
    parser.add_argument('--window', '-w', type=str, default='', required=False)
    parser.add_argument('--screen-route', '-S', type=str, default='', required=False)
    args = parser.parse_args()
    if args.force_update:
        args.force_update = False
        update()
    mian(args)
