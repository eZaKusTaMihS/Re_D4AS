import cv2 as cv
import os

boarder = 0.8


def match(tg, tp):
    th, tw = tp.shape[:2]
    rs = cv.matchTemplate(tg, tp, cv.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(rs)
    loc = max_loc if max_val >= boarder else (-1, -1)
    return loc, th, tw, max_val


def match_path(target: str, template: str):
    tg = cv.imread(target)
    tp = cv.imread(template)
    return match(tg, tp)


def match_all_best(target, template_folder, appointment='', ignore=None):
    appointment = appointment.rsplit('.', maxsplit=1)[0].strip() if type(appointment) is str else ''
    ignore = [] if not ignore else ignore if type(ignore) is list else [ignore] if type(ignore) is str else []
    tg = cv.imread(target)
    ml, mh, mw, mx = (-1, -1), 0, 0, -1
    for tp in os.listdir(template_folder):
        if tp.replace('.png', '') in ignore:
            continue
        if appointment:
            if tp.replace('.png', '') != appointment:
                continue
        elif not tp.endswith('.png') or tp.startswith('_'):
            continue
        tpl = cv.imread(os.path.join(template_folder, tp))
        loc, h, w, val = match(tg, tpl)
        if val > mx:
            ml, mh, mw, mx = loc, h, w, val
    return ml, mh, mw, mx


def match_all_avg(tg, templates):
    val, num = 0, 0
    loc, th, tw = (-1, -1), 0, 0
    if not os.path.isdir(templates) and templates.endswith('.png'):
        tp = cv.imread(templates)
        return match(tg, tp)
    for tpl in os.listdir(templates):
        if tpl.startswith('_'):
            continue
        num += 1
        tp = cv.imread(os.path.join(templates, tpl))
        loc, th, tw, max_val = match(tg, tp)
        if loc == (-1, -1):
            return -1, loc, th, tw
        val += max_val
    return val / max(num, 1), loc, th, tw


def get_stat(screen: str, stat_route: str):
    tg = cv.imread(screen)
    mx, st, stat = 0, '', ('', (-1, -1), 0, 0)
    for st in os.listdir(stat_route):
        if st.startswith('_'):
            continue
        rt = os.path.join(stat_route, st)
        avg, loc, h, w = match_all_avg(tg, rt)
        if avg > mx:
            mx = avg
            stat = (st, loc, h, w)
    # print('%s at score %.4f' % (stat[0], mx))
    # return stat
    return stat
