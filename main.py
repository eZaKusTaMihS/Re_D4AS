import argparse
import subprocess
import pickle

import utils


def __exec(command: str, hint: str = ''):
    if hint:
        print(hint)
    result = subprocess.run(command, shell=True, text=True, capture_output=True, encoding='utf-8')
    if result.returncode != 0:
        print(f'An error occurred while executing {command}: {result.stderr}')
        return None
    return result.stdout.strip()


def update():
    if __exec(f'git fetch origin master', 'Fetching from repository...') is None:
        return
    stat = __exec(f'git status')
    if 'Your branch is up to date' in stat:
        print('Already up to date.')
    else:
        print('Updating...')
        if __exec(f'git pull origin master') is None:
            print('Update failed.')
            return
    print('Update completed. Now starting.')


def mian():
    process = subprocess.Popen(f'{py} start.py',
                               shell=True,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               text=True,
                               encoding='utf-8')
    try:
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                print(output.strip('\n'))
    except KeyboardInterrupt:
        import signal
        process.send_signal(signal.CTRL_C_EVENT)
        print('See you.')
        exit(114514)


if __name__ == '__main__':
    info = utils.load_json('info.json')
    py = info['python-path']
    repo = info['repo']
    parser = argparse.ArgumentParser()
    parser.add_argument('--update', '-u', type=bool, default=True, required=False)
    parser.add_argument('--config', '-c', type=str, default='usr\\config.json', required=False)
    parser.add_argument('--serial', '-s', type=str, default='', required=False)
    parser.add_argument('--window', '-w', type=str, default='', required=False)
    parser.add_argument('--screen-route', '-S', type=str, default='', required=False)
    args = parser.parse_args()
    pickle.dump(args, open('temp\\args', 'wb'))
    if args.update:
        update()
    mian()
