import argparse
import utils
from d4 import GameController, ControllerCrashException


def main(_args: argparse.Namespace):
    try:
        controller = GameController(_args)
        controller.play()
    except KeyboardInterrupt:
        exit(114514)
    except Exception as e:
        print(e)
        exit(1919810)
