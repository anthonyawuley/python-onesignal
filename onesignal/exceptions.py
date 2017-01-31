# -*- coding: utf-8 -*-

"""
onesignal.exceptions
~~~~~~~~~~~~~~~~~

This module contains the set of onesignal exceptions.

"""

class OneSignalApiError(Exception):
    """Generic error class, catch-all for most OneSignal API issues.

    from onesignal import OneSignalApiError

    """
    def __init__(self, msg, status_code=None):
        self.status_code = status_code

        super(OneSignalApiError, self).__init__(msg)

    @property
    def msg(self):  # pragma: no cover
        return self.args[0]
