# -*- coding: utf-8 -*-


class SetupError(Exception):
    def __init__(self, msg):
        Exception.__init__(self, msg)
