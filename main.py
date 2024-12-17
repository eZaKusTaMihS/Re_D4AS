import argparse
import utils
import update
from d4 import GameController, D4ASException


def start(_args: argparse.Namespace, crash_cnt: int):
    try:
        controller = GameController(_args, crash_cnt)
        controller.play()
    except KeyboardInterrupt:
        exit(114514)
    except D4ASException:
        import traceback
        print(traceback.format_exc())
        return False


def mian(_args: argparse.Namespace):
    cnt = 1
    while not start(_args, cnt):
        cnt += 1
        if cnt > 5:
            break


if __name__ == '__main__':
    info = utils.load_json('info.json')
    conda_env = info['conda_env']
    if conda_env:
        utils.execute('conda activate %s' % conda_env)
    parser = argparse.ArgumentParser()
    parser.add_argument('--force-update', '-u', type=bool, default=False, required=False)
    parser.add_argument('--config', '-c', type=str, default='usr\\config.json', required=False)
    parser.add_argument('--serial', '-s', type=str, default='', required=False)
    parser.add_argument('--window', '-w', type=str, default='', required=False)
    parser.add_argument('--screen-route', '-S', type=str, default='', required=False)
    args = parser.parse_args()
    if args.force_update:
        update.update(info['ignore_list'])
    mian(args)
