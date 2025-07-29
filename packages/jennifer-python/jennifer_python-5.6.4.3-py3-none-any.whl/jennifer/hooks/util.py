# -*- coding: utf-8 -*-

import os
from datetime import datetime
import traceback

enable_diagnostics = os.getenv('JENNIFER_DBG') == '1'
diagnostics_to_file = os.getenv('JENNIFER_LOG_FILE') or None


def format_time(time_value):
    return time_value.strftime("[%Y-%m-%d %H:%M:%S]")


def _log_tb(*args):
    current_time = format_time(datetime.now())
    print(current_time, '[' + str(os.getpid()) + ']', 'ERROR', '[jennifer]', args)
    traceback.print_exc()


def _log(level, *args):
    current_time = format_time(datetime.now())
    print(current_time, '[' + str(os.getpid()) + ']', level, '[jennifer]', args)


def _to_valid_version(text):
    if text is None:
        return ""

    version_part = str(text).split(' ')[0]
    if len(version_part.split('.')) == 2:
        return version_part + ".0"

    return version_part


def _diag_log(level, *args):
    if enable_diagnostics is False:
        return

    time_now = datetime.now()
    time_column = format_time(time_now)

    print(time_column, '[' + str(os.getpid()) + ']', level, '[jennifer]', args)

    if diagnostics_to_file is not None:
        log_file_path = os.path.join(diagnostics_to_file, "agent_diag_" + str(os.getpid()) + ".log")
        with open(log_file_path, 'a') as log_file:
            log_file.write(time_column + ' ' + str(args) + '\n')