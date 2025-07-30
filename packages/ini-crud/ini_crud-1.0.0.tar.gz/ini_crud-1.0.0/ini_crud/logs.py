#!/usr/bin/env python3
# -*- coding:utf8 -*-
import logging

level = logging.INFO


def logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger
