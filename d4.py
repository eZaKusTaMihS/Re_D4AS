import time
import adb
import img_processor as ip
import os
import datetime


class GameController:
    general_btn_route = 'res\\general_btn'
    exception_route = 'res\\exceptions'
    pre_stat = ''
    logs = []

    def __init__(self, config: dict):
        self.st_time = datetime.datetime.now()
        general = config['general']
        play = config['play']
        tsk = config['tasks']
        self.serial = adb.serial = general['serial']
        self.screen = general['screen_route']
        self.stat_route = general['stat_route']
        self.voltage = play['voltage']
        self.multi = play['multi']
        self.sup = play['auto_sup']
        self.type = tsk['event_type']
        self.mode = tsk['mode']
        self.event_route = os.path.join('res', self.type)
        os.makedirs(self.screen.split('\\')[0], exist_ok=True)
        return

    def __update_config(self, config: dict):
        general = config['general']
        play = config['play']
        tsk = config['tasks']
        self.serial = adb.serial = general['serial']
        self.screen = general['screen_route']
        self.stat_route = general['stat_route']
        self.voltage = play['voltage']
        self.multi = play['multi']
        self.sup = play['auto_sup']
        self.type = tsk['event_type']
        self.event_route = os.path.join('res', self.type)

    def __echo(self, content):
        cur_t = datetime.datetime.now()
        log = '%s | Runtime: %s | %s' % (cur_t, cur_t - self.st_time, content)
        print(log)
        self.logs.append(log)

    def __write_log(self, mode='w', tb=''):
        with open('log.txt', mode, encoding='utf-8') as f:
            for log in self.logs:
                f.write(log + '\n')
            if tb:
                f.write(tb)
        return

    def __btn_clk(self, stat='general'):
        match stat:
            case 'title':
                adb.click((1130, 570), 110, 110)
            case 'live_sel':
                if self.type in ['yell', 'raid']:
                    adb.click((70, 180), 90, 70)
                else:
                    adb.click((1000, 180), 160, 120)
            case 'live':
                time.sleep(5)
            case _:
                event = 'event' in stat
                l, h, w, v = ip.match_all_best(self.screen, self.general_btn_route)
                # No matches
                if l == (-1, -1):
                    # Check event
                    app = self.mode if event else ''
                    l, h, w, v = ip.match_all_best(self.screen, self.event_route, appointment=app)
                    if l == (-1, -1):
                        return False
                x, y = adb.click(l, w, h)
                if x > 0 and y > 0:
                    self.__echo('Click @ (%s, %s)' % (x, y))
                else:
                    self.__echo('Click Failed.')
        return True

    def __loop(self):
        adb.screenshot(self.screen)
        brt = 0.7
        st, loc, h, w = ip.get_stat(screen=self.screen, stat_route=self.exception_route)
        if st:
            if 'empty_volt' in st:
                self.__echo('Voltage Supplement')
                if self.type == 'battle':
                    adb.click((400, 300), 190, 140)
                else:
                    adb.click(loc, w, h)
                    time.sleep(brt)
                    adb.click((400, 210), 200, 140)
                time.sleep(brt)
                adb.click((740, 300), 55, 55)
                time.sleep(brt)
                adb.click((660, 605), 200, 70)
                time.sleep(brt)
                adb.click((660, 490), 200, 60)
                time.sleep(1.2)
                adb.click((540, 490), 200, 60)
            else:
                adb.click(loc, w, h)
            time.sleep(brt)
            return
        stat = ip.get_stat(screen=self.screen, stat_route=self.stat_route)[0]
        if stat and stat != self.pre_stat:
            self.__echo('Current status: %s' % stat)
        clicked = self.__btn_clk(stat=stat)
        self.pre_stat = stat
        # if clicked:
        #     time.sleep(brt)

    def play(self):
        try:
            adb.connect(self.serial)
            self.st_time = datetime.datetime.now()
            while True:
                self.__loop()
                if len(self.logs) > 100:
                    self.__write_log(mode='w+')
                    self.logs.clear()
        except KeyboardInterrupt:
            self.__write_log()
        except:
            import traceback
            self.__write_log(tb=traceback.format_exc())
