import d4
import datetime

__logs = []
__last_cnt = 0
__auto_record = 50
logfile = 'log.txt'


def write_log(tb='', mode='w', del_record=True):
    global __logs, __last_cnt
    if tb:
        echo(tb, pr_time=False, auto_write=False)
    with open(file=logfile, mode=mode, encoding='utf-8') as f:
        for log in __logs[__last_cnt:]:
            f.write(log + '\n')
        if del_record:
            __logs = []
            __last_cnt = 0
        else:
            __last_cnt += len(__logs)
    return


def echo(content='', pr_time=True, auto_write=True):
    global __logs
    curt = datetime.datetime.now()
    log = '%s | Runtime: %s | %s' % (curt.strftime('%Y-%m-%d %H:%M:%S'), (curt - d4.st_time),
                                     content) if pr_time else content
    print(log)
    __append_log(log, auto_write)


def __append_log(log: str, auto_write: bool):
    __logs.append(log)
    if auto_write and (len(__logs) - __last_cnt >= __auto_record):
        write_log(tb='', mode='w+', del_record=True)
