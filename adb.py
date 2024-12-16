import numpy as np
import os

import log
import utils

serial = '127.0.0.1:16416'


def __exec(__statement: str):
    # import subprocess
    # p = subprocess.run(__statement, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
    # p = subprocess.Popen(__statement, shell=True, stdout=subprocess.PIPE)
    # while p.poll() is None:
    #     if p.wait() != 0:
    #         print("Failed")
    #         return False
    #     else:
    #         re = p.stdout.readlines()
    #         for result in re:
    #             print(result)
    # return True
    return utils.execute(__statement)


def screenshot(__route: str):
    if not __route.startswith(os.getcwd()[:2]):
        __route = os.path.join(os.getcwd(), __route)
    return __exec('adb -s %s exec-out screencap -p > %s' % (serial, __route))


def connect(__device=serial) -> bool:
    f = __exec('adb connect %s' % __device)
    if not f:
        log.echo(f'Failed to establish connection to {__device}.')
    return f


def click(pos: tuple[int, int], width=1, height=1):
    """
    Click randomly in a range [ ``pos``, ( ``pos[0]`` + ``width``, ``pos[1]`` + ``height`` ) ).
    The upper bound is excluded.
    :param pos: The starting coordinates. Counts from the upper-left corner where the position is (0, 0).
    :param width: Width range.
    :param height: Height range.
    :return: The actual point where the click occurs.
    """
    width, height = max(1, width), max(1, height)
    x, y = pos
    x += np.random.randint(width)
    y += np.random.randint(height)
    try:
        r = __exec('adb -s %s shell input tap %s %s' % (serial, x, y))
    except:
        return -1, -1
    if r:
        log.echo('Click @ (%s, %s)' % (x, y))
        return x, y
    print('Click failed.')
    return -1, -1


def start(pac='com.bushiroad.d4dj', act='com.unity3d.player.UnityPlayerActivity'):
    return __exec('adb -s %s shell am start -n %s/%s' % (serial, pac, act))


def stop(pac='com.bushiroad.d4dj'):
    return __exec('adb -s %s shell am force-stop %s' % (serial, pac))


def restart(interval=0, pac='com.bushiroad.d4dj', act='com.unity3d.player.UnityPlayerActivity'):
    stop(pac)
    interval = abs(int(interval))
    if interval:
        import time
        log.echo('Restart after %d minutes.' % interval)
        time.sleep(interval*60)
    return start(pac, act)
