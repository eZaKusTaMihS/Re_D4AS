import datetime
import os
import time

import adb
import img_processor as ip


class GameController:
    general_btn_route = 'res\\general_btn'
    exception_route = 'res\\exceptions'
    pre_stat = ''
    logs = []

    def __init__(self, config: dict):
        adb.start()
        self.st_time = datetime.datetime.now()
        general = config['general']
        play = config['play']
        tsk = config['tasks']
        self.serial = adb.serial = str(general['serial'])
        self.screen = str(general['screen_route'])
        self.stat_route = str(general['stat_route'])
        self.timeout = max(5, int(general['timeout']))
        self.voltage = max(0, int(play['voltage']))
        self.sup = bool(play['auto_sup'])
        self.vrf = bool(play['do_vrf'])
        h, m = str(play['rest_interval']).split(':', maxsplit=1)
        self.rhr, self.rmn = min(3, abs(int(h))), abs(int(m)) % 60
        self.type = str(tsk['event_type'])
        self.mode = str(tsk['mode'])
        self.event_route = os.path.join('res', self.type)
        os.makedirs(self.screen.split('\\')[0], exist_ok=True)
        self.lc_time = datetime.datetime.now()
        self.lv_time = datetime.datetime.now()
        self.lv_cnt = 0
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

    def __echo(self, content, stime=True):
        cur_t = datetime.datetime.now()
        log = '%s | Runtime: %s | %s' % (cur_t, cur_t - self.st_time, content) if stime else content
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
                adb.click((640, 360))
            case 'main':
                adb.click((1130, 570), 110, 110)
                time.sleep(0.5)
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
                time.sleep(0.5)
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
                if self.mode == 'sp':
                    adb.click(loc, w, h)
                    return
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
            elif st == 'auto_rej' and self.vrf:
                # Deal with detection
                import pygetwindow as gw
                d4w = gw.getWindowsWithTitle('d4dj')
                if d4w:
                    d = d4w[0]
                    d.minimize()
                    d.restore()
                    print(gw.getActiveWindow())
                    time.sleep(1)
                    # Input recording trigger
                    import keyboard
                    keyboard.press_and_release('g')
                    time.sleep(4)
                    d.minimize()
                return
            else:
                adb.click(loc, w, h)
            time.sleep(brt)
            return
        stat = ip.get_stat(screen=self.screen, stat_route=self.stat_route)[0]
        if stat and stat != self.pre_stat:
            if stat == 'live':
                if self.lv_cnt == 0:
                    l_time = 0
                else:
                    l_time = (datetime.datetime.now() - self.lv_time).total_seconds()
                self.__echo('Live times: %d | Last loop duration: %.2fs' % (self.lv_cnt, l_time))
                self.lv_cnt += 1
                self.lv_time = datetime.datetime.now()
            else:
                self.__echo('Current status: %s' % stat)
        clicked = self.__btn_clk(stat=stat)
        self.pre_stat = stat
        if clicked:
            self.lc_time = datetime.datetime.now()
        if not clicked:
            if datetime.datetime.now() - self.lc_time > datetime.timedelta(minutes=self.timeout):
                self.__echo('Timeout exceeded, trying to restart')
                adb.restart()
                self.lc_time = datetime.datetime.now()
        # Timer
        if ((not self.vrf) and
                datetime.datetime.now() - self.st_time > datetime.timedelta(hours=self.rhr, minutes=self.rmn) and
                stat != 'live'):
            adb.restart(15)
            self.st_time = datetime.datetime.now()


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
