#!/usr/bin/env python3
# -*- coding:utf8 -*-
class DIYError(Exception):
    ''' The base DIY exception from which all others should subclass '''

    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


class FileCopyError(DIYError):
    ''' Exception raised when a file copy fails '''
    pass


class FileNotFoundError(DIYError):
    ''' Exception raised when a file read fails '''
    pass
