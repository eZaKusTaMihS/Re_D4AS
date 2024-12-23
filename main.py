import argparse
import os

import utils
import start


def form_update(ignore_list=None, bat_file='update.bat') -> str:
    if ignore_list is None:
        ignore_list = ['']
    ignored = ''
    for e in ignore_list:
        ignored = ignored.join(e + ' ') if e else ignored
    ignored = ignored.strip()
    with open(bat_file, 'w', encoding='utf-8') as bat:
        if ignored:
            bat.write(ignored + '\n')
        bat.write('git fetch --all&&git reset --hard origin/master&&git pull\n')
    return bat_file


def reform_parser(args_dict: dict[str, any]) -> str:
    res = ''
    for k, v in args_dict.items():
        if not v:
            continue
        flag_k = f'--{k.replace('_', '-')}'
        res += f'{flag_k} {v} '
    return res.strip()


def form_start(args: argparse.Namespace, conda_env: str, bat_file='start.bat') -> str:
    ad = args.__dict__
    ad['force_update'] = False
    with open(bat_file, 'w', encoding='utf-8') as bat:
        if conda_env:
            bat.write(f'conda activate {conda_env}\n')
        parser_str = reform_parser(ad)
        bat.write(f'python start.py {parser_str}\n')
    return bat_file


def main():
    update_f, start_f = '', ''
    try:
        info = utils.load_json('info.json')
        conda_env = info['conda_env']
        ignore_list = info['ignore_list']
        args = parser.parse_args()
        if args.force_update:
            update_f = form_update(ignore_list)
            utils.execute(update_f)
        start_f = form_start(args, conda_env)
        utils.exec_on_new_window(start_f)
    finally:
        try:
            os.remove(update_f)
        except FileNotFoundError:
            pass
        finally:
            try:
                os.remove(start_f)
            except FileNotFoundError:
                pass
            finally:
                pass


if __name__ == '__main__':
    parser = start.parser
    main()