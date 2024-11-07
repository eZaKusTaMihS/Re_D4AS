import cv2 as cv
import os

boarder = 0.8


def __match(tg, tp) -> tuple[tuple[int, int], int, int, float]:
    th, tw = tp.shape[:2]
    rs = cv.matchTemplate(tg, tp, cv.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(rs)
    loc = max_loc if max_val >= boarder else (-1, -1)
    return loc, th, tw, max_val


def match_by_path(target: str, template: str):
    tg = cv.imread(target)
    tp = cv.imread(template)
    return __match(tg, tp)


def find_best(target, template_folder, appointment=None, ignore=None) -> tuple[tuple[int, int], int, int, float]:
    """
    Find the template that matches the most.
    :param str target: Path of target image to be matched.
    :param str template_folder: Path of template folder (without hierarchical structs).
    :param str appointment: Name of template you want to find. Default to be empty.
    :param list[str] ignore: List of names of templates to ignore. Default to be empty.
    :return: Pos of the up-left corner of the matched image (set to (-1, -1) if fails);
    height;
    width;
    score of the match.
    """
    appointment = appointment.rsplit('.', maxsplit=1)[0].strip() if type(appointment) is str else ''
    ignore = [] if not ignore else ignore if type(ignore) is list else [ignore]
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
        loc, h, w, val = __match(tg, tpl)
        if val > mx:
            ml, mh, mw, mx = loc, h, w, val
    return ml, mh, mw, mx


def detect(target: str, template_folder: str, aim: str):
    loc = find_best(target, template_folder, appointment=aim)[0]
    return loc != (-1, -1)


def match_all_avg(tg, templates):
    val, num = 0, 0
    loc, th, tw = (-1, -1), 0, 0
    if not os.path.isdir(templates) and templates.endswith('.png'):
        tp = cv.imread(templates)
        return __match(tg, tp)
    for tpl in os.listdir(templates):
        if tpl.startswith('_'):
            continue
        num += 1
        tp = cv.imread(os.path.join(templates, tpl))
        loc, th, tw, max_val = __match(tg, tp)
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
    return stat


class RecResult(dict):
    def __init__(self):
        super().__init__()
        self['name'] = ''
        self['loc'] = (-1, -1)
        self['h'] = 0
        self['w'] = 0
        self['val'] = 0.0
        self.type_d = dict(name=str, loc=tuple, h=int, w=int, val=float)

    def setvals(self, **kwargs):
        for k, v in kwargs.items():
            self.__set_element(k, v)
        return

    def __set_element(self, name, value):
        if name in self.keys():
            if isinstance(value, type(self[name])):
                self[name] = value
            else:
                raise TypeError(f'Attribute \'{name}\' must be {type(self[name])}.')
        else:
            raise AttributeError(f'No attribute named \'{name}\'.')
        return
