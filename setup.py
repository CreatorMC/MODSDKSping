# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name='mc-creatormc-sdkspring',
    version='1.0.0',
    description = "一个基于网易我的世界 MODSDK 开发的框架，可以让开发者更方便的使用 MODSDK。",
    long_description=open('README.md').read(),
    author='CreatorMC',
    url='https://github.com/CreatorMC/MODSDKSping',
    packages=find_packages(
        exclude=['plugins', 'plugins.*', 'template', 'template.*']
    ),
    install_requires=[],
    entry_points={
        'console_scripts': [
            'modsdkspring=command.main:main',
        ],
    },
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 2.7.18",
        "License :: MIT License"
    ],
    platforms='any'
)