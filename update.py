import utils


def update(ignore_list: list[str]):
    ignored = ''
    for e in ignore_list:
        ignored = ignored.join(e + ' ')
    ignored = ignored.strip()
    utils.execute('%sgit fetch --all&&git reset --hard origin/master&&git pull' %
                  (('git update-index --skip-worktree %s&&' % ignored) if ignored else ''))


if __name__ == '__main__':
    update(utils.load_json('info.json')['ignore_list'])
