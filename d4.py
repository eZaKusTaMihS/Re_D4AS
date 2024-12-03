import datetime
import os
import time
from argparse import Namespace

import adb
import img_processor as ip
import log

global st_time


class GameController:
    general_btn_route = 'res\\general_btn'
    exception_route = 'res\\exceptions'
    pre_stat = ''
    logs = []

    def __init__(self, config: dict, args: Namespace):
        global st_time
        self.general_btn_route = 'res\\general_btn'
        st_time = datetime.datetime.now()
        general = config['general']
        play = config['play']
        tsk = config['tasks']
        self.serial = adb.serial = args.serial if args.serial else str(general['serial'])
        self.window = args.window if args.window else str(general['window'])
        self.screen = str(general['screen_route'])
        self.stat_route = str(general['stat_route'])
        self.live_route = 'res\\live_sel'
        self.timeout = max(5, int(general['timeout']))
        self.voltage = max(0, int(play['voltage']))
        self.sup = bool(play['auto_sup'])
        self.vrf = bool(play['do_vrf'])
        h, m = str(play['rest_interval']).split(':', maxsplit=1)
        self.rest_interval = datetime.timedelta(hours=min(3, abs(int(h))), minutes=abs(int(m)) % 60)
        self.search_route: list[str] = play['search_route']
        self.search_route = self.search_route if self.search_route else ["$general_btn_route", "$event_route"]
        self.type = str(tsk['event_type'])
        self.mode = str(tsk['mode'])
        self.event_route = os.path.join('res', self.type)
        os.makedirs('temp\\fin', exist_ok=True)
        os.makedirs('temp\\screenshots', exist_ok=True)
        self.lc_time = datetime.datetime.now()
        self.lv_time = datetime.datetime.now()
        self.lv_cnt = 0
        self.lv_drt = 0
        self.fst = True
        for _ in range(len(self.search_route)):
            route = self.search_route[0]
            if route.startswith('$'):
                name = route.replace('$', '')
                if name not in self.__dict__.keys():
                    self.search_route.remove(route)
                    continue
                self.search_route.append(self.__getattribute__(name))
            else:
                self.search_route.append(route)
            self.search_route.remove(route)
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

    # def __echo(self, content, stime=True):
    #     cur_t = datetime.datetime.now()
    #     log = '%s | Runtime: %s | %s' % (cur_t, cur_t - st_time, content) if stime else content
    #     print(log)
    #     self.logs.append(log)
    #
    # def __write_log(self, mode='w', tb=''):
    #     with open('log.txt', mode, encoding='utf-8') as f:
    #         for log in self.logs:
    #             f.write(log + '\n')
    #         if tb:
    #             f.write(tb)
    #     return

    def __btn_clk(self, stat='general'):
        match stat:
            case 'title':
                adb.click((640, 360))
            case 'main':
                adb.click((1130, 570), 110, 110)
                self.lv_drt = 00
                time.sleep(0.5)
            case 'live_sel':
                if self.type in ['yell', 'raid'] or self.mode == 'sp':
                    adb.click((70, 180), 90, 70)
                else:
                    if self.mode == 'solo':
                        adb.click((670, 180), 160, 120)
                    else:
                        adb.click((1000, 180), 160, 120)
            case 'live':
                time.sleep(1)
                pass
            case _:
                event = 'event' in stat
                l, h, w, v = ip.find_best(self.screen, self.general_btn_route)
                # No matches
                if l == (-1, -1):
                    # Check event
                    app = self.mode if event else ''
                    l, h, w, v = ip.find_best(self.screen, self.event_route, appointment=app)
                    if l == (-1, -1):
                        return False
                adb.click(l, w, h)
                # if x > 0 and y > 0:
                #     log.echo('Click @ (%s, %s)' % (x, y))
                # else:
                #     log.echo('Click Failed.')
        return True

    def __loop(self) -> None:
        """
        Inner cycle for game controller.
        """
        global st_time
        adb.screenshot(self.screen)
        brt = 0.7
        # Handle exception situations in game
        exc, loc, h, w = ip.get_stat(screen=self.screen, stat_route=self.exception_route)
        if exc:
            if 'empty_volt' in exc:
                # Voltage supplement
                if self.mode == 'sp':
                    # Only click start for sp
                    adb.click(loc, w, h)
                    return
                log.echo('Voltage Supplement')
                if self.type == 'battle':
                    adb.click((400, 300), 190, 140)
                else:
                    adb.click(loc, w, h)
                    time.sleep(brt)
                    adb.click((400, 210), 200, 140)
                time.sleep(brt)
                # +1  5drink
                adb.click((740, 300), 55, 55)
                time.sleep(brt)
                adb.click((660, 605), 200, 70)
                time.sleep(brt)
                adb.click((660, 490), 200, 60)
                time.sleep(1.2)
                adb.click((540, 490), 200, 60)
            elif exc == 'auto_rej':
                # Deal with verification
                import pygetwindow as gw
                d4w = gw.getWindowsWithTitle(self.window)
                if d4w:
                    log.echo('Passing verification...')
                    d = [win for win in d4w if win.title == self.window][0]
                    # Get focus
                    d.minimize()
                    d.restore()
                    log.echo(gw.getActiveWindow())
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
        # Normal status
        stat = ip.get_stat(screen=self.screen, stat_route=self.stat_route)[0]
        if stat and stat != self.pre_stat:
            if stat == 'live':
                if self.lv_cnt == 0:
                    l_time = 0
                    self.lv_time = datetime.datetime.now()
                else:
                    l_time = (datetime.datetime.now() - self.lv_time).total_seconds()
                    self.lv_drt += l_time
                avg_time = self.lv_drt / self.lv_cnt if self.lv_cnt > 0 else 0
                log.echo('Live times: %d | Last loop duration: %.2fs (Avg: %.2fs)' %
                         (self.lv_cnt, l_time, avg_time))
                self.lv_cnt += 1
                self.lv_time = datetime.datetime.now()
            elif stat == 'result' and self.type == 'poker':
                from shutil import copy
                fn = f'screen_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.png'
                time.sleep(0.5)
                adb.screenshot(self.screen)
                if not ip.detect(self.screen, self.event_route, '_empty_card'):
                    copy(self.screen, f'temp\\fin\\{fn}')
                    log.echo(f'Result screenshot saved to {fn}')
                copy(self.screen, f'temp\\screenshots\\{fn}')
                log.echo('Poker screenshot saved.')
            else:
                log.echo('Current status: %s' % stat)
        clicked = self.__btn_clk(stat=stat)
        self.pre_stat = stat
        # Timeout handler
        if clicked:
            self.fst = True
            self.lc_time = datetime.datetime.now()
        if not clicked:
            if datetime.datetime.now() - self.lc_time > datetime.timedelta(minutes=self.timeout):
                if self.fst:
                    self.fst = False
                    l, h, w, v = ip.find_best(self.screen, self.general_btn_route, appointment='_home')
                    if l != (-1, -1):
                        adb.click(l, w, h)
                else:
                    log.echo('Timeout exceeded, trying to restart')
                    adb.restart()
                    self.lv_cnt = 0
                    self.lc_time = datetime.datetime.now()
        # Rest timer
        if (not self.vrf) and datetime.datetime.now() - st_time >= self.rest_interval and stat != 'live':
            adb.restart(15)
            st_time = datetime.datetime.now()

    def play(self):
        global st_time
        try:
            adb.connect(self.serial)
            adb.start()
            st_time = datetime.datetime.now()
            while True:
                self.__loop()
                if len(self.logs) > 100:
                    log.write_log(mode='w+')
                    self.logs.clear()
        except KeyboardInterrupt:
            log.write_log()
        except:
            import traceback
            log.write_log(tb=traceback.format_exc())
