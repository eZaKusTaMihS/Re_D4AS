import json
import argparse
from d4 import GameController

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--serial', '-s', type=str, default='127.0.0.1:16416', required=False)
    parser.add_argument('--window', '-w', type=str, default='d4dj', required=False)
    args = parser.parse_args()
    config = json.load(open('config.json'))
    controller = GameController(config, args)
    controller.play()
