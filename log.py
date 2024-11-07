import d4
import datetime

__logs = []
logfile = 'log.txt'


def write_log(tb='', mode='w', del_record=True):
    global __logs
    if tb:
        echo(tb, pr_time=False)
    with open(logfile, mode, encoding='utf-8') as f:
        for log in __logs:
            f.write(log + '\n')
        if del_record:
            __logs = []
    return


def echo(content='', pr_time=True):
    global __logs
    curt = datetime.datetime.now()
    log = '%s | Runtime: %s | %s' % (curt.strftime('%Y-%m-%d %H:%M:%S'), (curt - d4.st_time),
                                     content) if pr_time else content
    print(log)
    __logs.append(log)
