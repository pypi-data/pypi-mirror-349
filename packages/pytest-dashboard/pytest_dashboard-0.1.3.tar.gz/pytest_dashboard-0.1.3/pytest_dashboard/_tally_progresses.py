import os
from glob import glob
from time import sleep
from threading import Thread
from subprocess import run

import yaml

import pytest_dashboard
from pytest_dashboard import config


SAMPLE_PROGRESS_DIR = os.path.join(
    os.path.dirname(pytest_dashboard.__file__),
    '..',
    'sample-progress'
)

UPDATE_INTERVAL = 1

should_stop = False


def _progress_passed(data) -> bool:
    # if empty, return False
    if data is None:
        return False

    # if not started, return False
    if data['results'] is None:
        return False

    # if all(results), return True
    passed_list = []
    for result in data['results']:
        name = result['name']
        setup = result['setup'] if 'setup' in result.keys() else None
        call = result['call'] if 'call' in result.keys() else None
        teardown = result['teardown'] if 'teardown' in result.keys() else None
        passed = True
        if setup is not None:
            passed = passed * (setup == 'passed')
        if call is not None:
            passed = passed * (call == 'passed')
        if teardown is not None:
            passed = passed * (teardown == 'passed')
        passed_list.append(passed)
    return all(passed_list)


def _progress_state(data) -> str:
    # if empty, not started
    if data is None:
        return 'not started'

    # if len(items) == len(results) and data['results'][-1] has the key 'teardown', finished
    if data['results'] is not None:
        if (
                len(data['items']) == len(data['results'])
                and 'teardown' in data['results'][-1].keys()
        ):
            return 'finished'

    # else, ongoing
    return 'ongoing'


def _check_notification(data):

    global should_stop

    if data['entire']['state'] == 'finished':

        if data['entire']['passed']:
            prefix = '(passed)'
        else:
            prefix = '(failed)'

        sbj = prefix + 'finish pyenv-package-test!!'
        bdy = yaml.dump(data)

        run([
            'powershell',
            'send-mailmessage',
            '-from', config.mail_from,
            '-to', config.mail_to,
            '-subject', f'"{sbj}"',
            '-body', f'"{bdy}"',
            '-encoding', '([System.Text.Encoding]::UTF8)',
            '-port', config.port,
            '-smtpserver', config.smtpserver,
        ])

        should_stop = True


def merge_progress_files(progresses_dir, entire_progress_path, notification):
    # glob all -progress.yaml and check their state and passed
    merged_data = {}
    state_list = []
    passed_list = []
    for path in glob(os.path.join(progresses_dir, '*-progress.yaml')):
        with open(path, 'r') as f:
            data = yaml.safe_load(f)
            # add each progress
            name = os.path.basename(path)[:-14]  # -progress.yaml is 14 chars
            state = _progress_state(data)
            passed = _progress_passed(data)
            merged_data[name] = dict(state=state, passed=passed)
            # add to entire list
            state_list.append(state)
            passed_list.append(passed)

    # add entire progress
    name = 'entire'
    state = 'finished' if all([s=='finished' for s in state_list]) else 'ongoing'
    passed = all(passed_list)
    merged_data[name] = dict(state=state, passed=passed)

    # save merged entire-progress.yaml
    with open(entire_progress_path, 'w') as f:
        yaml.dump(merged_data, f)

    # check notification
    if notification:
        _check_notification(merged_data)


def _update_forever(progresses_dir, entire_progress_path, notification):
    while not should_stop:
        merge_progress_files(progresses_dir, entire_progress_path, notification)
        sleep(UPDATE_INTERVAL)


def monitor_progress(
        progresses_dir:str,
        entire_progress_path:str='./entire-progress.yaml',
        notification:bool=False,
):
    global should_stop

    entire_progress_path = os.path.abspath(entire_progress_path)

    t = Thread(
        target=_update_forever,
        args=(progresses_dir, entire_progress_path, notification,),
        daemon=True
    )
    t.start()
    print()
    print('##############################')
    print('  Starts continuous update of:')
    print('  ' + entire_progress_path)
    print('  Do not close this window')
    print('  while test is running.')
    print('  Press enter to quit.')
    print('##############################')
    input()
    should_stop = True
