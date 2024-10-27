import numpy as np
import subprocess
import os

serial = '127.0.0.1:16416'


def __exec(__statement: str):
    p = subprocess.Popen(__statement, shell=True, stdout=subprocess.PIPE)
    while p.poll() is None:
        if p.wait() != 0:
            print("Failed")
            return False
        else:
            re = p.stdout.readlines()
            for result in re:
                print(result)
    return True


def screenshot(__route: str):
    if not __route.startswith(os.getcwd()[:2]):
        __route = os.path.join(os.getcwd(), __route)
    return __exec('adb -s %s exec-out screencap -p > %s' % (serial, __route))


def connect(__device=serial):
    return __exec('adb connect %s' % __device)


def click(pos: tuple[int, int], width: int, height: int):
    width, height = max(1, width), max(1, height)
    x, y = pos
    x += np.random.randint(width)
    y += np.random.randint(height)
    try:
        r = __exec('adb -s %s shell input tap %s %s' % (serial, x, y))
    except:
        return -1, -1
    if r:
        # print('Click @ (%s, %s)' % (x, y))
        return x, y
    print('Click failed.')
    return -1, -1
