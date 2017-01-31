# -*- coding: utf-8 -*-
#
#      ____              _____ _                   _
#     / __ \            / ____(_)                 | |
#    | |  | |_ __   ___| (___  _  __ _ _ __   __ _| |
#    | |  | | '_ \ / _ \\___ \| |/ _` | '_ \ / _` | |
#    | |__| | | | |  __/____) | | (_| | | | | (_| | |
#     \____/|_| |_|\___|_____/|_|\__, |_| |_|\__,_|_|
#                                 __/ |
#                                |___/

"""
python-onesignal
----------------

python-onesignal is a Python wrapper for the OneSignal REST API.

"""

__version__ = '0.1.0'

from .api import OneSignal
from .exceptions import OneSignalApiError
