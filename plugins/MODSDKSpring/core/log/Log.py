# -*- coding: utf-8 -*-
import logging

level = logging.DEBUG
logger = logging.getLogger('MODSDKSpring')
logger.setLevel(level)

console_handler = logging.StreamHandler()
console_handler.setLevel(level)

formatter = logging.Formatter('[%(asctime)s][%(levelname)s][%(name)s]%(message)s')
console_handler.setFormatter(formatter)

logger.addHandler(console_handler)