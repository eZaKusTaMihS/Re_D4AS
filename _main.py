import time
import datetime
import adb
import img_processor as ip
import json


screen_route = 'temp\\screen.png'
stat_route = 'res\\stat'


def main():
    config = json.load(open('config.json'))
    general = config['general']
    adb.serial = general['serial']
    short_break = 0.7
    adb.connect()
    st_time = datetime.datetime.now()
    l_stat = ''
    same_cnt = 0
    while True:
        adb.screenshot(screen_route)
        stat, loc, h, w = ip.get_stat(screen_route, stat_route)
        same_cnt = same_cnt + 1 if stat == l_stat else 0
        if stat and stat != l_stat:
            print('Runtime: %s | Current status: %s' % (datetime.datetime.now() - st_time, stat))
        l_stat = stat
        match stat:
            case 'live':
                time.sleep(5)
            case 'title':
                adb.click((1130, 570), 110, 110)
            case 'live_sel':
                adb.click((1000, 180), 160, 120)
                # adb.click((660, 180), 160, 120)
            case 'st_0':
                # voltage supplement
                print('Voltage supplement')
                adb.click(loc, w, h)
                time.sleep(short_break)
                adb.click((400, 210), 200, 140)
                time.sleep(short_break)
                adb.click((740, 300), 55, 55)
                time.sleep(short_break)
                adb.click((660, 605), 200, 70)
                time.sleep(short_break)
                adb.click((660, 490), 200, 60)
                time.sleep(1.2)
                adb.click((540, 490), 200, 60)
            case '0rdm':
                if same_cnt < 2:
                    adb.click(loc, w, h)
            case '':
                continue
                # adb.click((1280, 720), 0, 0)
            case _:
                adb.click(loc, w, h)
        time.sleep(short_break)


if __name__ == '__main__':
    main()
