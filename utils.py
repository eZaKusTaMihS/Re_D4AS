import subprocess
import json


def execute(statement: str) -> bool:
    p = subprocess.Popen(statement, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
    if p.poll() is None:
        if p.wait() != 0:
            return False
        else:
            res = ''
            for r in [e.strip('\n') for e in p.stdout.readlines()]:
                res = res.join(r + '\n') if r else res
            if res:
                print(res.strip('\n'))
    return True


def exec_on_new_window(statement: str):
    p = subprocess.Popen(['cmd', '/c', statement], creationflags=subprocess.CREATE_NEW_CONSOLE)
    p.wait()


def load_json(path: str) -> dict:
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)
