import json
from d4 import GameController

if __name__ == '__main__':
    config = json.load(open('config.json'))
    controller = GameController(config)
    controller.play()
