#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
Project : AD_UI_test
Version : v0.1
Author : tangna@dangdang.com
Date : 2017-04-25
Note :
'''

class Error(Exception):
    """Base class"""
    pass

class AdListEmptyException(Error):
    def __init__(self, err='广告id列表为空'):
        Error.__init__(self, err)

class LinuxCommException(Error):
    def __init__(self, stderr):
        self.message = 'linux command error：{0}'.format(stderr)
        Error.__init__(self, self.message)